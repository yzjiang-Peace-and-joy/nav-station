# 视觉指导（VISUAL GUIDE）

> 本文档定义「个人导航站」的视觉语言：设计令牌、排版、配色、间距、组件交互与响应式规则。所有实现必须以此为准。
>
> 参考基准：Impeccable 设计规范（craft-floor / DESIGN.md），并针对"个人导航站 = Operate 模式（扫视性 > 表达性）"做了适配裁剪。

## 1. 设计理念

**极简（Minimal）**——参照 Vercel / Dashlane 的排版风格，同时吸收 Impeccable 的"craft floor"：

- 大留白 > 装饰，内容本身就是视觉主体；扫视性优先，1 秒内可定位到目标分类
- 无边框卡片：网格项默认透明，hover 才出现细边框与底色
- 全局只允许 **一个强调色**，其余全部来自经过**染色（tinted）**的中性色阶，禁止纯黑纯灰
- 圆角克制（6~12px），阴影克制（仅"边框"或"阴影"二选一，从不叠加）
- 品牌感体现在精确细节：浏览器原生表面（选区/滚动条/caret/focus）、字体、一个作者式入场动效

## 2. 设计令牌（Design Tokens）

所有颜色、间距、圆角、阴影必须通过 CSS 变量使用，禁止在组件里写死数值。

### 2.1 色彩系统

所有中性色均带轻微暖色染色（不是纯黑纯灰），确保深/浅两套主题的"纸感"。

#### 浅色主题（`:root` 默认）

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg-primary` | `#fafaf9` | 页面主背景（暖白） |
| `--bg-secondary` | `#ffffff` | 浮层、输入框背景 |
| `--bg-hover` | `rgba(17,24,39,0.04)` | 卡片 hover 底色 |
| `--fg-primary` | `#1c1917` | 主文字 / 站名（暖黑） |
| `--fg-secondary` | `#57534e` | 次要文字 / 描述（暖灰） |
| `--fg-tertiary` | `#a8a29e` | 弱化文字 / 占位符 |
| `--border` | `rgba(28,25,23,0.10)` | 分割线、默认边框 |
| `--border-strong` | `rgba(28,25,23,0.18)` | hover 边框、焦点边框 |
| `--accent` | `#2563eb` | 唯一强调色（星标选中、焦点、活动标签） |
| `--accent-muted` | `rgba(37,99,235,0.10)` | 强调色弱背景（活动标签底色、文本选区） |
| `--selection-bg` | `rgba(37,99,235,0.18)` | `::selection` 背景 |
| `--caret` | `#2563eb` | 输入框光标色 |

#### 深色主题（`[data-theme="dark"]`）

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg-primary` | `#101012` | 页面主背景（暖墨黑，非纯黑） |
| `--bg-secondary` | `#1a1a1d` | 浮层、输入框背景 |
| `--bg-hover` | `rgba(255,255,255,0.05)` | 卡片 hover 底色 |
| `--fg-primary` | `#f5f5f4` | 主文字 |
| `--fg-secondary` | `#a8a29e` | 次要文字（暖灰，保证 ≥4.5:1） |
| `--fg-tertiary` | `#78716c` | 弱化文字 |
| `--border` | `rgba(255,255,255,0.10)` | 分割线 |
| `--border-strong` | `rgba(255,255,255,0.22)` | hover 边框 |
| `--accent` | `#60a5fa` | 强调色（深色下提亮以保证对比度） |
| `--accent-muted` | `rgba(96,165,250,0.16)` | 强调色弱背景 |
| `--selection-bg` | `rgba(96,165,250,0.30)` | `::selection` 背景 |
| `--caret` | `#60a5fa` | 输入框光标色 |

### 2.2 字体系统

**原则（取自 Impeccable）：** 不落系统默认字体的"AI 味"，用一对有性格的字族；排版梯度必须有肉眼可辨的阶梯。

