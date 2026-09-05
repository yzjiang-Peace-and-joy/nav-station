# 架构变更日志

记录架构级决策与边界变化，不替代 Git history。

## 2026-09-05 — 建立 docs/ 架构文档体系

- **原因：** 根目录 `architecture.md` 已过时（仍描述 localStorage 置顶、缺少 JWT/认证组件），且前后端混写，不利于 Agent 快速定位。
- **变更：**
  - 新增 `docs/architecture/{overview,frontend,backend}.md` 与 `docs/README.md`
  - 根目录 `architecture.md` 改为指向 `docs/` 的兼容指针
  - 新增 `AGENTS.md` 作为 AI Agent 统一入口
  - 新增 `.cursor/rules/`（project-context、sync-architecture、frontend/backend conventions）
  - 新增 `.cursor/skills/nav-station-onboarding` 与 `update-architecture-docs`（含前后端 checklist）
- **影响文件：** `AGENTS.md`、`architecture.md`、`docs/**`、`.cursor/rules/**`、`.cursor/skills/**`
