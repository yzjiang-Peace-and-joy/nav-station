import json
import re
from html import unescape
from urllib.parse import urlparse

import httpx
from fastapi import HTTPException

from ..config import settings


TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
DESCRIPTION_RE = re.compile(
    r'<meta[^>]+(?:name|property)=["\'](?:description|og:description)["\'][^>]+content=["\'](.*?)["\']',
    re.IGNORECASE | re.DOTALL,
)


def normalize_url(url: str) -> str:
    value = url.strip()
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise HTTPException(400, "请输入有效的 http(s) 网址")
    while value.endswith("/") and value.count("/") > 2:
        value = value[:-1]
    return value


def _clean_html_value(value: str, max_length: int = 500) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", unescape(value)).strip()
    return value[:max_length]


def _page_context(url: str) -> tuple[str, str]:
    try:
        response = httpx.get(
            url,
            follow_redirects=True,
            timeout=httpx.Timeout(5.0, connect=3.0),
            headers={"User-Agent": "NavStation AI suggester/1.0"},
        )
        response.raise_for_status()
        html = response.text[:1_000_000]
        title_match = TITLE_RE.search(html)
        description_match = DESCRIPTION_RE.search(html)
        return (
            _clean_html_value(title_match.group(1)) if title_match else "",
            _clean_html_value(description_match.group(1)) if description_match else "",
        )
    except (httpx.HTTPError, UnicodeError):
        return "", ""


def _extract_json(content: str) -> dict:
    text = content.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.IGNORECASE | re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise HTTPException(502, "AI 返回的数据格式无效") from exc
    if not isinstance(value, dict):
        raise HTTPException(502, "AI 返回的数据格式无效")
    return value


def suggest_site(url: str, categories: list[str], tags: list[str]) -> dict:
    if not settings.agnes_api_key.strip():
        raise HTTPException(503, "AI 解析服务尚未配置 API Key")

    normalized_url = normalize_url(url)
    title, page_description = _page_context(normalized_url)
    category_text = "、".join(categories) or "暂无现有分类"
    tag_text = "、".join(tags) or "暂无现有标签"
    system_prompt = (
        "你是网站目录编辑。根据网址和页面摘要，为广场站点生成准确、简洁的中文信息。"
        "必须只输出一个 JSON 对象，不要 Markdown、解释或额外文字。"
    )
    user_prompt = f"""请解析这个网站并输出以下字段：
{{"name":"站点名称","url":"网址","desc":"一句话简介","detail":"详细介绍","category":"分类名称","tags":["标签1","标签2"]}}

网址：{normalized_url}
页面标题：{title or "未获取到"}
页面 description：{page_description or "未获取到"}
已有分类（优先选择其中一个）：{category_text}
已有标签（可参考，最多 5 个）：{tag_text}
要求：name 不超过 200 字，desc 不超过 500 字，detail 不超过 2000 字，tags 为 1-5 个简短中文标签；url 必须保持为输入网址。"""

    try:
        response = httpx.post(
            f"{settings.agnes_base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.agnes_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.agnes_model,
                "temperature": 0.2,
                "max_tokens": 1200,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=httpx.Timeout(30.0, connect=5.0),
        )
        response.raise_for_status()
        body = response.json()
        content = body["choices"][0]["message"]["content"]
    except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError) as exc:
        raise HTTPException(502, "AI 解析服务暂时不可用") from exc

    data = _extract_json(content)
    name = str(data.get("name", "")).strip()[:200]
    desc = str(data.get("desc", "")).strip()[:500]
    detail = str(data.get("detail", "")).strip()[:2000]
    category = str(data.get("category", "")).strip()[:100] or None
    raw_tags = data.get("tags", [])
    result_tags = [str(tag).strip()[:50] for tag in raw_tags if str(tag).strip()][:5] if isinstance(raw_tags, list) else []
    if not name or not desc:
        raise HTTPException(502, "AI 未能生成完整的站点信息")
    return {
        "name": name,
        "url": normalized_url,
        "desc": desc,
        "detail": detail,
        "category": category,
        "tags": result_tags,
    }
