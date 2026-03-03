<template>
  <div class="paste-metadata">
    <span class="meta-item">
      <span class="meta-label">Type:</span>
      <span class="meta-value">{{ displayType }}</span>
    </span>
    <span v-if="paste.language" class="meta-item">
      <span class="meta-label">Language:</span>
      <span class="meta-value">{{ paste.language }}</span>
    </span>
    <span class="meta-item">
      <span class="meta-label">Created:</span>
      <span class="meta-value">{{ formatDate(paste.created_at) }}</span>
    </span>
    <span v-if="paste.expires_at" class="meta-item">
      <span class="meta-label">Expires:</span>
      <span class="meta-value">{{ timeLeft }}</span>
    </span>
    <span v-else class="meta-item">
      <span class="meta-label">Expires:</span>
      <span class="meta-value">Never</span>
    </span>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({ paste: Object })

const displayType = computed(() => {
  const map = { code: 'Code', mermaid: 'Mermaid', text: 'Text' }
  return map[props.paste.content_type] || props.paste.content_type
})

const now = ref(Date.now())
let timer = null

onMounted(() => {
  timer = setInterval(() => { now.value = Date.now() }, 1000)
})
onBeforeUnmount(() => clearInterval(timer))

const timeLeft = computed(() => {
  if (!props.paste.expires_at) return 'Never'
  const diff = new Date(props.paste.expires_at).getTime() - now.value
  if (diff <= 0) return 'Expired'
  const hours = Math.floor(diff / 3600000)
  const minutes = Math.floor((diff % 3600000) / 60000)
  if (hours >= 24) {
    const days = Math.floor(hours / 24)
    return `${days}d ${hours % 24}h`
  }
  return `${hours}h ${minutes}m`
})

function formatDate(iso) {
  return new Date(iso).toLocaleString()
}
</script>

<style scoped>
.paste-metadata {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  padding: 12px 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  font-size: 13px;
}

.meta-label {
  color: var(--color-text-muted);
  margin-right: 4px;
}

.meta-value {
  color: var(--color-text);
}
</style>
