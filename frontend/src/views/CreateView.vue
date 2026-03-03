<template>
  <div class="create-view">
    <div class="form-controls">
      <div class="control-group">
        <label>Type</label>
        <select v-model="contentType">
          <option value="text">Text</option>
          <option value="code">Code</option>
          <option value="mermaid">Mermaid</option>
        </select>
      </div>

      <div v-if="contentType === 'code'" class="control-group">
        <label>Language</label>
        <select v-model="language">
          <option v-for="lang in languages" :key="lang" :value="lang">{{ lang }}</option>
        </select>
      </div>

      <div class="control-group">
        <label>Expires</label>
        <select v-model="ttl">
          <option value="1h">1 hour</option>
          <option value="1d">1 day</option>
          <option value="1w">1 week</option>
          <option value="1m">1 month</option>
          <option value="never">Never</option>
        </select>
      </div>
    </div>

    <div :class="['editor-area', { split: contentType === 'mermaid' }]">
      <textarea
        v-model="content"
        class="editor"
        placeholder="Paste your content here..."
        spellcheck="false"
      ></textarea>
      <MermaidPreview v-if="contentType === 'mermaid'" :code="content" class="preview-pane" />
    </div>

    <div class="actions">
      <button @click="submit" :disabled="submitting || !content.trim()" class="btn-primary">
        {{ submitting ? 'Creating...' : 'Create Paste' }}
      </button>
      <span v-if="errorMsg" class="error-msg">{{ errorMsg }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createPaste } from '../api/pastes'
import MermaidPreview from '../components/MermaidPreview.vue'

const router = useRouter()

const content = ref('')
const contentType = ref('text')
const language = ref('javascript')
const ttl = ref('1d')
const submitting = ref(false)
const errorMsg = ref('')

const languages = [
  'javascript', 'typescript', 'python', 'java', 'c', 'cpp', 'csharp',
  'go', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'sql', 'html',
  'css', 'json', 'yaml', 'xml', 'bash', 'dockerfile', 'markdown',
]

async function submit() {
  submitting.value = true
  errorMsg.value = ''
  try {
    const data = {
      content: content.value,
      content_type: contentType.value,
      ttl: ttl.value,
    }
    if (contentType.value === 'code') {
      data.language = language.value
    }
    const result = await createPaste(data)
    router.push(result.url)
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.form-controls {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.control-group label {
  font-size: 12px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.control-group select {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
}

.editor-area {
  margin-bottom: 16px;
}

.editor-area.split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.editor {
  width: 100%;
  min-height: 400px;
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 16px;
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  tab-size: 2;
}

.editor:focus {
  outline: none;
  border-color: var(--color-primary);
}

.preview-pane {
  min-height: 400px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-primary {
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-msg {
  color: #f85149;
  font-size: 14px;
}
</style>
