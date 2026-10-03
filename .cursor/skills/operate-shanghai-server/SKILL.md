---
name: operate-shanghai-server
description: Operate the authorized Shanghai production server for Nav Station. Use when the user asks about the server, SSH, disk, logs, Nginx, deploy, restart, or https://nav.5ai.icu, or before any production host change.
---

# Operate the Shanghai server

The user has authorized ongoing administration of this host. The always-applied rule `.cursor/rules/shanghai-server.mdc` is the session reminder; this skill is the procedure.

## Host

| Item | Value |
| --- | --- |
| Public site | `https://nav.5ai.icu` |
| SSH | `yzjiang_root@118.89.189.205:22` |
| Machine | Tencent Cloud Shanghai, hostname `VM-0-10-ubuntu` |
| App root | `/apps/nav_station` |
| API | systemd `nav-station-api`, `127.0.0.1:9966` |
| Web | Nginx serves `dist/` and proxies `/api/` to `9966` |
| TLS | `/etc/nginx/ssl/5ai.icu/` for `*.5ai.icu` |
| Credentials | `.cursor/server.env` only |

`.cursor/server.env` is gitignored. Expected variable names, with no secret values in git:

```
NAV_SSH_HOST
NAV_SSH_USER
NAV_SSH_PASSWORD
NAV_SSH_PORT
NAV_PUBLIC_HOST
```

If the file is absent on a new machine, stop and ask the user to restore it. Do not commit it.

## Connect

Load the env file in the shell and use `sshpass -e` so the password is not written into the command text. Install `sshpass` if it is missing. Accept the host key on first connect.

```bash
set -a
. /workspace/.cursor/server.env
set +a
export SSHPASS="$NAV_SSH_PASSWORD"
sshpass -e ssh -o StrictHostKeyChecking=accept-new \
  -o PreferredAuthentications=password -o PubkeyAuthentication=no \
  -p "$NAV_SSH_PORT" "${NAV_SSH_USER}@${NAV_SSH_HOST}"
```

`yzjiang_root` can use passwordless `sudo`. Do not print `NAV_SSH_PASSWORD` in chat, logs, or commits.

## Check the site

Run these on the server, not only from an overseas client:

```bash
systemctl is-active nginx nav-station-api
curl -sf http://127.0.0.1:9966/health
curl -sk -D- https://127.0.0.1/api/health -H 'Host: nav.5ai.icu' -o /dev/null
curl -sk -o /dev/null -w '%{http_code}\n' https://nav.5ai.icu/
```

Port 443 from outside China may never reach this host. A local timeout does not mean the service is down.

## Leave in place

- `/apps/nav_station`, its SQLite database, and `backend/.venv`
- `/etc/nginx/ssl`, `/root/ssl`, and the live Nginx vhosts
- `/usr/local/qcloud` and the Tencent monitoring agents
- Other sites on this Nginx: `cherrylawsite.com.cn`, `test-front.5ai.icu`, `nav-api.5ai.icu`

Logs, package caches, and idle editor remote-server directories may be removed when the user asks for cleanup. Confirm `nginx` and `nav-station-api` still return active afterward.
