import { ref } from 'vue'

const PACK_KEY = 'nav.themePack'
const SCHEME_KEY = 'nav.colorScheme'
const LEGACY_SCHEME_KEY = 'nav_theme'
const DEFAULT_PACK = 'sunset-coral'

const themePack = ref(DEFAULT_PACK)
const colorScheme = ref('system')
const theme = ref('light')

let mediaQuery = null
let listening = false

export function useTheme() {
  function init() {
    themePack.value = readPack()
    colorScheme.value = readScheme()
    theme.value = resolveScheme(colorScheme.value)
    apply(themePack.value, theme.value)
    persist()
    ensureSystemListener()
  }

  function toggle() {
    const next = theme.value === 'light' ? 'dark' : 'light'
    colorScheme.value = next
    theme.value = next
    apply(themePack.value, next)
    persist()
  }

  function apply(pack, resolved) {
    const root = document.documentElement
    root.setAttribute('data-theme-pack', pack)
    root.setAttribute('data-color-scheme', resolved)
    root.removeAttribute('data-theme')
  }

  function persist() {
    try {
      localStorage.setItem(PACK_KEY, themePack.value)
      localStorage.setItem(SCHEME_KEY, colorScheme.value)
    } catch {
      /* localStorage unavailable */
    }
  }

  function readPack() {
    try {
      const stored = localStorage.getItem(PACK_KEY)
      if (stored === DEFAULT_PACK) return stored
    } catch {
      /* ignore */
    }
    return DEFAULT_PACK
  }

  function readScheme() {
    try {
      const stored = localStorage.getItem(SCHEME_KEY)
      if (stored === 'light' || stored === 'dark' || stored === 'system') return stored
      const legacy = localStorage.getItem(LEGACY_SCHEME_KEY)
      if (legacy === 'light' || legacy === 'dark') return legacy
    } catch {
      /* ignore */
    }
    return 'system'
  }

  function resolveScheme(pref) {
    if (pref === 'light' || pref === 'dark') return pref
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }

  function onSystemChange() {
    if (colorScheme.value !== 'system') return
    theme.value = resolveScheme('system')
    apply(themePack.value, theme.value)
  }

  function ensureSystemListener() {
    if (listening) return
    mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', onSystemChange)
    listening = true
  }

  return { theme, themePack, colorScheme, init, toggle }
}
