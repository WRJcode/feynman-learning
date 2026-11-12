# OpenHands 与 Codex：学习对照

- 整理日期：2026-11-12（UTC）。
- 依据：本会话 2026-11-11 已检索的官方资料及 OpenHands 源码定点阅读。
- 归属：由 AI 应用户要求整理的学习输入，不是用户已经独立掌握的解释。

## 核心结论

两者都具备智能体任务执行能力，也都提供开发者集成入口。差别主要在产品整合方式、模型配置方式和系统组件组织；不能用“OpenHands 是平台、Codex 只是模型”来区分。

## 相同能力与不同取向

| 比较维度 | OpenHands | Codex | 依据 |
| --- | --- | --- | --- |
| 产品与组件 | Canvas 提供交互控制，SDK/Agent Server 承担核心执行，自动化服务负责触发 | 有 CLI、IDE 和云端体验，并开放可集成运行框架 | O1、O2、C1、C2 |
| 模型接入 | SDK 通过配置接入所选模型服务 | 常见方式为 ChatGPT 登录或 API；CLI 支持满足兼容要求的自定义提供商 | O2、C1、C3 |
| 工具 | 有终端、文件编辑等现成工具，也支持自定义工具 | 有内置执行能力，也能通过 MCP 等方式扩展 | O2、C2 |
| 执行环境 | 可用本地、容器和远程工作空间 | CLI 在本地运行，另有云端服务；不能把本地 CLI 与托管云端混为一谈 | O1、O2、C1 |
| 二次开发 | SDK、Agent Server 与界面分层，可以组合或替换应用层 | SDK、app-server、非交互执行等提供程序化集成方式 | O2、C2 |
| 源码开放 | 本次阅读的主仓库和 SDK 为开源项目 | CLI、app-server、SDK 等组件开源；模型访问和托管服务另计 | O1、O2、C1、C2 |

表格描述可配置能力，不保证任意模型、工具或部署方式直接兼容，也不表示某项能力只属于一方。

## 二者可以组合

OpenHands 的 Agent Canvas README 明确列出 Codex 作为可接入智能体后端之一（O1）。因此选择并非互斥：可以由 Canvas 提供统一交互入口，接入 Codex 执行任务。该组合本轮未部署，认证、适配器和具体功能可用性需按部署文档检查。

## 学习上的使用取向（AI 建议）

- 研究组成与执行链：可从 OpenHands 的 Conversation、Agent、Tool Executor、Event 入手，已完成两条模拟模型的实际试跑。
- 直接使用开发助手或嵌入 Codex：可从 Codex 现成入口、SDK 或 app-server 入手。

这是学习路径建议，不是对两者能力高低的评定。

## 验证范围与不可得结论

- OpenHands：已读定点源码，已用真实 SDK 与自定义工具执行最小实验；模型回复为脚本模拟。
- Codex：本轮比较主要来自官方文档与本会话的实际使用，不是完整源码审计或标准化对照测试。
- 未做同一模型、同一任务、同一权限配置的对照，不判定谁更聪明、更可靠、更快或更便宜。
- 模型费用、托管费用和自部署运维成本分别计算；没有在本轮比较价格或额度。
- 执行循环、上下文和工具反馈是可比较结构；未经查证的审批链和多 Agent 编排细节不纳入结论。

## 来源

### O1：OpenHands 主仓库

https://github.com/OpenHands/OpenHands

固定源码版本与阅读范围见[来源 S1](sources.md#s1openhands-主仓库与架构)。

### O2：SDK 官方架构

https://docs.openhands.dev/sdk/arch/overview

https://github.com/OpenHands/software-agent-sdk

固定源码与实验边界见[来源 S2、S3](sources.md#s2software-agent-sdk)。

### C1：Codex 官方开源仓库

https://github.com/openai/codex

### C2：Codex 作为平台的官方说明

https://developers.openai.com/blog/codex-as-a-platform

### C3：认证与自定义模型提供商

https://learn.chatgpt.com/docs/auth?surface=cli

外部文档可能随版本改变；本笔记记录本会话已读取的内容，未保存网页全文快照。

## 共同机制的后续学习

[第三轮会话](sessions/2026-11-12-03.md)记录了用户如何把二者归入“通用智能体循环在编程场景中的适配”：模型能力、项目上下文、开发工具和工程反馈共同支持迭代。当前[场景图](synthesis.md#第三轮新增ai-coding-的场景抽象)保留这一抽象，并区分 AI 补充与用户表达。本轮没有新增两产品的性能对照结果。
