# Backend → docs mapping

Scan `backend/app/`, `backend/alembic/`, `backend/requirements.txt`, `backend/README.md`, and deploy files under `nginx/` / systemd unit.

| Code change | Update |
|-------------|--------|
| New / rename / delete router under `app/routers/` | `backend.md` §2 目录 + §4 路由契约; `overview.md` API 总览 |
| Change route path, method, auth requirement, or response shape | `backend.md` §4; `overview.md` API 表; frontend callers in `frontend.md` if affected |
| Change models in `app/models/entities.py` | `backend.md` §3 数据模型 (tables + ER); `CHANGELOG.md` for schema decisions |
| Change `app/config.py` / env defaults | `backend.md` §6 配置; `overview.md` if deploy-facing |
| Change `app/security.py` or JWT/login behavior | `backend.md` §5; `overview.md` 认证流 |
| Change `app/seed.py` or seed JSON inputs | `backend.md` §7 Seed; `frontend.md` §2 if `src/data/*` role changes |
| Add Alembic migration or change `create_all` usage | `backend.md` §2 双轨说明; `CHANGELOG.md` |
| Change listen host/port, `run.py` / `run.sh`, systemd, or Nginx proxy | `backend.md` §1; `overview.md` 开发与生产 |
| Add pip dependency that affects architecture | `backend.md` §1; `CHANGELOG.md` if pattern changes (e.g. introducing a service layer) |

## Verify against code

- [ ] Router prefixes and methods match `backend.md` §4 and `overview.md`
- [ ] Entity table names and uniqueness constraints match §3
- [ ] Settings field defaults match §6
- [ ] Seed usernames, passwords policy, and JSON paths match §7
- [ ] Per-user `user_id` scoping is still documented as mandatory
