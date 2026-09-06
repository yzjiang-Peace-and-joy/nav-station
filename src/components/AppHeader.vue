<script setup>
import { computed } from 'vue'
import UserMenu from './UserMenu.vue'

const props = defineProps({
  query: { type: String, default: '' },
  theme: { type: String, default: 'light' },
  username: { type: String, default: '' },
  otherAccounts: { type: Array, default: () => [] },
  viewMode: { type: String, default: 'mine' },
  includeArchived: { type: Boolean, default: false }
})

const emit = defineEmits([
  'update:query',
  'toggle-theme',
  'toggle-menu',
  'logout',
  'switch-account',
  'update:viewMode',
  'create-plaza',
  'update:includeArchived'
])

const themeLabel = computed(() => (props.theme === 'dark' ? '切换到浅色模式' : '切换到深色模式'))
const searchPlaceholder = computed(() =>
  props.viewMode === 'plaza' ? '搜索广场站点、描述或标签…' : '搜索站点、描述或标签…'
)

function onInput(event) {
  emit('update:query', event.target.value)
}
</script>

<template>
  <header class="app-header">
    <div class="app-header-inner">
      <button
        type="button"
        class="menu-toggle"
        aria-label="打开分类导航"
        @click="emit('toggle-menu')"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <path d="M4 7h16M4 12h16M4 17h16" />
        </svg>
      </button>

      <div class="view-switch" role="tablist" aria-label="视图切换">
        <button
          type="button"
          role="tab"
          class="view-switch-btn"
          :class="{ active: viewMode === 'mine' }"
          :aria-selected="viewMode === 'mine'"
          @click="emit('update:viewMode', 'mine')"
        >
          我的
        </button>
        <button
          type="button"
          role="tab"
          class="view-switch-btn"
          :class="{ active: viewMode === 'plaza' }"
          :aria-selected="viewMode === 'plaza'"
          @click="emit('update:viewMode', 'plaza')"
        >
          广场
        </button>
      </div>

      <div class="header-search">
        <div class="search-box">
          <svg
            class="search-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            aria-hidden="true"
          >
            <circle cx="11" cy="11" r="7" />
            <path d="M21 21l-4.3-4.3" />
          </svg>
          <input
            class="search-input"
            type="search"
            :value="query"
            :placeholder="searchPlaceholder"
            aria-label="搜索站点"
            autocomplete="off"
            @input="onInput"
          />
        </div>
      </div>
      <div class="header-actions">
        <template v-if="viewMode === 'plaza'">
          <label class="archive-toggle">
            <input
              type="checkbox"
              :checked="includeArchived"
              @change="emit('update:includeArchived', $event.target.checked)"
            />
            <span>显示已下架</span>
          </label>
          <button type="button" class="header-text-btn" @click="emit('create-plaza')">
            提交网站
          </button>
        </template>
        <UserMenu
          v-if="username"
          :username="username"
          :other-accounts="otherAccounts"
          @logout="emit('logout')"
          @switch-account="emit('switch-account', $event)"
        />
        <button
          type="button"
          class="theme-toggle"
          :aria-label="themeLabel"
          @click="emit('toggle-theme')"
        >
          <svg
            v-if="theme === 'dark'"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="4.5" />
            <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
          </svg>
          <svg
            v-else
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>
