# 学习索引

依据仓库现有记录整理，更新于 2026-11-12（UTC）。本页是导航，不替代各知识点的证据记录；不根据对话次数或阅读数量判断掌握程度。

| 已归档主题 | 材料来源 | 当前学习状态 | 待核实或待验证 |
| --- | --- | --- | --- |
| [Nacos](topics/nacos/index.md) | [来源清单](topics/nacos/sources.md)：官方概览、AI 管理中心概述 | 核心管理对象、市场抽象及 AI 专区关联已有初步解释证据；配置映射及资源协作关系仍待验证 | 配置映射的独立解释；调用、配置生效与隔离边界；ARD 范围与 Agent 使用方式；新场景迁移 |
| [OpenHands](topics/openhands/index.md) | [来源与实验](topics/openhands/sources.md)：官方仓库、SDK 文档与定点源码、脚本化模型的本地实验、Codex 对照资料 | 执行反馈循环、工具与子 Agent、权限及 AI coding 场景已有不同程度的解释证据；尚无延迟复测通过记录 | 部署级审批接入、文件隔离边界、真实多 Agent 协作；将抽象用于新任务的能力 |
| [Codex](topics/codex/index.md) | [来源与实践](topics/codex/sources.md)：官方循环、项目指令和 Skill 文档，学习索引实践 | 能初步解释“将循环机制工程化”；职责及系统范围已接触校准 | 校准后的独立重讲；项目指令、Skill 与权限的区分；实际应用 |
| [Browser Use](topics/browser-use/index.md) | [来源与试跑](topics/browser-use/sources.md)：官方文档、定点源码及真实 Chromium 实验 | 循环与老师—学生关联能初步解释 | 精确组件分工、版本差异、实验与自主模型能力的证据边界；独立应用 |

| [Playwright](topics/playwright/index.md) | [官方来源](topics/playwright/sources.md)：README、自动等待与断言文档 | 自动化测试定位能初步解释；封装抽象与类比为 AI 示范 | 独立抽象与重讲；元素接口、截图方式及验证边界 |

## 查阅路径

- 看当前理解与图：[Nacos 总结](topics/nacos/synthesis.md)、[OpenHands 总结](topics/openhands/synthesis.md)、[Codex 总结](topics/codex/synthesis.md)、[Browser Use 总结](topics/browser-use/synthesis.md)、[Playwright 总结](topics/playwright/synthesis.md)。
- 查解释原话与修正过程：进入各主题目录页中的会话链接。
- 查平台差异：[OpenHands 与 Codex 对照](topics/openhands/comparison-codex.md)。该文是学习输入，不是用户掌握证据。
- 安排复测：[复测队列](reviews/queue.md)。各主题均待安排，本仓库没有后台提醒。

## 收录边界

本页仅收录已有 `topics/<主题>/index.md` 的主题。OpenCode 已在对话中讨论，但尚未形成仓库主题记录，因此未列入已归档主题。OpenHands 的本地工具实验使用脚本替代模型响应，不代表已验证真实模型自主纠错或多 Agent 协作。

## 本次索引的验收依据

1. 完整性：仓库现有主题目录页均已收录。
2. 可追溯性：状态和未决点可回到主题目录页、来源和复测队列核对；保留“初步”“提示后”等限制，不升级掌握状态。
3. 可导航性：本页及 README 新增的本地链接指向实际存在的文件。

索引由 AI 整理并检查；尚未经过用户验收。本次操作不构成用户“能应用”的学习证据。
