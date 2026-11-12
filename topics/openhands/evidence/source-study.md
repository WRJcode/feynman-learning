# OpenHands 源码学习与最小试跑

日期：2026-11-11。目标：理解 OpenHands 的任务执行链，不推断无法读取的 CSDN 文章内容。

## 固定源码版本

- Agent Canvas：OpenHands/OpenHands，提交 `c79599d6c0f6f3747ec172ffc2c56e2a5bad7657`。
- Software Agent SDK：OpenHands/software-agent-sdk，提交 `5ff99f1b6ca28f7d16870b69f57a31351e59bcd0`，项目版本 1.61.0。
- 两个仓库仅用于阅读，未修改其跟踪文件。SDK 通过 `uv sync --frozen --package openhands-sdk --no-dev` 安装在项目 .venv 中。

## 追踪到的源码关系

1. Canvas 的 `src/api/conversation-service/agent-server-conversation-service.api.ts:519` 中，`sendMessage()` 调用类型化客户端的 `sendEvent(..., {run: true})`，将消息交给后端并请求运行。此处为源码阅读，未启动前端或 HTTP Server。
2. SDK `openhands-sdk/openhands/sdk/conversation/impl/local_conversation.py:2041` 的 `send_message()` 接收用户消息；`:2136` 的 `run()` 管理循环，`:2237` 调用 `agent.step()`。
3. SDK `openhands-sdk/openhands/sdk/agent/agent.py:738` 的 `step()` 准备上下文并调用 LLM 的 `generate()`，处理回复中的工具请求与后续状态。
4. 同文件 `:1557` 的 `_execute_action_event()` 找到工具并调用 executor，将真实返回值包装为 ObservationEvent；执行中的部分参数错误可变成 AgentErrorEvent。
5. 事件被会话保存并用于下一轮模型输入；下面的实验检查了这一点。未知工具的错误也能返回到后续模型请求中。

这些是当前固定版本的实现，不应自动推广到所有旧版 OpenHands 或第三方 ACP 智能体。

## 实验设计与结果

`run_demo.py` 使用真实 SDK Agent、LocalConversation、工具注册、参数模型、executor 和事件流。模型网络调用由 `unittest.mock.patch` 替换为预设工具请求，不使用真实密钥。写文件工具为本次自定义的 `write_note`，不是官方 FileEditorTool。

| 案例 | 预设模型响应 | 实际验证 |
| --- | --- | --- |
| 正常写文件 | write_note → finish | note.txt 实际生成；观察进入下一次模型请求；finished |
| 未知工具后继续 | nonexistent_demo_tool → write_note → finish | 未知工具生成 AgentErrorEvent；错误进入下一次请求；正确工具实际写文件；finished |

正常路径发生 2 次模拟模型调用，错误路径 3 次。完整结果保存在 results.json。两条路径都明确断言文件内容、终止状态和反馈是否进入模型请求，错误路径额外检查错误事件。

注意：第二条后续调用是预设的，不证明真实模型自主纠错，也不证明真实任务成功率。没有启动完整 Canvas、远程 Server、Docker 或自动化服务。

## 运行说明与实际限制

使用 `/workspace/openhands-sdk-study/.venv/bin/python` 执行 run_demo.py，环境设为 `LITELLM_LOCAL_MODEL_COST_MAP=True OPENHANDS_SUPPRESS_BANNER=1`。该脚本要求两个案例目录中没有 note.txt，避免将旧产物误当作本次成功。再次试跑请使用新的实验根目录。

首次尝试遇到默认 ~/.openhands 配置目录不可写，已通过 LocalConversation 的 profile_store_dir 将配置限定在本实验目录。LocalConversation 不支持上下文管理器，实验采用 try/finally 显式 close()。这些是本次运行条件与 API 使用问题，不是已确认的产品缺陷。

## 学习提炼

- 模型生成的是下一步建议或工具请求；工具 executor 才会改变文件等外部状态。
- 单次 step 与整个 run 循环职责不同；会话管理任务状态和过程。
- action、observation 和 error 形成可观察的反馈链。错误提供继续调整的机会，但不能保证模型会正确调整。
- Canvas 负责交互入口，Server 暴露远程接口，SDK 承载执行逻辑；自动化服务负责触发时机，未在本次试跑覆盖。

当前只完成源码定点追踪与脚本化模型试跑，不把这些结果当成对整个系统的全面验收。
