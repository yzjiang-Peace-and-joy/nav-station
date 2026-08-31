import { ref, readonly } from 'vue'
import { apiFetch } from '../api/client.js'

const pinnedIds = ref(new Set())
let currentUserId = null

export function usePinned() {
  async function init(userId, defaultIds = []) {
    currentUserId = userId
    const data = await apiFetch('/pins')
    if (!data.site_ids.length && defaultIds.length) {
      await apiFetch('/pins', { method: 'PUT', body: JSON.stringify({ site_ids: defaultIds }) })
      pinnedIds.value = new Set(defaultIds)
    } else pinnedIds.value = new Set(data.site_ids)
  }
  function isPinned(id) { return pinnedIds.value.has(id) }
  async function toggle(id) {
    if (!currentUserId) return
    const data = await apiFetch(`/pins/${encodeURIComponent(id)}/toggle`, { method: 'POST' })
    pinnedIds.value = new Set(data.site_ids)
  }
  return { pinnedIds: readonly(pinnedIds), isPinned, toggle, init }
}
