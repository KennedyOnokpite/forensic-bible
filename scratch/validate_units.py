"""
Forensic Unit Validator
=======================
Audits all 41,000+ JSON unit files against the forensic schema rules.
Produces a detailed report of violations.

Usage: python scratch/validate_units.py
"""
import os
import json
import hashlib
from collections import defaultdict

ROOT = r'c:\Users\onokp\Desktop\bible\src\lib\books'
VALID_RULES = set(range(1, 80))
REQUIRED_FIELDS = [
    'index', 'hash', 'source-language', 'sentence', 'words',
    'word-count-original', 'grammatical-notes', 'dictionary-meaning',
    'polysemy-log', 'literal-translation', 'main-translation',
    'main-translation-explanation', 'rejected-translations',
    'rules-applied', 'forensic-confidence'
]

violations = defaultdict(list)
stats = {
    'total': 0,
    'populated': 0,
    'empty': 0,
    'schema_violations': 0,
    'hash_mismatches': 0,
    'word_count_mismatches': 0,
    'invalid_rules': 0,
    'dict_key_mismatches': 0,
    'low_confidence': 0,
}

def check_unit(file_path, data):
    book = file_path.replace('\\', '/').split('/')[-2]
    unit_id = data.get('index', '?')
    label = f"{book}/{unit_id}"

    # 1. Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            violations['missing_field'].append(f"{label}: missing '{field}'")
            stats['schema_violations'] += 1

    # 2. Check word-count-original matches words array
    words = data.get('words', [])
    declared_count = data.get('word-count-original', -1)
    if declared_count != len(words):
        violations['word_count_mismatch'].append(
            f"{label}: declared {declared_count} words but words[] has {len(words)}"
        )
        stats['word_count_mismatches'] += 1

    # 3. Check invalid rule numbers
    rules = data.get('rules-applied', [])
    bad_rules = [r for r in rules if r not in VALID_RULES]
    if bad_rules:
        violations['invalid_rule'].append(f"{label}: invalid rules {bad_rules}")
        stats['invalid_rules'] += 1

    # 4. Check dict keys exist in words
    dict_keys = set(data.get('dictionary-meaning', {}).keys())
    word_set = set(words)
    orphan_keys = dict_keys - word_set
    if orphan_keys:
        violations['dict_key_mismatch'].append(
            f"{label}: dict keys not in words: {orphan_keys}"
        )
        stats['dict_key_mismatches'] += 1

    # 5. Flag low forensic confidence on populated units
    confidence = data.get('forensic-confidence', 0)
    has_translation = bool(data.get('main-translation'))
    if has_translation and confidence < 70:
        violations['low_confidence'].append(
            f"{label}: populated but confidence={confidence}"
        )
        stats['low_confidence'] += 1

    # 6. Track population stats
    stats['total'] += 1
    if has_translation:
        stats['populated'] += 1
    else:
        stats['empty'] += 1


def main():
    print("=== FORENSIC UNIT VALIDATOR ===\n")
    for root, dirs, files in os.walk(ROOT):
        for file in sorted(files):
            if not file.endswith('.json'):
                continue
            if not file.replace('.json', '').isdigit():
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    check_unit(path, data)
                except json.JSONDecodeError:
                    violations['json_error'].append(path)

    # Report
    print(f"TOTAL UNITS SCANNED : {stats['total']:,}")
    print(f"  Populated         : {stats['populated']:,}")
    print(f"  Empty             : {stats['empty']:,}")
    print(f"  Schema violations : {stats['schema_violations']:,}")
    print(f"  Word count errors : {stats['word_count_mismatches']:,}")
    print(f"  Invalid rules     : {stats['invalid_rules']:,}")
    print(f"  Dict key mismatches: {stats['dict_key_mismatches']:,}")
    print(f"  Low confidence    : {stats['low_confidence']:,}")

    if any(violations.values()):
        print("\n--- VIOLATION DETAILS ---")
        for vtype, items in violations.items():
            print(f"\n[{vtype.upper()}] ({len(items)} issues)")
            for item in items[:10]:  # Show first 10 of each type
                print(f"  {item}")
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more")
    else:
        print("\n[OK] All units passed forensic validation.")

if __name__ == '__main__':
    main()
