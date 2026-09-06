<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  mode: { type: String, default: 'create' },
  site: { type: Object, default: null },
  categories: { type: Array, default: () => [] },
  busy: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'submit'])

const name = ref('')
const url = ref('')
const desc = ref('')
const detail = ref('')
const category = ref('')
const tagsText = ref('')
const error = ref('')

const title = computed(() => (props.mode === 'edit' ? '编辑广场站点' : '提交到广场'))

watch(
  () => [props.open, props.site, props.mode],
  () => {
    if (!props.open) return
    error.value = ''
    if (props.mode === 'edit' && props.site) {
      name.value = props.site.name || ''
      url.value = props.site.url || ''
      desc.value = props.site.desc || ''
      detail.value = props.site.detail || ''
      category.value =
        props.site.category_name ||
        props.categories.find((c) => c.id === props.site.category)?.name ||
        props.site.category ||
        ''
      tagsText.value = (props.site.tags || []).join(', ')
    } else {
      name.value = ''
      url.value = ''
      desc.value = ''
      detail.value = ''
      category.value = ''
      tagsText.value = ''
    }
  },
  { immediate: true }
)

function onBackdropClick() {
  if (!props.busy) emit('close')
}

function parseTags(text) {
  return text
    .split(/[,，]/)
    .map((t) => t.trim())
    .filter(Boolean)
}

function onSubmit() {
  error.value = ''
  const payload = {
    name: name.value.trim(),
    url: url.value.trim(),
    desc: desc.value.trim(),
    detail: detail.value.trim(),
    category: category.value.trim() || null,
    tags: parseTags(tagsText.value)
  }
  if (!payload.name || !payload.url) {
    error.value = '请填写名称和网址'
    return
  }
  emit('submit', payload)
}

function setError(message) {
  error.value = message || ''
}

defineExpose({ setError })
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="modal-backdrop" @click.self="onBackdropClick">
      <div class="modal-panel" role="dialog" aria-modal="true" :aria-label="title">
        <div class="modal-header">
          <h2>{{ title }}</h2>
          <button type="button" class="modal-close" aria-label="关闭" :disabled="busy" @click="emit('close')">
            ×
          </button>
        </div>

        <form class="modal-form" @submit.prevent="onSubmit">
          <label class="form-field">
            <span>名称</span>
            <input v-model="name" type="text" required maxlength="200" autocomplete="off" />
          </label>
          <label class="form-field">
            <span>网址</span>
            <input v-model="url" type="url" required maxlength="1000" placeholder="https://" autocomplete="off" />
          </label>
          <label class="form-field">
            <span>简介</span>
            <input v-model="desc" type="text" maxlength="500" autocomplete="off" />
          </label>
          <label class="form-field">
            <span>详情</span>
            <textarea v-model="detail" rows="3" maxlength="4000" />
          </label>
          <label class="form-field">
            <span>分类</span>
            <input
              v-model="category"
              type="text"
              list="plaza-category-options"
              maxlength="200"
              placeholder="可选，不存在则自动创建"
              autocomplete="off"
            />
            <datalist id="plaza-category-options">
              <option v-for="cat in categories" :key="cat.id" :value="cat.name" />
            </datalist>
          </label>
          <label class="form-field">
            <span>标签</span>
            <input
              v-model="tagsText"
              type="text"
              maxlength="500"
              placeholder="用逗号分隔，如：工具, 文档"
              autocomplete="off"
            />
          </label>

          <p v-if="error" class="form-error">{{ error }}</p>

          <div class="modal-actions">
            <button type="button" class="btn-secondary" :disabled="busy" @click="emit('close')">取消</button>
            <button type="submit" class="btn-primary" :disabled="busy">
              {{ busy ? '提交中…' : mode === 'edit' ? '保存' : '提交' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>
