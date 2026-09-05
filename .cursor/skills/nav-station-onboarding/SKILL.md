---
name: nav-station-onboarding
description: Orients agents to the Nav Station Vue + FastAPI project structure, docs, and key paths. Use when starting a new conversation, exploring the codebase, or when the user asks to understand, scan, or onboard to the project.
---

# Nav Station Onboarding

## Read order

1. `AGENTS.md` — project one-liner and mandatory post-change steps
2. `docs/README.md` — documentation index
3. By task:
   - Full-stack / deploy / auth boundary → `docs/architecture/overview.md`
   - Frontend UI or state → `docs/architecture/frontend.md`
   - API, models, seed, config → `docs/architecture/backend.md`
4. Extra:
   - Visual / CSS tokens → `VISUAL.md`
   - Acceptance criteria → `ACCEPTANCE.md`
   - Backend startup only → `backend/README.md`

Do not treat root `architecture.md` as the source of truth; it is a pointer to `docs/`.

## Architecture snapshot

- Frontend: Vue 3 SPA at repo root (`src/`), Vite on `5173`, no router/Pinia.
- Backend: FastAPI in `backend/`, SQLAlchemy + SQLite, JWT auth, port `9966`.
- Boundary: browser calls same-origin `/api` (Vite proxy or Nginx). Business data lives in SQLite; localStorage only holds `nav_token`, `nav_user`, `nav_theme`.

## Key paths

| Path | Role |
|------|------|
| `src/App.vue` | Root layout and page-level state |
| `src/api/client.js` | JWT Fetch client for `/api` |
| `src/composables/` | Auth, sites, pins, theme |
| `src/components/` | Presentational SFCs |
| `backend/app/main.py` | FastAPI app entry |
| `backend/app/routers/` | auth / nav / pins |
| `backend/app/models/entities.py` | SQLAlchemy models |
| `backend/app/config.py` | Settings and env defaults |

## After reading

Implement within documented conventions. Structural changes must follow `.cursor/skills/update-architecture-docs/`.
