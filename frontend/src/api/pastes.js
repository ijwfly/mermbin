export async function createPaste(data) {
  const res = await fetch('/api/pastes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Failed to create paste')
  }
  return res.json()
}

export async function getPaste(id) {
  const res = await fetch(`/api/pastes/${id}`)
  if (res.status === 404) return null
  if (!res.ok) throw new Error('Failed to fetch paste')
  return res.json()
}
