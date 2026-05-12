import os
import json

BOOKS_BASE_PATH = r"c:\Users\onokp\Desktop\bible\src\lib\books"

def get_unit_path(book_slug, index):
    return os.path.join(BOOKS_BASE_PATH, book_slug.lower(), f"{index}.json")

def load_unit(book_slug, index):
    path = get_unit_path(book_slug, index)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "index": index,
        "hash": "",
        "sentence": "",
        "words": [],
        "dictionary-meaning": {},
        "literal-translation": "",
        "main-translation": "",
        "main-translation-explanation": "",
        "rules-applied": [],
        "forensic-iterations": 1
    }

def save_unit(book_slug, index, data):
    path = get_unit_path(book_slug, index)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_field(batch_file, field_name, book_slug="genesis"):
    if not os.path.exists(batch_file):
        print(f"Batch file not found: {batch_file}")
        return

    with open(batch_file, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)

    for item in batch_data:
        index = item.get("index")
        if index is None: continue
        
        unit = load_unit(book_slug, index)
        
        # Special case for dictionary fields to merge instead of overwrite
        if field_name in ["dictionary-meaning", "main-translation-explanation"]:
            if not isinstance(unit.get(field_name), dict):
                unit[field_name] = {}
            unit[field_name].update(item.get(field_name, {}))
        else:
            unit[field_name] = item.get(field_name, unit.get(field_name))
            
        # Ensure sentence/words are updated if provided in the batch (usually dictionary batch carries these)
        if "sentence" in item: unit["sentence"] = item["sentence"]
        if "words" in item: unit["words"] = item["words"]
            
        save_unit(book_slug, index, unit)
        print(f"Updated {field_name} for unit {index}")
