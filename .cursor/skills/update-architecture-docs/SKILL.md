---
name: update-architecture-docs
description: Keeps Nav Station architecture docs synchronized with structural code changes. Use after adding or renaming components, composables, routers, models, API contracts, auth, localStorage keys, dependencies, seed, migrations, or deployment config; or when the user asks to update architecture docs.
---

# Update Architecture Docs

## When to run

Run after structural changes. Skip for pure style, copy, or non-structural bug fixes.

Triggers include:

- Add / remove / rename under `src/composables/`, `src/components/`, `backend/app/routers/`, `backend/app/models/`
- Change API paths or request/response shapes
- Change auth flow or localStorage keys
- Add architecture-affecting npm/pip dependencies
- Change seed, migrations, DB config, Nginx, ports, or env settings

## Workflow

1. Classify scope: `frontend` / `backend` / `both`.
2. Read the matching checklist:
   - [frontend-checklist.md](frontend-checklist.md)
   - [backend-checklist.md](backend-checklist.md)
3. Scan the real code and compare against the listed doc sections.
4. Update only the affected files:
   - `docs/architecture/frontend.md`
   - `docs/architecture/backend.md`
   - `docs/architecture/overview.md` (cross-stack: API table, auth, deploy, data ownership)
   - `docs/README.md` if the doc index itself changed
5. If the change is an architecture decision or boundary shift, append an entry to `docs/architecture/CHANGELOG.md`:
   - Date
   - What changed and why
   - Which docs/paths were affected
6. Confirm `AGENTS.md` key paths still match reality.

## Rules

- Prefer updating existing sections over duplicating content across docs.
- `overview.md` holds cross-stack facts only; put stack-specific detail in frontend/backend docs.
- Do not invent APIs or components that are not in the code.
- Keep root `architecture.md` as a short pointer unless the docs layout itself moves.
