import { ref, computed } from 'vue'
import { apiFetch } from '../api/client.js'

const SEARCH_DEBOUNCE = 150

export function usePlaza() {
  const categories = ref([])
  const sites = ref([])
  const tags = ref([])
  const loadError = ref(false)
  const searchQuery = ref('')
  const deferredQuery = ref('')
  const activeTag = ref(null)
  const activeCategory = ref('all')
  const includeArchived = ref(false)
  const busy = ref(false)
  let debounceTimer = null

  async function load() {
    loadError.value = false
    try {
      const params = new URLSearchParams()
      if (includeArchived.value) params.set('include_archived', 'true')
      const qs = params.toString()
      const data = await apiFetch(`/plaza${qs ? `?${qs}` : ''}`)
      normalize(data)
    } catch (err) {
      console.error('[nav_station] 广场加载失败：', err)
      loadError.value = true
      categories.value = []
      sites.value = []
      tags.value = []
    }
  }

  function normalize(data) {
    const validTags = new Set(Array.isArray(data.tags) ? data.tags : [])
    const seenIds = new Set()
    const seenCats = new Set()
    const validSites = (Array.isArray(data.sites) ? data.sites : []).filter((site) => {
      if (seenIds.has(site.id)) return false
      seenIds.add(site.id)
      site.tags = (site.tags || []).filter((tag) => validTags.has(tag))
      if (!site.category) site.category = '__uncategorized'
      return true
    })
    const validCategories = (Array.isArray(data.categories) ? data.categories : []).filter((cat) => {
      if (seenCats.has(cat.id)) return false
      seenCats.add(cat.id)
      return true
    })
    const catIds = new Set(validCategories.map((c) => c.id))
    let missing = false
    validSites.forEach((site) => {
      if (!catIds.has(site.category)) {
        site.category = '__uncategorized'
        missing = true
      }
    })
    categories.value = missing
      ? [...validCategories, { id: '__uncategorized', name: '未分类' }]
      : validCategories
    sites.value = validSites
    tags.value = [...validTags]
  }

  function setQuery(val) {
    searchQuery.value = val
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
      deferredQuery.value = val.trim()
    }, SEARCH_DEBOUNCE)
  }

  function setTag(tag) {
    activeTag.value = activeTag.value === tag ? null : tag
  }

  function setCategory(id) {
    activeCategory.value = id
  }

  function resetFilters() {
    clearTimeout(debounceTimer)
    searchQuery.value = ''
    deferredQuery.value = ''
    activeTag.value = null
    activeCategory.value = 'all'
  }

  async function setIncludeArchived(value) {
    includeArchived.value = Boolean(value)
    await load()
  }

  const filteredSites = computed(() => {
    const q = deferredQuery.value.toLowerCase()
    const tag = activeTag.value
    return sites.value.filter(
      (s) =>
        (!tag || s.tags.includes(tag)) &&
        (!q ||
          [s.name, s.desc, s.detail, s.tags.join(' ')].some((v) =>
            (v || '').toLowerCase().includes(q)
          ))
    )
  })

  const categoryCounts = computed(() =>
    Object.fromEntries(
      categories.value.map((c) => [
        c.id,
        filteredSites.value.filter((s) => s.category === c.id).length
      ])
    )
  )

  const displayGroups = computed(() => {
    const groups = categories.value
      .map((c) => ({
        ...c,
        sites: filteredSites.value.filter((s) => s.category === c.id)
      }))
      .filter((g) => g.sites.length)
    if (activeCategory.value === 'all') return groups
    return groups.filter((g) => g.id === activeCategory.value)
  })

  const hasResults = computed(() => displayGroups.value.length > 0)

  async function create(payload) {
    busy.value = true
    try {
      const site = await apiFetch('/plaza', { method: 'POST', body: JSON.stringify(payload) })
      await load()
      return { ok: true, site }
    } catch (err) {
      return { ok: false, message: err.message || '创建失败' }
    } finally {
      busy.value = false
    }
  }

  async function update(slug, payload) {
    busy.value = true
    try {
      const site = await apiFetch(`/plaza/${encodeURIComponent(slug)}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      })
      await load()
      return { ok: true, site }
    } catch (err) {
      return { ok: false, message: err.message || '更新失败' }
    } finally {
      busy.value = false
    }
  }

  async function archive(slug) {
    busy.value = true
    try {
      await apiFetch(`/plaza/${encodeURIComponent(slug)}/archive`, { method: 'POST' })
      await load()
      return { ok: true }
    } catch (err) {
      return { ok: false, message: err.message || '下架失败' }
    } finally {
      busy.value = false
    }
  }

  async function restore(slug) {
    busy.value = true
    try {
      await apiFetch(`/plaza/${encodeURIComponent(slug)}/restore`, { method: 'POST' })
      await load()
      return { ok: true }
    } catch (err) {
      return { ok: false, message: err.message || '恢复失败' }
    } finally {
      busy.value = false
    }
  }

  async function addToNav(slug, category = null) {
    busy.value = true
    try {
      const body = category ? { category } : {}
      const site = await apiFetch(`/plaza/${encodeURIComponent(slug)}/add`, {
        method: 'POST',
        body: JSON.stringify(body)
      })
      const local = sites.value.find((s) => s.id === slug)
      if (local) local.added = true
      return { ok: true, site }
    } catch (err) {
      return { ok: false, message: err.message || '添加失败' }
    } finally {
      busy.value = false
    }
  }

  return {
    categories,
    sites,
    tags,
    loadError,
    searchQuery,
    activeTag,
    activeCategory,
    includeArchived,
    busy,
    filteredSites,
    categoryCounts,
    displayGroups,
    hasResults,
    load,
    setQuery,
    setTag,
    setCategory,
    resetFilters,
    setIncludeArchived,
    create,
    update,
    archive,
    restore,
    addToNav
  }
}
