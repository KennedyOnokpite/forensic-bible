import os
import json

def mass_reset():
    base_path = os.path.abspath("../../src/lib/books")
    print(f"Targeting path: {base_path}")
    
    if not os.path.exists(base_path):
        print(f"ERROR: Path does not exist: {base_path}")
        return

    books = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    total_files = 0
    reset_files = 0

    print(f"--- Starting Clean Slate Protocol across {len(books)} books ---")

    for book in books:
        book_path = os.path.join(base_path, book)
        print(f"Processing book: {book}...", end="", flush=True)
        files = [f for f in os.listdir(book_path) if f.endswith('.json')]
        
        for filename in files:
            file_path = os.path.join(book_path, filename)
            total_files += 1
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check if we actually need to reset to save time
                needs_reset = any([
                    data.get('dictionary-meaning') != {},
                    data.get('literal-translation') != "",
                    data.get('main-translation') != "",
                    data.get('main-translation-explanation') != {},
                    data.get('rules-applied') != []
                ])

                if needs_reset:
                    data['dictionary-meaning'] = {}
                    data['literal-translation'] = ""
                    data['main-translation'] = ""
                    data['main-translation-explanation'] = {}
                    data['rules-applied'] = []
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    reset_files += 1
            except Exception as e:
                print(f"\nError resetting {file_path}: {e}")

        print(" Done.")

    print(f"\n--- Clean Slate Protocol Complete ---")
    print(f"Total files scanned: {total_files}")
    print(f"Total files actually reset: {reset_files}")

if __name__ == "__main__":
    mass_reset()
