<script lang="ts">
	import { playText, isPlaying, currentPlayingIndex, stopPlayback } from '$lib/stores/audioStore';
	import type { ForensicUnit } from '$lib/types';
	import { resolve } from '$app/paths';
	import ForensicText from '$lib/ForensicText.svelte';

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
		const speechLang = lang === 'en' ? 'en-US' : (data.book.language === 'Greek' ? 'el-GR' : 'he-IL');
		if ($currentPlayingIndex === unit.index && $isPlaying) {
			stopPlayback();
		} else {
			currentPlayingIndex.set(unit.index);
			playText(text, speechLang);
		}
	}

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

<div class="reading-container">
	<nav class="top-nav">
		<a href={resolve('/')} class="back-link">
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
				<path d="M19 12H5M12 19l-7-7 7-7"/>
			</svg>
			<span>Library</span>
		</a>

		<div class="jump-control">
			<input 
				type="number" 
				placeholder="Jump to Unit..." 
				min="1" 
				max={data.units.length}
				onkeydown={(e) => {
					if (e.key === 'Enter') {
						const val = (e.target as HTMLInputElement).value;
						document.getElementById(`unit-${val}`)?.scrollIntoView({ behavior: 'smooth' });
					}
				}}
			/>
		</div>

		<div class="toggle-container">
			<button 
				class="toggle-btn" 
				class:active={viewMode === 'original'} 
				onclick={() => viewMode = 'original'}
			>
				Original
			</button>
			<button 
				class="toggle-btn" 
				class:active={viewMode === 'english'} 
				onclick={() => viewMode = 'english'}
			>
				English
			</button>
		</div>
	</nav>

	<article>
		<header>
			<h1>{data.book.name}</h1>
			<p class="subtitle">
				{#if viewMode === 'english'}
					Sovereign Forensic Reconstruction
				{:else}
					{data.book.language} Holographic Source
				{/if}
			</p>
		</header>

		{#if viewMode === 'original'}
			<div class="content-view original-text {data.book.language.toLowerCase()}">
				{data.content}
			</div>
		{:else}
			<div class="content-view sota-units">
				{#if data.units && data.units.length > 0}
					{#each data.units as unit (unit.index)}
						<section class="unit-card" id="unit-{unit.index}">
							<div class="unit-header">
								<div class="unit-meta">
									<span class="unit-index">UNIT {unit.index}</span>
									{#if unit['forensic-confidence'] > 0}
										<span class="confidence-badge" class:low={unit['forensic-confidence'] < 70} title="Forensic Confidence Score">
											{unit['forensic-confidence']}% Forensic Certainty
										</span>
									{/if}
								</div>
								<div class="audio-controls">
									<button 
										class="audio-btn original" 
										onclick={() => handlePlay(unit, 'orig')}
										title="Play Original"
									>
										<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
											<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
											<path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
										</svg>
										<span>{data.book.language === 'Greek' ? 'GRK' : 'HBW'}</span>
									</button>
									<button 
										class="audio-btn main" 
										onclick={() => handlePlay(unit, 'en')}
										title="Play Translation"
									>
										<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
											<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
											<path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
										</svg>
										<span>ENG</span>
									</button>
								</div>
								<div class="unit-nav-arrows">
									{#if unit.index > 1}
										<a href="#unit-{unit.index - 1}" class="nav-arrow" title="Previous Unit">
											<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 15l-6-6-6 6"/></svg>
										</a>
									{/if}
									{#if unit.index < data.units.length}
										<a href="#unit-{unit.index + 1}" class="nav-arrow" title="Next Unit">
											<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
										</a>
									{/if}
								</div>
							</div>

							<div class="field-group translation">
								<p class="main-translation"><ForensicText text={unit['main-translation']} /></p>
								<div class="original-sentence-highlightable {data.book.language.toLowerCase()}">
									{#each unit.words as word, i (i)}
										<button 
											class="word-btn" 
											class:active={activeWord?.unit === unit.index && activeWord?.word === word}
											onclick={() => setActiveWord(unit.index, word)}
										>
											{word}
										</button>
									{/each}
								</div>
							</div>

							<details class="forensic-details">
								<summary>Forensic Metadata</summary>
								
								<div class="field-group">
									<span class="field-label">LITERAL MIRROR (Interlinear)</span>
									<div class="interlinear-table">
										{#each unit.words as word, i (i)}
											<div class="interlinear-pair">
												<span class="inter-orig {data.book.language.toLowerCase()}">{word}</span>
												<span class="inter-gloss">{Array.isArray(unit['literal-translation']) ? (unit['literal-translation'][i] || '...') : (i === 0 ? (unit['literal-translation'] || '...') : '...')}</span>
											</div>
										{/each}
									</div>
								</div>

								{#if Object.keys(unit['grammatical-notes'] || {}).length > 0}
									<div class="field-group">
										<span class="field-label">GRAMMATICAL DEPTH</span>
										<div class="grammatical-grid">
											{#each Object.entries(unit['grammatical-notes']) as [word, note], i (i)}
												<div class="grammatical-item">
													<span class="grammatical-word">{word}</span>
													<span class="grammatical-note">{note}</span>
												</div>
											{/each}
										</div>
									</div>
								{/if}

								<div class="field-group">
									<span class="field-label">DICTIONARY CONVERGENCE</span>
									<div class="dictionary-grid">
										{#each Object.entries(unit['dictionary-meaning']) as [word, meaning] (word)}
											<div 
												class="dict-item" 
												class:highlighted={activeWord?.unit === unit.index && activeWord?.word === word}
												id="dict-{unit.index}-{word}"
											>
												<span class="dict-word">{word}</span>
												<div class="dict-structured">
													{#each Object.entries(parseDictEntry(String(meaning))) as [key, val], j (j)}
														<div class="dict-row">
															<span class="dict-key">{key}</span>
															<span class="dict-val">{val}</span>
														</div>
													{/each}
												</div>
											</div>
										{/each}
									</div>
								</div>

								<div class="field-group">
									<span class="field-label">ADVERSARIAL CONVERGENCE</span>
									<div class="adversarial-list">
										{#each getExplanationEntries(unit['main-translation-explanation']) as [phrase, justification], i (i)}
											<div class="adversarial-entry">
												<span class="adversarial-phrase">"{phrase}"</span>
												<span class="adversarial-reason">{justification}</span>
											</div>
										{/each}
										{#if (unit['rejected-translations'] || []).length > 0}
											<div class="rejected-section">
												<span class="inner-label">EXPLICITLY REJECTED</span>
												{#each unit['rejected-translations'] as rejected, i (i)}
													<div class="rejected-entry">
														<span class="rejected-phrase">
															"{typeof rejected === 'object' ? rejected.phrase : rejected}"
														</span>
														{#if typeof rejected === 'object' && rejected.reason}
															<span class="rejected-reason">— {rejected.reason}</span>
														{/if}
													</div>
												{/each}
											</div>
										{/if}
									</div>
								</div>

								{#if Object.keys(unit['polysemy-log'] || {}).length > 0}
									<div class="field-group">
										<span class="field-label">POLYSEMY RESOLUTION (Rule 68)</span>
										<div class="polysemy-grid">
											{#each Object.entries(unit['polysemy-log']) as [word, data] (word)}
												<div class="polysemy-item">
													<span class="polysemy-word">{word}</span>
													<div class="polysemy-details">
														<span class="polysemy-options">Options: {data.options?.join(', ') || '...'}</span>
														<span class="polysemy-chosen">Chosen: <strong>{data.chosen}</strong></span>
														<span class="polysemy-reason">Reason: {data.reason}</span>
													</div>
												</div>
											{/each}
										</div>
									</div>
								{/if}

								<div class="field-group">
									<span class="field-label">RULES APPLIED</span>
									<div class="rules-tags">
										{#each unit['rules-applied'] as rule (rule)}
											<span class="rule-tag" title={RULE_NAMES[rule] ?? 'Unknown Rule'}>RULE {rule} — {RULE_NAMES[rule] ?? '?'}</span>
										{/each}
									</div>
								</div>
							</details>
						</section>
					{/each}
				{:else}
					<div class="placeholder">
						<p>SOTA Reconstruction for {data.book.name} is in progress.</p>
						<p class="small">Units are currently being populated through Wave cycles.</p>
					</div>
				{/if}
			</div>
		{/if}
	</article>
</div>

<style>
	:root {
		--bg-dark: #0a0a0a;
		--card-bg: rgba(255, 255, 255, 0.03);
		--accent-gold: #c5a059;
		--accent-blue: #4a90e2;
		--text-muted: #888;
	}

	.reading-container {
		max-width: 900px;
		margin: 0 auto;
		padding: 2rem;
		font-family: 'Inter', sans-serif;
	}

	.top-nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 4rem;
	}

	.back-link {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		text-decoration: none;
		color: var(--text-muted);
		font-weight: 500;
		transition: color 0.2s;
	}

	.toggle-container {
		display: flex;
		background: rgba(255, 255, 255, 0.05);
		padding: 4px;
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.toggle-btn {
		padding: 0.5rem 1.25rem;
		border-radius: 8px;
		border: none;
		background: transparent;
		color: var(--text-muted);
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s;
	}

	.toggle-btn.active {
		background: rgba(255, 255, 255, 0.1);
		color: #fff;
	}

	header {
		margin-bottom: 5rem;
		text-align: center;
	}

	header h1 {
		font-size: 4rem;
		font-weight: 800;
		letter-spacing: -0.05em;
		margin: 0;
		background: linear-gradient(to bottom, #fff, #888);
		-webkit-background-clip: text;
		background-clip: text;
		-webkit-text-fill-color: transparent;
	}

	.subtitle {
		color: var(--accent-gold);
		text-transform: uppercase;
		font-weight: 700;
		letter-spacing: 0.2em;
		font-size: 0.75rem;
		margin-top: 1rem;
	}

	.unit-card {
		background: var(--card-bg);
		border: 1px solid rgba(255, 255, 255, 0.05);
		border-radius: 24px;
		padding: 2.5rem;
		margin-bottom: 3rem;
		transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s;
	}

	.unit-card:hover {
		transform: translateY(-4px);
		border-color: rgba(197, 160, 89, 0.2);
	}

	.unit-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2rem;
	}

	.unit-index {
		font-size: 0.7rem;
		font-weight: 900;
		color: var(--text-muted);
		letter-spacing: 0.1em;
		background: rgba(255, 255, 255, 0.05);
		padding: 0.25rem 0.75rem;
		border-radius: 100px;
	}

	.unit-meta {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.confidence-badge {
		font-size: 0.6rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: #4ade80;
		background: rgba(74, 222, 128, 0.1);
		padding: 0.25rem 0.6rem;
		border-radius: 6px;
		border: 1px solid rgba(74, 222, 128, 0.2);
	}

	.confidence-badge.low {
		color: #f87171;
		background: rgba(248, 113, 113, 0.1);
		border-color: rgba(248, 113, 113, 0.2);
	}

	.unit-nav-arrows {
		display: flex;
		gap: 0.5rem;
	}

	.nav-arrow {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 28px;
		height: 28px;
		background: rgba(255,255,255,0.05);
		border: 1px solid rgba(255,255,255,0.1);
		border-radius: 6px;
		color: var(--text-muted);
		transition: all 0.2s;
	}

	.nav-arrow:hover {
		background: rgba(197, 160, 89, 0.1);
		border-color: var(--accent-gold);
		color: var(--accent-gold);
	}

	.audio-controls {
		display: flex;
		gap: 0.75rem;
	}

	.audio-btn {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: #fff;
		padding: 0.4rem 0.8rem;
		border-radius: 8px;
		cursor: pointer;
		font-size: 0.65rem;
		font-weight: 700;
		transition: all 0.2s;
	}

	.audio-btn:hover {
		background: rgba(255, 255, 255, 0.1);
		border-color: var(--accent-gold);
	}

	.main-translation {
		font-size: 1.6rem;
		line-height: 1.6;
		color: #efefef;
		font-weight: 400;
		margin: 0;
	}

	.main-translation :global(em) {
		color: var(--accent-gold);
		font-style: normal;
		font-weight: 600;
		border-bottom: 1px solid rgba(197, 160, 89, 0.3);
	}

	.forensic-details {
		margin-top: 2rem;
		padding-top: 2rem;
		border-top: 1px solid rgba(255, 255, 255, 0.05);
	}

	.forensic-details summary {
		font-size: 0.7rem;
		font-weight: 700;
		color: var(--text-muted);
		text-transform: uppercase;
		letter-spacing: 0.1em;
		cursor: pointer;
		list-style: none;
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.forensic-details summary::before {
		content: '+';
		font-size: 1.2rem;
		color: var(--accent-gold);
	}

	.field-group {
		margin-top: 2rem;
	}

	.field-label {
		display: block;
		font-size: 0.6rem;
		font-weight: 900;
		color: var(--accent-gold);
		letter-spacing: 0.15em;
		margin-bottom: 0.75rem;
		opacity: 0.8;
		text-transform: uppercase;
	}

	.interlinear-table {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
		background: rgba(0,0,0,0.2);
		padding: 1.5rem;
		border-radius: 16px;
		border: 1px solid rgba(255,255,255,0.05);
	}

	.interlinear-pair {
		display: flex;
		flex-direction: column;
		align-items: center;
		min-width: 60px;
		padding: 0.5rem;
		border-radius: 8px;
		transition: background 0.2s;
	}

	.interlinear-pair:hover {
		background: rgba(255,255,255,0.05);
	}

	.inter-orig {
		font-size: 1.1rem;
		color: #fff;
		margin-bottom: 0.25rem;
	}

	.inter-gloss {
		font-size: 0.65rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--accent-gold);
		opacity: 0.8;
	}

	.jump-control input {
		background: rgba(255,255,255,0.05);
		border: 1px solid rgba(255,255,255,0.1);
		border-radius: 8px;
		padding: 0.4rem 0.8rem;
		color: #fff;
		font-size: 0.75rem;
		width: 120px;
		outline: none;
		transition: border-color 0.2s;
	}

	.jump-control input:focus {
		border-color: var(--accent-gold);
	}

	.dictionary-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: 1rem;
	}

	.dict-item {
		background: rgba(0, 0, 0, 0.3);
		padding: 1.25rem;
		border-radius: 16px;
		border: 1px solid rgba(255, 255, 255, 0.05);
		border-left: 4px solid var(--accent-gold);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.dict-item.highlighted {
		background: rgba(197, 160, 89, 0.1);
		border-color: var(--accent-gold);
		transform: scale(1.02);
		box-shadow: 0 0 20px rgba(197, 160, 89, 0.2);
	}

	.dict-word {
		display: block;
		font-size: 1.2rem;
		font-weight: 800;
		color: #fff;
		margin-bottom: 0.75rem;
		border-bottom: 1px solid rgba(255,255,255,0.1);
		padding-bottom: 0.5rem;
	}

	.dict-structured { display: flex; flex-direction: column; gap: 0.4rem; }
	.dict-row { 
		display: grid; 
		grid-template-columns: 80px 1fr; 
		gap: 1rem; 
		align-items: baseline; 
	}
	.dict-key { 
		font-size: 0.55rem; 
		font-weight: 900; 
		color: var(--accent-gold); 
		letter-spacing: 0.1em; 
		text-transform: uppercase; 
		opacity: 0.8;
	}
	.dict-val { font-size: 0.75rem; color: #bbb; line-height: 1.4; }

	.original-sentence-highlightable {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
		margin-top: 1.5rem;
		padding-top: 1.5rem;
		border-top: 1px solid rgba(255,255,255,0.05);
	}

	.word-btn {
		background: transparent;
		border: 1px solid rgba(255,255,255,0.1);
		color: #888;
		padding: 0.2rem 0.6rem;
		border-radius: 6px;
		font-size: 1rem;
		cursor: pointer;
		transition: all 0.2s;
	}

	.word-btn:hover {
		background: rgba(255,255,255,0.05);
		color: #fff;
	}

	.word-btn.active {
		background: var(--accent-gold);
		color: #000;
		border-color: var(--accent-gold);
		font-weight: 700;
	}

	.adversarial-list { display: flex; flex-direction: column; gap: 0.75rem; }
	.adversarial-entry { background: rgba(0,0,0,0.2); border-left: 2px solid rgba(197,160,89,0.4); padding: 0.6rem 0.8rem; border-radius: 0 8px 8px 0; }
	.adversarial-phrase { display: block; font-size: 0.78rem; font-weight: 700; color: var(--accent-gold); margin-bottom: 0.25rem; }
	.adversarial-reason { font-size: 0.72rem; color: #999; font-style: italic; line-height: 1.5; }

	.rejected-section { margin-top: 1rem; padding-top: 1rem; border-top: 1px dashed rgba(255,255,255,0.1); }
	.inner-label { font-size: 0.55rem; font-weight: 900; color: #f87171; letter-spacing: 0.1em; margin-bottom: 0.5rem; display: block; opacity: 0.7; }
	.rejected-entry { font-size: 0.72rem; margin-bottom: 0.35rem; }
	.rejected-phrase { color: #f87171; font-weight: 600; text-decoration: line-through; opacity: 0.8; }
	.rejected-reason { color: #777; font-style: italic; }

	.grammatical-grid, .polysemy-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1rem; }
	.grammatical-item, .polysemy-item { background: rgba(0,0,0,0.2); padding: 0.8rem; border-radius: 10px; border-left: 2px solid var(--accent-blue); }
	.grammatical-word, .polysemy-word { display: block; font-size: 0.85rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem; }
	.grammatical-note { font-size: 0.7rem; color: #999; line-height: 1.4; }
	.polysemy-details { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.65rem; color: #888; }
	.polysemy-chosen strong { color: var(--accent-gold); }

	.rules-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; }
	.rule-tag {
		font-size: 0.6rem;
		font-weight: 700;
		background: rgba(74, 144, 226, 0.08);
		color: var(--accent-blue);
		padding: 0.25rem 0.7rem;
		border-radius: 4px;
		border: 1px solid rgba(74, 144, 226, 0.2);
		cursor: default;
	}

	.placeholder {
		text-align: center;
		padding: 6rem 2rem;
		background: var(--card-bg);
		border-radius: 32px;
		border: 1px dashed rgba(255, 255, 255, 0.1);
	}

	.hebrew {
		direction: rtl;
		font-family: 'SBL Hebrew', serif;
	}
</style>

