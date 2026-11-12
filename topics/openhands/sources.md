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

权限审批的具体触发、授权主体和多智能体编排范围未在此次定点阅读或实验中核实。老师与学生是用户类比；图中具体组件映射由 AI 辅助，不是产品官方比喻。
