const TOKEN_KEY = 'nav_token'
// 同源调用：生产环境由 nginx 把 /api 反代到本机 FastAPI(9966)，
// 开发环境由 vite.config.js 的 server.proxy 转发。
const API_BASE_URL = ''

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
  if (!response.ok) throw new Error(data.detail || '请求失败')
  return data
}

export function setToken(token) { localStorage.setItem(TOKEN_KEY, token) }
export function clearToken() { localStorage.removeItem(TOKEN_KEY) }
export function getToken() { return localStorage.getItem(TOKEN_KEY) }
