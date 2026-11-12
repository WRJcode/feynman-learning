# 学习看板设计

## 目标

让学习者快速看到学过什么、解释到哪里、缺什么证据，并能追溯原话和来源。保留现有 Markdown 为唯一内容来源，网页只读展示；网页不自动修改学习状态。

## 信息结构

1. 首页：主题数、知识点数、有解释证据数、复测通过数。统计单位明确，不生成掌握百分比。
2. 理解看板：按知识点分为待验证／补充、能解释、能应用、复测通过。原始状态原文保留；“有情境判断”等非标准状态先归入待验证，不擅自升级。
3. 主题档案：当前总结、来源、学习会话、理解图。第一版链接 GitHub 原文；后续可生成站内阅读页并渲染 Mermaid。
4. 实践入口：展示明确标注为 AI 建议的下一步。未来可增加实践产物、验收依据及复测记录，不推断用户已掌握。

## 视觉与交互

米白底、森林绿主色、低饱和阶段栏；强调原话和证据。桌面四栏，手机单栏。搜索主题、知识点、状态和边界，证据按需展开；保留键盘焦点及空搜索结果。当前预览不支持拖动改状态、在线编辑或自动通知。

## 本地预览

运行 `python scripts/build_dashboard.py`，生成 `web/index.html`。可直接用浏览器打开生成文件，也可运行 `python -m http.server 8000 --directory web` 后访问本机地址。生成器不需要第三方依赖。

数据来自 `topics/*/index.md`，新主题只要遵守现有四列表格格式即可纳入。来源与会话文件名自动发现。修改 Markdown 后需重新生成。当前日期与复测提示针对 2026-11-12 的设计预览；正式版应从记录解析，避免硬编码复测状态和日期。

## GitHub Pages 发布方案（尚未执行）

GitHub Actions 在 main 内容更新后运行生成器，再发布 web 目录。只发布明确选择的内容，不上传整个仓库或凭据；项目站点路径兼容，不需要数据库。首次上线前应将“本地预览”提示替换为真实发布状态。

当前仓库私有。GitHub Free 的 Pages 面向公开仓库，私有仓库支持取决于套餐；私有仓库生成的站点不自动私有。Pages 私有访问控制通常要求组织的 Enterprise Cloud 能力。因此本次只准备本地版本，未开启 Pages、变更仓库可见性或发布内容。需要先确定公开精选内容，还是使用有登录保护的托管方式。

参考：https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

访问控制：https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site

## 验证与后续

已用 Chromium 检查：三个主题、16 张知识点卡片；搜索 Codex 得到四条；证据展开；无结果状态；390px 手机宽度无横向溢出。浏览器截图仅保存在本次环境 /tmp 下，不是学习应用证据。

后续优先做站内文档与 Mermaid 阅读、复测记录展示，再考虑编辑和在线 Agent。静态 Pages 不能直接安全保存模型密钥或承担服务器端 Agent 执行。
