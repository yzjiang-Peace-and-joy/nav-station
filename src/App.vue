<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import CategorySection from './components/CategorySection.vue'
import SiteCard from './components/SiteCard.vue'
import PlazaSiteCard from './components/PlazaSiteCard.vue'
import PlazaSiteForm from './components/PlazaSiteForm.vue'
import LoginView from './components/LoginView.vue'
import { useTheme } from './composables/useTheme.js'
import { usePinned } from './composables/usePinned.js'
import { useSites } from './composables/useSites.js'
import { usePlaza } from './composables/usePlaza.js'
import { useAuth } from './composables/useAuth.js'

const { theme: themeName, init: initTheme, toggle: toggleTheme } = useTheme()
const pinned = usePinned()
const {
  isAuthenticated,
  username,
  otherAccounts,
  init: initAuth,
  login,
  logout,
  switchAccount
} = useAuth()

const {
  categories,
  tags,
  sites,
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
  defaultPinnedIds,
  syncFromPlaza
} = useSites({ isPinned: pinned.isPinned })

const {
  categories: plazaCategories,
  tags: plazaTags,
  loadError: plazaLoadError,
  searchQuery: plazaSearchQuery,
  activeTag: plazaActiveTag,
  activeCategory: plazaActiveCategory,
  includeArchived,
  busy: plazaBusy,
  categoryCounts: plazaCategoryCounts,
  displayGroups: plazaDisplayGroups,
  hasResults: plazaHasResults,
  load: loadPlaza,
  setQuery: setPlazaQuery,
  setTag: setPlazaTag,
  setCategory: setPlazaCategory,
  resetFilters: resetPlazaFilters,
  setIncludeArchived,
  create: createPlaza,
  update: updatePlaza,
  archive: archivePlaza,
  restore: restorePlaza,
  addToNav
} = usePlaza()

const entered = ref(false)
const sidebarOpen = ref(false)
const loginViewRef = ref(null)
const viewMode = ref('mine')
const formOpen = ref(false)
const formMode = ref('create')
const editingSite = ref(null)
const formRef = ref(null)
const toast = ref('')
const syncingId = ref(null)
let toastTimer = null

const isPlaza = computed(() => viewMode.value === 'plaza')

const headerQuery = computed(() => (isPlaza.value ? plazaSearchQuery.value : searchQuery.value))
const sidebarCategories = computed(() => (isPlaza.value ? plazaCategories.value : categories.value))
const sidebarTags = computed(() => (isPlaza.value ? plazaTags.value : tags.value))
const sidebarActiveTag = computed(() => (isPlaza.value ? plazaActiveTag.value : activeTag.value))
const sidebarActiveCategory = computed(() =>
  isPlaza.value ? plazaActiveCategory.value : activeCategory.value
)
const sidebarCounts = computed(() =>
  isPlaza.value ? plazaCategoryCounts.value : categoryCounts.value
)
const currentLoadError = computed(() => (isPlaza.value ? plazaLoadError.value : loadError.value))
const mineIsEmpty = computed(
  () => !loadError.value && sites.value.length === 0 && !searchQuery.value && !activeTag.value
)

onMounted(async () => {
  initTheme()
  await initAuth()
  if (isAuthenticated.value) {
    await initUserData()
  }
  await nextTick()
  setTimeout(() => {
    entered.value = true
  }, 600)
})

watch(viewMode, async (mode) => {
  sidebarOpen.value = false
  if (mode === 'plaza') {
    resetPlazaFilters()
    await loadPlaza()
  } else {
    resetFilters()
  }
})

async function initUserData() {
  viewMode.value = 'mine'
  await loadSites()
  await pinned.init(username.value, defaultPinnedIds())
  resetFilters()
}

async function handleLogin({ username: name, password }) {
  const result = await login(name, password)
  if (!result.ok) {
    loginViewRef.value?.setError(result.message)
    return
  }
  await initUserData()
}

function handleLogout() {
  logout()
  resetFilters()
  resetPlazaFilters()
  viewMode.value = 'mine'
}

async function handleSwitchAccount({ username: name, password, onError, onSuccess }) {
  const result = await switchAccount(name, password)
  if (!result.ok) {
    onError?.(result.message)
    return
  }
  await initUserData()
  onSuccess?.()
}

function togglePin(id) {
  pinned.toggle(id)
}

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function closeSidebar() {
  sidebarOpen.value = false
}

function onUpdateQuery(val) {
  if (isPlaza.value) setPlazaQuery(val)
  else setQuery(val)
}

function onSetCategory(id) {
  if (isPlaza.value) setPlazaCategory(id)
  else setCategory(id)
}

function onSetTag(tag) {
  if (isPlaza.value) setPlazaTag(tag)
  else setTag(tag)
}

function showToast(message) {
  toast.value = message
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toast.value = ''
  }, 2200)
}

function openCreateForm() {
  formMode.value = 'create'
  editingSite.value = null
  formOpen.value = true
}

function openEditForm(site) {
  formMode.value = 'edit'
  editingSite.value = site
  formOpen.value = true
}

function closeForm() {
  formOpen.value = false
  editingSite.value = null
}

async function handleFormSubmit(payload) {
  const result =
    formMode.value === 'edit' && editingSite.value
      ? await updatePlaza(editingSite.value.id, payload)
      : await createPlaza(payload)
  if (!result.ok) {
    formRef.value?.setError(result.message)
    return
  }
  closeForm()
  showToast(formMode.value === 'edit' ? '已保存' : '已提交到广场')
}

