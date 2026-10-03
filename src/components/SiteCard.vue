<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  site: { type: Object, required: true },
  isPinned: { type: Boolean, default: false },
  index: { type: Number, default: 0 },
  syncing: { type: Boolean, default: false }
})

const emit = defineEmits(['toggle-pin', 'sync-from-plaza'])

const faviconError = ref(false)

const domain = computed(() => {
  try {
    return new URL(props.site.url).hostname
  } catch {
    return props.site.id
  }
})

const faviconUrl = computed(
  () => `https://www.google.com/s2/favicons?domain=${domain.value}&sz=64`
)

const fallbackClass = computed(() => {
  let hash = 0
  for (const ch of props.site.id) hash = (hash * 31 + ch.charCodeAt(0)) >>> 0
  return `favicon-fallback--${hash % 6}`
})

const nameChar = computed(() => (props.site.name || '?').charAt(0).toUpperCase())
const staggerStyle = computed(() => ({ '--stagger-index': props.index }))
const canSync = computed(() => Boolean(props.site.source_plaza_id))

function onTogglePin() {
  emit('toggle-pin', props.site.id)
}

function onSync() {
  if (!canSync.value || props.syncing) return
  emit('sync-from-plaza', props.site.id)
}
</script>

<template>
  <article
    class="site-card"
    :style="staggerStyle"
    :aria-describedby="site.detail ? `tip-${site.id}` : undefined"
  >
    <a :href="site.url" target="_blank" rel="noopener noreferrer" class="site-card-link">
      <div class="site-card-top">
        <span class="site-favicon-wrap">
          <img
            v-if="!faviconError"
            :src="faviconUrl"
            :alt="`${site.name} 图标`"
            class="site-favicon"
            loading="lazy"
            @error="faviconError = true"
          />
          <span v-else class="site-favicon favicon-fallback" :class="fallbackClass">
            {{ nameChar }}
          </span>
        </span>
        <span class="site-name">{{ site.name }}</span>
      </div>
      <p class="site-desc">{{ site.desc }}</p>
    </a>
    <div
      v-if="site.detail"
      :id="`tip-${site.id}`"
      class="site-tooltip"
      role="tooltip"
    >
      {{ site.detail }}
    </div>
    <div class="site-card-actions">
      <button
        v-if="canSync"
        type="button"
        class="sync-btn"
        :disabled="syncing"
        :aria-label="`从广场同步 ${site.name}`"
        title="从广场同步"
        @click="onSync"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
          <path d="M21 12a9 9 0 0 0-15.5-6.4M3 4v5h5" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M3 12a9 9 0 0 0 15.5 6.4M21 20v-5h-5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </button>
      <button
        type="button"
        class="pin-btn"
        :class="{ pinned: isPinned }"
        :aria-pressed="isPinned"
        :aria-label="isPinned ? `取消置顶 ${site.name}` : `置顶 ${site.name}`"
        @click="onTogglePin"
      >
        <svg v-if="isPinned" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path
            d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
          />
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
          <path
            d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
          />
        </svg>
      </button>
    </div>
  </article>
</template>
