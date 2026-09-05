# Nav Station — AI Agent Guide

## 项目简介

个人导航站：Vue 3 SPA + FastAPI API，JWT 多用户认证，SQLite 持久化。

## 读文档顺序

1. `docs/architecture/overview.md`：全栈边界、部署和 API
2. 前端任务读 `docs/architecture/frontend.md`
3. 后端任务读 `docs/architecture/backend.md`
4. UI 任务额外读 `VISUAL.md`；验收任务读 `ACCEPTANCE.md`

## 改代码后必做

新增或删除目录、composable、组件、router、model，或修改 API、认证、localStorage key、依赖、部署方式后，执行 `.cursor/skills/update-architecture-docs/` 并更新架构文档。纯样式、文案和不改变结构的 bug fix 通常不需要更新。

## 关键路径

- 前端入口：`src/App.vue`
- API 客户端：`src/api/client.js`
- 前端逻辑：`src/composables/`
- 后端入口：`backend/app/main.py`
- 路由：`backend/app/routers/`
- 数据模型：`backend/app/models/entities.py`
- 配置：`backend/app/config.py`
