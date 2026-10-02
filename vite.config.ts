/// <reference types="vitest/config" />
import react from '@vitejs/plugin-react'
import { configDefaults } from 'vitest/config'
import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  base: './',
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icono-192.png', 'icono-512.png'],
      manifest: {
        name: 'Dilución EV',
        short_name: 'Dilución EV',
        description: 'Dilución, velocidad de infusión y compatibilidad de medicamentos endovenosos. Material de formación.',
        lang: 'es-CL',
        theme_color: '#0e7490',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: './',
        scope: './',
        icons: [
          { src: 'icono-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icono-512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' },
        ],
      },
      // og.png es solo la vista previa para redes sociales: no hace falta guardarla para uso sin internet
      workbox: { globPatterns: ['**/*.{js,css,html,png,svg,webmanifest}'], globIgnores: ['og.png'] },
    }),
  ],
  test: {
    environment: 'jsdom',
    setupFiles: ['src/test/setup.ts'],
    exclude: [...configDefaults.exclude, 'supabase/**'],
  },
})
