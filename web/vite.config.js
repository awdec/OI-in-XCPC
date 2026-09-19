import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  base: '/XCPCAtlas/',
  plugins: [vue(), tailwindcss()],
  server: {
    port: 11451,
    host: false,
  },
})
