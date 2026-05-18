import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Default base '/' for Railway deployment
// For GitHub Pages, build with: BASE_URL=/DesignSite/ npx vite build
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  base: process.env.BASE_URL || (mode === 'pages' ? '/DesignSite/' : '/'),
}))
