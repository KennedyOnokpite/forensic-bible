/**
 * Sanitizes a string for use with {@html} by only allowing a whitelist of safe tags.
 * Primary targets: <em> for Rule 5, <strong> for emphasis, and <br>.
 */
export function sanitizeForensicHtml(html: string): string {
	if (!html) return '';
	
	// 1. Escape the entire string first to neutralize all tags
	const temp = html
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;')
		.replace(/'/g, '&#039;');

	// 2. Re-enable specifically whitelisted forensic tags
	return temp
		.replace(/&lt;em&gt;/g, '<em>')
		.replace(/&lt;\/em&gt;/g, '</em>')
		.replace(/&lt;strong&gt;/g, '<strong>')
		.replace(/&lt;\/strong&gt;/g, '</strong>')
		.replace(/&lt;br\s*\/?&gt;/g, '<br/>');
}
