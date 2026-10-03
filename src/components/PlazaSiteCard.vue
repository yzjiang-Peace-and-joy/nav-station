<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  site: { type: Object, required: true },
  index: { type: Number, default: 0 },
  busy: { type: Boolean, default: false }
})

const emit = defineEmits(['add', 'edit', 'archive', 'restore'])

const faviconError = ref(false)
const menuOpen = ref(false)

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
const isArchived = computed(() => props.site.status === 'archived')
const isAdded = computed(() => Boolean(props.site.added))

function onAdd() {
  if (isAdded.value || isArchived.value || props.busy) return
  emit('add', props.site.id)
}

function onEdit() {
  menuOpen.value = false
  emit('edit', props.site)
}

function onArchiveToggle() {
  menuOpen.value = false
  if (isArchived.value) emit('restore', props.site.id)
  else emit('archive', props.site.id)
}
</script>

<template>
  <article
    class="site-card plaza-site-card"
    :class="{ 'is-archived': isArchived }"
    :style="staggerStyle"
    :aria-describedby="site.detail ? `plaza-tip-${site.id}` : undefined"
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
        <span v-if="isArchived" class="plaza-status-badge">已下架</span>
      </div>
      <p class="site-desc">{{ site.desc }}</p>
    </a>
    <div
      v-if="site.detail"
      :id="`plaza-tip-${site.id}`"
      class="site-tooltip"
      role="tooltip"
    >
      {{ site.detail }}
    </div>

    <div class="plaza-card-actions">
      <button
        type="button"
        class="plaza-add-btn"
        :class="{ added: isAdded }"
        :disabled="isAdded || isArchived || busy"
        :aria-label="isAdded ? `${site.name} 已添加` : `添加 ${site.name} 到我的目录`"
        @click="onAdd"
      >
        {{ isAdded ? '已添加' : '添加' }}
      </button>

      <div class="plaza-menu">
        <button
          type="button"
          class="plaza-menu-btn"
          aria-label="更多操作"
          :aria-expanded="menuOpen"
          @click="menuOpen = !menuOpen"
        >
          <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <circle cx="12" cy="5" r="1.6" />
            <circle cx="12" cy="12" r="1.6" />
            <circle cx="12" cy="19" r="1.6" />
          </svg>
        </button>
        <div v-if="menuOpen" class="plaza-menu-panel" role="menu">
          <button type="button" role="menuitem" @click="onEdit">编辑</button>
          <button type="button" role="menuitem" @click="onArchiveToggle">
            {{ isArchived ? '恢复' : '下架' }}
          </button>
        </div>
      </div>
    </div>
  </article>
</template>
