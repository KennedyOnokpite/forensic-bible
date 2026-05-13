<script lang="ts">
	import books from '$lib/books.json';
	import { Root as CardRoot, Header as CardHeader, Title as CardTitle } from '$lib/components/ui/card/index.js';
	import { resolve } from '$app/paths';
</script>

<svelte:head>
	<title>Books | Forensic Biblical Explorer</title>
</svelte:head>

<div class="container mx-auto px-6 py-24">
	<h1 class="mb-12 text-4xl font-black tracking-tighter text-white">Biblical <span class="text-primary">Library</span></h1>
	<div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
		{#each books as book (book.id)}
			<a href={resolve(`/book/${book.slug}`)} class="group">
				<CardRoot class="h-full border-white/5 bg-white/2 transition-all hover:border-primary/50 hover:bg-primary/5">
					<CardHeader class="p-4 text-center">
						<span class="mb-1 block font-greek text-xl text-primary/80 group-hover:text-primary">{book.original_language_name}</span>
						<CardTitle class="text-xs font-bold text-white">{book.name}</CardTitle>
					</CardHeader>
				</CardRoot>
			</a>
		{/each}
	</div>
</div>
