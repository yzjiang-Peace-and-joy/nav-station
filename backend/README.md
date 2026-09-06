# Nav Station Backend

## 启动

```bash
cd backend
source .venv/bin/activate
python -m app.seed
python run.py
```

本地 `run.py` 监听 `0.0.0.0:9966`，健康检查地址为 `/health`。

生产使用 systemd 单元 `nav-station-api.service`（仓库内 `backend/nav-station-api.service`）：

```bash
sudo cp backend/nav-station-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now nav-station-api
sudo systemctl status nav-station-api
```

生产进程监听 `127.0.0.1:9966`，由 Nginx `location /api/` 反代。
