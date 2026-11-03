# 视觉指导（VISUAL GUIDE）v2 · 日落珊瑚 · 登录 + 我的

> 本文档定义「个人导航站」**本期可上线**的视觉语言：设计令牌、排版、配色、间距、组件交互、响应式与**可扩展主题包架构**。所有实现必须以此为准。
>
> **产品定调（余镇江 2026-11-03）**：首发主题 **日落珊瑚（Sunset Coral）**——青春、风格化、温暖潮流；版式气质贴近选型稿 B（仪轨感 / 创意排版），颜色采用 BY2 珊瑚方案。打开浏览器的第一站仍是个人收藏快速找回 + 搜索，但视觉从 v1「Operate 冷蓝极简」抬到「温暖风格化」。
> **本期范围**：登录页 + 登录后「我的」（个人收藏 / 搜索 / 置顶）。**分享广场视觉后置**（见 §10）。
> **骨架决策（已定 · 选项 A）**：规范追上侧栏 IA——常驻 `AppSidebar`；主内容为「侧栏右侧流体列」，不再要求整页 1080 居中柱。
> **主题扩展**：以后会给用户更丰富主题选择 → **组件只消费语义 token**；颜色全部由主题包注入；禁止组件内写死珊瑚色或任何色值。
> **与 draft / v1**：布局、侧栏 IA、搜索中心、焦点分工、无障碍、动效上限大量继承 v1；**色板、圆角、SiteCard 常态、登录氛围、主题架构以本 v2 为准**。本 v2 **取代** v1 Operate 冷蓝作为实现准绳；v1 仅作历史参考。
>
> 选型预览：`/workspace/nav-station-designs/B-youth/BY2-coral/`（login/mine × light/dark）。

---

## 目录

