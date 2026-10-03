# 前端架构

## 1. 技术选型与边界

- Vue 3 Composition API 与 `<script setup>`。
- Vite 开发与构建；开发服务器端口 `5173`。默认 API 为同源 `/api`（Vite proxy 或生产 Nginx 反代至 `9966`）。可用 `VITE_API_BASE_URL` 覆盖基址。
- 全局 CSS 与 CSS 变量；不引入 Pinia/Vuex、`vue-router`、axios、UI 框架、CSS 预处理器或 TypeScript。
- 业务数据来自 FastAPI；组件不直接读取 JSON 或调用 API。
- 页面级状态由 `src/App.vue` 持有，逻辑集中在 composables；用 `viewMode: 'mine' | 'plaza'` 切换个人目录与广场（无路由）。

## 2. 目录与关键文件

```text
src/
├── App.vue                 # 页面布局、认证切换、mine/plaza 视图状态
├── main.js                 # Vue 挂载与全局样式
├── api/
│   ├── client.js           # /api Fetch 客户端与 JWT
│   └── aiSiteSuggest.js    # 从 URL 请求后端生成站点字段
├── data/sites.json         # seed 输入（写入广场）
├── data/sites-test.json    # 历史测试数据；当前 seed 不再灌个人目录
├── components/
│   ├── AppHeader.vue       # 我的/广场切换、搜索、主题、用户菜单、广场提交入口
│   ├── AppSidebar.vue      # 分类、置顶、标签导航；移动端 drawer
│   ├── BrandMark.vue       # 品牌几何标识（登录页与侧栏共用）
│   ├── CategorySection.vue
│   ├── LoginView.vue
│   ├── PlazaSiteCard.vue   # 广场卡片：添加 / 编辑 / 下架恢复
│   ├── PlazaSiteForm.vue   # 广场创建（URL→审阅）与编辑弹层
│   ├── SiteCard.vue        # 个人站点卡片；可同步广场来源
│   ├── TagFilter.vue
│   └── UserMenu.vue
├── composables/
│   ├── useAuth.js
│   ├── usePinned.js
│   ├── usePlaza.js
│   ├── useSites.js
│   └── useTheme.js
└── styles/main.css
```

组件使用 `PascalCase.vue`，composable 使用 `use` 前缀驼峰命名，CSS 变量使用 `--kebab-case`。

## 3. Composable 契约

### `useAuth.js`

管理 JWT 登录状态与账户切换。`init()` 用 `nav_token` 调用 `/auth/me`，`login(name, password)` 调用 `/auth/login`，并维护 `currentUser`、`isAuthenticated`、`username`、`otherAccounts`。用户标识缓存为 `nav_user`；登出会清理 token 与用户缓存。

### `useSites.js`

通过 `/api/nav` 加载当前用户的 categories、tags、sites，并暴露 `loadError`、`searchQuery`、`activeTag`、`activeCategory`、`pinnedSites`、`categoryCounts`、`displayGroups`、`showPinnedView`、`hasResults`、`defaultPinnedIds()`、`createSite(payload)`、`syncFromPlaza(siteSlug)` 及筛选操作。搜索与标签、分类筛选叠加；服务端返回的 `pinned` 只用于默认置顶初始化；`source_plaza_id` 用于展示同步入口。`createSite(payload)` 调用 `POST /nav/sites`（含可选 `publish_to_plaza`），成功后重新 `load()`。

### `usePlaza.js`

通过 `/api/plaza` 加载全局广场数据，暴露筛选（含 `includeArchived`）、`create` / `update` / `archive` / `restore` / `addToNav`。列表按分类分组；添加成功后本地标记 `added`。

### `usePinned.js`

置顶不再使用 localStorage。`init(userId, defaultIds)` 调用 `/api/pins`，必要时用默认站点初始化；`toggle(id)` 调用 `/api/pins/{site_id}/toggle`。仅在内存中维护只读 `pinnedIds`。

### `useTheme.js`

