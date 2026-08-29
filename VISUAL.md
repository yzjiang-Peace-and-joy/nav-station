# 视觉指导（VISUAL GUIDE）

> 本文档定义「个人导航站」的视觉语言：设计令牌、排版、配色、间距、组件交互与响应式规则。所有实现必须以此为准。

## 1. 设计理念

**极简（Minimal）**——参照 Vercel / Dashlane 的排版风格：

- 大留白 > 装饰，内容本身就是视觉主体
- 无边框卡片：网格项默认透明，hover 才出现细边框与底色
- 全局只允许 **一个强调色**，其余全部来自中性色阶
- 圆角克制（4~8px），阴影克制（hover 才出现，且极浅）

## 2. 设计令牌（Design Tokens）

所有颜色、间距、圆角、阴影必须通过 CSS 变量使用，禁止在组件里写死数值。

### 2.1 色彩系统

#### 浅色主题（`:root` 默认）

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg-primary` | `#fafafa` | 页面主背景 |
| `--bg-secondary` | `#ffffff` | 浮层、hover 底色 |
| `--bg-hover` | `rgba(0,0,0,0.035)` | 卡片 hover 底色 |
| `--fg-primary` | `#111111` | 主文字 / 站名 |
| `--fg-secondary` | `#6b7280` | 次要文字 / 描述 |
| `--fg-tertiary` | `#9ca3af` | 弱化文字 / 占位符 |
| `--border` | `rgba(0,0,0,0.10)` | 分割线、边框 |
| `--border-strong` | `rgba(0,0,0,0.18)` | hover 边框 |
| `--accent` | `#3b82f6` | 唯一强调色（星标选中、焦点、活动标签） |
| `--accent-muted` | `rgba(59,130,246,0.12)` | 强调色弱背景（活动标签底色） |

#### 深色主题（`[data-theme="dark"]`）

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg-primary` | `#0d0d0d` | 页面主背景 |
| `--bg-secondary` | `#171717` | 浮层、hover 底色 |
| `--bg-hover` | `rgba(255,255,255,0.06)` | 卡片 hover 底色 |
| `--fg-primary` | `#f5f5f5` | 主文字 |
| `--fg-secondary` | `#a3a3a3` | 次要文字 |
| `--fg-tertiary` | `#737373` | 弱化文字 |
| `--border` | `rgba(255,255,255,0.10)` | 分割线 |
| `--border-strong` | `rgba(255,255,255,0.22)` | hover 边框 |
| `--accent` | `#60a5fa` | 强调色（深色下提亮以保证对比度） |
| `--accent-muted` | `rgba(96,165,250,0.16)` | 强调色弱背景 |

### 2.2 字体系统

| 变量 | 值 | 用途 |
|------|-----|------|
| `--font-family` | `system-ui, -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif` | 全站字体栈 |
| `--font-size-base` | `14px` | 正文 / 站点名称 |
| `--font-size-sm` | `12.5px` | 描述、标签、辅助文字 |
| `--font-size-title` | `15px` | 分类标题 |
| `--font-size-brand` | `16px` | 站名品牌字 |

### 2.3 间距 / 布局

| 变量 | 值 | 用途 |
|------|-----|------|
| `--space-1` | `4px` | 内聚间距 |
| `--space-2` | `8px` | 元素内部间距 |
| `--space-3` | `12px` | 常规间距 |
| `--space-4` | `16px` | 组件间间距 |
| `--space-6` | `24px` | 区块内间距 |
| `--space-8` | `32px` | 分类间间距 |
| `--content-max` | `1080px` | 内容最大宽度，居中 |
| `--header-height` | `60px` | 固定 Header 高度 |
| `--grid-min` | `200px` | 网格最小列宽 |

### 2.4 圆角 / 阴影 / 过渡

| 变量 | 值 | 用途 |
|------|-----|------|
| `--radius-sm` | `4px` | 标签 chip、小元素 |
| `--radius-md` | `8px` | 卡片、输入框、按钮 |
| `--shadow-hover` | `0 1px 2px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.06)` | hover 浮起阴影 |
| `--transition` | `150ms ease` | 所有状态过渡 |

## 3. 布局规范

### 3.1 页面骨架

```
┌──────────────────────────────────────────────┐
│  AppHeader（固定顶部，高 60px，底部 1px 分隔线）│
│  ┌───┬─────────────────────────┬───────────┐ │
│  │站名│       搜索框（居中）       │ ☀/🌙 切换 │ │
│  └───┴─────────────────────────┴───────────┘ │
├──────────────────────────────────────────────┤
│  TagFilter（标签 chips 栏，横向滚动）          │
├──────────────────────────────────────────────┤
│  主内容区（max-width 1080px，左右留白 ≥ 24px） │
│  ├── 置顶区块（有置顶时显示）                  │
│  └── 分类区块 × N                            │
└──────────────────────────────────────────────┘
```

