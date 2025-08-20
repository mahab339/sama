import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  resolve: {
    alias: {
      // This ensures consistent Bootstrap JS loading
      'bootstrap': 'bootstrap/dist/js/bootstrap.bundle.min.js'
    }
  }
});