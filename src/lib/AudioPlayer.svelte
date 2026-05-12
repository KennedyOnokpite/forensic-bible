<script lang="ts">
	import { audioStore } from '$lib/stores/audioStore.svelte';
	import { fade, slide } from 'svelte/transition';

	let showVoices = $state(false);

	function togglePlay() {
		if (audioStore.isPaused) {
			audioStore.resumePlayback();
		} else {
			audioStore.pausePlayback();
		}
	}

	const speeds = [0.75, 1, 1.25, 1.5, 2];
</script>

{#if audioStore.isPlaying || audioStore.isPaused}
	<div class="audio-player-fixed" transition:slide={{ axis: 'y' }}>
		<div class="player-content">
			<div class="unit-info">
				<div class="playing-indicator">
					<div class="bar" class:active={!audioStore.isPaused}></div>
					<div class="bar" class:active={!audioStore.isPaused}></div>
					<div class="bar" class:active={!audioStore.isPaused}></div>
				</div>
				<div class="text-info">
					<span class="label">PLAYING UNIT</span>
					<span class="index">#{audioStore.currentUnitIndex}</span>
				</div>
			</div>

			<div class="main-controls">
				<button class="control-btn secondary" onclick={() => audioStore.stopPlayback()} title="Stop Playback" aria-label="Stop Playback">
					<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
						<rect x="6" y="6" width="12" height="12" rx="2" />
					</svg>
				</button>

				<button 
					class="control-btn primary" 
					onclick={togglePlay} 
					title={audioStore.isPaused ? 'Resume Playback' : 'Pause Playback'}
					aria-label={audioStore.isPaused ? 'Resume Playback' : 'Pause Playback'}
				>
					{#if audioStore.isPaused}
						<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
							<path d="M8 5v14l11-7z" />
						</svg>
					{:else}
						<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
							<rect x="6" y="4" width="4" height="16" rx="1" />
							<rect x="14" y="4" width="4" height="16" rx="1" />
						</svg>
					{/if}
				</button>
			</div>

			<div class="progress-section">
				<div class="progress-bar-bg">
					<div class="progress-fill" style="width: {audioStore.progress * 100}%"></div>
				</div>
			</div>

			<div class="settings-section">
				<div class="speed-control">
					{#each speeds as s (s)}
						<button 
							class="speed-btn" 
							class:active={audioStore.speed === s}
							onclick={() => audioStore.setSpeed(s)}
							aria-label="Set speed to {s}x"
						>
							{s}x
						</button>
					{/each}
				</div>

				<div class="voice-picker">
					<button 
						class="settings-btn" 
						class:active={audioStore.continuous}
						onclick={() => audioStore.continuous = !audioStore.continuous} 
						title="Continuous Playback" 
						aria-label="Toggle Continuous Playback"
					>
						<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
							<path d="M17 2l4 4-4 4" />
							<path d="M3 11v-1a4 4 0 0 1 4-4h14" />
							<path d="M7 22l-4-4 4-4" />
							<path d="M21 13v1a4 4 0 0 1-4 4H3" />
						</svg>
					</button>
				</div>

				<div class="voice-picker">
					<button class="settings-btn" onclick={() => showVoices = !showVoices} title="Select Voice" aria-label="Select Voice">
						<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
							<circle cx="12" cy="12" r="3" />
							<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33 1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1-2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82 1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
						</svg>
					</button>

					{#if showVoices}
						<div class="voice-dropdown" transition:fade>
							<div class="dropdown-header">Select Voice</div>
							<div class="voice-list">
								{#each audioStore.availableVoices as v (v.name)}
									<button 
										class="voice-item" 
										class:active={audioStore.voice?.name === v.name}
										onclick={() => { audioStore.setVoice(v); showVoices = false; }}
										aria-label="Use voice {v.name}"
									>
										<span class="v-name">{v.name}</span>
										<span class="v-lang">{v.lang}</span>
									</button>
								{/each}
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.audio-player-fixed {
		position: fixed;
		bottom: 2rem;
		left: 50%;
		transform: translateX(-50%);
		width: calc(100% - 4rem);
		max-width: 800px;
		background: rgba(15, 15, 15, 0.85);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 24px;
		padding: 1rem 2rem;
		z-index: 1000;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
	}

	.player-content {
		display: flex;
		align-items: center;
		gap: 2rem;
	}

	.unit-info {
		display: flex;
		align-items: center;
		gap: 1rem;
		min-width: 140px;
	}

	.playing-indicator {
		display: flex;
		align-items: flex-end;
		gap: 2px;
		height: 16px;
	}

	.bar {
		width: 3px;
		height: 100%;
		background: #c5a059;
		border-radius: 1px;
	}

	.bar.active {
		animation: bounce 0.8s ease-in-out infinite alternate;
	}

	.bar:nth-child(2) { animation-delay: 0.2s; }
	.bar:nth-child(3) { animation-delay: 0.4s; }

	@keyframes bounce {
		0% { height: 30%; }
		100% { height: 100%; }
	}

	.text-info {
		display: flex;
		flex-direction: column;
	}

	.label { font-size: 0.55rem; font-weight: 800; color: #666; letter-spacing: 0.1em; }
	.index { font-size: 0.9rem; font-weight: 800; color: #fff; }

	.main-controls {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.control-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		border: none;
		cursor: pointer;
		transition: all 0.2s;
	}

	.control-btn.primary {
		width: 48px;
		height: 48px;
		background: #fff;
		color: #000;
	}

	.control-btn.secondary {
		width: 36px;
		height: 36px;
		background: rgba(255, 255, 255, 0.1);
		color: #fff;
	}

	.control-btn:hover { transform: scale(1.05); }

	.progress-section {
		flex: 1;
	}

	.progress-bar-bg {
		height: 6px;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 100px;
		overflow: hidden;
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(90deg, #c5a059, #fff);
		transition: width 0.1s linear;
	}

	.settings-section {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	.speed-control {
		display: flex;
		background: rgba(255, 255, 255, 0.05);
		padding: 2px;
		border-radius: 8px;
	}

	.speed-btn {
		padding: 0.25rem 0.5rem;
		font-size: 0.65rem;
		font-weight: 700;
		color: #888;
		background: transparent;
		border: none;
		cursor: pointer;
		border-radius: 6px;
	}

	.speed-btn.active { background: rgba(255, 255, 255, 0.1); color: #fff; }

	.voice-picker { position: relative; }

	.settings-btn {
		background: transparent;
		border: none;
		color: #888;
		cursor: pointer;
		transition: color 0.2s;
	}

	.settings-btn:hover, .settings-btn.active { color: #fff; }
	.settings-btn.active { color: #c5a059; }

	.voice-dropdown {
		position: absolute;
		bottom: 100%;
		right: 0;
		margin-bottom: 1.5rem;
		width: 240px;
		background: #1a1a1a;
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
		overflow: hidden;
	}

	.dropdown-header {
		padding: 0.75rem 1rem;
		font-size: 0.7rem;
		font-weight: 800;
		color: #666;
		text-transform: uppercase;
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
	}

	.voice-list { max-height: 300px; overflow-y: auto; }

	.voice-item {
		width: 100%;
		padding: 0.75rem 1rem;
		text-align: left;
		background: transparent;
		border: none;
		color: #aaa;
		display: flex;
		flex-direction: column;
		cursor: pointer;
		border-bottom: 1px solid rgba(255, 255, 255, 0.03);
	}

	.voice-item:hover { background: rgba(255, 255, 255, 0.05); color: #fff; }
	.voice-item.active { background: rgba(197, 160, 89, 0.15); color: #c5a059; }

	.v-name { font-size: 0.75rem; font-weight: 600; }
	.v-lang { font-size: 0.55rem; opacity: 0.6; }
</style>
