# 架构变更日志

记录架构级决策与边界变化，不替代 Git history。

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