管理 `light`/`dark` 主题，读取与写入 localStorage 键 `nav_theme`，并更新 `<html data-theme>`。`index.html` 内联脚本在首屏前写入 `data-theme` 以避免 FOUC；`App.vue` 挂载时再调用 `init()` 同步 composable 状态。

## 4. 组件通信

`App.vue` 是唯一页面级状态持有者：向下传递 props，接收 emit 或回调。组件不得直接调用 API、读取 composable 内部状态或导入 `sites.json`。

| 组件 | 主要输入 | 主要输出 |
|---|---|---|
| `AppHeader` | `query`、`theme`、`viewMode`、`includeArchived`、用户与账户 | `update:query`、`update:viewMode`、`update:includeArchived`、`create-site`（我的）、`create-plaza`（广场）、主题/菜单/登出/切账户 |
| `AppSidebar` | 分类、标签、活动项、计数、`showPinned`、`brandTitle`、drawer | `update:active-category`、`update:active-tag`、`close` |
| `BrandMark` | `size`（可选，默认 28） | 无；纯展示品牌几何标识 |
| `LoginView` | `theme` | `login`、`toggle-theme` |
| `CategorySection` | `title`、`sites` | `leading` slot 与默认 slot |
| `SiteCard` | `site`、`isPinned`、`index`、`syncing` | `toggle-pin`、`sync-from-plaza` |
| `PlazaSiteCard` | `site`、`index`、`busy` | `add`、`edit`、`archive`、`restore` |
| `PlazaSiteForm` | `open`、`mode`、`site`、`categories`、`busy`、`context`（`mine` \| `plaza`，创建时选择字段）；create 为两步（仅网址 → 审阅全字段），经 `aiSiteSuggest.suggestSiteFromUrl` 预填；`context=mine` 的创建流程含「同步公开到广场」开关（默认关）并随 payload 提交 `publish_to_plaza`；edit 仍为全字段 | `close`、`submit`；`setError` |
| `TagFilter` | `tags`、`activeTag` | `update:activeTag` |
| `UserMenu` | 当前用户、其他账户 | 登出、切换账户 |

## 5. 数据与持久化

| Key | 内容 | 归属 |
|---|---|---|
| `nav_token` | JWT access token | `api/client.js` |
| `nav_user` | 当前用户名缓存 | `useAuth.js` |
| `nav_theme` | `light` 或 `dark` | `useTheme.js` |

站点、分类、标签、置顶与广场均由后端 SQLite 持久化；`nav_pinned` 已废弃，不得重新引入。

## 6. API 边界

所有请求经 `apiFetch()` 发出。默认基址为空串，最终 URL 为同源 `/api{path}`（生产即 `https://nav.5ai.icu/api...`）；可用 `VITE_API_BASE_URL` 覆盖。请求自动设置 JSON 头与 `Authorization: Bearer`。401 会清理认证缓存。完整路由表见 [API.md](../API.md)。

`GET /api/nav` 站点对象含可选 `source_plaza_id`。广场相关接口由 `usePlaza` / `useSites.syncFromPlaza` 调用；「我的」创建走 `useSites.createSite` → `POST /api/nav/sites`，`App.vue` 按提交时的 `viewMode` 分流到 `createSite` 或 `createPlaza`。

`api/aiSiteSuggest.js` 导出 `suggestSiteFromUrl(url)`，经 `apiFetch('/plaza/ai-suggest')` 调用后端 Agnes 解析服务，返回与广场创建字段对齐的 `{ name, url, desc, detail, category, tags }`。API Key 仅存后端 `.env`，前端不接触模型凭据。

生产不要默认把 API 指到 `nav-api.5ai.icu`：浏览器侧易出现 `ERR_CONNECTION_RESET`（见故障复盘文档）。

## 7. 容错

加载失败显示数据错误状态；无筛选结果显示空状态；个人目录为空时提供「添加网站」入口（复用创建弹层）；favicon 失败由卡片降级展示。认证失败回到登录视图。API 或持久化行为变化时，必须同步前端、概览和后端文档。
