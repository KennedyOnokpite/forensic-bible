<script lang="ts">
	import { resolve } from '$app/paths';
	import books from '$lib/books.json';

	const oldBooks = books.filter(b => b.testament === 'Old');
	const newBooks = books.filter(b => b.testament === 'New');
</script>

<svelte:head>
	<title>The Original Scriptures | Forensic Biblical Explorer</title>
	<meta name="description" content="A forensic, 100%-accurate reconstruction of all 66 books of the Bible from their original Hebrew, Aramaic, and Koine Greek texts." />
</svelte:head>

<div class="container">
	<header class="header">
		<div class="header-badge">Forensic Biblical Explorer</div>
		<h1>The Original Scriptures</h1>
		<p>A pure, unadulterated Sovereign Forensic Reconstruction of the 66 books of the Bible — Hebrew, Aramaic &amp; Koine Greek.</p>
	</header>

	<div class="testament-section">
		<h2 class="testament-label">
			<span class="testament-line"></span>
			Old Testament <em>Hebrew &amp; Aramaic</em>
			<span class="testament-line"></span>
		</h2>
		<div class="book-grid">
			{#each oldBooks as book (book.id)}
				<a href={resolve('/book/' + book.slug)} class="book-card" id="book-{book.slug}">
					<span class="original-name">{book.original_language_name}</span>
					<span class="name">{book.name}</span>
					<span class="lang">{book.language}</span>
				</a>
			{/each}
		</div>
	</div>

	<div class="testament-section">
		<h2 class="testament-label">
			<span class="testament-line"></span>
			New Testament <em>Koine Greek</em>
			<span class="testament-line"></span>
		</h2>
		<div class="book-grid">
			{#each newBooks as book (book.id)}
				<a href={resolve('/book/' + book.slug)} class="book-card" id="book-{book.slug}">
					<span class="original-name">{book.original_language_name}</span>
					<span class="name">{book.name}</span>
					<span class="lang">{book.language}</span>
				</a>
			{/each}
		</div>
	</div>
</div>

<style>
	.container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 3rem 2rem 6rem;
	}

	.header {
		text-align: center;
		padding: 5rem 0 4rem;
	}

	.header-badge {
		display: inline-block;
		font-size: 0.65rem;
		font-weight: 800;
		letter-spacing: 0.25em;
		text-transform: uppercase;
		color: #c5a059;
		border: 1px solid rgba(197, 160, 89, 0.3);
		padding: 0.3rem 1rem;
		border-radius: 100px;
		margin-bottom: 1.5rem;
	}

	.header h1 {
		font-size: clamp(2.5rem, 6vw, 4.5rem);
		font-weight: 800;
		letter-spacing: -0.04em;
		margin: 0 0 1rem;
		background: linear-gradient(to bottom, #ffffff, #888888);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.header p {
		color: #888;
		font-size: 1.05rem;
		max-width: 560px;
		margin: 0 auto;
		line-height: 1.7;
	}

	.testament-section {
		margin-bottom: 4rem;
	}

	.testament-label {
		display: flex;
		align-items: center;
		gap: 1rem;
		font-size: 0.7rem;
		font-weight: 800;
		letter-spacing: 0.2em;
		text-transform: uppercase;
		color: #666;
		margin-bottom: 2rem;
	}

	.testament-label em {
		font-style: normal;
		color: #c5a059;
	}

	.testament-line {
		flex: 1;
		height: 1px;
		background: rgba(255,255,255,0.06);
	}

	.book-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
		gap: 1rem;
	}

	.book-card {
		background: rgba(255, 255, 255, 0.03);
		border: 1px solid rgba(255, 255, 255, 0.06);
		padding: 1.25rem 1rem;
		border-radius: 16px;
		text-decoration: none;
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		gap: 0.35rem;
		transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.book-card:hover {
		border-color: rgba(197, 160, 89, 0.35);
		background: rgba(197, 160, 89, 0.05);
		transform: translateY(-3px);
		box-shadow: 0 8px 24px rgba(0,0,0,0.4);
	}

	.original-name {
		font-size: 1.1rem;
		color: #c5a059;
		line-height: 1.2;
		min-height: 1.4rem;
	}

	.name {
		font-size: 0.85rem;
		font-weight: 700;
		color: #eee;
	}

	.lang {
		font-size: 0.6rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: #555;
	}
</style>
