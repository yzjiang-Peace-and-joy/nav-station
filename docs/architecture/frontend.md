# 前端架构

## 1. 技术选型与边界

- Vue 3 Composition API 与 `<script setup>`。
- Vite 开发与构建；开发服务器端口 `5173`，`/api` 代理至 `9966`。
- 全局 CSS 与 CSS 变量；不引入 Pinia/Vuex、`vue-router`、axios、UI 框架、CSS 预处理器或 TypeScript。
- 业务数据来自 FastAPI；组件不直接读取 JSON 或调用 API。
- 页面级状态由 `src/App.vue` 持有，逻辑集中在 composables。

## 2. 目录与关键文件

```text
src/
├── App.vue                 # 页面布局、认证切换、页面级状态
├── main.js                 # Vue 挂载与全局样式
├── api/client.js           # /api Fetch 客户端与 JWT
├── data/sites.json         # seed 输入数据
├── data/sites-test.json    # 测试用户 seed 数据
├── components/
│   ├── AppHeader.vue       # 搜索、主题、用户菜单入口
│   ├── AppSidebar.vue      # 分类、置顶、标签导航；移动端 drawer
│   ├── CategorySection.vue
│   ├── LoginView.vue
│   ├── SiteCard.vue
│   ├── TagFilter.vue
│   └── UserMenu.vue
├── composables/
│   ├── useAuth.js
│   ├── usePinned.js
│   ├── useSites.js
│   └── useTheme.js
└── styles/main.css
```

组件使用 `PascalCase.vue`，composable 使用 `use` 前缀驼峰命名，CSS 变量使用 `--kebab-case`。

## 3. Composable 契约

### `useAuth.js`

管理 JWT 登录状态与账户切换。`init()` 用 `nav_token` 调用 `/auth/me`，`login(name, password)` 调用 `/auth/login`，并维护 `currentUser`、`isAuthenticated`、`username`、`otherAccounts`。用户标识缓存为 `nav_user`；登出会清理 token 与用户缓存。

### `useSites.js`

通过 `/api/nav` 加载当前用户的 categories、tags、sites，并暴露 `loadError`、`searchQuery`、`activeTag`、`activeCategory`、`pinnedSites`、`categoryCounts`、`displayGroups`、`showPinnedView`、`hasResults`、`defaultPinnedIds()` 及筛选操作。搜索与标签、分类筛选叠加；服务端返回的 `pinned` 只用于默认置顶初始化。

### `usePinned.js`

置顶不再使用 localStorage。`init(userId, defaultIds)` 调用 `/api/pins`，必要时用默认站点初始化；`toggle(id)` 调用 `/api/pins/{site_id}/toggle`。仅在内存中维护只读 `pinnedIds`。

### `useTheme.js`

管理 `light`/`dark` 主题，读取与写入 localStorage 键 `nav_theme`，并更新 `<html data-theme>`。`index.html` 内联脚本在首屏前写入 `data-theme` 以避免 FOUC；`App.vue` 挂载时再调用 `init()` 同步 composable 状态。

## 4. 组件通信

`App.vue` 是唯一页面级状态持有者：向下传递 props，接收 emit 或回调。组件不得直接调用 API、读取 composable 内部状态或导入 `sites.json`。

| 组件 | 主要输入 | 主要输出 |
|---|---|---|
| `AppHeader` | `query`、`theme`、用户与账户 | `update:query`、`toggle-theme`、菜单、登出、切换账户 |
| `AppSidebar` | 分类、标签、活动项、计数、drawer 状态 | `update:active-category`、`update:active-tag`、`close` |
| `LoginView` | `theme` | `login`、`toggle-theme` |
| `CategorySection` | `title`、`sites` | `leading` slot 与默认 slot |
| `SiteCard` | `site`、`isPinned`、`index` | `toggle-pin` |
| `TagFilter` | `tags`、`activeTag` | `update:activeTag` |
| `UserMenu` | 当前用户、其他账户 | 登出、切换账户 |

## 5. 数据与持久化

| Key | 内容 | 归属 |
|---|---|---|
| `nav_token` | JWT access token | `api/client.js` |
| `nav_user` | 当前用户名缓存 | `useAuth.js` |
| `nav_theme` | `light` 或 `dark` | `useTheme.js` |

站点、分类、标签和置顶均由后端 SQLite 持久化；`nav_pinned` 已废弃，不得重新引入。

## 6. API 边界

所有请求经 `apiFetch()` 访问 `/api`，自动设置 JSON 头与 `Authorization: Bearer`。401 会清理认证缓存。前端 API 对照表见 [overview.md](overview.md)。

## 7. 容错

加载失败显示数据错误状态；无筛选结果显示空状态；favicon 失败由卡片降级展示。认证失败回到登录视图。API 或持久化行为变化时，必须同步前端、概览和后端文档。
