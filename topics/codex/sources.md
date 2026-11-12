# 来源与范围

读取及归档日期：2026-11-12（UTC）。本轮读取官方文档，没有阅读 Codex 核心源码或新运行 Codex CLI 实验；不是全产品审计。

## S1：智能体循环与执行框架

- https://openai.com/index/unrolling-the-codex-agent-loop/
- 2026-01-23 官方工程文章，侧重 Codex harness 与 CLI。
- 支持：框架组织用户、模型与工具的交互；模型返回工具请求或回复，执行结果进入后续输入。
- 版本边界：文章介绍当时架构，不保证所有入口当前细节完全相同。

## S2：项目指令

- https://learn.chatgpt.com/docs/agent-configuration/agents-md.md
- 原链接 https://developers.openai.com/codex/guides/agents-md/ 当前重定向至上述文档。
- 支持：发现并组合适用的 AGENTS.md 指令。项目指令不等于操作系统或执行环境的访问权限。

## S3：Skill

- https://learn.chatgpt.com/docs/build-skills.md
- 原链接 https://developers.openai.com/codex/skills/ 当前重定向至上述文档。
- 支持：Skill 打包说明、资源和可选脚本；先呈现名称描述，选用后加载完整说明；支持明确调用及任务匹配。
- 安装不等于每轮调用，具体入口能力以版本为准。

## S4：本地索引实践

- [学习索引](../../LEARNING-INDEX.md)、[仓库规则](../../AGENTS.md)。
- 可见执行记录：AI 读取主题目录、来源及复测队列，生成索引和 README 入口；Python 检查报告当时两个主题收录、10 个本地链接有效，git diff --check 通过。
- 这是当前会话的实际工具操作，没有另启动 Codex CLI，也没有保存独立运行日志。数字只对应索引初版，后续增补会改变链接数量。
- 用户对事前预测回答“不明确”；AI 随后示范。不能作为用户独立完成任务或能应用的证据。
