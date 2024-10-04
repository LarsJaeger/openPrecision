import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { threeMinifier } from "@yushijinhun/three-minifier-rollup";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte(), threeMinifier()],
  ssr: {
    noExternal: ['three'],
  },
})
