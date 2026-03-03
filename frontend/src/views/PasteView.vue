<template>
  <div class="paste-view">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="!paste" class="not-found">
      <h2>Paste not found</h2>
      <p>This paste may have expired or never existed.</p>
      <router-link to="/" class="btn-secondary">Create New Paste</router-link>
    </div>
    <template v-else>
      <PasteMetadata :paste="paste" />

      <div class="paste-actions">
        <button @click="copyContent" class="btn-secondary">
          {{ copied ? 'Copied!' : 'Copy' }}
        </button>
        <router-link to="/" class="btn-secondary">New Paste</router-link>
      </div>

      <div v-if="paste.content_type === 'mermaid'" class="mermaid-layout">
        <MermaidPanZoom :code="paste.content" />
        <details class="source-details" open>
          <summary>Source</summary>
          <pre class="source-code">{{ paste.content }}</pre>
        </details>
      </div>

      <CodeHighlight
        v-else-if="paste.content_type === 'code'"
        :code="paste.content"
        :language="paste.language"
      />

      <pre v-else class="plain-text">{{ paste.content }}</pre>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPaste } from '../api/pastes'
import PasteMetadata from '../components/PasteMetadata.vue'
import MermaidPanZoom from '../components/MermaidPanZoom.vue'
import CodeHighlight from '../components/CodeHighlight.vue'

const route = useRoute()
const paste = ref(null)
const loading = ref(true)
const copied = ref(false)

onMounted(async () => {
  try {
    paste.value = await getPaste(route.params.id)
  } catch {
    paste.value = null
  } finally {
    loading.value = false
  }
})

async function copyContent() {
  try {
    await navigator.clipboard.writeText(paste.value.content)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {
    // fallback
    const ta = document.createElement('textarea')
    ta.value = paste.value.content
    document.body.appendChild(ta)
    ta.select()
    document.execCommand('copy')
    document.body.removeChild(ta)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  }
}
</script>

<style scoped>
.paste-view {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.loading {
  text-align: center;
  color: var(--color-text-muted);
  padding: 48px;
}

.not-found {
  text-align: center;
  padding: 48px;
}

.not-found h2 {
  margin-bottom: 8px;
}

.not-found p {
  color: var(--color-text-muted);
  margin-bottom: 16px;
}

.paste-actions {
  display: flex;
  gap: 8px;
}

.btn-secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.btn-secondary:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.mermaid-layout {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.source-details {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
}

.source-details summary {
  padding: 8px 16px;
  cursor: pointer;
  color: var(--color-text-muted);
  font-size: 13px;
}

.source-code {
  padding: 16px;
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.6;
  overflow-x: auto;
  margin: 0;
  border-top: 1px solid var(--color-border);
}

.plain-text {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 16px;
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}
</style>
