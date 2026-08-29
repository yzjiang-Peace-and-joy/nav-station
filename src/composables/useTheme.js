import { ref } from 'vue'

const THEME_KEY = 'nav_theme'

const theme = ref('light')

export function useTheme() {
  function init() {
    const stored = readStored()
    if (stored) {
      theme.value = stored
    } else {
      theme.value = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
    apply(theme.value)
  }

  function toggle() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    apply(theme.value)
    persist(theme.value)
  }

  function apply(val) {
    document.documentElement.setAttribute('data-theme', val)
  }

  function persist(val) {
    try {
      localStorage.setItem(THEME_KEY, val)
    } catch {
      /* localStorage unavailable */
    }
  }

  function readStored() {
    try {
      const v = localStorage.getItem(THEME_KEY)
      if (v === 'light' || v === 'dark') return v
    } catch {
      /* ignore */
    }
    return null
  }

  return { theme, init, toggle }
}