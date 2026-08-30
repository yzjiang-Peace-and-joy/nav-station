<script setup>
import { ref } from 'vue'

const props = defineProps({
  theme: { type: String, default: 'light' }
})

const emit = defineEmits(['login', 'toggle-theme'])

const username = ref('yzjiang')
const password = ref('')
const error = ref('')
const loading = ref(false)

const accounts = ['yzjiang', 'test']

function onSubmit() {
  error.value = ''
  if (!username.value.trim()) {
    error.value = '请输入用户名'
    return
  }
  if (!password.value) {
    error.value = '请输入密码'
    return
  }
  loading.value = true
  emit('login', { username: username.value.trim(), password: password.value })
  loading.value = false
}

function selectAccount(name) {
  username.value = name
  error.value = ''
}

defineExpose({ setError: (msg) => { error.value = msg } })
</script>

<template>
  <div class="login-page">
    <button
      type="button"
      class="login-theme-toggle"
      :aria-label="theme === 'dark' ? '切换到浅色模式' : '切换到深色模式'"
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

    <div class="login-card">
      <h1 class="login-title">导航站</h1>
      <p class="login-subtitle">登录以访问你的站点收藏</p>

      <div class="login-accounts">
        <button
          v-for="name in accounts"
          :key="name"
          type="button"
          class="login-account-chip"
          :class="{ 'is-active': username === name }"
          @click="selectAccount(name)"
        >
          {{ name }}
        </button>
      </div>

      <form class="login-form" @submit.prevent="onSubmit">
        <label class="login-field">
          <span class="login-label">用户名</span>
          <input
            v-model="username"
            class="login-input"
            type="text"
            autocomplete="username"
            placeholder="请输入用户名"
          />
        </label>
        <label class="login-field">
          <span class="login-label">密码</span>
          <input
            v-model="password"
            class="login-input"
            type="password"
            autocomplete="current-password"
            placeholder="请输入密码"
          />
        </label>
        <p v-if="error" class="login-error" role="alert">{{ error }}</p>
        <button type="submit" class="login-submit" :disabled="loading">
          登录
        </button>
      </form>
    </div>
  </div>
</template>
