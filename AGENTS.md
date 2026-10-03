# Nav Station — AI Agent Guide

## 项目简介

导航站：Vue 3 SPA + FastAPI API，JWT 多用户认证，SQLite 持久化；含个人网址目录与全局共享广场。

## 读文档顺序

1. `docs/architecture/overview.md`：全栈边界、部署和 API
2. 前端任务读 `docs/architecture/frontend.md`
3. 后端任务读 `docs/architecture/backend.md`
4. UI 任务额外读 `VISUAL.md`；验收任务读 `ACCEPTANCE.md`

## 改代码后必做

新增或删除目录、composable、组件、router、model，或修改 API、认证、localStorage key、依赖、部署方式后，执行 `.cursor/skills/update-architecture-docs/` 并更新架构文档。纯样式、文案和不改变结构的 bug fix 通常不需要更新。

## 关键路径

- 前端入口：`src/App.vue`
- API 客户端：`src/api/client.js`；AI 字段建议（mock）：`src/api/aiSiteSuggest.js`
- 前端逻辑：`src/composables/`
- 后端入口：`backend/app/main.py`
- 路由：`backend/app/routers/`
- 数据模型：`backend/app/models/entities.py`
- 配置：`backend/app/config.py`

## Cursor Cloud specific instructions

Cloud Agent 的 `install` 会安装 `python3.12-venv`、执行 `npm ci`，并在 `backend/.venv` 安装 `backend/requirements.txt`。`start` 会在 `backend/` 下执行 `.venv/bin/python -m app.seed`，然后拉起 API 与 Vite。依赖和进程已由环境托管，不要在 `start` 里再装包。

- 前端：`http://127.0.0.1:5173`。Vite 把 `/api` 代理到 `127.0.0.1:9966`。
- 后端：工作目录 `backend/`，命令 `.venv/bin/python run.py`，监听 `0.0.0.0:9966`。健康检查是 `GET /health` 和 `GET /api/health`。
- 种子用户：`yzjiang` 与 `test`，密码都是 `123456`。广场数据来自 `src/data/sites.json`。SQLite 文件是启动目录下的 `nav_station.db`（即 `backend/nav_station.db`）。
- 仓库没有自动化测试。前端生产构建命令是 `npm run build`。
- `AGNES_API_KEY` 只用于广场 AI 字段建议。登录、个人目录和广场浏览不需要它。
- 仓库里的 `vite.config.js` 把 HMR 指到 `wss://test-front.5ai.icu`，那是远程前端隧道用的。Cloud Agent 的 `start` 会写一份临时 Vite 配置，把 HMR 关掉后再启动 `5173`，避免浏览器去连那台隧道。不要把这份临时配置提交进仓库。

## 生产服务器

用户已授权代理长期管理上海主机。每个新会话都会通过 `.cursor/rules/shanghai-server.mdc` 看到这件事。登录、巡检、清磁盘或改 Nginx 之前，先读 `.cursor/skills/operate-shanghai-server/SKILL.md`。

公网入口是 `https://nav.5ai.icu`。SSH 用户是 `yzjiang_root`，主机是 `118.89.189.205`。登录密码只写在本机 `.cursor/server.env`（已被 `.gitignore` 忽略）。这个仓库是公开的，不要把密码、私钥或 `.cursor/server.env` 提交上去。新环境如果没有这个文件，先向用户要回凭据，不要把密码写进仓库。
