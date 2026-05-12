import { error } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';
import booksRaw from '$lib/books.json';
import type { PageServerLoad } from './$types';
import type { ForensicUnit, BookMetadata } from '$lib/types';

const books = booksRaw as BookMetadata[];

export const load: PageServerLoad = async ({ params }) => {
	const book = books.find((b) => b.slug.toLowerCase() === params.slug.toLowerCase());

	if (!book) {
		throw error(404, 'Book not found');
	}

	const bookDir = path.join(process.cwd(), 'src', 'lib', 'books', book.slug);
	
	try {
		// Load text content
		const textFilename =
			book.slug === 'genesis' ? 'Gen_Hebrew.txt'
			: book.slug === 'revelation' ? 'Re_Greek.txt'
			: `${book.name.replace(/\s/g, '_')}_${book.language === 'Hebrew' ? 'Hebrew' : 'Greek'}.txt`;
		
		const textPath = path.join(bookDir, textFilename);
		let content = '';
		if (fs.existsSync(textPath)) {
			content = fs.readFileSync(textPath, 'utf-8');
		}

		// Load and sort unit JSON files
		const files = fs.readdirSync(bookDir);
		const unitFiles = files
			.filter(f => /^\d+\.json$/.test(f))
			.sort((a, b) => parseInt(a) - parseInt(b));

		const units: ForensicUnit[] = unitFiles.map(file => {
			const filePath = path.join(bookDir, file);
			return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
		});

		return {
			book,
			content,
			units
		};
	} catch (err) {
		console.error(`Error loading book ${book.slug}:`, err);
		throw error(500, `Failed to load forensic data for ${book.name}`);
	}
};
