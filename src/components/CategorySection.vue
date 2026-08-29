<script setup>
defineProps({
  title: { type: String, required: true },
  sites: { type: Array, required: true }
})
</script>

<template>
  <section class="section">
    <div class="section-header">
      <slot name="leading" />
      <h2 class="section-title">{{ title }}</h2>
      <span class="section-count">{{ sites.length }}</span>
    </div>
    <div class="section-divider" role="separator" />
    <div class="sites-grid">
      <slot />
    </div>
  </section>
</template>