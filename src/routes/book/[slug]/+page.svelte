<script lang="ts">
	import { audioStore } from '$lib/stores/audioStore.svelte';
	import type { ForensicUnit } from '$lib/types';
	import { resolve } from '$app/paths';
	import ForensicText from '$lib/ForensicText.svelte';
	import AudioPlayer from '$lib/AudioPlayer.svelte';
	import { onMount } from 'svelte';
	import { Root as CardRoot, Header as CardHeader, Content as CardContent } from '$lib/components/ui/card/index.js';
	import { Root as TabsRoot, List as TabsList, Trigger as TabsTrigger } from '$lib/components/ui/tabs/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Volume2, ChevronLeft, ChevronDown } from '@lucide/svelte';

	let { data } = $props();
	let viewMode = $state('english');

	const RULE_NAMES: Record<number, string> = {
		1: 'Total Contextual Disclosure', 2: 'Zero Contextual Drift', 3: 'Pure English Only',
		4: 'Modern Basic English', 5: 'Italicized Grouping', 6: 'Perfect Word + Bracket',
		7: 'Ancient Idiomatic Expressions', 8: 'Modern Value Comparison', 9: 'Verb Aspect Disclosure',
		10: 'Status Permanence Disclosure', 11: 'Agency and Causality', 12: 'Collective vs Individual Agency',
		13: 'Instructional Intent Tone', 14: 'Certainty and Mood', 15: 'Level of Obligation',
		16: 'Degree of Urgency', 17: 'Instrument and Means', 18: 'Completeness of Action',
		19: 'Source of Authority', 20: 'Consolidated Syntax', 21: 'Functional Object Disclosure',
		22: 'Symbolic Attire + Object', 23: 'Social Identity of Roles', 24: 'Situational Name Disclosure',
		25: 'Intertextual Echoes', 26: 'Prophetic Fulfillment', 28: 'Disciplinary Context',
		29: 'Geographical Orientation', 30: 'Contextual Targeting & Bridging', 31: 'Divine vs Human Time',
		32: 'Legal Status of Subject', 33: 'Eyewitness vs Reported Speech', 34: 'Intensity of Sacredness',
		35: 'Direction of Address', 36: 'Wisdom vs Practical Insight', 37: 'Life Type Differentiation',
		38: 'Community vs Individual', 39: 'Identity of We and Us', 40: 'Intimacy & Relationship Tone',
		41: 'Gender Scope Disclosure', 42: 'Intensity Grading', 43: 'Emotional Intensity Pathos',
		44: 'Honor and Shame Context', 45: 'Temple & Ceremonial Context', 46: 'Social Scandal & Taboo',
		47: 'Anthropological Disclosure', 48: 'Status Permanence (Perfect Tense)', 49: 'Patronage Relationship',
		50: 'Ancient Hospitality Laws', 51: 'Facial & Body Gesture Disclosure', 52: 'Structural Therefore',
		53: 'Forgiveness as Economic Debt', 54: 'Master-Disciple Relationship', 55: 'Theophanic Phenomenon',
		56: 'Suffix of Endearment Diminutives', 57: 'Covenantal Signs & Seals', 58: 'Plainness of Speech Parrhesia',
		59: 'Ancestral & Lineage Weight', 60: 'Cognate Accusative Emphasis', 61: 'Nature & Animal Symbolism',
		62: 'Honorifics & Social Hierarchy', 63: 'Channel vs Source Agency', 64: 'Conditional Reality',
		65: 'Genitive Directionality', 66: 'Hendiadys Double-Word Unity', 67: 'Ancient Monetary Scale',
		68: 'Polysemy Resolution', 69: 'Verbal Inspiration Granularity', 70: 'Optimal Bridging Phrase',
		71: 'Biological vs Forensic Sonship', 72: 'Cognitive Center Realignment', 73: 'Forensic Theological Boundary',
		74: 'Conjunctive Chain Precision', 75: 'Absence-of-Article Significance', 76: 'Word-Order Emphasis',
		77: 'Resumptive Pronoun Disclosure', 78: 'Hapax Legomenon Flag', 79: 'Semantic Range Boundary'
	};

	function parseDictEntry(raw: string): Record<string, string> {
		const result: Record<string, string> = {};
		const parts = raw.split(/;\s*/);
		for (const part of parts) {
			const colon = part.indexOf(':');
			if (colon > -1) {
				result[part.slice(0, colon).trim()] = part.slice(colon + 1).trim();
			}
		}
		return result;
	}

	function handlePlay(unit: ForensicUnit, lang: string) {
		const text = lang === 'en' ? unit['main-translation'] : unit.sentence;
		
		let speechLang = 'en-US';
		if (lang !== 'en') {
			const sourceLang = unit['source-language'] || data.book.language;
			if (sourceLang === 'Greek') speechLang = 'el-GR';
			else if (sourceLang === 'Hebrew') speechLang = 'he-IL';
			else if (sourceLang === 'Aramaic') speechLang = 'arc';
		}
		
		if (audioStore.currentUnitIndex === unit.index && audioStore.isPlaying) {
			audioStore.stopPlayback();
		} else {
			audioStore.playText(text, unit.index, speechLang);
		}
	}

	$effect(() => {
		if (audioStore.currentUnitIndex) {
			const el = document.getElementById(`unit-${audioStore.currentUnitIndex}`);
			if (el) {
				el.scrollIntoView({ behavior: 'smooth', block: 'center' });
			}
		}
	});

	onMount(() => {
		const handleEnded = (e: Event) => {
			const customEvent = e as CustomEvent<{ index: number }>;
			if (audioStore.continuous) {
				const currentIndex = customEvent.detail.index;
				const nextUnit = data.units.find(u => u.index === currentIndex + 1);
				if (nextUnit) {
					const langMode = audioStore.currentText === nextUnit.sentence ? 'orig' : 'en';
					handlePlay(nextUnit, langMode);
				}
			}
		};

		window.addEventListener('audio-unit-ended', handleEnded);
		return () => window.removeEventListener('audio-unit-ended', handleEnded);
	});

	function getExplanationEntries(exp: Record<string, string> | string | null | undefined): [string, string][] {
		if (!exp || typeof exp === 'string') return exp ? [['Note', exp]] : [];
		return Object.entries(exp) as [string, string][];
	}

	let activeWord = $state<{ unit: number; word: string } | null>(null);

	function setActiveWord(unitIndex: number, word: string) {
		if (activeWord?.unit === unitIndex && activeWord?.word === word) {
			activeWord = null;
		} else {
			activeWord = { unit: unitIndex, word };
		}
	}
