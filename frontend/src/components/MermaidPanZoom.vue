<template>
  <div class="mermaid-panzoom-wrapper">
    <div ref="container" class="mermaid-panzoom" v-html="svg"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import mermaid from 'mermaid'
import panzoom from 'panzoom'

mermaid.initialize({ startOnLoad: false, theme: 'dark' })

const props = defineProps({ code: String })
const container = ref(null)
const svg = ref('')
let pzInstance = null

onMounted(async () => {
  try {
    const { svg: rendered } = await mermaid.render('mermaid-view', props.code)
    svg.value = rendered
    await nextTick()
    const svgEl = container.value?.querySelector('svg')
    if (svgEl) {
      pzInstance = panzoom(svgEl, {
        maxZoom: 10,
        minZoom: 0.1,
        smoothScroll: false,
      })
    }
  } catch (e) {
    svg.value = `<p style="color: #f85149;">Failed to render diagram: ${e.message}</p>`
  }
})

onBeforeUnmount(() => {
  pzInstance?.dispose()
})
</script>

<style scoped>
.mermaid-panzoom-wrapper {
  border: 1px solid var(--color-border);
  border-radius: 6px;
  overflow: hidden;
  background: var(--color-surface);
  min-height: 300px;
  cursor: grab;
}

.mermaid-panzoom-wrapper:active {
  cursor: grabbing;
}

.mermaid-panzoom {
  width: 100%;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.mermaid-panzoom :deep(svg) {
  max-width: 100%;
  height: auto;
}
</style>
