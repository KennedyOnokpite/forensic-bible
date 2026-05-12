export interface PolysemyEntry {
	options: string[];
	chosen: string;
	reason: string;
}

export interface RejectedTranslation {
	phrase: string;
	reason?: string;
}

export interface ForensicUnit {
	index: number;
	hash: string;
	'source-language': 'Hebrew' | 'Greek' | 'Aramaic';
	sentence: string;
	words: string[];
	'word-count-original': number;
	'grammatical-notes': Record<string, string>;
	'dictionary-meaning': Record<string, string>;
	'polysemy-log': Record<string, PolysemyEntry>;
	'literal-translation': string | string[];
	'main-translation': string;
	'main-translation-explanation': Record<string, string>;
	'rejected-translations': (string | RejectedTranslation)[];
	'rules-applied': number[];
	'forensic-confidence': number;
}

export interface BookMetadata {
	id: number;
	name: string;
	slug: string;
	language: 'Hebrew' | 'Greek';
	testament: 'Old' | 'New';
	canonical_order: number;
	original_language_name: string;
}
