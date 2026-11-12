# 来源与证据

阅读、试跑和归档日期：2026-11-12（UTC）。

## S1：官方 README

- https://github.com/browser-use/browser-use
- https://raw.githubusercontent.com/browser-use/browser-use/main/README.md
- 当前主分支 README，未固定提交，后续可能变化。
- 定位：浏览器智能体；提供 Python 库、CLI 与云服务。1.0 让模型编写 Python，通过持久 REPL、浏览器辅助能力和 CDP 操作浏览器。

## S2：迁移说明

- https://raw.githubusercontent.com/browser-use/browser-use/main/MIGRATING.md
- 范围：0.x 至 1.0 的引擎变化、默认模型与浏览器、兼容和权限边界；不能将旧版固定动作式说明直接套到当前版本。

## S3：定点源码

- https://raw.githubusercontent.com/browser-use/browser-use/main/browser_use/agent/service.py
- https://raw.githubusercontent.com/browser-use/browser-use/main/browser_use/agent/loop.py
- 读取 Agent 与循环相关代码，随后检查本地安装版本的模型接入、Python 工具、结束工具与浏览器启动等实现，不是全仓审计。
- 发布包固定 browser-use==1.0.2；依赖 pydantic-ai-slim==2.66.0、browser-harness==0.1.13。主分支与发布包不能假定逐行相同。

## S4：真实执行与模拟模型的本地试跑

- [实验说明](evidence/README.md)、[脚本](evidence/run_demo.py)、[运行结果](evidence/results.json)、[页面状态](evidence/browser-state.json)、[截图](evidence/browser-result.png)。
- 真实 Browser Use Agent、Python REPL、Chromium 与 CDP；使用 FunctionModel 预设四次响应，不调用外部模型。
- 初始列表三个主题；不存在的选择器触发错误；错误进入后续请求；修正后输入 Codex，只剩一项，计数“1 个主题”；前轮变量保留。断言通过，退出码 0。
- 后续修正是预设的，不证明模型自主纠错、页面理解或规划。AI 执行实验不等于用户独立应用。
