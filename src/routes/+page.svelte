<script lang="ts">
	import books from '$lib/books.json';
	import { Root as CardRoot, Header as CardHeader, Title as CardTitle, Description as CardDescription } from '$lib/components/ui/card/index.js';
	import { resolve } from '$app/paths';

	const oldBooks = books.filter((b) => b.testament === 'Old');
	const newBooks = books.filter((b) => b.testament === 'New');
</script>

<svelte:head>
	<title>The Original Scriptures | Forensic Biblical Explorer</title>
	<meta
		name="description"
		content="A forensic, 100%-accurate reconstruction of all 66 books of the Bible from their original Hebrew, Aramaic, and Koine Greek texts."
	/>
</svelte:head>

<div class="container mx-auto px-6 py-12 md:py-32">
	<header class="mb-20 text-center md:mb-32">
		<div
			class="mb-8 inline-flex items-center rounded-full border border-primary/20 bg-primary/5 px-6 py-2 text-[10px] font-black uppercase tracking-[0.4em] text-primary"
		>
			Sovereign Forensic Reconstruction
		</div>
		<h1 class="mb-8 text-5xl font-black tracking-tighter text-white md:text-9xl">
			The Original <span class="text-primary">Scriptures</span>
		</h1>
		<p class="mx-auto max-w-2xl text-lg leading-relaxed text-muted-foreground md:text-2xl">
			A pure reconstruction of all 66 books from their original <span class="text-white">Hebrew</span>,
			<span class="text-white">Aramaic</span>, and <span class="text-white">Koine Greek</span> texts.
		</p>
	</header>

	<div class="space-y-24 md:space-y-32">
		<section>
			<div class="mb-12 flex items-center gap-6">
				<h2 class="text-xs font-black uppercase tracking-[0.5em] text-primary">Old Testament</h2>
				<div class="h-px flex-1 bg-white/5"></div>
				<span class="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Hebrew & Aramaic</span>
			</div>
			<div class="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8">
				{#each oldBooks as book (book.id)}
					<a href={resolve(`/book/${book.slug}`)} class="group">
						<CardRoot
							class="h-full border-white/5 bg-white/1 transition-all duration-300 hover:border-primary/40 hover:bg-primary/5 hover:-translate-y-1.5"
						>
							<CardHeader class="p-6 text-center">
								<span
									class="mb-3 block font-greek text-2xl font-medium text-primary/70 transition-colors group-hover:text-primary"
								>
									{book.original_language_name}
								</span>
								<CardTitle class="text-sm font-black tracking-tight text-white">{book.name}</CardTitle>
								<CardDescription class="mt-1 text-[8px] font-bold uppercase tracking-[0.2em] text-muted-foreground"
									>{book.language}</CardDescription
								>
							</CardHeader>
						</CardRoot>
					</a>
				{/each}
			</div>
		</section>

		<section>
			<div class="mb-12 flex items-center gap-6">
				<h2 class="text-xs font-black uppercase tracking-[0.5em] text-primary">New Testament</h2>
				<div class="h-px flex-1 bg-white/5"></div>
				<span class="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Koine Greek</span>
			</div>
			<div class="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8">
				{#each newBooks as book (book.id)}
					<a href={resolve(`/book/${book.slug}`)} class="group">
						<CardRoot
							class="h-full border-white/5 bg-white/1 transition-all duration-300 hover:border-primary/40 hover:bg-primary/5 hover:-translate-y-1.5"
						>
							<CardHeader class="p-6 text-center">
								<span
									class="mb-3 block font-greek text-2xl font-medium text-primary/70 transition-colors group-hover:text-primary"
								>
									{book.original_language_name}
								</span>
								<CardTitle class="text-sm font-black tracking-tight text-white">{book.name}</CardTitle>
								<CardDescription class="mt-1 text-[8px] font-bold uppercase tracking-[0.2em] text-muted-foreground"
									>{book.language}</CardDescription
								>
							</CardHeader>
						</CardRoot>
					</a>
				{/each}
			</div>
		</section>
	</div>
</div>
