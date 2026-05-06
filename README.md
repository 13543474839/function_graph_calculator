纯前端/轻量级图形计算器
一个基于 FastAPI + HTML5 Canvas 的数学函数图形计算器。

技术栈
后端：FastAPI (Python)
前端：原生 HTML + CSS + JS (无框架，单文件在 static/index.html)
解析：自研简易表达式解析器 (expr_parser.py)
快速启动
确保安装了 uv，在项目根目录运行：
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload

浏览器访问 `http://localhost:8000` 即可。

## 外网访问（内网穿透）
使用**樱花 FRP (SakuraFrp)**：
1. 本地保持 uvicorn 运行在 8000 端口。
2. 樱花面板配置：协议选 `HTTP` 或 `HTTPS`，本地 IP 填 `127.0.0.1`，本地端口填 `8000`。
3. 启动隧道，将生成的链接发给他人即可跨局域网使用。

---

## ⚠️ 核心踩坑记录（后续修改必看！）

### 1. 表达式解析器的“试运行陷阱” (`expr_parser.py`)
- **问题**：之前第4步试运行用的是 `x=0`。如果用户输入 `1/x`，试运行直接触发 `ZeroDivisionError`，导致合法公式被判定为非法。
- **修复**：试运行必须用 `x=1.0`。并且 `except` 捕获异常时，必须区分**语法错误**（直接拦截）和**数学算术错误**（如 `ZeroDivisionError`, `OverflowError`，应该放行 `pass`）。

### 2. 采样器的容错处理 (`sampler.py`)
- **问题**：虽然解析器放行了，但在密集采样时（比如 `tan(x)` 接近 90 度），依然可能算出 `inf` 或报错。
- **修复**：在第3步计算 `y = f(x)` 时，必须用 `try...except` 包裹单次计算。捕获到 `ZeroDivisionError` 等异常时，直接赋值 `y = float("nan")`。最后统一将 `nan` 转为 `None`（JSON 的 `null`）传给前端。

### 3. 前端画布的“断线逻辑” (`index.html`)
- **问题**：遇到 `1/x` 的 `x=0` 处，如果不断开画笔，会把正负无穷大连成一条竖线。
- **修复**：前端遍历后端返回的点时，遇到 `y === null` 或 `!isFinite(y)` 时，**千万不能画线**，必须执行 `ctx.moveTo(nextX, nextY)` 移动画笔，跳过当前点，直到遇到下一个有效点再 `lineTo`。
