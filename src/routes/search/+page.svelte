<script lang="ts">
	import { Search } from '@lucide/svelte';
	import Input from '$lib/components/ui/input/input.svelte';
</script>

<svelte:head>
	<title>Search | Forensic Biblical Explorer</title>
</svelte:head>

<div class="container mx-auto px-6 py-24 text-center">
	<div class="mx-auto max-w-xl">
		<Search class="mx-auto mb-6 h-12 w-12 text-primary opacity-50" />
		<h1 class="mb-4 text-4xl font-black tracking-tighter text-white">Forensic <span class="text-primary">Search</span></h1>
		<p class="mb-12 text-muted-foreground">Search through the original Hebrew, Aramaic, and Greek texts.</p>
		
		<div class="relative">
			<Search class="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
			<Input class="h-14 border-white/10 bg-white/5 pl-12 text-lg focus-visible:ring-primary/50" placeholder="Enter verse or keyword..." />
		</div>
	</div>
</div>
