import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { aiIndex } from './ai-index'

export default defineConfig({
  plugins: [react(), aiIndex()],
  server: { port: 5190 },
})