</script>

<svelte:head>
	<title>{data.book.name} | Forensic Biblical Explorer</title>
</svelte:head>

<div class="mx-auto max-w-4xl px-6 py-12 md:py-24">
	<nav class="mb-12 flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
		<a href={resolve('/')} class="flex items-center gap-2 text-xs font-black uppercase tracking-[0.3em] text-muted-foreground transition-colors hover:text-primary">
			<ChevronLeft class="h-4 w-4" />
			Library
		</a>

		<div class="flex items-center gap-4">
			<TabsRoot value={viewMode} class="w-[200px]" onValueChange={(v) => viewMode = v}>
				<TabsList class="grid w-full grid-cols-2 bg-white/5 border border-white/5">
					<TabsTrigger value="english" class="text-[10px] font-black uppercase tracking-widest">English</TabsTrigger>
					<TabsTrigger value="original" class="text-[10px] font-black uppercase tracking-widest">Original</TabsTrigger>
				</TabsList>
			</TabsRoot>
		</div>
	</nav>

	<article>
		<header class="mb-20 text-center">
			<h1 class="mb-4 text-5xl font-black tracking-tighter text-white md:text-7xl">{data.book.name}</h1>
			<p class="text-[10px] font-black uppercase tracking-[0.4em] text-primary">
				{#if viewMode === 'english'}
					Sovereign Forensic Reconstruction
				{:else}
					{data.book.language} Holographic Source
				{/if}
			</p>
		</header>

		{#if viewMode === 'original'}
			<div class="rounded-3xl border border-white/5 bg-white/2 p-8 md:p-16">
				<div class="original-text leading-[2.5] md:leading-[3] {data.book.language.toLowerCase()} text-2xl md:text-4xl text-center">
					{data.content}
				</div>
			</div>
		{:else}
			<div class="space-y-12">
				{#if data.units && data.units.length > 0}
					{#each data.units as unit (unit.index)}
						<CardRoot 
							id="unit-{unit.index}"
							class="overflow-hidden border-white/5 bg-white/1 transition-all duration-500 {audioStore.currentUnitIndex === unit.index ? 'border-primary/50 bg-primary/3 ring-1 ring-primary/20' : ''}"
						>
							<CardHeader class="flex flex-row items-center justify-between border-b border-white/5 bg-white/2 px-6 py-4">
								<div class="flex items-center gap-4">
									<span class="text-[10px] font-black tracking-[0.2em] text-muted-foreground">UNIT {unit.index}</span>
									{#if unit['forensic-confidence'] > 0}
										<div class="flex items-center gap-1.5 rounded-full bg-green-500/10 px-3 py-1 text-[9px] font-bold text-green-500 border border-green-500/20">
											<div class="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse"></div>
											{unit['forensic-confidence']}% Forensic Certainty
										</div>
									{/if}
								</div>
								<div class="flex items-center gap-2">
									<Button 
										variant="ghost" 
										size="sm" 
										class="h-8 gap-2 text-[9px] font-black tracking-widest {audioStore.currentUnitIndex === unit.index && audioStore.isPlaying && audioStore.currentText === unit.sentence ? 'text-primary bg-primary/10' : 'text-muted-foreground'}"
										onclick={() => handlePlay(unit, 'orig')}
									>
										<Volume2 class="h-3.5 w-3.5" />
										{data.book.language === 'Greek' ? 'GRK' : 'HBW'}
									</Button>
									<Button 
										variant="ghost" 
										size="sm" 
										class="h-8 gap-2 text-[9px] font-black tracking-widest {audioStore.currentUnitIndex === unit.index && audioStore.isPlaying && audioStore.currentText === unit['main-translation'] ? 'text-primary bg-primary/10' : 'text-muted-foreground'}"
										onclick={() => handlePlay(unit, 'en')}
									>
										<Volume2 class="h-3.5 w-3.5" />
										ENG
									</Button>
								</div>
							</CardHeader>
							<CardContent class="p-8 md:p-12">
								<div class="mb-10">
									<p class="text-2xl font-medium leading-relaxed text-white md:text-3xl">
										<ForensicText text={unit['main-translation']} />
									</p>
								</div>
								
								<div class="flex flex-wrap gap-2 pt-6 border-t border-white/5 {data.book.language.toLowerCase() === 'hebrew' ? 'flex-row-reverse' : ''}">
									{#each unit.words as word, i (i)}
										<button 
											class="rounded-lg border border-white/5 px-3 py-1.5 font-greek text-lg transition-all hover:border-primary/50 hover:text-primary {activeWord?.unit === unit.index && activeWord?.word === word ? 'bg-primary text-black font-bold border-primary' : 'text-muted-foreground'}"
											onclick={() => setActiveWord(unit.index, word)}
										>
											{word}
										</button>
									{/each}
								</div>

								<div class="mt-8">
									<details class="group">
										<summary class="flex cursor-pointer items-center gap-2 text-[10px] font-black uppercase tracking-[0.2em] text-muted-foreground hover:text-primary transition-colors list-none">
											<div class="h-5 w-5 rounded-full border border-white/10 flex items-center justify-center transition-transform group-open:rotate-180">
												<ChevronDown class="h-3 w-3" />
											</div>
											Forensic Metadata
										</summary>
										<div class="mt-8 space-y-10 border-t border-white/5 pt-8">
											<div class="grid grid-cols-1 md:grid-cols-2 gap-10">
												<!-- Interlinear -->
												<div class="space-y-4">
													<h4 class="text-[9px] font-black uppercase tracking-[0.3em] text-primary/60">Literal Mirror</h4>
													<div class="flex flex-wrap gap-4 rounded-2xl bg-black/40 p-6 border border-white/5">
														{#each unit.words as word, i (i)}
															<div class="flex flex-col items-center gap-1 min-w-[50px]">
																<span class="text-lg font-greek text-white">{word}</span>
																<span class="text-[9px] font-bold uppercase text-primary/80">{Array.isArray(unit['literal-translation']) ? (unit['literal-translation'][i] || '...') : (i === 0 ? (unit['literal-translation'] || '...') : '...')}</span>
															</div>
														{/each}
													</div>
												</div>

												<!-- Grammatical -->
												{#if Object.keys(unit['grammatical-notes'] || {}).length > 0}
													<div class="space-y-4">
														<h4 class="text-[9px] font-black uppercase tracking-[0.3em] text-primary/60">Grammatical Depth</h4>
														<div class="grid gap-3">
															{#each Object.entries(unit['grammatical-notes']) as [word, note] (word)}
																<div class="flex flex-col gap-1 rounded-xl bg-white/2 p-3 border border-white/5">
																	<span class="text-sm font-bold text-white">{word}</span>
																	<span class="text-xs text-muted-foreground leading-relaxed">{note}</span>
																</div>
															{/each}
														</div>
													</div>
												{/if}

												<!-- Dictionary -->
												{#if Object.keys(unit['dictionary-meaning'] || {}).length > 0}
													<div class="space-y-4 md:col-span-2">
														<h4 class="text-[9px] font-black uppercase tracking-[0.3em] text-primary/60">Dictionary Convergence</h4>
														<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
															{#each Object.entries(unit['dictionary-meaning']) as [word, meaning] (word)}
																<div class="rounded-2xl border border-white/5 bg-white/2 p-5 {activeWord?.unit === unit.index && activeWord?.word === word ? 'border-primary ring-1 ring-primary/20 bg-primary/5' : ''}">
																	<span class="mb-4 block text-lg font-bold text-white border-b border-white/5 pb-2">{word}</span>
																	<div class="space-y-2">
																		{#each Object.entries(parseDictEntry(String(meaning))) as [key, val] (key)}
																			<div class="grid grid-cols-[80px_1fr] gap-4">
																				<span class="text-[8px] font-black uppercase tracking-widest text-primary/70">{key}</span>
																				<span class="text-[11px] text-muted-foreground leading-tight">{val}</span>
																			</div>
																		{/each}
																	</div>
																</div>
															{/each}
														</div>
													</div>
												{/if}
											</div>

											<!-- Rules -->
											<div class="space-y-4">
												<h4 class="text-[9px] font-black uppercase tracking-[0.3em] text-primary/60">Forensic Rules Applied</h4>
												<div class="flex flex-wrap gap-2">
													{#each unit['rules-applied'] as rule (rule)}
														<div class="rounded-lg border border-primary/20 bg-primary/5 px-3 py-1.5 text-[9px] font-black tracking-widest text-primary flex items-center gap-2" title={RULE_NAMES[rule]}>
															<span class="opacity-50">RULE {rule}</span>
															<span>{RULE_NAMES[rule]}</span>
														</div>
													{/each}
												</div>
											</div>

											<!-- Adversarial -->
											<div class="space-y-4 md:col-span-2">
												<h4 class="text-[9px] font-black uppercase tracking-[0.3em] text-primary/60">Adversarial Convergence</h4>
												<div class="space-y-4">
													{#each getExplanationEntries(unit['main-translation-explanation']) as [phrase, justification] (phrase)}
														<div class="rounded-2xl bg-white/2 p-5 border border-white/5 border-l-primary/50 border-l-2">
															<span class="block text-[11px] font-black text-primary mb-2 uppercase tracking-widest">"{phrase}"</span>
															<p class="text-[13px] text-muted-foreground leading-relaxed italic">{justification}</p>
														</div>
													{/each}
													
													{#if (unit['rejected-translations'] || []).length > 0}
														<div class="mt-8 space-y-4 pt-8 border-t border-white/5">
															<span class="text-[10px] font-black uppercase tracking-[0.3em] text-red-500/70">Explicitly Rejected</span>
															<div class="grid gap-3">
																{#each unit['rejected-translations'] as rejected (typeof rejected === 'object' ? rejected.phrase : rejected)}
																	<div class="text-[11px] flex flex-col md:flex-row md:items-baseline gap-2">
																		<span class="text-red-500/50 font-bold line-through">"{typeof rejected === 'object' ? rejected.phrase : rejected}"</span>
																		{#if typeof rejected === 'object' && rejected.reason}
																			<span class="text-muted-foreground/60">— {rejected.reason}</span>
																		{/if}
																	</div>
																{/each}
															</div>
														</div>
													{/if}
												</div>
											</div>
										</div>
									</details>
								</div>
							</CardContent>
						</CardRoot>
					{/each}
				{:else}
					<div class="py-32 text-center border border-dashed border-white/10 rounded-[3rem]">
						<p class="text-xl font-bold text-muted-foreground tracking-tighter italic">SOTA Reconstruction in progress...</p>
					</div>
				{/if}
			</div>
		{/if}
	</article>

	<AudioPlayer />
</div>

<style>
	.original-text.hebrew {
		direction: rtl;
		font-family: 'SBL Hebrew', serif;
	}
</style>