| 变量 | 值 | 用途 |
|------|-----|------|
| `--font-brand` | `"Space Grotesk", "Noto Sans SC", system-ui, sans-serif` | 站名 / 分类标题（拉丁字型有几何性格，中文回退 Noto Sans SC） |
| `--font-body` | `"Noto Sans SC", "Noto Sans", system-ui, sans-serif` | 正文、站点名、描述 |
| `--font-mono` | `"JetBrains Mono", "SFMono-Regular", Consolas, monospace` | 计数、辅助数据（仅用于数据，不作"技术感"装饰） |

字体通过 Google Fonts 引入（`Space Grotesk` 400/500/700 + `Noto Sans SC` 400/500/700）；离线时优雅回退到系统字体，不回退时保持可读性即可。

**字号阶梯（阶梯差必须肉眼可辨，禁止 14/15/16 这类无感逼近）：**

| 变量 | 值 | 用途 |
|------|-----|------|
| `--font-size-brand` | `18px` | 站名品牌字，600 |
| `--font-size-title` | `16px` | 分类标题，600 |
| `--font-size-base` | `14px` | 站点名称，500 |
| `--font-size-sm` | `12px` | 描述、标签、辅助文字 |
| `--font-size-xs` | `11px` | 计数、徽标、元信息 |

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

**节奏规则（Impeccable spacing floor）：** 组内收紧、组间宽松；**标题上方留白 > 标题下方留白**。分类标题上边距 `--space-8`，标题与分隔线之间 `--space-3`，分隔线与网格之间 `--space-4`。

### 2.4 圆角 / 阴影 / 过渡

| 变量 | 值 | 用途 |
|------|-----|------|
| `--radius-xs` | `4px` | 标签 chip、小元素、favicon |
| `--radius-sm` | `6px` | 控制件（输入框、按钮） |
| `--radius-md` | `10px` | 卡片 |
| `--shadow-hover` | `0 2px 8px rgba(17,24,39,0.06)` | 浅色主题 hover 阴影（仅独立使用，不与边框叠加） |
| `--shadow-hover-dark` | `0 2px 10px rgba(0,0,0,0.45)` | 深色主题 hover 阴影 |
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | 入场动效专用缓出（指数级，无弹性回弹） |
| `--transition` | `150ms ease` | 状态切换过渡（hover/focus/星标） |

## 3. 布局规范

### 3.1 页面骨架

```
┌──────────────────────────────────────────────┐
│  AppHeader（sticky 顶部，高 60px，底部 1px 分隔线）│
│  ┌────────┬─────────────────────┬───────────┐ │
│  │视图切换 │      搜索框（居中）    │ CTA/主题  │ │
│  └────────┴─────────────────────┴───────────┘ │
├──────────┬───────────────────────────────────┤
│ Sidebar  │ 主内容区                           │
│ BrandMark│  ├── page-intro（视图标题+说明+计数）│
│ + 站名   │  ├── 置顶区块（有置顶时显示）        │
│ 分类导航 │  └── 分类区块 × N                  │
│ 标签筛选 │                                   │
└──────────┴───────────────────────────────────┘
```

- Header 吸顶（`position: sticky; top: 0`），背景 `--bg-primary` + 半透明（alpha 0.85）+ `backdrop-filter: blur(8px)`；此 blur 仅用于 Header 滚动遮挡，属功能性而非装饰
- 主内容上下 padding：`40px 24px`（`--space-8` / `--space-6`）
- 分类区块间距 `--space-8`，分类内部站点间距 `--space-4`
- 语义化结构：`<header>` → 侧栏 `<h1>` 站名 → `<main>`（含 `page-intro`）→ 每个分类用 `<section>` + `<h2>`。**不用 eyebrow/kicker、不用 01/02/03 编号**——标题自己承载层级
- `page-intro` 使用 `<p>` 承载视图标题（不是第二个 `h1`），右侧以 `--font-mono` 显示当前结果计数
- 品牌标识 `BrandMark`：与 favicon 同源的几何山形标，用于登录页与侧栏，颜色走 `--accent`

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
| 视图切换 | 分段控件，「我的 / 广场」；活动态 `--accent-muted` 底 + `--accent` 字 |
| 搜索框 | 居中，最大宽 `480px`，圆角 `--radius-sm`，背景 `--bg-secondary`，1px `--border` 边框；聚焦用 focus ring（`--accent` 描边 + `--accent-muted` 外晕），`caret-color: var(--caret)` |
| 主 CTA | 「添加网站 / 提交网站」使用强调色实心按钮（白字 + `--accent` 底），与次要描边按钮区分 |
| 主题按钮 | 图标按钮 36×36px，透明背景，hover 时 `--bg-hover`，`aria-label` 区分当前状态 |

