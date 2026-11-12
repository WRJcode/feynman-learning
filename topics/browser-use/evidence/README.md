# 试跑证据

Browser Use 1.0.2，Pydantic AI FunctionModel，真实 Chromium /usr/bin/chromium。完整过程见 [results.json](results.json)，页面状态见 [browser-state.json](browser-state.json)，截图见 [browser-result.png](browser-result.png)。模型响应全部预设，无真实模型推理。

复现：在独立虚拟环境安装 requirements.txt，在本目录执行 run_demo.py。需要本地 Chromium，可按环境修改脚本浏览器路径。ROOT 根据脚本位置确定；复跑将覆盖本目录实验结果。未复制虚拟环境。

真实测试页通过 CDP 写入空白页，不访问外部业务网站，不使用个人浏览器资料。脚本验证读取初始列表、错误回传、修正后筛选结果和跨轮变量保留。首次沙箱内启动未完成，终止后获准在外层执行成功。最终复跑退出码为 0。

原工作目录为 /workspace/browser-use-study，结果中的绝对路径属于本次环境，不保证其他机器存在。results.json 仅保存模型请求中的可见工具反馈，不保存隐藏推理。没有同任务真实模型性能、登录流程或云浏览器验证。
