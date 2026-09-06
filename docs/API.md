# 前后端 API 接口说明

## 部署拓扑

| 角色 | 地址 | 说明 |
|------|------|------|
| 前端 SPA | `https://nav.5ai.icu` | Nginx 提供 `dist/` 静态资源 |
| 生产 API（推荐） | `https://nav.5ai.icu/api/...` | 同源反代到本机 FastAPI `127.0.0.1:9966` |
| 独立 API 域名 | `https://nav-api.5ai.icu` | 同样反代到 9966；**浏览器侧曾出现 `ERR_CONNECTION_RESET`，前端默认不使用** |
| 本机 API | `http://127.0.0.1:9966` | uvicorn / `python run.py` |

前端通过 [`src/api/client.js`](../src/api/client.js) 发起请求：

- 默认 `API_BASE_URL = ''`（空串），请求走同源 `/api/...`
- 实际 URL：生产为 `https://nav.5ai.icu/api/...`；开发为 Vite 同源并由 `vite.config.js` proxy 到 `9966`
- 可用 `VITE_API_BASE_URL` 覆盖基址；不建议在生产默认指向 `nav-api.5ai.icu`

若必须排查独立域名，见 [API_PROXY_TROUBLESHOOTING.md](API_PROXY_TROUBLESHOOTING.md)。

## 认证

除标注「否」的接口外，均需：

```http
Authorization: Bearer <access_token>
```

登录成功后前端将 token 存入 `localStorage.nav_token`，后续请求由 `apiFetch` 自动附加。

## 接口一览

### 健康检查

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| `GET` | `/health` | 否 | `{"status":"ok"}`（注意：不在 `/api` 前缀下） |

### 认证 `/api/auth`

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| `POST` | `/api/auth/login` | 否 | body: `{username,password}` → `{access_token,token_type,username}` |
| `GET` | `/api/auth/me` | 是 | `{username}` |
| `GET` | `/api/auth/accounts` | 是 | 其他账户列表 `[{username}]` |

### 个人导航 `/api/nav`

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| `GET` | `/api/nav` | 是 | `{categories,tags,sites}`；站点含可选 `source_plaza_id` |
| `POST` | `/api/nav/sites/{site_slug}/sync-from-plaza` | 是 | 从广场来源覆盖个人副本字段 |

站点对象字段：`id`、`name`、`url`、`desc`、`detail`、`category`、`tags`、`pinned`、`source_plaza_id`。

### 置顶 `/api/pins`

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| `GET` | `/api/pins` | 是 | `{site_ids:[slug,...]}` |
| `PUT` | `/api/pins` | 是 | body: `{site_ids:[...]}` 整体替换 |
| `POST` | `/api/pins/{site_id}/toggle` | 是 | 切换置顶；`site_id` 为个人站点 slug |

### 广场 `/api/plaza`

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| `GET` | `/api/plaza` | 是 | 列表；query: `q`、`category`、`tag`、`include_archived` |
| `GET` | `/api/plaza/meta` | 是 | `{categories,tags}` |
| `GET` | `/api/plaza/{slug}` | 是 | 详情 |
| `POST` | `/api/plaza` | 是 | 创建；body: `{name,url,desc?,detail?,category?,tags?}` |
| `PUT` | `/api/plaza/{slug}` | 是 | wiki 全量更新（字段同创建） |
| `POST` | `/api/plaza/{slug}/archive` | 是 | 软下架 |
| `POST` | `/api/plaza/{slug}/restore` | 是 | 恢复 |
| `POST` | `/api/plaza/{slug}/add` | 是 | 复制到个人目录；可选 `{category}` |

广场站点字段含：`id`、`name`、`url`、`desc`、`detail`、`category`、`tags`、`status`、`added`、创建/更新者与时间。

## 前端调用约定

| Composable | 主要接口 |
|------------|----------|
| `useAuth` | `/api/auth/login`、`/me`、`/accounts` |
| `useSites` | `/api/nav`、`/api/nav/sites/{slug}/sync-from-plaza` |
| `usePinned` | `/api/pins*` |
| `usePlaza` | `/api/plaza*` |

组件不直接 `fetch`；统一经 `apiFetch(path)`，`path` 以 `/auth`、`/nav`、`/pins`、`/plaza` 开头（函数内会再拼 `/api` 与基址）。

## 验证命令

```bash
# 推荐：同源 API
curl -sk https://nav.5ai.icu/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"yzjiang","password":"123456"}'

# 广场列表（替换 TOKEN）
curl -sk https://nav.5ai.icu/api/plaza \
  -H "Authorization: Bearer TOKEN"

# 本机直连
curl -sS http://127.0.0.1:9966/health
```

若 `/api/plaza` 返回 `{"detail":"Not Found"}`，通常是后端进程仍是旧代码，需在 `backend/` 重启 uvicorn（例如 `python run.py` 或 systemd `nav-station-api`）。

## 相关配置

- 前端客户端：[`src/api/client.js`](../src/api/client.js)
- 开发代理：[`vite.config.js`](../vite.config.js)（仅当 `VITE_API_BASE_URL` 为空时使用）
- 生产前端反代备选：[`nginx/nav.5ai.icu.conf`](../nginx/nav.5ai.icu.conf) 的 `location /api/`
- CORS：[`backend/app/config.py`](../backend/app/config.py) 的 `CORS_ORIGINS`
- 故障复盘：[`API_PROXY_TROUBLESHOOTING.md`](API_PROXY_TROUBLESHOOTING.md)
