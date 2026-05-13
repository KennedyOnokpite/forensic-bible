import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		watch: {
			// Deeply ignore the data directory to stop the 60s timeout
			ignored: ['**/static/data/**', '**/.svelte-kit/**', '**/node_modules/**']
		},
		fs: {
			// Allow static folder for icons and manifest
			allow: ['src', 'static', 'node_modules']
		}
	},
	optimizeDeps: {
		// Pre-bundle core UI libs to speed up initial load
		include: ['@lucide/svelte', 'tailwind-variants', 'clsx', 'tailwind-merge', 'bits-ui']
	}
});
