<script setup>
import { ref, onMounted, nextTick } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import CategorySection from './components/CategorySection.vue'
import SiteCard from './components/SiteCard.vue'
import { useTheme } from './composables/useTheme.js'
import { usePinned } from './composables/usePinned.js'
import { useSites } from './composables/useSites.js'

const { theme: themeName, init: initTheme, toggle: toggleTheme } = useTheme()
const pinned = usePinned()

const {
  categories,
  tags,
  loadError,
  searchQuery,
  activeTag,
  activeCategory,
  pinnedSites,
  categoryCounts,
  displayGroups,
  showPinnedView,
  hasResults,
  load: loadSites,
  setQuery,
  setTag,
  setCategory,
  resetFilters,
  defaultPinnedIds
} = useSites({ isPinned: pinned.isPinned })

const entered = ref(false)
const sidebarOpen = ref(false)

onMounted(async () => {
  initTheme()
  await loadSites()
  pinned.init(defaultPinnedIds())
  await nextTick()
  setTimeout(() => {
    entered.value = true
  }, 600)
})

function togglePin(id) {
  pinned.toggle(id)
}

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function closeSidebar() {
  sidebarOpen.value = false
}
</script>

<template>
  <div class="app" :class="{ 'anim-enter': !entered }">
    <AppHeader
      :query="searchQuery"
      :theme="themeName"
      @update:query="setQuery"
      @toggle-theme="toggleTheme"
      @toggle-menu="toggleSidebar"
    />

    <div class="app-body">
      <div
        class="sidebar-backdrop"
        :class="{ 'is-visible': sidebarOpen }"
        aria-hidden="true"
        @click="closeSidebar"
      />

      <AppSidebar
        :categories="categories"
        :active-category="activeCategory"
        :category-counts="categoryCounts"
        :pinned-count="pinnedSites.length"
        :tags="tags"
        :active-tag="activeTag"
        :open="sidebarOpen"
        @update:active-category="setCategory"
        @update:active-tag="setTag"
        @close="closeSidebar"
      />

      <main class="app-main">
        <template v-if="loadError">
          <div class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
              <path d="M3 7h18M4 7v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7M8 3l-2 4M16 3l2 4" />
            </svg>
            <p>数据加载失败，请检查站点数据后重试</p>
          </div>
        </template>

        <template v-else-if="hasResults">
          <CategorySection
            v-if="showPinnedView"
            title="置顶收藏"
            :sites="pinnedSites"
          >
            <template #leading>
              <svg class="pinned-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
              </svg>
            </template>
            <SiteCard
              v-for="(site, index) in pinnedSites"
              :key="site.id"
              :site="site"
              :is-pinned="pinned.isPinned(site.id)"
              :index="index"
              @toggle-pin="togglePin"
            />
          </CategorySection>

          <CategorySection
            v-for="group in displayGroups"
            :key="group.id"
            :title="group.name"
            :sites="group.sites"
          >
            <SiteCard
              v-for="(site, index) in group.sites"
              :key="site.id"
              :site="site"
              :is-pinned="pinned.isPinned(site.id)"
              :index="index"
              @toggle-pin="togglePin"
            />
          </CategorySection>
        </template>

        <div v-else class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
            <circle cx="11" cy="11" r="7" />
            <path d="M21 21l-4.3-4.3M8 11h6" />
          </svg>
          <p>
            <template v-if="searchQuery">没有找到与「{{ searchQuery }}」相关的网站</template>
            <template v-else-if="activeTag">没有找到标签「{{ activeTag }}」下的网站</template>
            <template v-else>没有找到匹配的网站</template>
          </p>
          <button type="button" class="empty-clear-btn" @click="resetFilters">
            清除搜索
          </button>
        </div>
      </main>
    </div>
  </div>
</template>
