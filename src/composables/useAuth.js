import { ref, computed } from 'vue'

const AUTH_KEY = 'nav_user'

const USERS = {
  yzjiang: {
    password: '123456',
    sitesFile: 'yzjiang'
  },
  test: {
    password: '123456',
    sitesFile: 'test'
  }
}

const currentUser = ref(null)

export function useAuth() {
  const isAuthenticated = computed(() => currentUser.value !== null)
  const username = computed(() => currentUser.value)
  const otherAccounts = computed(() =>
    Object.keys(USERS).filter((name) => name !== currentUser.value)
  )

  function init() {
    const stored = readStored()
    if (stored && USERS[stored]) {
      currentUser.value = stored
    }
  }

  function login(name, password) {
    const user = USERS[name]
    if (!user || user.password !== password) {
      return { ok: false, message: '用户名或密码错误' }
    }
    currentUser.value = name
    persist(name)
    return { ok: true }
  }

  function logout() {
    currentUser.value = null
    clearStored()
  }

  function switchAccount(name, password) {
    if (name === currentUser.value) return { ok: true }
    return login(name, password)
  }

  function getSitesFile() {
    if (!currentUser.value) return null
    return USERS[currentUser.value].sitesFile
  }

  return {
    currentUser,
    username,
    isAuthenticated,
    otherAccounts,
    init,
    login,
    logout,
    switchAccount,
    getSitesFile
  }
}

function readStored() {
  try {
    const v = localStorage.getItem(AUTH_KEY)
    if (v && typeof v === 'string') return v
  } catch {
    /* ignore */
  }
  return null
}

function persist(name) {
  try {
    localStorage.setItem(AUTH_KEY, name)
  } catch {
    /* ignore */
  }
}

function clearStored() {
  try {
    localStorage.removeItem(AUTH_KEY)
  } catch {
    /* ignore */
  }
}
