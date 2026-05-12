<script lang="ts">
	/**
	 * Renders forensic text safely without using {@html}.
	 * Specifically handles <em> tags for Rule 5 (Italicized Grouping).
	 */
	let { text = '' } = $props();

	// Parse string into chunks of { text: string, italic: boolean }
	let chunks = $derived.by(() => {
		if (!text) return [];
		
		const result: { text: string; italic: boolean }[] = [];
		const parts = text.split(/(<em>|<\/em>)/g);
		
		let isItalic = false;
		for (const part of parts) {
			if (part === '<em>') {
				isItalic = true;
			} else if (part === '</em>') {
				isItalic = false;
			} else if (part) {
				result.push({ text: part, italic: isItalic });
			}
		}
		return result;
	});
</script>

{#each chunks as chunk, i (i)}
	{#if chunk.italic}
		<em>{chunk.text}</em>
	{:else}
		<span>{chunk.text}</span>
	{/if}
{/each}
