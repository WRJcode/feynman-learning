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


from openhands.sdk.security.confirmation_policy import AlwaysConfirm, NeverConfirm, ConfirmRisky
from openhands.sdk.security.risk import SecurityRisk
ROOT = Path('/workspace/openhands-study/security-check-20261112')
ROOT.mkdir(exist_ok=True)
reports=[]
for decision in ['approve','reject']:
    workspace=ROOT/decision
    workspace.mkdir(exist_ok=True)
    target=workspace/'note.txt'
    assert not target.exists()
    replies=[reply(WriteNoteTool.name,{'text':'Approved note.'},0),reply('finish',{'message':'done'},1)]
    requests=[];events=[]
    def provider(messages,**kwargs):
        requests.append(messages)
        return replies.pop(0)
    conversation=LocalConversation(
        agent=Agent(llm=LLM(model='gpt-4o',api_key=SecretStr('mock-key'),usage_id=decision),tools=[Tool(name=WriteNoteTool.name)]),
        workspace=str(workspace),profile_store_dir=ROOT/'profiles',
        callbacks=[events.append],visualizer=None,max_iteration_per_run=4)
    try:
        conversation.set_confirmation_policy(AlwaysConfirm())
        with patch('openhands.sdk.llm.llm.litellm_completion',side_effect=provider):
            conversation.send_message('Write a note.')
            conversation.run()
            waiting=conversation.state.execution_status.value
            assert waiting=='waiting_for_confirmation',waiting
            assert not target.exists()
            if decision=='reject':
                conversation.reject_pending_actions('Rejected in study demonstration.')
            conversation.run()
            assert conversation.state.execution_status.value=='finished'
        assert target.exists()==(decision=='approve')
        if decision=='reject':
            assert any(type(e).__name__=='UserRejectObservation' for e in events)
            assert 'Rejected in study demonstration.' in json.dumps(requests[-1],default=str)
        reports.append({'decision':decision,'status_before_decision':waiting,'file_before_decision':False,
                        'file_after_decision':target.exists(),'final_status':conversation.state.execution_status.value,
                        'events':[type(e).__name__ for e in events],'real_model_invoked':False})
    finally:
        conversation.close()
policy=ConfirmRisky()
assert policy.should_confirm(SecurityRisk.HIGH)
assert not policy.should_confirm(SecurityRisk.LOW)
assert policy.should_confirm(SecurityRisk.UNKNOWN)
(ROOT/'results.json').write_text(json.dumps({'cases':reports,'default_risk_policy':{'high':True,'low':False,'unknown':True}},indent=2))
print(json.dumps(reports,indent=2))