async function handleAddToNav(slug) {
  const result = await addToNav(slug)
  if (!result.ok) {
    showToast(result.message)
    return
  }
  await loadSites()
  showToast('已添加到我的目录')
}

async function handleArchive(slug) {
  const result = await archivePlaza(slug)
  showToast(result.ok ? '已下架' : result.message)
}

async function handleRestore(slug) {
  const result = await restorePlaza(slug)
  showToast(result.ok ? '已恢复' : result.message)
}

async function handleSyncFromPlaza(siteId) {
  syncingId.value = siteId
  const result = await syncFromPlaza(siteId)
  syncingId.value = null
  showToast(result.ok ? '已从广场同步' : result.message)
}

function goPlaza() {
  viewMode.value = 'plaza'
}

function clearCurrentFilters() {
  if (isPlaza.value) resetPlazaFilters()
  else resetFilters()
}
</script>

<template>
  <LoginView
    v-if="!isAuthenticated"
    ref="loginViewRef"
    :theme="themeName"
    @login="handleLogin"
    @toggle-theme="toggleTheme"
  />

  <div v-else class="app" :class="{ 'anim-enter': !entered }">
    <AppHeader
      :query="headerQuery"
      :theme="themeName"
      :username="username"
      :other-accounts="otherAccounts"
      :view-mode="viewMode"
      :include-archived="includeArchived"
      @update:query="onUpdateQuery"
      @update:view-mode="viewMode = $event"
      @update:include-archived="setIncludeArchived"
      @create-plaza="openCreateForm"
      @toggle-theme="toggleTheme"
      @toggle-menu="toggleSidebar"
      @logout="handleLogout"
      @switch-account="handleSwitchAccount"
    />

    <div class="app-body">
      <div
        class="sidebar-backdrop"
        :class="{ 'is-visible': sidebarOpen }"
        aria-hidden="true"
        @click="closeSidebar"
      />

      <AppSidebar
        :categories="sidebarCategories"
        :active-category="sidebarActiveCategory"
        :category-counts="sidebarCounts"
        :pinned-count="isPlaza ? 0 : pinnedSites.length"
        :tags="sidebarTags"
        :active-tag="sidebarActiveTag"
        :open="sidebarOpen"
        :show-pinned="!isPlaza"
        :brand-title="isPlaza ? '广场' : '导航站'"
        @update:active-category="onSetCategory"
        @update:active-tag="onSetTag"
        @close="closeSidebar"
      />

      <main class="app-main">
        <template v-if="currentLoadError">
          <div class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
              <path d="M3 7h18M4 7v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7M8 3l-2 4M16 3l2 4" />
            </svg>
            <p>{{ isPlaza ? '广场加载失败，请稍后重试' : '数据加载失败，请检查站点数据后重试' }}</p>
          </div>
        </template>

        <template v-else-if="isPlaza">
          <template v-if="plazaHasResults">
            <CategorySection
              v-for="group in plazaDisplayGroups"
              :key="group.id"
              :title="group.name"
              :sites="group.sites"
            >
              <PlazaSiteCard
                v-for="(site, index) in group.sites"
                :key="site.id"
                :site="site"
                :index="index"
                :busy="plazaBusy"
                @add="handleAddToNav"
                @edit="openEditForm"
                @archive="handleArchive"
                @restore="handleRestore"
              />
            </CategorySection>
          </template>
          <div v-else class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
              <circle cx="11" cy="11" r="7" />
              <path d="M21 21l-4.3-4.3M8 11h6" />
            </svg>
            <p>
              <template v-if="plazaSearchQuery">没有找到与「{{ plazaSearchQuery }}」相关的广场网站</template>
              <template v-else-if="plazaActiveTag">没有找到标签「{{ plazaActiveTag }}」下的广场网站</template>
              <template v-else>广场暂无站点，点击右上角「提交网站」添加</template>
            </p>
            <button
              v-if="plazaSearchQuery || plazaActiveTag"
              type="button"
              class="empty-clear-btn"
              @click="clearCurrentFilters"
            >
              清除搜索
            </button>
            <button
              v-else
              type="button"
              class="empty-clear-btn"
              @click="openCreateForm"
            >
              提交网站
            </button>
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
              :syncing="syncingId === site.id"
              @toggle-pin="togglePin"
              @sync-from-plaza="handleSyncFromPlaza"
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
              :syncing="syncingId === site.id"
              @toggle-pin="togglePin"
              @sync-from-plaza="handleSyncFromPlaza"
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
            <template v-else-if="mineIsEmpty">你的目录还是空的，去广场挑一些实用网站吧</template>
            <template v-else>没有找到匹配的网站</template>
          </p>
          <button
            v-if="searchQuery || activeTag"
            type="button"
            class="empty-clear-btn"
            @click="clearCurrentFilters"
          >
            清除搜索
          </button>
          <button
            v-else-if="mineIsEmpty"
            type="button"
            class="empty-clear-btn"
            @click="goPlaza"
          >
            前往广场
          </button>
        </div>
      </main>
    </div>

    <PlazaSiteForm
      ref="formRef"
      :open="formOpen"
      :mode="formMode"
      :site="editingSite"
      :categories="plazaCategories"
      :busy="plazaBusy"
      @close="closeForm"
      @submit="handleFormSubmit"
    />

    <div v-if="toast" class="app-toast" role="status">{{ toast }}</div>
  </div>
</template>
