"""SDK loop demo: scripted model responses, real tools and conversation state."""
import json
from pathlib import Path
from unittest.mock import patch

from litellm.types.utils import Choices, Message as ProviderMessage, ModelResponse, Usage
from pydantic import SecretStr
from openhands.sdk import LLM, Action, Agent, LocalConversation, Observation, TextContent, ToolDefinition
from openhands.sdk.tool import Tool, ToolExecutor, register_tool

ROOT = Path('/workspace/openhands-study')

class WriteNoteAction(Action):
    text: str

class WriteNoteObservation(Observation):
    path: str
    contents: str

    @property
    def to_llm_content(self):
        return [TextContent(text=f'WROTE {self.path}: {self.contents}')]

class WriteNoteExecutor(ToolExecutor):
    def __call__(self, action, conversation=None):
        path = Path(conversation.state.workspace.working_dir) / 'note.txt'
        path.write_text(action.text, encoding='utf-8')
        return WriteNoteObservation(path=str(path), contents=action.text)

class WriteNoteTool(ToolDefinition[WriteNoteAction, WriteNoteObservation]):
    @classmethod
    def create(cls, conv_state=None, **params):
        return [cls(description='Write a note.txt file in the workspace.',
                    action_type=WriteNoteAction, observation_type=WriteNoteObservation,
                    executor=WriteNoteExecutor())]

register_tool(WriteNoteTool.name, WriteNoteTool)


def reply(name, args, index):
    return ModelResponse(id=f'demo-{index}', model='gpt-4o', created=0,
        choices=[Choices(index=0, message=ProviderMessage(role='assistant',content='',
            tool_calls=[{'id':f'call-{index}','type':'function','function':{
                'name':name,'arguments':json.dumps(args)}}]),finish_reason='tool_calls')],
        usage=Usage(prompt_tokens=10,completion_tokens=10,total_tokens=20))

results=[]
for case, missing in [('write_note',False),('unknown_tool_then_recover',True)]:
    workspace=ROOT/case
    workspace.mkdir(exist_ok=True)
    artifact=workspace/'note.txt'
    assert not artifact.exists(), 'Use a fresh workspace for each trial.'
    calls=[]
    events=[]
    answers=[]
    if missing:
        answers.append(reply('nonexistent_demo_tool',{},0))
    answers.append(reply(WriteNoteTool.name,{'text':'Hello from the real OpenHands tool executor.'},len(answers)))
    answers.append(reply('finish',{'message':'Done.'},len(answers)))
    def scripted_completion(messages, **kwargs):
        calls.append(messages)
        return answers.pop(0)
    llm=LLM(model='gpt-4o',api_key=SecretStr('demo-no-real-key'),usage_id=case)
    agent=Agent(llm=llm,tools=[Tool(name=WriteNoteTool.name)])
    with patch('openhands.sdk.llm.llm.litellm_completion',side_effect=scripted_completion):
        conversation = LocalConversation(agent=agent,workspace=str(workspace),callbacks=[events.append],
                          visualizer=None,max_iteration_per_run=5,
                          persistence_dir=str(workspace/'state'),
                          profile_store_dir=ROOT/'profiles',delete_on_close=False)
        try:
            conversation.send_message('Write note.txt, then finish.')
            conversation.run()
            status=conversation.state.execution_status.value
        finally:
            conversation.close()
    assert artifact.read_text()=='Hello from the real OpenHands tool executor.'
    assert status=='finished',status
    last_messages=json.dumps(calls[-1],default=str)
    assert 'WROTE' in last_messages, 'Tool observation must reach next model request.'
    errors=[e for e in events if type(e).__name__=='AgentErrorEvent']
    assert bool(errors)==missing
    if missing:
        assert 'not found' in errors[0].error
        assert 'nonexistent_demo_tool' in json.dumps(calls[1],default=str)
    result={'case':case,'status':status,'model_calls_scripted':len(calls),
            'event_types':[type(e).__name__ for e in events],
            'error_messages':[e.error for e in errors],
            'file':str(artifact),'file_contents':artifact.read_text(),
            'observation_in_next_model_request':True,
            'real_model_invoked':False}
    results.append(result)
(ROOT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False,indent=2))
