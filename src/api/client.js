const TOKEN_KEY = 'nav_token'

export async function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers || {})
  headers.set('Content-Type', 'application/json')
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) headers.set('Authorization', `Bearer ${token}`)
  const response = await fetch(`/api${path}`, { ...options, headers })
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
