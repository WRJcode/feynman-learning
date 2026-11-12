# 来源与证据

- 阅读与实验日期：2026-11-11；本轮学习归档：2026-11-12（UTC）。
- 阅读范围：官方 README、架构文档和下列定点源码；不是全仓库审计。

## S1：OpenHands 主仓库与架构

- https://github.com/OpenHands/OpenHands
- https://github.com/OpenHands/OpenHands/blob/main/docs/architecture.md
- 本地固定提交：`c79599d6c0f6f3747ec172ffc2c56e2a5bad7657`。
- 源码定位：`src/api/conversation-service/agent-server-conversation-service.api.ts:519`，sendMessage 使用类型化客户端发送消息并请求运行。
- 核心摘记：当前主仓库侧重 Agent Canvas；界面层与后端执行层分离。

## S2：Software Agent SDK

- https://github.com/OpenHands/software-agent-sdk
- https://docs.openhands.dev/sdk/arch/overview
- 本地固定提交：`5ff99f1b6ca28f7d16870b69f57a31351e59bcd0`；项目版本 1.61.0。
- 源码定位：`openhands-sdk/openhands/sdk/conversation/impl/local_conversation.py:2041`（send_message）、`:2136`（run）、`:2237`（调用 agent.step）；`openhands-sdk/openhands/sdk/agent/agent.py:738`（step）、`:1557`（执行动作并形成观察）。
- 核心摘记：模型决策、工具执行、会话状态和事件形成反馈链。

## S3：最小试跑的本地证据

- [结果](evidence/results.json)、[实验脚本](evidence/run_demo.py)、[完整实验说明](evidence/source-study.md)。
- 实际运行 SDK 与自定义写文件工具；模型响应被脚本替代。
- 正常路径两次模拟模型调用，未知工具后继续路径三次；均创建真实文件并断言反馈进入下一次模型请求。
- 后续正确调用是预设的，不证明模型自主纠错。未启动 Canvas 网页、远程 Server、Docker 或自动化服务。原产物绝对路径属于本次执行环境，JSON 是留存结果，不能假定其他环境有这些路径。

## S4：与 Codex 对照的官方资料

- https://github.com/openai/codex
- https://developers.openai.com/blog/codex-as-a-platform
- https://learn.chatgpt.com/docs/auth?surface=cli
- 对照范围：产品入口、开放运行框架、模型认证与扩展方式；没有同任务性能或成本测试。
- 核心校准：二者均有智能体执行和集成能力；不能概括成 OpenHands 是平台、Codex 只是模型。

完整对照与逐项来源见[OpenHands 与 Codex](comparison-codex.md)。该对照为 AI 整理的学习输入，不能作为用户掌握证据。

## S5：未读取材料

- 用户提供：https://blog.csdn.net/CrystalwaveEagle34/article/details/170410615
- 正文未获取，直接请求返回 HTTP 521；不从其标题或链接推断文章结论。

## 来源边界

第一轮没有核实权限审批与多 Agent 范围；第二轮已补充 S6、S7。具体部署的审批主体、确认处理器接入、真实多模型协作效果仍未验证。老师与学生是用户类比；图由 AI 辅助绘制，不是官方比喻。

## S6：权限确认与多智能体编排的补充核实

- 阅读日期：2026-11-12；固定 SDK 提交与 S2 相同。
- 官方资料：https://docs.openhands.dev/sdk/guides/security 、https://docs.openhands.dev/sdk/guides/task-tool-set 、https://docs.openhands.dev/sdk/guides/agent-dynamic-workflow 。
- 定点源码与版本边界见[报告](evidence/permissions-and-orchestration.md)。
- 核实内容：确认策略、拒绝反馈、Task 委派与恢复、并行及 workflow 组合、共享工作目录。
- 重要条件：TaskManager 无 confirmation_handler 时可继续待确认动作；不能仅凭继承策略认定部署中有人审批。
- 多智能体部分为文档与源码核对，未运行真实多模型协作。

## S7：动作确认的最小试跑

- [脚本](evidence/check-security.py)、[结果](evidence/security-results.json)。
- 模型调用被脚本替代；真实 SDK 与自定义工具执行。
- 批准前没有文件，批准后生成；拒绝前后均无文件，拒绝理由进入后续模型输入。也检查了 ConfirmRisky 对高、低及未知风险的默认判断。
- 不验证真实模型决策、页面交互、服务端授权或操作系统权限提升。脚本含本次环境绝对路径，复跑需准备对应 SDK 和新的实验目录。

## S8：AI coding 机制的新增资料

- 检索日期：2026-11-12；本轮基于已读官方文档整理，没有新代码试跑。
- https://openai.com/index/unrolling-the-codex-agent-loop/ ：2026-01-23 工程文章，说明模型、工具、上下文与 agent loop 的关系；具体实现以版本为准。
- https://docs.openhands.dev/sdk/arch/overview ：SDK 的 Agent、Conversation、Tool、Workspace 等角色，与 S2 源码证据相互参照。
- https://openai.com/index/introducing-upgrades-to-codex/ ：2025-09-15 历史发布资料，介绍 GPT-5-Codex 针对工程任务的训练；不能据此断言所有当前模型使用同一训练流程。
- https://openai.com/index/introducing-codex/ ：2025-05-16 历史发布资料，页面已注明过时；仅支持历史训练与开发环境介绍，不将旧价格、联网或产品默认值作为当前事实。
- 观点归属：可执行工程环境和检查反馈有助于迭代，是本轮综合解释；不承诺任务可被完全自动验证，也未比较两者性能。
