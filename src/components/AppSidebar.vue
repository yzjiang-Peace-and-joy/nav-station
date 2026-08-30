<script setup>
import { ref, computed, nextTick } from 'vue'
import TagFilter from './TagFilter.vue'

const props = defineProps({
  categories: { type: Array, default: () => [] },
  activeCategory: { type: String, default: 'all' },
  categoryCounts: { type: Object, default: () => ({}) },
  pinnedCount: { type: Number, default: 0 },
  tags: { type: Array, default: () => [] },
  activeTag: { type: String, default: null },
  open: { type: Boolean, default: false }
})

const emit = defineEmits(['update:activeCategory', 'update:activeTag', 'close'])

const tagsExpanded = ref(true)
const tagSearchOpen = ref(false)
const tagSearchQuery = ref('')
const tagSearchInput = ref(null)

const filteredTags = computed(() => {
  const q = tagSearchQuery.value.trim().toLowerCase()
  if (!q) return props.tags
  return props.tags.filter((t) => t.toLowerCase().includes(q))
})

function selectCategory(id) {
  emit('update:activeCategory', id)
  emit('close')
}

function toggleTagsSection() {
  tagsExpanded.value = !tagsExpanded.value
  if (!tagsExpanded.value) {
    closeTagSearch()
  }
}

async function openTagSearch() {
  tagsExpanded.value = true
  tagSearchOpen.value = true
  await nextTick()
  tagSearchInput.value?.focus()
}

function closeTagSearch() {
  tagSearchOpen.value = false
  tagSearchQuery.value = ''
}

function onTagSearchKeydown(event) {
  if (event.key === 'Escape') {
    closeTagSearch()
  }
}
</script>

<template>
  <aside class="app-sidebar" :class="{ 'is-open': open }" aria-label="分类导航">
    <h1 class="sidebar-brand">导航站</h1>

    <div class="sidebar-body">
      <div class="sidebar-section sidebar-section--nav">
        <p class="sidebar-section-label">分类</p>
        <nav class="sidebar-nav" aria-label="站点分类">
          <button
            type="button"
            class="sidebar-item"
            :class="{ active: activeCategory === 'all' }"
            :aria-current="activeCategory === 'all' ? 'page' : undefined"
            @click="selectCategory('all')"
          >
            <span class="sidebar-item-label">全部</span>
          </button>

          <button
            v-if="pinnedCount > 0"
            type="button"
            class="sidebar-item"
            :class="{ active: activeCategory === 'pinned' }"
            :aria-current="activeCategory === 'pinned' ? 'page' : undefined"
            @click="selectCategory('pinned')"
          >
            <svg class="sidebar-item-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
            </svg>
            <span class="sidebar-item-label">置顶收藏</span>
            <span class="sidebar-item-count">{{ pinnedCount }}</span>
          </button>

          <button
            v-for="cat in categories"
            :key="cat.id"
            type="button"
            class="sidebar-item"
            :class="{
              active: activeCategory === cat.id,
              disabled: !categoryCounts[cat.id]
            }"
            :aria-current="activeCategory === cat.id ? 'page' : undefined"
            :disabled="!categoryCounts[cat.id] && activeCategory !== cat.id"
            @click="selectCategory(cat.id)"
          >
            <span class="sidebar-item-label">{{ cat.name }}</span>
            <span v-if="categoryCounts[cat.id]" class="sidebar-item-count">{{ categoryCounts[cat.id] }}</span>
          </button>
        </nav>
      </div>

      <div
        class="sidebar-section sidebar-section--tags"
        :class="{ 'is-collapsed': !tagsExpanded }"
      >
        <div class="sidebar-tags-header" :class="{ 'is-searching': tagSearchOpen }">
          <button
            type="button"
            class="sidebar-tags-toggle"
            :aria-expanded="tagsExpanded"
            @click="toggleTagsSection"
          >
            <svg
              class="sidebar-chevron"
              :class="{ 'is-collapsed': !tagsExpanded }"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              aria-hidden="true"
            >
              <path d="M6 9l6 6 6-6" />
            </svg>
            <span>标签筛选</span>
          </button>

          <div class="sidebar-tags-search">
            <input
              v-if="tagSearchOpen"
              ref="tagSearchInput"
              v-model="tagSearchQuery"
              type="search"
              class="tag-search-input"
              placeholder="搜索标签…"
              aria-label="搜索标签"
              @keydown="onTagSearchKeydown"
            />
            <button
              v-else
              type="button"
              class="tag-search-btn"
              aria-label="搜索标签"
              @click.stop="openTagSearch"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
                <circle cx="11" cy="11" r="7" />
                <path d="M21 21l-4.3-4.3" />
              </svg>
            </button>
          </div>
        </div>

        <div v-show="tagsExpanded" class="sidebar-tags-panel">
          <TagFilter
            v-if="filteredTags.length"
            layout="vertical"
            :tags="filteredTags"
            :active-tag="activeTag"
            @update:activeTag="emit('update:activeTag', $event)"
          />
          <p v-else class="tag-search-empty">无匹配标签</p>
        </div>
      </div>
    </div>
  </aside>
</template>
