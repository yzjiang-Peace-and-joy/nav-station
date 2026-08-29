<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  site: { type: Object, required: true },
  isPinned: { type: Boolean, default: false },
  index: { type: Number, default: 0 }
})

const emit = defineEmits(['toggle-pin'])

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

function onTogglePin() {
  emit('toggle-pin', props.site.id)
}
</script>

<template>
  <article class="site-card" :style="staggerStyle">
    <a :href="site.url" target="_blank" rel="noopener noreferrer" class="site-card-link">
      <div class="site-card-top">
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
        <span class="site-name">{{ site.name }}</span>
      </div>
      <p class="site-desc">{{ site.desc }}</p>
    </a>
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
  </article>
</template>
