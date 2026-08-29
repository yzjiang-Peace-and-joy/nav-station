# 架构指导（ARCHITECTURE GUIDE）

> 本文档定义「个人导航站」的整体架构、目录约定、数据模型与扩展边界。所有代码实现必须遵循本指导。

## 1. 技术选型与原则

| 维度 | 决策 | 说明 |
|------|------|------|
| 框架 | Vue 3（Composition API，`<script setup>`） | 组件化、组合式函数拆分逻辑 |
| 构建工具 | Vite | 开发启动快、静态产物简洁 |
| 状态管理 | 不引入 Pinia/Vuex | 单页场景用 composables 足够，保持轻量 |
| 路由 | 不引入 vue-router | 单页展示，无多页面需求 |
| 数据源 | `src/data/sites.json` | 静态 JSON，运行时加载 |
| 持久化 | localStorage | 仅存用户偏好（主题、置顶），不存业务数据 |
| 样式方案 | 全局 CSS + CSS 变量 | 不引入 UI 框架、不引入 CSS 预处理器 |

**核心原则：**
- 数据与视图完全分离：组件只消费 composable 暴露的状态，绝不直接 `import` JSON 在组件内过滤
- 所有业务数据操作集中在 `useSites`，后续替换为管理后台 API 时只改这一处
- 组件保持无业务副作用：读写 localStorage 的逻辑必须收敛在 composables 中

## 2. 目录结构约定

```
nav_station/
├── index.html                  # SPA 入口，设置 lang、title、主题初始化脚本
├── package.json
├── vite.config.js              # 仅 vue 插件，必要时配 @ 别名
├── public/
│   └── favicon.svg             # 站点图标
└── src/
    ├── main.js                 # createApp 挂载，引入全局样式
    ├── App.vue                 # 布局骨架（唯一根组件，持有页面级状态）
    ├── data/
    │   └── sites.json          # 伪数据：categories / tags / sites
    ├── components/
    │   ├── AppHeader.vue       # 站名 + 搜索框 + 主题切换（页面顶部）
    │   ├── TagFilter.vue       # 标签筛选 chips 栏
    │   ├── CategorySection.vue # 单个分类区块（分类标题 + 站点网格）
    │   └── SiteCard.vue        # 单个站点条目（favicon + 名称 + 描述 + 星标）
    ├── composables/
    │   ├── useSites.js         # 数据加载、搜索、标签过滤
    │   ├── useTheme.js         # 主题切换（localStorage + 系统偏好）
    │   └── usePinned.js        # 置顶收藏（localStorage）
    └── styles/
        └── main.css            # 设计令牌、全局重置、双主题变量、基础组件样式
```

### 命名约定
- 组件文件：`PascalCase.vue`
- 组合式函数：`use` 前缀驼峰（`useSites.js`）
- 数据文件：`sites.json`（禁止拆分多文件，保持单一数据源）
- CSS 变量：`--` 前缀 kebab-case（如 `--bg-primary`）

## 3. 数据模型规范

### 3.1 `sites.json` 结构（唯一数据源）

```json
{
  "categories": [
    { "id": "dev", "name": "开发工具" }
  ],
  "tags": ["代码", "写作"],
  "sites": [
    {
      "id": "github",
      "name": "GitHub",
      "url": "https://github.com",
      "desc": "代码托管与协作平台",
      "category": "dev",
      "tags": ["代码"],
      "pinned": true
    }
  ]
}
```

### 3.2 字段约束

| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| `categories[].id` | string | ✅ | 全局唯一，英文短横线，作为 `sites[].category` 的外键 |
| `categories[].name` | string | ✅ | 展示名 |
| `tags[]` | string[] | ✅ | 全局标签池，去重 |
| `sites[].id` | string | ✅ | 全局唯一 |
| `sites[].name` | string | ✅ | 站点名称 |
| `sites[].url` | string | ✅ | 完整 URL（含协议） |
| `sites[].desc` | string | ❌ | 一句话描述，≤ 40 字 |
| `sites[].category` | string | ✅ | 必须引用 `categories[].id`，否则视为脏数据 |
| `sites[].tags` | string[] | ❌ | 必须为 `tags[]` 池的子集 |
| `sites[].pinned` | boolean | ❌ | 数据源中的默认置顶（用户手动置顶存 localStorage） |

### 3.3 数据校验规则（开发期）

- `useSites` 加载数据后执行一次轻量校验：
  - 站点 `category` 引用不存在 → 控制台 `console.warn` 并归类到「未分类」
  - 站点 `tags` 含未知标签 → `console.warn`，展示时忽略
  - `id` 重复 → `console.warn` 并只保留第一个
