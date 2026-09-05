# API 代理故障复盘：nav-api.5ai.icu 连接被关闭

## 1. 背景

Nav Station 前端部署在 `https://nav.5ai.icu`，FastAPI 后端监听本机 `0.0.0.0:9966`，原计划通过独立域名 `https://nav-api.5ai.icu` 提供 API。

本次故障发生在后端首次部署和前端切换 API 地址之后。页面可以正常打开，但登录请求失败：

```text
POST https://nav-api.5ai.icu/api/auth/login net::ERR_CONNECTION_CLOSED
```

## 2. 故障现象

- `nav.5ai.icu` 页面和静态资源返回 HTTP 200。
- 浏览器向 `nav-api.5ai.icu` 发起登录请求时报告 `ERR_CONNECTION_CLOSED`。
- nginx 配置中，`nav-api.5ai.icu` 被代理到 `127.0.0.1:9966`。
- 后端服务最初没有监听 9966，因此代理会返回 502。
- 前端之前使用 `https://nav.5ai.icu` 作为 API 基地址时，`/api/auth/login` 实际命中了 SPA 静态站点，POST 请求返回 405 或 HTML，而不是 JSON。

## 3. 排查过程与关键证据

### 3.1 先看监听端口，不先猜代码

```bash
ss -tlnp | grep 9966
curl -sS http://127.0.0.1:9966/health
```

第一次检查时 9966 没有监听，nginx 反代目标不可用。服务器上另有一个不相关的 FastAPI 服务监听 8000，不能把“有 FastAPI 进程”误判为 Nav Station 后端正常。

### 3.2 检查后端启动日志和依赖

启动失败的直接原因是 `passlib 1.7.4` 与 `bcrypt 5.0.0` 不兼容：

```text
AttributeError: module 'bcrypt' has no attribute '__about__'
ValueError: password cannot be longer than 72 bytes
```

同时发现多个长时间未结束的 `pip install` 进程，导致后续 seed 和服务启动实际上没有完成。

处理方式：

- 停止卡住的安装进程。
- 移除 `passlib` 的使用。
- 直接调用 `bcrypt.hashpw` 和 `bcrypt.checkpw`。
- 重新执行 seed。

### 3.3 验证数据库，而不是只验证服务进程

```bash
cd backend
.venv/bin/python -m app.seed
```

seed 后确认数据量：

- 用户：2
- 分类：10
- 标签：24
- 站点：63

### 3.4 区分“后端问题”和“域名/代理问题”

分别测试本机、API 域名和前端域名：

```bash
curl -sS http://127.0.0.1:9966/health
curl -sk https://nav-api.5ai.icu/health
curl -sk https://nav.5ai.icu/api/health
```

在服务启动后，命令行访问 `nav-api.5ai.icu` 可以得到 200，但浏览器仍出现连接关闭，且用户请求没有出现在 nginx 访问日志中。这说明该独立 API 域名链路不稳定，不能作为前端唯一入口。

随后发现部署中的 `nav.5ai.icu` server 块缺少 `/api/` 反代。由于 `location /` 的 `try_files` 会兜底到 `index.html`，同源 API 请求会表现为 HTML 或 405，而不是 FastAPI JSON。

## 4. 根因

本次不是单一故障，而是多个部署问题叠加：

1. **后端未真正启动**：9966 没有监听，初始请求只能得到 502。
2. **依赖兼容性问题**：`passlib 1.7.4` 与 `bcrypt 5.0.0` 导致 seed 失败。
3. **生产 nginx 配置不完整**：实际生效的 `nav.5ai.icu` 配置没有 `/api/` 反代规则。
4. **前端 API 入口选择不稳**：独立域名 `nav-api.5ai.icu` 在浏览器侧出现 `ERR_CONNECTION_CLOSED`，而前端没有同源 fallback。
5. **静态站点兜底掩盖了 API 配置错误**：请求 `/api/...` 被 `location /` 接管时返回 SPA HTML，容易被误判成前端 JSON 或 CORS 问题。

## 5. 最终修复方案

### 后端

- 在 `backend/.venv` 中运行 FastAPI。
- 使用 `bcrypt` 直接完成密码哈希和校验，避免 passlib/bcrypt 版本冲突。
- 执行 `python -m app.seed` 初始化 SQLite。
- 使用 `run.py` 将服务监听在 `0.0.0.0:9966`。

### nginx

生产环境在 `nav.5ai.icu` 的 server 块中明确配置：

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:9966;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

`location /api/` 必须位于 SPA 的 `location /` 之前或与其同级，确保 API 不会落入 `try_files` 的前端兜底逻辑。

### 前端

`src/api/client.js` 使用同源基地址：

```js
const API_BASE_URL = ''
```

最终请求路径为 `/api/auth/login`。生产由 nginx 代理，开发由 Vite proxy 代理到 9966：

```js
proxy: {
  '/api': {
    target: 'http://127.0.0.1:9966',
    changeOrigin: true
  }
}
```

这样避免了独立 API 域名的 DNS、TLS、SNI、网络策略和跨域变量，同时保留了前后端边界。

## 6. 验证清单

每次部署后按以下顺序验证：

```bash
# 1. 端口和进程
ss -tlnp | grep 9966

# 2. 后端健康检查
curl -sS http://127.0.0.1:9966/health

# 3. nginx 配置
sudo nginx -t
sudo systemctl reload nginx

# 4. 同源健康检查
curl -sk https://nav.5ai.icu/api/health

# 5. 登录必须返回 JSON 和 200
curl -sk -X POST https://nav.5ai.icu/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"yzjiang","password":"123456"}'

# 6. 带 token 访问业务接口
curl -sk https://nav.5ai.icu/api/nav \
  -H "Authorization: Bearer <TOKEN>"
```

期望结果：

- `/health` 返回 `{"status":"ok"}`。
- 登录返回 `access_token`、`token_type` 和 `username`。
- `/api/nav` 返回 `categories`、`tags`、`sites`，而不是 `index.html`。
- nginx access log 中能看到对应 API 请求，FastAPI 日志中能看到对应路由访问。
- 浏览器强制刷新后，Network 面板中的请求地址为 `https://nav.5ai.icu/api/...`，不再是 `nav-api.5ai.icu`。

## 7. 后续预防措施

- 后端使用 systemd 或其他进程管理器托管，避免 `nohup` 进程在重启后消失。
- 部署脚本中按顺序执行：安装依赖、seed、健康检查、启动/重启服务、nginx 配置检查、外部 API 检查。
- 不要只检查 HTTP 状态码；同时检查 `Content-Type` 和响应体是否为 JSON，防止把 SPA HTML 当成 API 响应。
- 维护仓库中的 nginx 配置与服务器实际生效配置，修改后执行 `nginx -T` 核对。
- 变更 API 域名、端口或反代规则时，同时检查 `src/api/client.js`、`vite.config.js`、nginx 配置和浏览器 Network 请求。
- 依赖升级后重新执行 seed 和登录测试，特别关注密码哈希库的兼容性。