### 4.1b BrandMark / 侧栏品牌

- `BrandMark`：正方形圆角几何标（山形负形），填充 `--accent`，负形用 `--bg-secondary`
- 侧栏 `h1`：BrandMark + 站名横排；站名 `--font-size-brand`、`--font-brand`、600

### 4.1c 登录页

- 品牌优先：BrandMark（40px）在上，站名 28px / 700 居中，副文案一行
- 氛围：两个纯色 `--accent-muted` 圆形装饰（非渐变、非图片），仅登录页使用
- 卡片入场：一次 `translateY(8px)` + 淡入，`--ease-out`，尊重 `prefers-reduced-motion`
- 账户 chip 使用 `--radius-xs`（非胶囊 pill）

### 4.2 TagFilter（标签栏）

- chips 高度 28px，`--radius-xs`，内边距 `0 10px`
- 默认态：透明背景 + 1px `--border` 边框，文字 `--fg-secondary`
- 活动态：`--accent-muted` 背景 + `--accent` 文字，无边框
- hover：边框变 `--border-strong`
- 超过容器宽度时横向滚动，滚动条隐藏（样式仍走自定义滚动条）

### 4.3 SiteCard（站点卡片）

极简原则下卡片无独立背景，仅文字 + favicon 构成：

```
┌───────────────────────────┐
│  [icon]  站点名称      ★   │
│          描述（一行省略）    │
└───────────────────────────┘
```

| 状态 | 表现 |
|------|------|
| 默认 | 无背景、无边框，`--radius-md`，内边距 `12px 14px` |
| hover | 背景 `--bg-hover` + 1px `--border` 边框，**不叠加阴影、不上移**（声明一次高度） |
| 星标（未置顶） | 默认隐藏，hover 显现，颜色 `--fg-tertiary`，SVG 线条 |
| 星标（已置顶） | 常显，颜色 `--accent`，SVG 填充实心 |

- favicon 托盘：28×28px，`--bg-hover` 底 + 1px `--border`，圆角 `--radius-sm`；内部图标 18×18px
- favicon 加载失败降级为首字母色块（颜色由站点 id hash 映射到 6 个柔和色）
- 描述：`--font-size-sm`，`--fg-secondary`，单行省略（`text-overflow: ellipsis`），左缩进对齐站名
- 整个卡片为链接，点击 `target="_blank"` 新标签打开

### 4.4 CategorySection（分类区块）

```
分类名称（--font-size-title，600 字重，--font-brand，带 count 弱化计数）
──────────────────────────────  （1px --border 分隔线）
[站点网格]
```

- 分类名与分隔线之间保持 `--space-3` 间距，分隔线与网格之间 `--space-4`
- 计数文字 `--fg-tertiary`，`--font-size-xs`，`--font-mono`（数据用途），置于弱底色 pill 中（仅作计数容器，非营销 chip）

### 4.5 置顶区块

- 标题「置顶收藏」+ 星标 SVG 图标，样式同分类标题
- 若置顶集合为空，整个区块隐藏

### 4.6 空状态 / 加载状态

- **空状态**（搜索无结果 / 分类无站点）：虚线边框容器居中，图标为 SVG 线条，文案「没有找到与「xxx」相关的网站」，`--fg-secondary`
- **加载状态**（可选，数据较小可不做）：用 3~4 个骨架块，圆角 `--radius-md`，背景 `--bg-hover`，加轻微透明度呼吸动画（尊重 `prefers-reduced-motion`）