- 校验失败不阻塞渲染，仅降级处理，保证页面永远可用

## 4. 状态管理设计（composables）

### 4.1 `useTheme.js` — 主题

```js
// 职责：管理 light / dark 主题
const THEME_KEY = 'nav_theme'

// 对外暴露：theme (ref)、toggle()、init()
// 优先级：localStorage 手动选择 > 系统 prefers-color-scheme
// 生效方式：向 <html> 元素写入 data-theme 属性，CSS 变量按属性切换
```

约束：
- 初始渲染前必须在 `index.html` 内联脚本读取 localStorage 设置 `data-theme`，避免闪烁（FOUC）
- 切换时同步写 localStorage + 更新 `<html data-theme>`

### 4.2 `usePinned.js` — 置顶

```js
// 职责：管理用户手动置顶的站点 id 集合
const PINNED_KEY = 'nav_pinned'

// 对外暴露：pinnedIds (ref<Set>)、isPinned(id)、toggle(id)
// 初始化：从 localStorage 读取 JSON 数组，容错（解析失败返回空 Set）
// 变更时：同步写回 localStorage，无需手动保存
```

### 4.3 `useSites.js` — 数据与过滤（核心）

```js
// 职责：加载 sites.json、搜索、标签过滤、组装视图数据
// 对外暴露：
//   categories (ref)          — 分类列表
//   filteredSites (computed)  — 当前过滤结果（搜索 + 标签叠加）
//   searchQuery (ref)         — 搜索关键字
//   activeTag (ref)           — 当前选中标签（null 表示全部）
//   pinnedSites (computed)    — 置顶站点列表
// 内部：
//   filterSites(sites)        — 搜索匹配 name/desc/tags；标签精确匹配
//   groupByCategory(sites)    — 按 category 分组，保留 categories.json 的声明顺序
```

过滤优先级约定：**搜索与标签是叠加关系（AND）**，不是互斥。

## 5. 组件通信约定

```
App.vue（唯一状态持有者）
 ├─ 持有 searchQuery / activeTag / theme / pinned 等状态入口
 ├─ 通过 props 向下传递数据
 └─ 通过 emit / 回调向上接收事件
```

| 组件 | Props（入） | Emits（出） |
|------|-------------|-------------|
| `AppHeader` | `query` | `update:query`、`toggle-theme` |
| `TagFilter` | `tags`、`activeTag` | `update:activeTag` |
| `CategorySection` | `title`、`sites` | — |
| `SiteCard` | `site`、`isPinned` | `toggle-pin` |

约束：
- 禁止跨层组件直接读写 composable 内部状态（除 `App.vue` 外组件只接收 props）
- 组件不得直接 `import` `sites.json`
- 事件命名统一 `kebab-case`

## 6. 全局状态键位表（localStorage 命名空间）

| Key | 类型 | 内容 | 归属 |
|-----|------|------|------|
| `nav_theme` | `'light' \| 'dark'` | 手动主题选择 | useTheme |
| `nav_pinned` | JSON 数组 | 用户置顶的站点 id | usePinned |

- 所有 key 以 `nav_` 前缀隔离命名空间，避免与其他应用冲突
- 业务数据（站点/分类）一律不落 localStorage

## 7. 容错与降级策略

| 场景 | 降级行为 |
|------|----------|
| favicon 加载失败 / 超时 | 显示站点名首字母彩色块（颜色由站点 id hash 决定） |
| localStorage 不可用或被清空 | 回退到系统主题、空置顶集合，页面照常运行 |
| JSON 解析失败 | 控制台报错，页面显示空状态提示「数据加载失败」 |
| 搜索无结果 | 显示空状态文案，不放置顶区，不显示空分类 |

## 8. 扩展边界（本期不实现，但必须预留）

| 未来能力 | 本期预留方式 |
|----------|--------------|
| 管理后台（增删改） | 数据模型字段已规范化，`sites.json` 可直接映射为表结构 |
| 后端 API | 修改 `useSites` 的加载函数即可，组件零改动 |
| 多用户 / 登录 | localStorage 键位已带命名空间，可平滑迁移 |
| 新视图（详情页等） | 组件与逻辑已分离，新增组件不影响现有结构 |

**红线：本期禁止引入的依赖** — vue-router、Pinia、UI 组件库、axios、CSS 预处理器、TypeScript（除非用户明确要求）。