- Header 吸顶（`position: sticky; top: 0`），背景 `--bg-primary` + 半透明 + `backdrop-filter: blur(8px)`
- 主内容上下 padding：`40px 24px`
- 分类区块间距 `--space-8`，分类内部站点间距 `--space-4`

### 3.2 网格

```css
.sites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--grid-min), 1fr));
  gap: var(--space-4);
}
```

- 单行最多自然排布，不设固定列数上限
- 搜索/过滤时若区块为空，整个分类区块隐藏

## 4. 组件视觉规范

### 4.1 AppHeader（顶栏）

| 元素 | 规范 |
|------|------|
| 站名 | 左对齐，`--font-size-brand`，`--fg-primary`，600 字重 |
| 搜索框 | 居中，最大宽 `480px`，圆角 `--radius-md`，背景 `--bg-secondary`，1px `--border` 边框；聚焦时边框变 `--accent` 并出现 `--shadow-hover` |
| 主题按钮 | 图标按钮 36×36px，透明背景，hover 时 `--bg-hover` |

### 4.2 TagFilter（标签栏）

- chips 高度 28px，`--radius-sm`，内边距 `0 10px`
- 默认态：透明背景 + 1px `--border` 边框，文字 `--fg-secondary`
- 活动态：`--accent-muted` 背景 + `--accent` 文字，无边框
- hover：边框变 `--border-strong`
- 超过容器宽度时横向滚动，隐藏滚动条

### 4.3 SiteCard（站点卡片）

极简原则下卡片无独立背景，仅文字 + favicon 构成：

```
┌───────────────────────────┐
│  [icon]  站点名称    ★     │
│           描述（一行省略）   │
└───────────────────────────┘
```

| 状态 | 表现 |
|------|------|
| 默认 | 无背景、无边框，`--radius-md`，内边距 `10px 12px` |
| hover | 背景 `--bg-hover`，边框 `--border`，轻微上移 `translateY(-1px)`，星标显现 |
| 星标（未置顶） | 默认隐藏，hover 显现，颜色 `--fg-tertiary` |
| 星标（已置顶） | 常显，颜色 `--accent`，填充实心 |

- favicon：20×20px，圆角 4px，加载失败降级为首字母色块
- 描述：`--font-size-sm`，`--fg-secondary`，单行省略（`text-overflow: ellipsis`）
- 整个卡片为链接，点击 `target="_blank"` 新标签打开

### 4.4 CategorySection（分类区块）

```
分类名称（--font-size-title，600 字重，带 count 弱化计数）
──────────────────────────────  （1px --border 分隔线）
[站点网格]
```

- 分类名与分隔线之间保持 `--space-3` 间距
- 计数文字 `--fg-tertiary`，`--font-size-sm`

### 4.5 置顶区块

- 标题「置顶收藏」+ 星标图标，样式同分类标题
- 若置顶集合为空，整个区块隐藏

## 5. 交互与动效规范

- 所有状态切换（hover / focus / 星标）过渡时长统一 `--transition`（150ms ease）
- 过渡属性限定 `background-color, border-color, color, opacity, transform`
- 不使用 scale 放大动画（破坏极简感），hover 上移限制在 1px
- 焦点可见性：键盘 Tab 聚焦元素必须有可见 focus ring（`outline: 2px solid var(--accent); outline-offset: 2px`）

## 6. 响应式断点

| 断点 | 行为 |
|------|------|
| `> 1080px` | 内容居中，标准网格 |
| `720px ~ 1080px` | 内容随视口收缩，网格自动折行 |
| `< 720px` | 搜索框占满整行（Header 换行），网格最小列宽降至 `160px`，分类间距减半 |

## 7. 无障碍与可访问性

- 图标按钮必须有 `aria-label`
- 星标按钮用 `<button>` 元素（非链接），带 `aria-pressed` 状态
- 深色/浅色两种主题下正文对比度 ≥ 4.5:1
- 主题切换不影响已渲染布局（无跳动）

## 8. 禁止事项（红线）

- ❌ 不使用渐变背景、不使用图片背景
- ❌ 不使用 emoji 作为图标（favicon 与星标除外，统一用 SVG 线条图标）
- ❌ 不引入第三方 UI 组件库 / 图标库（用内联 SVG）
- ❌ 卡片不添加默认背景色块、不添加粗边框
- ❌ 不使用 `!important`（除非覆盖第三方样式，本项目中无此场景）
- ❌ 不在组件内联样式中写死颜色，全部走 CSS 变量
