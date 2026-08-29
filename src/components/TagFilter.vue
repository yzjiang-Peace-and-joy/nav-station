<script setup>
defineProps({
  tags: { type: Array, default: () => [] },
  activeTag: { type: String, default: null }
})

const emit = defineEmits(['update:activeTag'])

function onSelect(tag) {
  emit('update:activeTag', tag)
}
</script>

<template>
  <nav class="tag-bar" aria-label="标签筛选">
    <div class="tag-bar-inner">
      <button
        v-for="tag in tags"
        :key="tag"
        type="button"
        class="tag-chip"
        :class="{ active: activeTag === tag }"
        :aria-pressed="activeTag === tag"
        @click="onSelect(tag)"
      >
        {{ tag }}
      </button>
    </div>
  </nav>
</template>
