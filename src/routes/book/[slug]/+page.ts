import { error } from '@sveltejs/kit';
import booksRaw from '$lib/books.json';
import type { PageLoad } from './$types';
import type { ForensicUnit, BookMetadata } from '$lib/types';

const books = booksRaw as (BookMetadata & { unit_count?: number })[];

export const load = (async ({ params, fetch }) => {
	const book = books.find((b) => b.slug.toLowerCase() === params.slug.toLowerCase());

	if (!book) {
		throw error(404, 'Book not found');
	}

	// Derive text filename
	const textFilename =
		book.slug === 'genesis' ? 'Gen_Hebrew.txt'
		: book.slug === 'revelation' ? 'Re_Greek.txt'
		: `${book.name.replace(/\s/g, '_')}_${book.language === 'Hebrew' ? 'Hebrew' : 'Greek'}.txt`;

	const textPath = `/data/books/${book.slug}/${textFilename}`;

	try {
		// Fetch text content
		const textRes = await fetch(textPath);
		const content = textRes.ok ? await textRes.text() : '';

		// Fetch all units in batches to avoid overwhelming the network/server
		const bookUnits: ForensicUnit[] = [];
		const unitCount = book.unit_count || 0;
		const BATCH_SIZE = 50;

		for (let i = 1; i <= unitCount; i += BATCH_SIZE) {
			const chunk = Array.from(
				{ length: Math.min(BATCH_SIZE, unitCount - i + 1) },
				(_, j) => i + j
			);
			
			const results = await Promise.all(
				chunk.map(id => 
					fetch(`/data/books/${book.slug}/${id}.json`).then(res => {
						if (!res.ok) throw new Error(`Failed to fetch unit ${id}`);
						return res.json() as Promise<ForensicUnit>;
					})
				)
			);
			bookUnits.push(...results);
		}

		return { book, content, units: bookUnits };
	} catch (err) {
		console.error(err);
		throw error(500, `Error loading data for ${book.name}`);
	}
}) satisfies PageLoad;
