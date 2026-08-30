<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  username: { type: String, required: true },
  otherAccounts: { type: Array, default: () => [] }
})

const emit = defineEmits(['logout', 'switch-account'])

const open = ref(false)
const switchingTo = ref(null)
const switchPassword = ref('')
const switchError = ref('')
const menuRef = ref(null)
const dropdownRef = ref(null)
const dropdownStyle = ref({})

function updateDropdownPosition() {
  const trigger = menuRef.value?.querySelector('.user-menu-trigger')
  if (!trigger) return
  const rect = trigger.getBoundingClientRect()
  dropdownStyle.value = {
    top: `${rect.bottom + 6}px`,
    right: `${window.innerWidth - rect.right}px`
  }
}

function toggle() {
  open.value = !open.value
  if (!open.value) resetSwitch()
}

function close() {
  open.value = false
  resetSwitch()
}

function resetSwitch() {
  switchingTo.value = null
  switchPassword.value = ''
  switchError.value = ''
}

function startSwitch(name) {
  switchingTo.value = name
  switchPassword.value = ''
  switchError.value = ''
}

function confirmSwitch() {
  if (!switchingTo.value) return
  emit('switch-account', {
    username: switchingTo.value,
    password: switchPassword.value,
    onError: (msg) => { switchError.value = msg },
    onSuccess: () => { close() }
  })
}

function onLogout() {
  close()
  emit('logout')
}

function onClickOutside(event) {
  const target = event.target
  if (menuRef.value?.contains(target)) return
  if (dropdownRef.value?.contains(target)) return
  close()
}

function onKeydown(event) {
  if (event.key === 'Escape') close()
}

watch(open, async (isOpen) => {
  if (isOpen) {
    await nextTick()
    updateDropdownPosition()
    document.addEventListener('click', onClickOutside)
    window.addEventListener('resize', updateDropdownPosition)
    window.addEventListener('scroll', updateDropdownPosition, true)
  } else {
    document.removeEventListener('click', onClickOutside)
    window.removeEventListener('resize', updateDropdownPosition)
    window.removeEventListener('scroll', updateDropdownPosition, true)
  }
})

onMounted(() => {
  document.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', onClickOutside)
  window.removeEventListener('resize', updateDropdownPosition)
  window.removeEventListener('scroll', updateDropdownPosition, true)
  document.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div ref="menuRef" class="user-menu">
    <button
      type="button"
      class="user-menu-trigger"
      :aria-expanded="open"
      aria-haspopup="true"
      @click.stop="toggle"
    >
      <span class="user-avatar">{{ username.charAt(0).toUpperCase() }}</span>
      <span class="user-name">{{ username }}</span>
      <svg
        class="user-chevron"
        :class="{ 'is-open': open }"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        aria-hidden="true"
      >
        <path d="M6 9l6 6 6-6" />
      </svg>
    </button>

    <Teleport to="body">
      <div
        v-if="open"
        ref="dropdownRef"
        class="user-menu-dropdown"
        :style="dropdownStyle"
        role="menu"
        @click.stop
      >
        <div class="user-menu-header">
          <span class="user-menu-label">当前账号</span>
          <span class="user-menu-current">{{ username }}</span>
        </div>

        <template v-if="switchingTo">
          <div class="user-menu-switch-form">
            <p class="user-menu-switch-hint">切换到 <strong>{{ switchingTo }}</strong></p>
            <input
              v-model="switchPassword"
              class="user-menu-switch-input"
              type="password"
              placeholder="输入密码"
              autocomplete="current-password"
              @keydown.enter="confirmSwitch"
            />
            <p v-if="switchError" class="user-menu-error" role="alert">{{ switchError }}</p>
            <div class="user-menu-switch-actions">
              <button type="button" class="user-menu-btn user-menu-btn--ghost" @click.stop="resetSwitch">
                取消
              </button>
              <button type="button" class="user-menu-btn user-menu-btn--primary" @click.stop="confirmSwitch">
                确认
              </button>
            </div>
          </div>
        </template>

        <template v-else>
          <button
            v-for="name in otherAccounts"
            :key="name"
            type="button"
            class="user-menu-item"
            role="menuitem"
            @click.stop="startSwitch(name)"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
              <path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l6 6M4 4l5 5" />
            </svg>
            切换到 {{ name }}
          </button>
          <div class="user-menu-divider" />
          <button type="button" class="user-menu-item user-menu-item--danger" role="menuitem" @click.stop="onLogout">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9" />
            </svg>
            退出登录
          </button>
        </template>
      </div>
    </Teleport>
  </div>
</template>
