<template>
  <pre class="code-highlight"><code ref="codeEl" :class="langClass" v-text="code"></code></pre>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

const props = defineProps({
  code: String,
  language: String,
})

const codeEl = ref(null)
const langClass = ref(props.language ? `language-${props.language}` : '')

function highlight() {
  if (codeEl.value) {
    codeEl.value.removeAttribute('data-highlighted')
    hljs.highlightElement(codeEl.value)
  }
}

onMounted(highlight)
watch(() => props.code, highlight)
</script>

<style scoped>
.code-highlight {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}
</style>
