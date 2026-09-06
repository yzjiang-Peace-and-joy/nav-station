# Agnes 2.5 Flash API 接入文档（国内站）

> 已实测调通。适用于在其他项目中快速接入免费文本模型 **Agnes 2.5 Flash**。
> 官方文档：[概述](https://www.agnes-ai.com/zh-Hans/docs/overview) · [Agnes 2.5 Flash](https://www.agnes-ai.com/zh-Hans/docs/agnes-25-flash)

---

## 1. 快速结论

| 项 | 值 |
| --- | --- |
| 站点 | **国内站** |
| Base URL | `https://api.agnes-ai.cn/v1` |
| 模型名 | `agnes-2.5-flash` |
| 接口 | `POST /v1/chat/completions`（OpenAI 兼容） |
| 认证 | `Authorization: Bearer <API_KEY>` |
| 控制台 | https://platform.agnes-ai.cn |
| 当前价格（文档标注） | 输入 / 输出均为 `$0 / 1M tokens`（以控制台为准） |

**重要：** 国内站 Key 只能打国内站 Base URL。国际站 Key / 国际站 URL 混用会返回 `401 无效的令牌`。

---

## 2. 环境变量

```bash
# 必填
AGNES_API_KEY=sk-你的国内站密钥

# 可选（默认已是国内站，一般不用设）
AGNES_BASE_URL=https://api.agnes-ai.cn/v1
```

PowerShell：

```powershell
$env:AGNES_API_KEY='sk-你的国内站密钥'
$env:AGNES_BASE_URL='https://api.agnes-ai.cn/v1'   # 可选
```

本地验证脚本：`agnes_chat.py`

```powershell
python agnes_chat.py "你好"
python agnes_chat.py --stream "写一首短诗"
```

---

## 3. 最小请求（curl）

```bash
curl https://api.agnes-ai.cn/v1/chat/completions \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-2.5-flash",
    "messages": [
      {"role": "system", "content": "You are a helpful AI assistant."},
      {"role": "user", "content": "用一句话介绍你自己"}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
  }'
```

### 成功响应示例

```json
{
  "id": "chatcmpl_xxx",
  "object": "chat.completion",
  "model": "agnes-2.5-flash",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 30,
    "total_tokens": 50
  }
}
```

读取回复：`choices[0].message.content`

---

## 4. 其他项目接入方式

### 4.1 Python（`openai` SDK，推荐）

```bash
pnpm dlx --help > /dev/null 2>&1; pip install openai
```

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["AGNES_API_KEY"],
    base_url="https://api.agnes-ai.cn/v1",
)

resp = client.chat.completions.create(
    model="agnes-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "你好"},
    ],
    temperature=0.7,
    max_tokens=1024,
)

print(resp.choices[0].message.content)
```

流式：

```python
stream = client.chat.completions.create(
    model="agnes-2.5-flash",
    messages=[{"role": "user", "content": "写一首短诗"}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
```

### 4.2 Node.js / TypeScript（`openai` SDK）

```bash
pnpm add openai
```

```ts
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.AGNES_API_KEY,
  baseURL: "https://api.agnes-ai.cn/v1",
});

const resp = await client.chat.completions.create({
  model: "agnes-2.5-flash",
  messages: [
    { role: "system", content: "You are a helpful AI assistant." },
    { role: "user", content: "你好" },
  ],
  temperature: 0.7,
  max_tokens: 1024,
});

console.log(resp.choices[0]?.message?.content);
```

### 4.3 裸 HTTP（任意语言）

```http
POST https://api.agnes-ai.cn/v1/chat/completions
Authorization: Bearer sk-你的密钥
Content-Type: application/json

{
  "model": "agnes-2.5-flash",
  "messages": [
    {"role": "user", "content": "你好"}
  ]
}
```

从已有 OpenAI 项目迁移时，通常只改三处：

1. `base_url` / `baseURL` → `https://api.agnes-ai.cn/v1`
2. `api_key` → 国内站 Agnes Key
3. `model` → `agnes-2.5-flash`

---

## 5. 常用参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `model` | 是 | 固定用 `agnes-2.5-flash` |
| `messages` | 是 | OpenAI 风格对话数组（`system` / `user` / `assistant`） |
| `temperature` | 否 | 随机性，越低越稳定 |
| `max_tokens` | 否 | 最大生成 token |
| `stream` | 否 | `true` 时 SSE 流式返回 |
| `tools` / `tool_choice` | 否 | 工具调用（Function Calling） |

能力参考（官方文档）：

- 上下文窗口：`512K`
- 最大输出：`65.5K`
- 支持多轮对话、流式、工具调用、图像 URL 理解

---

## 6. 线路对照（排错用）

| 线路 | Base URL | 本项目是否使用 |
| --- | --- | --- |
| **国内站** | `https://api.agnes-ai.cn/v1` | **是（默认）** |
| 国际站主线路 | `https://apihub.agnes-ai.com/v1` | 否 |
| 国际站备用 | `https://apihub.agnes-ai.cn/v1` | 否 |

实测：同一把国内站 Key 打国际站 URL → `401 无效的令牌`；打国内站 URL → 成功。

---

## 7. 常见错误

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `401 无效的令牌` | Key 错误 / 过期 / 站点与 Key 不匹配 | 去 https://platform.agnes-ai.cn 重建 Key；确认 Base URL 为国内站 |
| `404` / 路径异常 | Base URL 多拼或少拼了 `/v1` | SDK 场景一般带 `/v1`；若工具会自动追加 `/v1`，则 base 不要再带 `/v1` |
| 连接超时 | 网络或打错线路 | 国内环境优先用 `api.agnes-ai.cn` |
| 回复被截断 | `max_tokens` 过小 | 调大 `max_tokens` |

---

## 8. 安全建议

- API Key 只放服务端 / 环境变量 / CI Secret，**不要写进前端、仓库、截图、文档正文**
- 泄露后立刻在控制台删除或重置
- 本仓库演示脚本通过 `AGNES_API_KEY` 读取，不在代码中硬编码密钥

---

## 9. 相关文件

| 文件 | 说明 |
| --- | --- |
| `agnes_chat.py` | 国内站调通演示脚本（标准库，无第三方依赖） |
| 本文档 | 跨项目接入说明 |

官方参考：

- 概述：https://www.agnes-ai.com/zh-Hans/docs/overview
- 模型：https://www.agnes-ai.com/zh-Hans/docs/agnes-25-flash
- 控制台：https://platform.agnes-ai.cn
