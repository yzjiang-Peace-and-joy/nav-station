<script setup>
defineProps({
  size: { type: [Number, String], default: 28 }
})
</script>

<template>
  <svg
    class="brand-mark"
    :width="size"
    :height="size"
    viewBox="0 0 32 32"
    aria-hidden="true"
    focusable="false"
  >
    <rect width="32" height="32" rx="8" />
    <path class="brand-mark-cutout" d="M9 20l5-8 3 4 2-3 4 7H9z" />
  </svg>
</template>
