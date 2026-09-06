# 架构变更日志

记录架构级决策与边界变化，不替代 Git history。

## 2026-09-06 — 生产稳定性：systemd + 关闭 HTTP/2

- **原因：** 浏览器偶发 `ERR_CONNECTION_CLOSED`（Network 无状态码、0 B，nginx access 无记录），属 TLS/连接层中断；叠加后端曾用 `python run.py` 裸跑，重启窗口会出现旧路由 404。Nginx 1.18 在同一 `:443` 上任一 `listen ... http2` 会使全部站点协商 HTTP/2。
- **变更：** 启用并开机自启 `nav-station-api`（`backend/nav-station-api.service`）；生产与仓库 `nginx/nav.5ai.icu.conf` 改为仅 HTTP/1.1；本机全部 `:443` listen 去掉 `http2` 后 **restart**（非 reload）nginx。
- **影响文件：** `backend/nav-station-api.service`、`nginx/nav.5ai.icu.conf`、`docs/architecture/{overview,backend,CHANGELOG}.md`

## 2026-09-06 — 生产 API 改回同源 /api

- **原因：** 浏览器访问 `nav-api.5ai.icu` 出现 `ERR_CONNECTION_RESET`；服务端 curl 正常，但前端不可用。同源 `https://nav.5ai.icu/api` 登录与广场均正常。
- **变更：** `client.js` 默认 `API_BASE_URL=''`；文档改为推荐同源，独立 API 域名仅作备选。
- **影响文件：** `src/api/client.js`、`docs/API.md`、`docs/architecture/{overview,frontend,CHANGELOG}.md`

## 2026-09-06 — 生产 API 基址改为 nav-api.5ai.icu

- **原因：** 广场接口 404 因旧后端未加载路由；曾尝试直连独立 API 域名。
- **变更：** 一度将默认基址设为 `https://nav-api.5ai.icu`；新增 `docs/API.md`。后因浏览器连接重置已回退同源（见上一条）。
- **影响文件：** `src/api/client.js`、`docs/API.md`、`docs/README.md`、`docs/architecture/{overview,frontend,CHANGELOG}.md`

## 2026-09-06 — 广场前端与数据初始化

- **原因：** 后端广场就绪后，需要把历史个人站点迁入共享库，并补齐可直接使用的广场前端（浏览/添加/创建/编辑/归档/同步）。
- **变更：**
  - 新增 `migrate_to_plaza`；`seed` 改为创建空用户 + 从 `sites.json` 写入广场
  - 前端新增 `usePlaza`、`PlazaSiteCard`、`PlazaSiteForm`；`App.vue` 以 `viewMode` 切换我的/广场；个人卡片支持 `sync-from-plaza`
- **影响文件：** `backend/app/migrate_to_plaza.py`、`backend/app/seed.py`、`src/App.vue`、`src/composables/usePlaza.js`、`src/components/Plaza*.vue`、`docs/architecture/{frontend,backend,CHANGELOG}.md`

## 2026-09-06 — 广场（plaza）共享层

- **原因：** 从纯个人导航扩展为多人可共同维护的实用网站分享平台，需要全局共享数据与「导入个人目录」写路径。
- **变更：**
  - 新增全局表 `plaza_categories` / `plaza_tags` / `plaza_sites` / `plaza_site_tags`；个人 `sites` 增加可空 `source_plaza_site_id` 与部分唯一索引
  - 新增 `routers/plaza.py`（列表/详情/创建/wiki 更新/归档恢复/导入）与 `POST /api/nav/sites/{site_slug}/sync-from-plaza`
  - Alembic `0002_plaza`；协作模型为任意登录用户可编辑，删除为软下架
- **影响文件：** `backend/app/models/entities.py`、`backend/app/routers/plaza.py`、`backend/app/routers/nav.py`、`backend/app/main.py`、`backend/alembic/versions/0002_plaza.py`、`docs/architecture/{backend,overview,CHANGELOG}.md`

## 2026-09-05 — API 代理故障复盘文档

- **原因：** 记录 `nav-api.5ai.icu` 连接关闭、后端未监听 9966、bcrypt 依赖冲突及生产 nginx 缺少同源 `/api/` 反代等问题，便于后续部署复盘。
- **变更：** 新增 `docs/API_PROXY_TROUBLESHOOTING.md`，补充故障现象、排查证据、根因、修复方案、验证命令和预防措施；更新 `docs/README.md` 文档索引。
- **影响文件：** `docs/API_PROXY_TROUBLESHOOTING.md`、`docs/README.md`

## 2026-09-05 — 建立 docs/ 架构文档体系

- **原因：** 根目录 `architecture.md` 已过时（仍描述 localStorage 置顶、缺少 JWT/认证组件），且前后端混写，不利于 Agent 快速定位。
- **变更：**
  - 新增 `docs/architecture/{overview,frontend,backend}.md` 与 `docs/README.md`
  - 根目录 `architecture.md` 改为指向 `docs/` 的兼容指针
  - 新增 `AGENTS.md` 作为 AI Agent 统一入口
  - 新增 `.cursor/rules/`（project-context、sync-architecture、frontend/backend conventions）
  - 新增 `.cursor/skills/nav-station-onboarding` 与 `update-architecture-docs`（含前后端 checklist）
- **影响文件：** `AGENTS.md`、`architecture.md`、`docs/**`、`.cursor/rules/**`、`.cursor/skills/**`
