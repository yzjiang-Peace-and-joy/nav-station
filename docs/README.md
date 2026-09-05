# Nav Station 文档

## 架构文档

- [全栈概览](architecture/overview.md)：系统拓扑、认证流、部署与跨栈 API 边界
- [前端架构](architecture/frontend.md)：Vue 组件、composables、状态与前端约定
- [后端架构](architecture/backend.md)：FastAPI、模型、路由、配置与数据初始化
- [架构变更日志](architecture/CHANGELOG.md)：架构级决策与影响范围

## 专项文档

- [视觉规范](../VISUAL.md)
- [验收标准](../ACCEPTANCE.md)
- [后端 README](../backend/README.md)

## 维护约定

结构性代码变更完成后，使用 `.cursor/skills/update-architecture-docs/` 对照 checklist 更新文档。纯样式、文案或不改变结构的 bug fix 通常不需要更新架构文档。
