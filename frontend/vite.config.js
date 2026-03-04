import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    sourcemap: false,
  },
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
