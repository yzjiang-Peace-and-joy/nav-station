import { ref, computed } from 'vue'
import { apiFetch, clearToken, getToken, setToken } from '../api/client.js'

const AUTH_KEY = 'nav_user'
const currentUser = ref(null)
const accounts = ref([])

export function useAuth() {
  const isAuthenticated = computed(() => currentUser.value !== null)
  const username = computed(() => currentUser.value)
  const otherAccounts = computed(() => accounts.value.filter((name) => name !== currentUser.value))

  async function init() {
    if (!getToken()) return
    try {
      const user = await apiFetch('/auth/me')
      currentUser.value = user.username
      localStorage.setItem(AUTH_KEY, user.username)
      await loadAccounts()
    } catch { logout() }
  }

  async function loadAccounts() {
    const data = await apiFetch('/auth/accounts')
    accounts.value = data.map((item) => item.username)
  }

  async function login(name, password) {
    try {
      const data = await apiFetch('/auth/login', { method: 'POST', body: JSON.stringify({ username: name, password }) })
      setToken(data.access_token)
      currentUser.value = data.username
      localStorage.setItem(AUTH_KEY, data.username)
      await loadAccounts()
      return { ok: true }
    } catch (err) { return { ok: false, message: err.message } }
  }

  function logout() {
    currentUser.value = null
    accounts.value = []
    clearToken()
    localStorage.removeItem(AUTH_KEY)
  }

  function switchAccount(name, password) {
    if (name === currentUser.value) return Promise.resolve({ ok: true })
    return login(name, password)
  }

  return { currentUser, username, isAuthenticated, otherAccounts, init, login, logout, switchAccount }
}
