# Nav Station Backend

## 启动

```bash
cd backend
source .venv/bin/activate
python -m app.seed
python run.py
```

服务监听 `0.0.0.0:9966`，健康检查地址为 `/health`。

生产环境建议通过 systemd、Supervisor 或 Docker 管理进程，并通过 Nginx 反向代理到 `127.0.0.1:9966`。
