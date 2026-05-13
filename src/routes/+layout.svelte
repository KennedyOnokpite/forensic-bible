<script lang="ts">
	import './layout.css';
	import { Home, BookOpen, Search, Menu } from '@lucide/svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Root as SheetRoot, Trigger as SheetTrigger, Content as SheetContent, Header as SheetHeader, Title as SheetTitle } from '$lib/components/ui/sheet/index.js';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';

	let { children } = $props();

	const navItems = [
		{ label: 'Home', icon: Home, href: '/' },
		{ label: 'Books', icon: BookOpen, href: '/books' },
		{ label: 'Search', icon: Search, href: '/search' }
	] as const;
</script>

<div class="flex min-h-screen flex-col bg-background text-foreground">
	<!-- Desktop Header -->
	<header class="sticky top-0 z-40 hidden border-b border-white/5 bg-background/80 backdrop-blur-xl md:block">
		<div class="container mx-auto flex h-20 items-center justify-between px-8">
			<div class="flex items-center gap-3">
				<div class="h-8 w-8 rounded-full border border-primary/50 bg-primary/10 flex items-center justify-center">
					<span class="text-primary font-bold text-xs">FB</span>
				</div>
				<a href={resolve('/')} class="text-xl font-extrabold tracking-tighter text-white">
					Forensic <span class="text-primary">Bible</span>
				</a>
			</div>
			<nav class="flex items-center gap-10">
				{#each navItems as item (item.href)}
					<a
						href={resolve(item.href)}
						class="text-sm font-bold uppercase tracking-widest transition-all hover:text-primary {page.url.pathname ===
						item.href
							? 'text-primary'
							: 'text-muted-foreground'}"
					>
						{item.label}
					</a>
				{/each}
			</nav>
			<div>
				<Button variant="outline" class="border-primary/20 bg-primary/5 text-primary hover:bg-primary hover:text-black">
					Explorer Mode
				</Button>
			</div>
		</div>
	</header>

	<!-- Mobile Header -->
	<header class="sticky top-0 z-40 border-b border-white/5 bg-background/80 px-6 py-4 backdrop-blur-xl md:hidden">
		<div class="flex items-center justify-between">
			<div class="flex items-center gap-2">
				<a href={resolve('/')} class="text-lg font-black tracking-tighter text-white">Forensic <span class="text-primary">Bible</span></a>
			</div>
			<SheetRoot>
				<SheetTrigger>
					{#snippet child({ props })}
						<Button {...props} variant="ghost" size="icon" class="h-10 w-10 text-white/50 hover:text-white">
							<Menu class="h-6 w-6" />
						</Button>
					{/snippet}
				</SheetTrigger>
				<SheetContent side="left" class="border-white/5 bg-black/95 p-0 backdrop-blur-2xl">
					<SheetHeader class="border-b border-white/5 p-8 text-left">
						<SheetTitle class="flex items-center gap-3 text-2xl font-black tracking-tighter text-white">
							<BookOpen class="h-6 w-6 text-primary" />
							FORENSIC <span class="text-primary">BIBLE</span>
						</SheetTitle>
					</SheetHeader>
					<div class="mt-12 flex flex-col gap-6 p-8">
						{#each navItems as item (item.href)}
							<a
								href={resolve(item.href)}
								class="flex items-center gap-4 text-xl font-bold {page.url.pathname === item.href
									? 'text-primary'
									: 'text-muted-foreground'}"
							>
								<item.icon class="h-6 w-6" />
								{item.label}
							</a>
						{/each}
					</div>
				</SheetContent>
			</SheetRoot>
		</div>
	</header>

	<main class="flex-1 overflow-x-hidden pb-24 md:pb-0">
		{@render children()}
	</main>

	<!-- Mobile Bottom Navigation -->
	<nav
		class="fixed bottom-0 left-0 right-0 z-50 border-t border-white/5 bg-background/80 pb-safe pt-2 backdrop-blur-xl md:hidden"
	>
		<div class="flex items-center justify-around">
			{#each navItems as item (item.href)}
				<a
					href={resolve(item.href)}
					class="flex flex-col items-center gap-1.5 p-3 transition-all {page.url.pathname === item.href
						? 'text-primary'
						: 'text-muted-foreground'}"
				>
					<item.icon class="h-6 w-6" strokeWidth={page.url.pathname === item.href ? 2.5 : 1.5} />
					<span class="text-[9px] font-black uppercase tracking-[0.2em]">{item.label}</span>
				</a>
			{/each}
		</div>
	</nav>
</div>

<style>
	:global(.pb-safe) {
		padding-bottom: env(safe-area-inset-bottom);
	}
</style>
