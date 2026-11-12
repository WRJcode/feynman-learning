# 来源与范围

阅读与归档：2026-11-12（UTC）。本轮读取官方 README 和核心文档，未深入源码、未新增 Playwright 试跑。链接为可变页面，未固定提交。

## S1：官方仓库

- https://github.com/microsoft/playwright
- https://raw.githubusercontent.com/microsoft/playwright/main/README.md
- 定位：浏览器自动化与测试；支持 Chromium、Firefox、WebKit；库、测试框架、CLI、MCP 等入口须区分。

## S2：测试框架介绍

- https://playwright.dev/docs/intro
- 支持：测试执行、断言、隔离、并行及报告。普通自动化代码不要求模型，AI 集成也不代表核心库自行规划。

## S3：自动等待

- https://playwright.dev/docs/actionability
- 支持：按动作进行可操作性检查，满足条件后执行，超时失败。检查因动作而异，不能概括成每种操作都有相同检查。

## S4：断言

- https://playwright.dev/docs/test-assertions
- 支持：给定预期与匹配器，网页专用断言可自动重试直到满足条件或超时。通过只支持已检查的条件，不保证全部业务正确。

## S5：本轮比较依据与先前操作

- [Browser Use 来源与固定版本试跑](../browser-use/sources.md)：当前所学 1.0 路径为 Python REPL、浏览器辅助能力与 CDP，不能推断内部必经 Playwright。
- [看板设计与验证说明](../../docs/dashboard-design.md)：此前 AI 用 Playwright 检查过搜索、证据展开和手机布局。本轮没有新增 Playwright 实验；既有操作不是用户独立应用证据。
- computer use 比较为 AI 对执行方式的概念区分，未对某个指定 computer-use 产品做源码或性能比较。截图驱动和元素接口可组合，不互斥。