## 5. 交互与动效规范

- **状态过渡**（hover / focus / 星标切换）：统一 `--transition`（150ms ease），过渡属性限定 `background-color, border-color, color, opacity`
- **唯一作者式入场动效**：页面加载时网格项做一次交错淡入 + `translateY(4px)` 归零，使用 `--ease-out`（指数缓出），单卡片 300ms、按行 40ms 交错，总时长 ≤ 500ms
- 登录卡片、`page-intro`、Toast、Modal 可各有一次同类短入场（≤ 420ms），同样尊重 `prefers-reduced-motion`
- 禁止 scale 放大动画（破坏极简感）；hover 不上移
- 焦点可见性：键盘 Tab 聚焦元素必须有可见 focus ring（`outline: 2px solid var(--accent); outline-offset: 2px`），仅 `:focus-visible` 触发
- **尊重 `prefers-reduced-motion`**：检测到用户关闭动效时，入场动画与呼吸动画全部禁用

## 6. 浏览器原生表面（Craft Floor 细节）

这些"没特意画"的部分同样承载设计语言，是最廉价的"精心打造"信号：

| 表面 | 规范 |
|------|------|
| 文本选区 `::selection` | 背景 `--selection-bg`，文字 `--fg-primary` |
| 输入框光标 `caret-color` | `--caret`（随主题切换） |
| 滚动条 | 宽度 10px，轨道透明，滑块 `--border` 圆角 `--radius-xs`，hover 时 `--border-strong`；深浅主题自动生效 |
| 焦点环 | 见第 5 节 focus ring 规则 |
| 超链下划线 | 卡片内部不使用下划线；若出现文本链接，hover 时 `text-underline-offset: 3px` |

## 7. 响应式断点

| 断点 | 行为 |
|------|------|
| `> 1080px` | 内容居中，标准网格 |
| `720px ~ 1080px` | 内容随视口收缩，网格自动折行 |
| `< 720px` | 搜索框占满整行（Header 换行），网格最小列宽降至 `160px`，分类间距减半 |

## 8. 无障碍与可访问性

- 图标按钮必须有 `aria-label`
- 星标按钮用 `<button>` 元素（非链接），带 `aria-pressed` 状态
- 深色/浅色两种主题下正文对比度 ≥ 4.5:1（用染色中性色保证，而非叠加 opacity 降对比）
- 主题切换不影响已渲染布局（无跳动）
- 所有可交互元素可键盘操作（Tab 顺序、Enter 触发）

## 9. 主题策略

- 默认跟随系统 `prefers-color-scheme`（**从使用场景决定**：本机使用环境的光线），用户手动切换后存 localStorage 覆盖
- 首屏无闪烁：`index.html` 内联脚本在首帧前读取偏好写入 `<html data-theme>`

## 10. 禁止事项（红线）

- ❌ 不使用渐变背景、不使用图片背景、**不使用渐变文字**（强调靠字重/字号）；登录页允许纯色 `--accent-muted` 圆形氛围块，禁止渐变/图片氛围
- ❌ 不使用 emoji 作为图标（统一内联 SVG 线条图标）
- ❌ 不引入第三方 UI 组件库 / 图标库（用内联 SVG）
- ❌ 卡片不添加默认背景色块、不添加粗边框；**hover 不同时叠加边框+阴影**（ghost card）
- ❌ 不使用硬偏移阴影（`4px 4px 0` 这类非新粗野主义世界的"服装"）
- ❌ 不使用彩色侧边条（卡片/列表项上 >1px 的 border-left/right）
- ❌ 不使用玻璃拟态作装饰（仅 Header 滚动遮挡可用 blur）
- ❌ 不使用弹性/回弹缓动（bounce/elastic），统一指数缓出
- ❌ 不使用 `!important`
- ❌ 不在组件内联样式中写死颜色，全部走 CSS 变量
- ❌ 不使用纯黑 `#000` / 纯白 `#fff` 作为大面积背景
- ❌ 不把等宽字体当"技术感"装饰，仅用于真实数据/计数
