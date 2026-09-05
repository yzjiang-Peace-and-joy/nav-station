# Frontend → docs mapping

Scan `src/`, `package.json`, `vite.config.js`, and `index.html`. Update docs only where code and docs diverge.

| Code change | Update |
|-------------|--------|
| New / rename / delete `src/composables/useX.js` | `frontend.md` §3 Composable 契约; directory tree in §2 |
| New / rename / delete `src/components/*.vue` | `frontend.md` §2 目录树; §4 组件通信表 |
| Change props / emits of a component | `frontend.md` §4 组件通信 |
| Change `src/api/client.js` (base path, headers, 401, token keys) | `frontend.md` §5–§6; `overview.md` 认证流 / API 总览 |
| Change which endpoints composables call | `frontend.md` §3; `overview.md` API 表; if backend routes changed, also `backend.md` |
| Change localStorage keys (`nav_*`) | `frontend.md` §5; `overview.md` 数据归属 |
| Change theme FOUC script in `index.html` or `useTheme.js` | `frontend.md` §3 `useTheme` |
| Add / remove npm dependency that affects architecture | `frontend.md` §1 技术选型与边界; note in `CHANGELOG.md` if a previous red line is lifted |
| Change Vite port, proxy, or HMR host | `frontend.md` §1; `overview.md` 开发与生产 |
| Change auth UX entry (`LoginView`, account switch) | `frontend.md` §3 `useAuth` + §4; `overview.md` 认证流 |

## Verify against code

- [ ] `src/components/` list matches `frontend.md` directory tree
- [ ] `src/composables/` list and public APIs match §3
- [ ] localStorage keys in code match §5 (`nav_token`, `nav_user`, `nav_theme` only for business-adjacent browser state)
- [ ] No doc still claims pins live in localStorage
- [ ] Overview API table still matches frontend clients
