import { error } from '@sveltejs/kit';
import booksRaw from '$lib/books.json';
import type { PageLoad } from './$types';
import type { ForensicUnit, BookMetadata } from '$lib/types';

const books = booksRaw as BookMetadata[];

// Vite requires static glob patterns at build time.
// We glob ALL unit files across ALL books once, then filter client-side by slug.
// This is the correct pattern for filesystem-driven SvelteKit apps.
// To keep the build memory sane, we use `import.meta.glob` with `lazy: true`
// so modules are only loaded on demand, not bundled eagerly.

const texts = import.meta.glob('/src/lib/books/**/*.txt', {
	query: '?raw',
	import: 'default',
	eager: false
});

const unitFiles = import.meta.glob('/src/lib/books/**/*.json', { eager: false });

export const load = (async ({ params }) => {
	const book = books.find((b) => b.slug.toLowerCase() === params.slug.toLowerCase());

	if (!book) {
		throw error(404, 'Book not found');
	}

	// Derive text filename
	const textFilename =
		book.slug === 'genesis' ? 'Gen_Hebrew.txt'
		: book.slug === 'revelation' ? 'Re_Greek.txt'
		: `${book.name.replace(/\s/g, '_')}_${book.language === 'Hebrew' ? 'Hebrew' : 'Greek'}.txt`;

	const textPath = `/src/lib/books/${book.slug}/${textFilename}`;
	const loadText = texts[textPath];

	try {
		const content = loadText ? ((await loadText()) as string) : '';

		// Filter to only numeric unit files for this book
		const bookUnits: ForensicUnit[] = [];
		const relevantFiles = Object.entries(unitFiles)
			.filter(([path]) => {
				if (!path.startsWith(`/src/lib/books/${book.slug}/`)) return false;
				const filename = path.split('/').pop() ?? '';
				return /^\d+\.json$/.test(filename);
			})
			.sort((a, b) => {
				const idA = parseInt(a[0].split('/').pop()!.replace('.json', ''));
				const idB = parseInt(b[0].split('/').pop()!.replace('.json', ''));
				return idA - idB;
			});

		for (const [, loader] of relevantFiles) {
			const unitModule = (await loader()) as { default: ForensicUnit };
			bookUnits.push(unitModule.default);
		}

		return { book, content, units: bookUnits };
	} catch (err) {
		console.error(err);
		throw error(500, `Error loading data for ${book.name}`);
	}
}) satisfies PageLoad;
