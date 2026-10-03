<script setup>
defineProps({
  size: { type: Number, default: 28 }
})
</script>

<template>
  <span class="brand-mark" :style="{ '--brand-mark-size': `${size}px` }" aria-hidden="true">
    <svg viewBox="0 0 32 32" fill="none">
      <rect width="32" height="32" rx="8" fill="currentColor" class="brand-mark-bg" />
      <path
        d="M9 20l5-8 3 4 2-3 4 7H9z"
        fill="var(--bg-secondary)"
        opacity="0.95"
      />
    </svg>
  </span>
</template>
