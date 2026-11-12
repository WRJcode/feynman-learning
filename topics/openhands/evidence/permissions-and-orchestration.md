# OpenHands：权限确认与多智能体编排核实

日期：2026-11-12。源码固定为 SDK 提交 5ff99f1b6ca28f7d16870b69f57a31351e59bcd0（1.61.0）。本次新增阅读与小实验，不代表所有版本或托管部署采用相同配置。

## 权限确认

- `openhands-sdk/openhands/sdk/security/confirmation_policy.py`：AlwaysConfirm、NeverConfirm、ConfirmRisky；ConfirmRisky 默认 HIGH 阈值、未知风险需要确认。
- `openhands-sdk/openhands/sdk/agent/agent.py:1208`：执行前分析风险，策略命中后置 WAITING_FOR_CONFIRMATION；单独 finish/think 动作不要求确认。
- `openhands-sdk/openhands/sdk/conversation/state.py:129`：SDK 基础状态默认 NeverConfirm；不能据此断言所有产品界面的默认配置。
- `openhands-sdk/openhands/sdk/conversation/impl/local_conversation.py:2891`：reject_pending_actions 产生 UserRejectObservation，将拒绝理由回传。
- `openhands-agent-server/openhands/agent_server/event_service.py:2122`：确认通过后继续 run，拒绝则处理待执行动作。审批的业务角色由接入应用定义，不内置固定上级审批链。
- 这是“是否准许尝试动作”的控制，不会自动授予操作系统文件权限、平台账号权限或改变容器隔离。

### 实际试跑

[脚本](check-security.py)使用真实 SDK 与自定义写文件工具，模型回复由脚本替代。

[结果](security-results.json)：批准与拒绝两条路径都先暂停，文件均未生成；批准后文件生成；拒绝后文件未生成，拒绝原因进入后续模型请求。只验证 SDK 动作确认，不验证 UI、服务器认证或操作系统权限提升。

## 多智能体编排

- `openhands-tools/openhands/tools/task/definition.py`：TaskAction 提供 prompt、subagent_type、resume，TaskObservation 提供任务标识、状态和结果。
- `openhands-tools/openhands/tools/task/manager.py`：创建独立子会话、执行任务、提取最终结果并返回；支持保存和恢复。当前实现复用父工作目录，独立会话不等于文件系统隔离。
- `openhands-tools/openhands/tools/task/impl.py`：TaskExecutor 调用任务管理器，返回完成结果或错误；单次调用阻塞，独立任务可结合并行工具执行机制并发。
- `openhands-sdk/openhands/sdk/subagent/schema.py` 与 registry/load：可用程序或 Markdown 定义专职子 Agent，配置提示、工具、模型档案和资源限制等。
- `openhands-tools/openhands/tools/workflow/impl.py` 和 definition.py：提供 run_agent、map_agents、reduce_agent、pipeline，支持并发上限；Task 路径支持 resume，当前 workflow 路径刻意不暴露恢复。
- 旧 Delegate 路径标为废弃，当前应区分 Task 工具和动态 workflow，避免混用旧版文章说明。

### 子任务审批的具体行为

`TaskManager._set_confirmation_policy` 默认继承父策略，也允许 Agent 定义覆盖。`_run_until_finished` 在等待确认时使用传入 confirmation_handler；当前源码在处理器为 None 时直接继续运行。因此，策略继承不保证有人审批，必须检查接入应用如何配置处理器。此点来自源码阅读，没有用真实子 Agent 场景复现实验。

多智能体部分完成官方文档与源码核对，未启动多个真实模型，不据此保证分工质量、并发安全、自动汇总正确性或默认启用情况。

## 官方文档

- https://docs.openhands.dev/sdk/guides/security
- https://docs.openhands.dev/sdk/guides/task-tool-set
- https://docs.openhands.dev/sdk/guides/agent-dynamic-workflow

本报告原为补充学习材料；现随第二轮学习归档。未因此自动提交或推送。
