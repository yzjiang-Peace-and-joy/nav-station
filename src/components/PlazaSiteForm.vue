<script setup>
import { ref, watch, computed } from 'vue'
import { suggestSiteFromUrl } from '../api/aiSiteSuggest.js'

const props = defineProps({
  open: { type: Boolean, default: false },
  mode: { type: String, default: 'create' },
  site: { type: Object, default: null },
  categories: { type: Array, default: () => [] },
  busy: { type: Boolean, default: false },
  context: { type: String, default: 'plaza' }
})

const emit = defineEmits(['close', 'submit'])

const step = ref('url')
const suggesting = ref(false)
const name = ref('')
const url = ref('')
const desc = ref('')
const detail = ref('')
const category = ref('')
const tagsText = ref('')
const publishToPlaza = ref(false)
const error = ref('')

const isCreate = computed(() => props.mode !== 'edit')
const isMine = computed(() => props.context === 'mine')
const title = computed(() => {
  if (!isCreate.value) return '编辑广场站点'
  if (isMine.value) return step.value === 'url' ? '添加到我的' : '审阅站点信息'
  return step.value === 'url' ? '提交到广场' : '审阅站点信息'
})
const locked = computed(() => props.busy || suggesting.value)

function resetCreateFields() {
  step.value = 'url'
  name.value = ''
  url.value = ''
  desc.value = ''
  detail.value = ''
  category.value = ''
  tagsText.value = ''
  publishToPlaza.value = false
}

function fillFromSuggestion(suggestion) {
  name.value = suggestion.name || ''
  url.value = suggestion.url || url.value
  desc.value = suggestion.desc || ''
  detail.value = suggestion.detail || ''
  category.value = suggestion.category || ''
  tagsText.value = (suggestion.tags || []).join(', ')
}

watch(
  () => [props.open, props.site, props.mode],
  () => {
    if (!props.open) return
    error.value = ''
    suggesting.value = false
    if (props.mode === 'edit' && props.site) {
      step.value = 'review'
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
      resetCreateFields()
    }
  },
  { immediate: true }
)

function onBackdropClick() {
  if (!locked.value) emit('close')
}

function parseTags(text) {
  return text
    .split(/[,，]/)
    .map((t) => t.trim())
    .filter(Boolean)
}

function goManualFill() {
  error.value = ''
  if (!url.value.trim()) {
    error.value = '请先填写网址'
    return
  }
  step.value = 'review'
}

function backToUrl() {
  if (locked.value) return
  error.value = ''
  step.value = 'url'
}

async function runSuggest() {
  error.value = ''
  const rawUrl = url.value.trim()
  if (!rawUrl) {
    error.value = '请填写网址'
    return
  }
  suggesting.value = true
  try {
    const suggestion = await suggestSiteFromUrl(rawUrl)
    fillFromSuggestion(suggestion)
    step.value = 'review'
  } catch (err) {
    error.value = err.message || '解析失败，请重试或手动填写'
  } finally {
    suggesting.value = false
  }
}

function onSubmit() {
  error.value = ''
  const payload = {
    name: name.value.trim(),
    url: url.value.trim(),
    desc: desc.value.trim(),
    detail: detail.value.trim(),
    category: category.value.trim() || null,
    tags: parseTags(tagsText.value),
    ...(isMine.value && isCreate.value ? { publish_to_plaza: publishToPlaza.value } : {})
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
          <button
            type="button"
            class="modal-close"
            aria-label="关闭"
            :disabled="locked"
            @click="emit('close')"
          >
            ×
          </button>
        </div>

        <!-- Create: URL-only step -->
        <form
          v-if="isCreate && step === 'url'"
          class="modal-form"
          @submit.prevent="runSuggest"
        >
          <p class="form-hint">粘贴网址，由 AI 自动补全名称、简介、分类与标签，你再审阅确认。</p>
          <label class="form-field">
            <span>网址</span>
            <input
              v-model="url"
              type="url"
              required
              maxlength="1000"
              placeholder="https://"
              autocomplete="off"
              :disabled="suggesting"
            />
          </label>

          <label v-if="isMine && isCreate" class="form-check">
            <input v-model="publishToPlaza" type="checkbox" :disabled="suggesting" />
            <span>同步公开到广场</span>
          </label>

          <p v-if="error" class="form-error">{{ error }}</p>

          <div class="modal-actions">
            <button type="button" class="btn-secondary" :disabled="locked" @click="emit('close')">
              取消
            </button>
            <button type="button" class="btn-secondary" :disabled="locked" @click="goManualFill">
              手动填写
            </button>
            <button type="submit" class="btn-primary" :disabled="locked">
              {{ suggesting ? '解析中…' : '智能解析' }}
            </button>
          </div>
        </form>

        <!-- Create review / Edit full form -->
        <form v-else class="modal-form" @submit.prevent="onSubmit">
          <p v-if="isCreate" class="form-hint">请确认或修改以下字段后提交。</p>

          <label class="form-field">
            <span>名称</span>
            <input
              v-model="name"
              type="text"
              required
              maxlength="200"
              autocomplete="off"
              :disabled="suggesting"
            />
          </label>
          <label class="form-field">
            <span>网址</span>
            <input
              v-model="url"
              type="url"
              required
              maxlength="1000"
              placeholder="https://"
              autocomplete="off"
              :disabled="suggesting"
            />
          </label>
          <label class="form-field">
            <span>简介</span>
            <input
              v-model="desc"
              type="text"
              maxlength="500"
              autocomplete="off"
              :disabled="suggesting"
            />
          </label>
          <label class="form-field">
            <span>详情</span>
            <textarea v-model="detail" rows="3" maxlength="4000" :disabled="suggesting" />
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
              :disabled="suggesting"
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
              :disabled="suggesting"
            />
          </label>
          <label v-if="isMine && isCreate" class="form-checkbox">
            <input v-model="publishToPlaza" type="checkbox" :disabled="suggesting" />
            <span>同步公开到广场</span>
          </label>

          <p v-if="error" class="form-error">{{ error }}</p>

          <div class="modal-actions">
            <template v-if="isCreate">
              <button type="button" class="btn-secondary" :disabled="locked" @click="backToUrl">
                返回改网址
              </button>
              <button type="button" class="btn-secondary" :disabled="locked" @click="runSuggest">
                {{ suggesting ? '解析中…' : '重新解析' }}
              </button>
              <button type="submit" class="btn-primary" :disabled="locked">
                {{ busy ? '提交中…' : '提交' }}
              </button>
            </template>
            <template v-else>
              <button type="button" class="btn-secondary" :disabled="busy" @click="emit('close')">
                取消
              </button>
              <button type="submit" class="btn-primary" :disabled="busy">
                {{ busy ? '提交中…' : '保存' }}
              </button>
            </template>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.form-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-hint {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--fg-secondary);
  line-height: 1.5;
}

.modal-actions {
  flex-wrap: wrap;
}
</style>
