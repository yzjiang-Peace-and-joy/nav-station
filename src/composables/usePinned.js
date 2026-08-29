import { ref, readonly } from 'vue'

const PINNED_KEY = 'nav_pinned'

const pinnedIds = ref(new Set())

function load() {
  try {
    const raw = localStorage.getItem(PINNED_KEY)
    if (raw === null) return null
    const arr = JSON.parse(raw)
    if (!Array.isArray(arr)) return new Set()
    return new Set(arr.filter((id) => typeof id === 'string'))
  } catch {
    return new Set()
  }
}

function save(set) {
  try {
    localStorage.setItem(PINNED_KEY, JSON.stringify([...set]))
  } catch {
    /* localStorage unavailable */
  }
}

export function usePinned() {
  function init(defaultIds = []) {
    const stored = load()
    if (stored === null) {
      pinnedIds.value = new Set(defaultIds)
      save(pinnedIds.value)
    } else {
      pinnedIds.value = stored
    }
  }

  function isPinned(id) {
    return pinnedIds.value.has(id)
  }

  function toggle(id) {
    const next = new Set(pinnedIds.value)
    if (next.has(id)) {
      next.delete(id)
    } else {
      next.add(id)
    }
    pinnedIds.value = next
    save(next)
  }

  return { pinnedIds: readonly(pinnedIds), isPinned, toggle, init }
}