1. [设计理念](#1-设计理念)
2. [Design Tokens](#2-设计-tokens)
3. [布局](#3-布局)
4. [组件](#4-组件)
5. [动效](#5-动效)
6. [浏览器原生表面](#6-浏览器原生表面)
7. [无障碍](#7-无障碍)
8. [主题策略（加重）](#8-主题策略加重)
9. [禁止事项](#9-禁止事项)
10. [附录：本期 Out of Scope](#10-附录本期-out-of-scope)
11. [给前端的落地优先级清单](#11-给前端的落地优先级清单)

---

## 1. 设计理念

**青春风格化 · 仪轨感排版**——仍 1 秒内定位到目标分类 / 站点，但打开即有温暖潮流气质：

| 原则 | 落地含义 |
|------|----------|
| 语义色 > 硬编码 | 组件只写 `var(--accent)` 等；换主题包 = 换气质，不改组件 |
| 单强调色（包内） | 每个主题包只暴露一个 `--accent`；禁止第二品牌色作 UI 强调 |
| 仪轨感版式 | 标题阶梯分明、字距略收；侧栏品牌锚点 + 主栏搜索中心（继承选型 B 结构） |
| 青春圆角 | 6 / 10 / 14（登录卡可达 16）；chip / 计数允许 `pill 999px`（**以本 v2 为准，覆盖 v1「禁止胶囊」**） |
| 浅底卡片 | SiteCard 常态「浅底 + 细边」（非纯 ghost）；hover 仍 **边框 / 阴影二选一** |
| 柔和氛围 | 登录页允许 `--glow-ambient` 珊瑚光晕；禁止乱闪赛博、禁止照片背景 |
| 侧栏是导航壳 | 品牌锚点在侧栏；主栏专注「搜索结果 + 分类网格」 |

**本期「看起来对味」的硬约束：**

1. 骨架写死侧栏 IA，主栏按流体列标定留白（`--main-pad-y: 40px`）。
2. Header 减噪：搜索是视觉中心；「我的/广场」保留但广场视觉后置。
3. SiteCard：浅底细边常态；描述单行 ellipsis + 原生 `title`；禁止默认 tooltip 弹层叠边框+阴影。
4. 入场总时长 ≤ 500ms。
5. **主题包架构本期到位**（见 §8），即使设置页主题切换后置。

---

## 2. Design Tokens

所有颜色、间距、圆角、阴影必须通过 CSS 变量使用。**颜色令牌的值由当前主题包 + 深浅方案赋值**；`main.css`（或等价全局结构表）只放结构 / 间距 / 圆角 / 字体与组件规则，**不写死珊瑚色**。

### 2.1 语义色彩令牌（组件只准用这些）

| 变量 | 用途 | 组件可否写死色值 |
|------|------|------------------|
| `--bg-primary` | 页面主背景；主内容区 | ❌ |
| `--bg-secondary` | 浮层、输入、侧栏分区、favicon 托盘、登录卡 | ❌ |
| `--bg-hover` | 卡片 / 控件 hover 底 | ❌ |
| `--fg-primary` | 主文字 / 站名 | ❌ |
| `--fg-secondary` | 次要文字 / 描述（正文对比 ≥4.5:1） | ❌ |
| `--fg-tertiary` | 弱化 / 占位符 / 计数弱态 | ❌ |
| `--border` | 分割线、默认边框 | ❌ |
| `--border-strong` | hover 边框 | ❌ |
| `--accent` | **唯一**强调色（星标、活动标签、主 CTA、焦点、BrandMark） | ❌ |
| `--accent-muted` | 强调弱底（活动标签、搜索外晕、侧栏活动态） | ❌ |
| `--on-accent` | 强调色实心底上的文字/图标 | ❌ |
| `--danger` | 错误 / 危险底或边（若用） | ❌ |
| `--danger-fg` | 危险前景字色 | ❌ |
| `--selection-bg` | `::selection` | ❌ |
| `--caret` | 输入光标 | ❌ |
| `--favicon-0` … `--favicon-5` | favicon 失败首字母底（hash） | ❌ |
| `--favicon-fg` | 首字母前景 | ❌ |
| `--shadow-hover` | 登录卡 / 浮层等**独立**阴影 | ❌ |
| `--glow-ambient` | **可选**；登录页氛围光晕（柔和；禁止动画乱闪） | ❌ |

> 需要新语义时先扩令牌表，再改主题包；**禁止**在组件里发明 `--coral` / `#FB7185` 之类。

### 2.2 首发主题包：`sunset-coral` 色值

选择器约定见 §8。下列为 **`data-theme-pack="sunset-coral"`** 下两套深浅赋值。

#### 浅色（`data-color-scheme="light"` 或未标 dark）

| 变量 | 值 | 备注 |
|------|-----|------|
| `--bg-primary` | `#FFF7F5` | 暖粉白纸感（可用 `#FFF5F2`，全站统一即可） |
| `--bg-secondary` | `#FFFFFF` | 浮层 / 侧栏 / 输入 / 卡 |
| `--bg-hover` | `rgba(244,63,94,0.06)` | 带一点珊瑚染色的 hover |
| `--fg-primary` | `#2A1218` | 暖深褐黑 |
| `--fg-secondary` | `#7C4A56` | ≈6.7:1 @ `#FFF7F5` |
| `--fg-tertiary` | `#8F5F6B` | ≈4.9:1；占位可用 |
| `--border` | `rgba(42,18,24,0.10)` | |
| `--border-strong` | `rgba(42,18,24,0.18)` | |
| `--accent` | `#F43F5E` | **浅色 CTA / 强调**（保证实心钮上白字大文本对比） |
| `--accent-muted` | `rgba(244,63,94,0.12)` | |
| `--on-accent` | `#FFFFFF` | 青春实心钮白字（定稿） |
| `--selection-bg` | `rgba(244,63,94,0.20)` | |
| `--caret` | `#F43F5E` | |
| `--danger` | `#E11D48` | 同色系危险，勿回冷蓝红以外的无关色相亦可，但须令牌化 |
| `--danger-fg` | `#E11D48` | |
| `--favicon-0` | `#F43F5E` | **0 号对齐 accent** |
| `--favicon-1` | `#E879F9` | 保留多色哈希 |
| `--favicon-2` | `#FB923C` | |
| `--favicon-3` | `#A78BFA` | |
| `--favicon-4` | `#2DD4BF` | |
| `--favicon-5` | `#F472B6` | |
| `--favicon-fg` | `#FFF7F5` | |
| `--shadow-hover` | `0 4px 16px rgba(42,18,24,0.08)` | 登录卡等 |
| `--glow-ambient` | `rgba(251,113,133,0.22)` | 登录柔光；可用纯色径向，勿照片 |

#### 深色（`data-color-scheme="dark"`）

| 变量 | 值 | 备注 |
|------|-----|------|
| `--bg-primary` | `#140A12` | 深梅紫黑（选型统一） |
| `--bg-secondary` | `#1F121C` | 侧栏 / 浮层 / 输入 |
| `--bg-hover` | `rgba(251,113,133,0.08)` | |
| `--fg-primary` | `#FDF2F8` | 暖白粉 |
| `--fg-secondary` | `#D4A8B4` | ≈9.3:1 @ `#140A12` |
| `--fg-tertiary` | `#A87884` | ≈5.3:1 |
| `--border` | `rgba(253,242,248,0.10)` | |
| `--border-strong` | `rgba(253,242,248,0.22)` | |
| `--accent` | `#FB7185` | 选型稿珊瑚；图标 / 焦点 / 星标 / 活动态 |
| `--accent-muted` | `rgba(251,113,133,0.16)` | |
| `--on-accent` | `#FFFFFF` | 定稿 |
| `--selection-bg` | `rgba(251,113,133,0.30)` | |
| `--caret` | `#FB7185` | |
| `--danger` | `#FB7185` | 深色危险可提亮；或 `#FDA4AF`——定一即可 |
| `--danger-fg` | `#FDA4AF` | 深色危险字略亮于实心 accent，保证可读 |
| `--favicon-0` … `--favicon-5` | **同浅色表** | 跨深浅固定，避免跳色；0 号仍为浅色 accent `#F43F5E` 或深浅各自 0 号对齐**当前** `--accent`——**推荐跨主题固定浅色表值**，与 v1 策略一致 |
| `--favicon-fg` | `#FDF2F8` | |
| `--shadow-hover` | `0 4px 18px rgba(0,0,0,0.45)` | |
| `--glow-ambient` | `rgba(251,113,133,0.28)` | 登录氛围 |

**实心主按钮与白字对比（写清）：**

- 浅色：`--accent: #F43F5E` + `--on-accent: #FFFFFF` ≈ **3.67:1** → 按 **大文本 / 粗体按钮**（≥14px 且字重 ≥500）满足 AA Large。
- 深色：选型 accent `#FB7185` + 白 ≈ 2.69:1，**不足** AA Large。**深色实心 Primary 底必须改用 `#F43F5E`**（仍属 sunset-coral 同色相），实现方式二选一且全站统一：
  1. **推荐**：深色方案里把 `--accent` 仍作 `#FB7185`（线框/焦点/星标），另增语义令牌 `--accent-fill: #F43F5E` 专供实心 CTA；或
  2. 深色方案直接令 `--accent: #F43F5E`（实心与焦点同色，更简单，青春感略收敛）。
- 本期默认采用 **方案 1**：组件 Primary 使用 `background: var(--accent-fill, var(--accent))`；`sunset-coral` 浅色 `--accent-fill` = `--accent`；深色 `--accent-fill: #F43F5E`。

### 2.3 字体系统

与 v1 相同（结构令牌，不随主题包变色）：

| 变量 | 值 | 用途 |
|------|-----|------|
| `--font-brand` | `"Space Grotesk", "Noto Sans SC", system-ui, sans-serif` | 站名、分类标题、page-intro 标题 |
| `--font-body` | `"Noto Sans SC", "Noto Sans", system-ui, sans-serif` | 正文、站名、描述、控件 |
| `--font-mono` | `"JetBrains Mono", "SFMono-Regular", Consolas, monospace` | 计数、结果 meta（仅数据） |

**必须同页加载：** Space Grotesk 400/500/600/700；Noto Sans SC 400/500/700；JetBrains Mono 400/500。

**字号阶梯（可略加强仪轨感；禁止 14/15/16 逼近）：**

| 变量 | 值 | 用途 |
|------|-----|------|
| `--font-size-display` | `28px` | 登录页站名，700，`letter-spacing: -0.03em`（可至 `-0.04em`） |
| `--font-size-intro` | `22px` | page-intro，600，`letter-spacing: -0.02em`；`<720` → `20px` |
| `--font-size-brand` | `18px` | 侧栏站名，600 |
| `--font-size-title` | `16px` | 分类标题，600 |
| `--font-size-base` | `14px` | 站点名、主控件，500 |
| `--font-size-sm` | `12px` | 描述、标签、辅助 |
| `--font-size-xs` | `11px` | 计数、元信息 |

中文 UI；**禁止 emoji 当图标**。

### 2.4 间距 / 布局令牌

继承 v1：

| 变量 | 值 | 用途 |
|------|-----|------|
| `--space-1` | `4px` | 内聚 |
| `--space-2` | `8px` | 元素内 |
| `--space-3` | `12px` | 常规 |
| `--space-4` | `16px` | 组件间 / 网格 gap |
| `--space-6` | `24px` | 区块内 / 主栏左右 pad |
| `--space-8` | `32px` | 分类间距 / page-intro 下边距基准 |
| `--main-pad-y` | `40px` | 主栏上下 padding |
| `--content-max` | `1080px` | 内容参考上限 |
| `--header-height` | `60px` | 桌面 Header；移动端同步见 §3.3 |
| `--sidebar-width` | `220px` | 常驻侧栏宽 |
| `--grid-min` | `220px` | 网格最小列宽；`<720` → `160px` |

节奏：组内收紧、组间宽松；**标题上方留白 > 标题下方留白**。

### 2.5 圆角 / 过渡（相对 v1 放大 · 青春）

| 变量 | 值 | 用途 |
|------|-----|------|
| `--radius-xs` | `6px` | 小元素、favicon 图本身（v1 为 4） |
| `--radius-sm` | `10px` | 输入、按钮、favicon 托盘、view-switch（v1 为 6） |
| `--radius-md` | `14px` | 卡片、空状态；**登录卡可用 16px**（写死 `16px` 或另令牌 `--radius-lg: 16px`） |
| `--radius-pill` | `999px` | chip、TagFilter、计数 pill（**青春允许**） |
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | 入场 |
| `--transition` | `150ms ease` | 状态切换 |

**过渡属性白名单（默认）：** `background-color, border-color, color, opacity`。  
例外：搜索 focus 的 `box-shadow`；chevron `transform`；主 CTA hover `filter: brightness(1.06)`；登录氛围透明度（静态或一次淡入，禁止循环闪烁）。

---

## 3. 布局

### 3.1 登录页

未登录唯一全屏表面。无侧栏、无 AppHeader 业务槽。

```
┌─────────────────────────────────────────────────────────┐
│  [深浅切换 36×36 · 右上]                                   │
│                                                           │
│        Soft glow（--glow-ambient 径向柔光，非照片）         │
│                                                           │
│              ┌─────────────────────┐                      │
│              │  BrandMark 40×40     │  radius ≈ 16         │
│              │  站名 28px / 700     │                      │
│              │  副文案一行 sm/tert  │                      │
│              │  账户 chips（pill）  │                      │
│              │  密码输入 高 42      │                      │
│              │  主按钮「登录」高 42 │                      │
│              └─────────────────────┘                      │
│                   max-width 400px                         │
└─────────────────────────────────────────────────────────┘
```

| 项 | 规范 |
|----|------|
| 页底 | `--bg-primary`；`min-height: 100vh`；内容垂直水平居中；`padding: var(--space-6)` |
| 氛围 | 允许 1～2 个柔和径向光斑，颜色 `var(--glow-ambient)` 或 `var(--accent-muted)`；**禁止**渐变文字、照片/插画背景、粒子乱闪、赛博扫描线 |
| 登录卡 | `--bg-secondary` + 1px `--border` + **单独** `box-shadow: var(--shadow-hover)`；圆角 `--radius-lg`（16）或 `--radius-md`（14） |
| BrandMark | 40px；色走 `--accent` |
| 账户 chip | 可用 `--radius-pill`；活动态 `--accent-muted` 底 + `--accent` 字 |
| 主按钮 | 底 `var(--accent-fill, var(--accent))`，字 `--on-accent`；hover `brightness(1.06)`；禁用 `opacity: 0.6` |
| 错误 | `--danger-fg` |
| 输入 focus | `border-color: var(--accent)` + `box-shadow: 0 0 0 3px var(--accent-muted)`；`outline: none` |

### 3.2 登录后骨架（Header + Sidebar + Main）

继承 v1 Decision A：

```
┌────────────────────────────────────────────────────────────────┐
│ AppHeader sticky · 高 --header-height(60) · 底 1px --border    │
│ 汉堡(<720) · view-switch · 搜索(max 480 居中) · CTA · User · 深浅 │
├────────────┬───────────────────────────────────────────────────┤
│ AppSidebar │  main.app-main                                    │
│ w=220      │  padding: var(--main-pad-y) var(--space-6)         │
│ bg-sec.    │  max-width: calc(var(--content-max)               │
│ Brand+ h1  │            - var(--sidebar-width) + 80px)         │
│ 分类 / 标签 │  page-intro → 置顶 → CategorySection × N           │
└────────────┴───────────────────────────────────────────────────┘
```

**语义：** `<header>` → `<aside>`（唯一页面级 `<h1>`）→ `<main>`（`page-intro` 用 `<p class="page-intro-title">`，不是第二个 h1）→ `<section>` + `<h2>`。

| 区域 | 关键规则 |
|------|----------|
| Header | `sticky; top: 0`；背景 `color-mix(in srgb, var(--bg-primary) 85%, transparent)` + `backdrop-filter: blur(8px)`（仅滚动遮挡） |
| Sidebar | `width: var(--sidebar-width)`；`sticky; top: var(--header-height)`；`height: calc(100vh - var(--header-height))`；`--bg-secondary`；右 1px `--border` |
| Main | 上下 `--main-pad-y`、左右 `--space-6`；非整页 1080 居中柱 |

### 3.3 响应式

| 断点 | 行为 |
|------|------|
| `> 1080px` | 侧栏常驻 220；主栏流体 |
| `720px ~ 1080px` | 侧栏常驻；网格折行 |
| `< 720px` | 侧栏 drawer；`--grid-min → 160px`；分类间距减半；page-intro 纵排，标题 20px |

**移动端 Header 高度同步（P0 继承）：** `<720` 若 Header 实际高度 > 60，必须用 ResizeObserver（或强制单行）把 `--header-height` 写回，侧栏 / drawer 一律读变量。

### 3.4 网格

```css
.sites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--grid-min), 1fr));
  gap: var(--space-4);
}
```

搜索/过滤后无站点的 CategorySection **整块不渲染**。

---

## 4. 组件

### 4.1 BrandMark

| 项 | 规范 |
|----|------|
| 形态 | 正方形圆角几何标（山形负形），与产品 favicon 同源 |
| 尺寸 | 侧栏 `28px`；登录 `40px`（`--brand-mark-size`） |
| 色 | `currentColor` / 填充 → `--accent`；挖空透出 `--bg-secondary` |
| 用法 | 仅登录品牌区 + 侧栏 `h1` 横排；Header **不**放站名 |

### 4.2 AppHeader（「我的」）

| 槽位 | 规范 |
|------|------|
| 汉堡 | 仅 `<720`；36×36；`aria-expanded` / `aria-controls` |
| view-switch | 分段「我的 / 广场」；容器 pad 3px、`--bg-secondary`、1px `--border`、`--radius-sm`；活动态 `--accent-muted` + `--accent` 字 |
| 搜索 | 视觉中心；max-width `480px`；`--bg-secondary`、1px `--border`、`--radius-sm`；`caret-color: var(--caret)` |
| 主 CTA | 「添加网站」——`var(--accent-fill, var(--accent))` + `--on-accent`；高 32–36；`--radius-sm` |
| UserMenu | 面板 `--bg-secondary` + 边框；危险项 `--danger-fg` |
| 深浅切换 | 36×36；切换 `data-color-scheme`（见 §8）；**不是**主题包切换 |
| 主题包切换 | **本期可不进 Header**；预留设置页（§8.5） |

**减噪：** ❌「我的」不展示广场归档开关；❌ Header 不再放站名；✅ 窄屏优先保证搜索 ≥ 200px。

**搜索聚焦：**

```css
.search-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-muted);
  outline: none;
}
```

### 4.3 AppSidebar

| 区 | 规范 |
|----|------|
| 品牌行 | BrandMark 28 + 站名 `h1`；`--font-size-brand` / 600；`letter-spacing: -0.02em` |
| 分类导航 | 默认 `--fg-secondary`；活动 `--accent` 或 `--accent-muted` 底（全站统一一种） |
| 标签区 | 纵向 TagFilter；组间 ≥ `--space-4` |
| 滚动 | `overflow-y: auto`；滚动条 §6 |

### 4.4 TagFilter（侧栏纵向）

| 态 | 规范 |
|----|------|
| 尺寸 | 高 26px；padding `0 10px`；字 `--font-size-xs`；**`--radius-pill`**（青春） |
| 默认 | 透明或极浅底 + 1px `--border`；字 `--fg-secondary` |
| 活动 | `--accent-muted` 底 + `--accent` 字 |
| hover | 边框 `--border-strong` |

### 4.5 page-intro

| 项 | 规范 |
|----|------|
| 结构 | 左：标题 `<p>` + 说明；右：`mono` 计数 |
| 标题 | `--font-size-intro`、`--font-brand`、600、`--fg-primary`；字距可 `-0.02em` |
| 说明 | `--font-size-sm`、`--fg-tertiary`；例：「个人收藏，搜索后快速打开」 |
| 计数 | `--font-mono` |
| 分隔 | 底 1px `--border`；下边距 `--space-8` |

### 4.6 CategorySection

标题（16/600/brand）+ 计数 pill（`--radius-pill`）+ 1px 线 + `sites-grid`。  
标题↔线 `--space-3`；线↔网格 `--space-4`；区块间距 `--space-8`。

### 4.7 SiteCard（相对 v1：浅底细边常态）

```
┌─────────────────────────────────────┐
│ [托盘 26]  站点名称            ★    │
│            描述（一行省略）           │
└─────────────────────────────────────┘
```

| 状态 | 表现 |
|------|------|
| 默认 | **`--bg-secondary` + 1px `--border`**（青春卡片感）；`--radius-md`；内边距 `12px 14px` |
| hover | **二选一（全站统一）：** ① 边框改 `--border-strong` + `--bg-hover`；或 ② 保持边框、加 `box-shadow: var(--shadow-hover)`。**禁止边框加粗同时叠阴影** |
| 星标未置顶 | 默认隐，hover/焦点显；`--fg-tertiary`；`aria-pressed="false"` |
| 星标已置顶 | 常显；`--accent` 实心；`aria-pressed="true"` |

**结构：** `article.site-card` → `a.site-card-link` + 独立 `button.pin-btn`。

| 细节 | 规范 |
|------|------|
| favicon 托盘 | 26×26；`--bg-primary` 或略深于卡底 + 1px `--border`；`--radius-sm`；内 16×16 |
| 失败首字母 | 底 `var(--favicon-N)`；字 `var(--favicon-fg)` |
| 站名 | `--font-size-base` / 500 / `--fg-primary`；ellipsis |
| 描述 | 单行 ellipsis；完整文案用原生 `title`；禁止默认 `.site-tooltip` 弹层 |

### 4.8 空状态

虚线容器 `border: 1px dashed var(--border)`；`--radius-md`；底 `color-mix(in srgb, var(--bg-hover) 70%, transparent)`；SVG 线稿 36×36（禁 emoji）；文案走 `--fg-secondary`。

### 4.9 深浅切换控件

Header / 登录右上：36×36；只切换 `data-color-scheme`；图标随当前方案；无布局跳动。

### 4.10 主 CTA / 次要按钮

| 类型 | 规范 |
|------|------|
| Primary | `var(--accent-fill, var(--accent))` + `--on-accent`；hover `brightness(1.06)` |
| Secondary | 透明或 `--bg-secondary` + 1px `--border`；hover `--bg-hover` + `--border-strong` |
| Danger 文本 | `--danger-fg` |

---

## 5. 动效

| 动效 | 规格 | 上限 |
|------|------|------|
| 网格入场 | opacity + `translateY(4px→0)`；单卡 300ms；stagger 40ms×index；`--ease-out` | **总 ≤ 500ms** |
| page-intro | 可选 ≤360ms | |
| 登录卡 | ≤420ms | |
| 状态过渡 | `--transition` 150ms | 白名单 §2.5 |

**禁止：** scale 放大；hover 上移；bounce/elastic；装饰性无限循环（含氛围光脉冲循环）；赛博闪烁。

### 焦点策略

| 控件 | 表现 |
|------|------|
| 文本输入 | border `--accent` + `0 0 0 3px var(--accent-muted)`；`outline: none` |
| 按钮 / chip / 链接 | `:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }` |

### `prefers-reduced-motion: reduce`

关闭入场与氛围动画；元素直接静态可见。保留必要颜色/边框状态变化。

---

## 6. 浏览器原生表面

| 表面 | 规范 |
|------|------|
| `::selection` | `--selection-bg` + `--fg-primary` |
| `caret-color` | `--caret` |
| 滚动条 | 宽 10px；轨道透明；滑块 `--border`；hover `--border-strong`；圆角 `--radius-xs` |
| 超链 | 卡内无下划线；独立文本链 hover `text-underline-offset: 3px` |

---

## 7. 无障碍

- 图标按钮必须有 `aria-label`。
- 星标：`<button>` + `aria-pressed`。
- 正文 `--fg-secondary` 对 `--bg-primary` ≥ **4.5:1**（本包已按此校准）。
- Primary 实心钮按大文本对比；深色用 `--accent-fill`（见 §2.2）。
- 深浅 / 主题包切换不引起布局跳动。
- 全键盘可达；drawer：`Esc` / backdrop 关闭。
- 页面仅一个 `h1`（侧栏站名）。
- 中文界面；勿仅靠颜色传达唯一信息（活动态可用底+字色双通道）。

---

## 8. 主题策略（加重）

> 本节是 v2 相对 v1 的核心增量。以后用户会有更丰富主题；**本期就必须把架构写死**，避免二次重构。

### 8.1 两层切换（必须同时存在）

| 层 | DOM 约定（推荐） | 含义 |
|----|------------------|------|
| **主题包** | `data-theme-pack="sunset-coral"` 写在 `<html>`（或 `<body>`，全站统一一处） | 换整套色板 / 氛围（珊瑚 / 薄荷 / 铂银…） |
| **深浅方案** | `data-color-scheme="light"` \| `"dark"` | **同一包内**的浅色 / 深色 |

兼容说明：若现网已用 `data-theme="dark"`，允许过渡期映射为 `data-color-scheme="dark"`，但新代码与文档统一用 `data-color-scheme`；**不要**用同一个属性既表示包又表示深浅。

示例：

```html
<html data-theme-pack="sunset-coral" data-color-scheme="dark">
```

```css
/* 伪代码结构 */
html[data-theme-pack="sunset-coral"][data-color-scheme="light"] { /* 赋浅色 token */ }
html[data-theme-pack="sunset-coral"][data-color-scheme="dark"]  { /* 赋深色 token */ }
```

### 8.2 文件约定（给前端）

```
src/styles/
  main.css                 # 结构 / 间距 / 圆角 / 字体 / 组件规则（无品牌色字面量）
  themes/
    _registry.css          # 可选：@import 各包；或 JS 注册表
    sunset-coral.css       # 本期唯一必实现：导出 light + dark 两套赋值
    soft-pop.css           # 预留（本期可空壳或仅注释）
    mint-pop.css
    lav-cream.css
    platinum.css
    nova-cyan.css
```

规则：

1. **组件与 `main.css` 只引用 §2.1 语义名**，不出现 `#FB7185` / `#F43F5E` 等字面量（字面量仅允许出现在 `themes/*.css`）。
2. 每个主题包文件内用属性选择器写齐 light + dark。
3. 新增主题 = 新文件 + 注册表加一行；**不改组件**。

### 8.3 主题包 ID 登记

| pack id | 显示名（设置页用） | 本期 | 说明 |
|---------|-------------------|------|------|
| `sunset-coral` | 日落珊瑚 | **必实现** | 首发；BY2 |
| `soft-pop` | 软糖紫粉 | 预留 | BY1；主题市场/设置后置 |
| `mint-pop` | 电薄荷 | 预留 | BY3 |
| `lav-cream` | 薰衣草奶油 | 预留 | BY4 |
| `platinum` | 铂银仪轨 | 预留 | B2 |
| `nova-cyan` | 深空青辉 | 预留 | 方向 A |

> **本期勿写死 UI** 去展示未实现包；不要在设置页画六个色点却点了无效。预留包可建空 CSS 文件或 registry 注释，色值后续补。

### 8.4 用户偏好持久化

| 键 | 建议值 | 说明 |
|----|--------|------|
| `localStorage['nav.themePack']` | `"sunset-coral"` | 主题包 id |
| `localStorage['nav.colorScheme']` | `"light"` \| `"dark"` \| `"system"` | 深浅；`system` = 跟随 `prefers-color-scheme` |

也可合并为单一 JSON 键 `nav.theme`：`{ "pack": "sunset-coral", "scheme": "system" }`——二选一，全站统一。

**默认：** `sunset-coral` + `system`（或上次用户选择）。

**首屏防闪：** `index.html` 内联脚本在首帧前读取上述键，写好 `data-theme-pack` 与 `data-color-scheme`（若为 `system` 则当时解析成 light/dark）。

### 8.5 主题切换 UX

| 能力 | 本期 | 说明 |
|------|------|------|
| 深浅切换 | **要做** | Header / 登录右上已有入口；只改 `data-color-scheme` + 持久化 |
| 主题包切换 | **可后置** | 设置页 / 主题市场；**token 架构与 `sunset-coral.css` 本期必须到位** |
| 预览六包 | 不做 | 避免半残 UI |

### 8.6 组件消费契约（验收用）

```text
✅ className / CSS 中仅 var(--bg-*) var(--fg-*) var(--accent*) …
❌ style={{ color: '#FB7185' }}
❌ .site-card { border-color: #F43F5E }
❌ if (theme === 'dark') return '#60a5fa'  // 旧冷蓝分支
```

主题包切换时，React/Vue 等**不应**为每个主题复制组件；最多在根节点设 DOM 属性。

---

## 9. 禁止事项（红线）

- ❌ 组件内写死任何颜色（含 `#fff`、`#FB7185`、favicon 六色）——一律语义令牌；字面量仅主题包文件。
- ❌ 用同一 `data-*` 属性同时表示「主题包」与「深浅」。
- ❌ 照片背景 / 乱闪赛博 / 渐变文字；登录仅允许柔和 `--glow-ambient`。
- ❌ emoji 当图标；第三方 UI / 图标库。
- ❌ SiteCard hover **同时**叠加粗边框 + 阴影。
- ❌ 默认弹出带边框+阴影的 description tooltip。
- ❌ 硬偏移阴影（`4px 4px 0`）；彩色侧边条（>1px 装饰 border-left）。
- ❌ 装饰性玻璃拟态（仅 Header 滚动遮挡可用 blur）。
- ❌ 弹性缓动；`!important` 刷色。
- ❌ 大面积纯黑 `#000` / 纯冷灰作页面主背景（回到 v1 冷蓝默认亦禁止）。
- ❌ 等宽字体当装饰；仅计数/数据。
- ❌ 入场总时长 >500ms。
- ❌ 「我的」顶栏塞入广场归档开关。
- ❌ 本期设置页展示未实现主题包的假入口（预留包勿冒充可用）。

---

## 10. 附录：本期 Out of Scope

- 分享广场信息流、`PlazaSiteCard`、提交网站 Modal/Toast 微观规格
- 「显示已下架」归档开关
- **主题包切换设置页 / 主题市场 UI**（架构本期做，UI 后置）
- 预留包（`soft-pop` 等）的正式色值与预览图验收
- 广场运营、审核、推荐相关 UI

一句话：**广场视觉后置；主题市场后置；本期验收 = 登录 +「我的」+ sunset-coral 深浅 + 语义 token 架构。**

---

## 11. 给前端的落地优先级清单

| 优先级 | 项 | 验收要点 |
|--------|----|----------|
| **P0** | 主题包 CSS 骨架 | `src/styles/themes/sunset-coral.css`（或等价路径）含 light + dark 全套 §2.1/§2.2 赋值；`<html>` 具备 `data-theme-pack` + `data-color-scheme` |
| **P0** | 组件去硬编码色 | 全局搜十六进制 / 旧蓝 `#2563eb`/`#60a5fa`；改语义 token；Primary 用 `var(--accent-fill, var(--accent))` |
| **P0** | `main.css` 无品牌色字面量 | 结构/间距/圆角/字体/组件规则与色值文件分离 |
| **P0** | 日落圆角与卡片 | `--radius-xs/sm/md` 按 §2.5；登录卡 14–16；TagFilter/chip 可用 pill；SiteCard 浅底+细边常态 |
| **P0** | 珊瑚强调与深浅切换 | 首发仅 `sunset-coral`；Header/登录深浅切换读写 `nav.colorScheme`（或合并键）并防闪 |
| **P0** | 登录氛围 | `--glow-ambient` 柔光；无照片/无闪烁循环 |
| **P0** | 焦点 / 搜索 / 入场 / Mono 字体 | 继承 v1：搜索外晕、按钮 `:focus-visible`、入场 ≤500ms、JetBrains Mono 加载 |
| **P0** | 骨架 §3.2 | 侧栏 IA、主栏 `padding-y: 40px`、品牌在侧栏 |
| **P1** | 预留包注册 | `soft-pop` / `mint-pop` / `lav-cream` / `platinum` / `nova-cyan` 空文件或 registry 注释；**不**做设置页假入口 |
| **P1** | `nav.themePack` 读写 | 即使 UI 后置，持久化与首屏脚本先支持 pack 键（默认 `sunset-coral`） |
| **P1** | 空状态虚线容器、移动 Header 高度同步、page-intro | 按 §4.8 / §3.3 / §4.5 |
| **P2** | 设置页主题包切换 UI | 后置；有正式色值与预览后再做 |

**P0 条数：8**（上表 P0 行）。

---

**文档版本：** v2-sunset-coral · 2026-11-03（Asia/Singapore）  
**适用仓库：** `yzjiang-Peace-and-joy/nav-station`  
**线上对照：** https://nav.5ai.icu  
**选型预览：** `/workspace/nav-station-designs/B-youth/BY2-coral/`  
**取代关系：** **本 v2 取代 v1 Operate 冷蓝作为实现准绳**；`/workspace/nav-station-VISUAL-v1-mine-login.md` 仅历史参考。可覆盖仓库 `VISUAL.md` 中「个人导航」章节；广场专章与主题市场专章待后续文档。
