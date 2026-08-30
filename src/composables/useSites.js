import { ref, computed } from 'vue'

const SEARCH_DEBOUNCE = 150

export function useSites({ isPinned }) {
  const categories = ref([])
  const sites = ref([])
  const tags = ref([])
  const loadError = ref(false)

  const searchQuery = ref('')
  const deferredQuery = ref('')
  const activeTag = ref(null)
  const activeCategory = ref('all')
  let debounceTimer = null

  async function load() {
    try {
      const module = await import('../data/sites.json')
      validateAndNormalize(module.default)
    } catch (err) {
      console.error('[nav_station] 数据加载失败：', err)
      loadError.value = true
    }
  }

  function validateAndNormalize(data) {
    const seenIds = new Set()
    const seenCats = new Set()
    const tagPool = new Set(Array.isArray(data.tags) ? data.tags : [])
    const validSites = []

    for (const site of Array.isArray(data.sites) ? data.sites : []) {
      if (seenIds.has(site.id)) {
        console.warn(`[sites.json] 重复的站点 id：${site.id}，仅保留第一个`)
        continue
      }
      seenIds.add(site.id)

      const normalized = { ...site, tags: [] }
      for (const t of Array.isArray(site.tags) ? site.tags : []) {
        if (tagPool.has(t)) {
          normalized.tags.push(t)
        } else {
          console.warn(`[sites.json] 站点 ${site.id} 含未知标签「${t}」，已忽略`)
        }
      }
      validSites.push(normalized)
    }

    const validCategories = []
    for (const cat of Array.isArray(data.categories) ? data.categories : []) {
      if (seenCats.has(cat.id)) {
        console.warn(`[sites.json] 重复的分类 id：${cat.id}`)
        continue
      }
      seenCats.add(cat.id)
      validCategories.push(cat)
    }

    const catIds = new Set(validCategories.map((c) => c.id))
    let hasUncategorized = false
    for (const site of validSites) {
      if (!catIds.has(site.category)) {
        console.warn(`[sites.json] 站点 ${site.id} 引用不存在的分类「${site.category}」，归入未分类`)
        site.category = '__uncategorized'
        hasUncategorized = true
      }
    }

    categories.value = hasUncategorized
      ? [...validCategories, { id: '__uncategorized', name: '未分类' }]
      : validCategories
    sites.value = validSites
    tags.value = [...tagPool]
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

  function isPinnedSite(site) {
    return isPinned(site.id)
  }

  function defaultPinnedIds() {
    return sites.value.filter((s) => s.pinned === true).map((s) => s.id)
  }

  const filteredSites = computed(() => {
    const q = deferredQuery.value.toLowerCase()
    const tag = activeTag.value
    return sites.value.filter((site) => {
      if (tag && !site.tags.includes(tag)) return false
      if (!q) return true
      const name = (site.name || '').toLowerCase()
      const desc = (site.desc || '').toLowerCase()
      const siteTags = (site.tags || []).join(' ').toLowerCase()
      return name.includes(q) || desc.includes(q) || siteTags.includes(q)
    })
  })

  const pinnedSites = computed(() => filteredSites.value.filter(isPinnedSite))

  const visibleSites = computed(() => filteredSites.value.filter((s) => !isPinnedSite(s)))

  const categoryCounts = computed(() => {
    const counts = {}
    for (const cat of categories.value) {
      counts[cat.id] = visibleSites.value.filter((s) => s.category === cat.id).length
    }
    return counts
  })

  const displayGroups = computed(() => {
    const groups = categories.value
      .map((cat) => ({
        ...cat,
        sites: visibleSites.value.filter((s) => s.category === cat.id)
      }))
      .filter((g) => g.sites.length > 0)

    if (activeCategory.value === 'all') return groups
    if (activeCategory.value === 'pinned') return []
    return groups.filter((g) => g.id === activeCategory.value)
  })

  const showPinnedView = computed(
    () => activeCategory.value === 'pinned' && pinnedSites.value.length > 0
  )

  const hasResults = computed(
    () => showPinnedView.value || displayGroups.value.length > 0
  )

  return {
    categories,
    sites,
    tags,
    loadError,
    searchQuery,
    activeTag,
    activeCategory,
    filteredSites,
    pinnedSites,
    categoryCounts,
    displayGroups,
    showPinnedView,
    hasResults,
    load,
    setQuery,
    setTag,
    setCategory,
    resetFilters,
    defaultPinnedIds
  }
}