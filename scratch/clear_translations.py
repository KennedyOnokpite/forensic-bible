import os
import json

VALID_RULES = set(range(1, 80))  # Rules 1-79

def clear_translation(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"ERROR decoding {file_path}")
            return

    # Determine source language from file path
    parts = file_path.replace('\\', '/').split('/')
    book_slug = parts[-2] if len(parts) >= 2 else ''
    hebrew_books = {
        'genesis','exodus','leviticus','numbers','deuteronomy','joshua','judges',
        'ruth','1-samuel','2-samuel','1-kings','2-kings','1-chronicles','2-chronicles',
        'ezra','nehemiah','esther','job','psalms','proverbs','ecclesiastes',
        'song-of-solomon','isaiah','jeremiah','lamentations','ezekiel','daniel',
        'hosea','joel','amos','obadiah','jonah','micah','nahum','habakkuk',
        'zephaniah','haggai','zechariah','malachi'
    }
    lang = 'Hebrew' if book_slug in hebrew_books else 'Greek'

    # Build new schema (preserve structural fields, reset translation fields)
    new_data = {
        "index": data.get("index", 0),
        "hash": data.get("hash", ""),
        "source-language": data.get("source-language", lang),
        "sentence": data.get("sentence", ""),
        "words": data.get("words", []),
        "word-count-original": len(data.get("words", [])),
        "grammatical-notes": data.get("grammatical-notes", {}),
        "dictionary-meaning": {},
        "polysemy-log": {},
        "literal-translation": "",
        "main-translation": "",
        "main-translation-explanation": {},
        "rejected-translations": [],
        "rules-applied": [],
        "forensic-confidence": 0
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print(f"Cleared: {file_path}")

def main():
    root_dir = r'c:\Users\onokp\Desktop\bible\src\lib\books'
    cleared = 0
    for root, dirs, files in os.walk(root_dir):
        for file in sorted(files):
            if not file.endswith('.json'):
                continue
            if not file.replace('.json', '').isdigit():
                continue  # Skip discourse_map.json etc.
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    has_work = bool(
                        data.get('main-translation') or
                        data.get('literal-translation') or
                        data.get('dictionary-meaning') or
                        data.get('rules-applied')
                    )
                    needs_schema_update = 'source-language' not in data or 'grammatical-notes' not in data
                    if has_work or needs_schema_update:
                        clear_translation(file_path)
                        cleared += 1
                except json.JSONDecodeError:
                    continue
    print(f"\nDone. {cleared} files updated to new schema.")

if __name__ == '__main__':
    main()
