<template>
  <div class="mermaid-preview">
    <div v-if="error" class="mermaid-error">{{ error }}</div>
    <div v-else v-html="svg" class="mermaid-svg"></div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import mermaid from 'mermaid'

mermaid.initialize({ startOnLoad: false, theme: 'dark' })

const props = defineProps({ code: String })
const svg = ref('')
const error = ref('')
let debounceTimer = null
let renderId = 0

watch(
  () => props.code,
  (val) => {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(async () => {
      if (!val?.trim()) {
        svg.value = ''
        error.value = ''
        return
      }
      const id = `mermaid-preview-${++renderId}`
      try {
        const { svg: rendered } = await mermaid.render(id, val)
        svg.value = rendered
        error.value = ''
      } catch (e) {
        error.value = e.message || 'Invalid diagram'
        // mermaid may have inserted a broken element, remove it
        document.getElementById(id)?.remove()
      }
    }, 300)
  },
  { immediate: true }
)
</script>

<style scoped>
.mermaid-preview {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 16px;
  overflow: auto;
}

.mermaid-error {
  color: #f85149;
  font-family: var(--font-mono);
  font-size: 13px;
  white-space: pre-wrap;
}

.mermaid-svg :deep(svg) {
  max-width: 100%;
  height: auto;
}
</style>
