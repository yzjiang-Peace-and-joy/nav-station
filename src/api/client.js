const TOKEN_KEY = 'nav_token'
// 同源调用：生产由 Nginx 把 https://nav.5ai.icu/api 反代到 FastAPI(9966)；
// 开发由 Vite proxy 转发。可用 VITE_API_BASE_URL 覆盖（例如临时指向其他基址）。
// 注意：浏览器直连 https://nav-api.5ai.icu 曾出现 ERR_CONNECTION_RESET，生产不要默认使用。
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

export async function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers || {})
  headers.set('Content-Type', 'application/json')
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) headers.set('Authorization', `Bearer ${token}`)
  const response = await fetch(`${API_BASE_URL}/api${path}`, { ...options, headers })
  if (response.status === 401) {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem('nav_user')
  }
  const data = await response.json().catch(() => ({}))
  const detail = data.detail
  const message = Array.isArray(detail)
    ? detail.map((item) => item.msg || JSON.stringify(item)).join('; ')
    : detail || '请求失败'
  if (!response.ok) throw new Error(message)
  return data
}

export function setToken(token) { localStorage.setItem(TOKEN_KEY, token) }
export function clearToken() { localStorage.removeItem(TOKEN_KEY) }
export function getToken() { return localStorage.getItem(TOKEN_KEY) }
export function getApiBaseUrl() { return API_BASE_URL }
