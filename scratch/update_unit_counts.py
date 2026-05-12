import json
import os

MANIFEST_PATH = r'c:\Users\onokp\Desktop\bible\src\lib\books.json'
BOOKS_DIR = r'c:\Users\onokp\Desktop\bible\static\data\books'

with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
    books = json.load(f)

for book in books:
    slug = book['slug']
    book_path = os.path.join(BOOKS_DIR, slug)
    if os.path.exists(book_path):
        unit_files = [f for f in os.listdir(book_path) if f.endswith('.json') and f[:-5].isdigit()]
        book['unit_count'] = len(unit_files)
    else:
        book['unit_count'] = 0
        print(f"Warning: Path not found for {slug}")

with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

print("Updated books.json with unit counts.")
