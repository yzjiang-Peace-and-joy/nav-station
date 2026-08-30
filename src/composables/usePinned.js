import { ref, readonly } from 'vue'

const PINNED_KEY_PREFIX = 'nav_pinned_'

const pinnedIds = ref(new Set())
let currentUserId = null

function storageKey(userId) {
  return `${PINNED_KEY_PREFIX}${userId}`
}

function load(userId) {
  try {
    const raw = localStorage.getItem(storageKey(userId))
    if (raw === null) return null
    const arr = JSON.parse(raw)
    if (!Array.isArray(arr)) return new Set()
    return new Set(arr.filter((id) => typeof id === 'string'))
  } catch {
    return new Set()
  }
}

function save(userId, set) {
  try {
    localStorage.setItem(storageKey(userId), JSON.stringify([...set]))
  } catch {
    /* localStorage unavailable */
  }
}

export function usePinned() {
  function init(userId, defaultIds = []) {
    currentUserId = userId
    const stored = load(userId)
    if (stored === null) {
      pinnedIds.value = new Set(defaultIds)
      save(userId, pinnedIds.value)
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
    if (currentUserId) save(currentUserId, next)
  }

  return { pinnedIds: readonly(pinnedIds), isPinned, toggle, init }
}