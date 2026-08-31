import { ref, computed } from 'vue'
import { apiFetch } from '../api/client.js'

const SEARCH_DEBOUNCE = 150
export function useSites({ isPinned }) {
  const categories = ref([]), sites = ref([]), tags = ref([]), loadError = ref(false)
  const searchQuery = ref(''), deferredQuery = ref(''), activeTag = ref(null), activeCategory = ref('all')
  let debounceTimer = null
  async function load() {
    loadError.value = false; categories.value = []; sites.value = []; tags.value = []; resetFilters()
    try { validateAndNormalize(await apiFetch('/nav')) } catch (err) { console.error('[nav_station] 数据加载失败：', err); loadError.value = true }
  }
  function validateAndNormalize(data) {
    const validTags = new Set(Array.isArray(data.tags) ? data.tags : []), seenIds = new Set(), seenCats = new Set()
    const validSites = (Array.isArray(data.sites) ? data.sites : []).filter((site) => { if (seenIds.has(site.id)) return false; seenIds.add(site.id); site.tags = (site.tags || []).filter((tag) => validTags.has(tag)); return true })
    const validCategories = (Array.isArray(data.categories) ? data.categories : []).filter((cat) => { if (seenCats.has(cat.id)) return false; seenCats.add(cat.id); return true })
    const catIds = new Set(validCategories.map((c) => c.id)); let missing = false
    validSites.forEach((site) => { if (!catIds.has(site.category)) { site.category = '__uncategorized'; missing = true } })
    categories.value = missing ? [...validCategories, { id: '__uncategorized', name: '未分类' }] : validCategories
    sites.value = validSites; tags.value = [...validTags]
  }
  function setQuery(val) { searchQuery.value = val; clearTimeout(debounceTimer); debounceTimer = setTimeout(() => { deferredQuery.value = val.trim() }, SEARCH_DEBOUNCE) }
  function setTag(tag) { activeTag.value = activeTag.value === tag ? null : tag }
  function setCategory(id) { activeCategory.value = id }
  function resetFilters() { clearTimeout(debounceTimer); searchQuery.value = ''; deferredQuery.value = ''; activeTag.value = null; activeCategory.value = 'all' }
  function defaultPinnedIds() { return sites.value.filter((s) => s.pinned === true).map((s) => s.id) }
  const filteredSites = computed(() => { const q = deferredQuery.value.toLowerCase(); const tag = activeTag.value; return sites.value.filter((s) => (!tag || s.tags.includes(tag)) && (!q || [s.name, s.desc, s.tags.join(' ')].some((v) => (v || '').toLowerCase().includes(q)))) })
  const pinnedSites = computed(() => filteredSites.value.filter(isPinned)), visibleSites = computed(() => filteredSites.value.filter((s) => !isPinned(s)))
  const categoryCounts = computed(() => Object.fromEntries(categories.value.map((c) => [c.id, visibleSites.value.filter((s) => s.category === c.id).length])))
  const displayGroups = computed(() => { const groups = categories.value.map((c) => ({ ...c, sites: visibleSites.value.filter((s) => s.category === c.id) })).filter((g) => g.sites.length); if (activeCategory.value === 'all' || activeCategory.value === 'pinned') return activeCategory.value === 'all' ? groups : []; return groups.filter((g) => g.id === activeCategory.value) })
  const showPinnedView = computed(() => activeCategory.value === 'pinned' && pinnedSites.value.length > 0), hasResults = computed(() => showPinnedView.value || displayGroups.value.length > 0)
  return { categories, sites, tags, loadError, searchQuery, activeTag, activeCategory, filteredSites, pinnedSites, categoryCounts, displayGroups, showPinnedView, hasResults, load, setQuery, setTag, setCategory, resetFilters, defaultPinnedIds }
}
