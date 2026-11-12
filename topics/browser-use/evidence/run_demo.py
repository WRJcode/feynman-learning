"""Real Browser Use / Chromium execution; model responses are scripted, not LLM inference."""
import asyncio, json, os
from pathlib import Path
from importlib.metadata import version
os.environ['ANONYMIZED_TELEMETRY']='false'
from browser_use import Agent, Browser
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelResponse, ToolCallPart, ToolReturnPart, RetryPromptPart
ROOT=Path(__file__).resolve().parent
calls=[]
fixture=(ROOT/'test-page.html').read_text()
code1=f'''new_tab()
js({('document.open(); document.write('+json.dumps(fixture)+'); document.close(); document.title')!r})
before = js("Array.from(document.querySelectorAll('li')).map(x=>x.textContent)")
print('BEFORE:', before)
assert before == ['Nacos', 'OpenHands', 'Codex']'''
code2='js("document.querySelector(\'#missing-input\').focus()")'
code3=f'''js("document.querySelector('#filter').focus()")
cdp('Input.insertText', text='Codex')
state = js("({{query:document.querySelector('#filter').value, visible:Array.from(document.querySelectorAll('li')).filter(x=>!x.hidden).map(x=>x.textContent),count:document.querySelector('#count').textContent}})")
assert before == ['Nacos', 'OpenHands', 'Codex']
assert state['visible'] == ['Codex'], state
assert state['count'] == '1 个主题', state
import json, base64
from pathlib import Path
Path({str(ROOT/'browser-state.json')!r}).write_text(json.dumps(state,ensure_ascii=False,indent=2))
shot=cdp('Page.captureScreenshot',format='png')
Path({str(ROOT/'browser-result.png')!r}).write_bytes(base64.b64decode(shot['data']))
print('VERIFIED:', state)'''
def scripted(messages, info):
    feedback=[]
    for m in messages:
        for part in m.parts:
            if isinstance(part,(ToolReturnPart,RetryPromptPart)):
                feedback.append(str(part.content))
    n=len(calls)
    calls.append({'request':n+1,'tools':[t.name for t in info.function_tools], 'feedback':feedback})
    if n==1:
        assert any('BEFORE:' in x for x in feedback),feedback
    if n==2:
        assert any('Error:' in x or 'null' in x for x in feedback),feedback
    if n==3:
        assert any('VERIFIED:' in x for x in feedback),feedback
        return ModelResponse(parts=[ToolCallPart('finish',{'result':'本地页面筛选完成：仅 Codex 可见，共 1 个主题。','success':True})])
    if n>3: raise RuntimeError('Unexpected extra request')
    return ModelResponse(parts=[ToolCallPart('python',{'code':[code1,code2,code3][n]})])
async def main():
    agent=Agent('在本地测试页筛选 Codex 并验证结果。测试中的模型响应全部预设。',llm=FunctionModel(scripted),browser=Browser('chromium',headless=True,executable_path='/usr/bin/chromium'),mode='default',workspace=ROOT/'workspace',highlight_actions=False)
    try:
        result=await agent.run(max_steps=8,timeout=120)
        state=json.loads((ROOT/'browser-state.json').read_text())
        assert state['visible']==['Codex'] and state['count']=='1 个主题'
        report={'browser_use_version':version('browser-use'),'real_llm':False,'model':'Pydantic AI FunctionModel; scripted responses','model_calls':len(calls),'state':state,'final_result':result.final_result(),'scope':'real Browser Use agent loop, persistent Python REPL and Chromium CDP; scripted error and correction do not prove autonomous recovery','calls':calls}
        (ROOT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        print(json.dumps({k:v for k,v in report.items() if k!='calls'},ensure_ascii=False,indent=2))
    finally:
        (ROOT/'calls.json').write_text(json.dumps(calls,ensure_ascii=False,indent=2))
if __name__=='__main__':asyncio.run(main())
