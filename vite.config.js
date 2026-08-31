import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: true,
    port: 5173,
    hmr: {
      protocol: 'wss',
      host: 'test-front.5ai.icu',
      clientPort: 443
    },
    proxy: { '/api': 'http://127.0.0.1:8000' }
  }
})
