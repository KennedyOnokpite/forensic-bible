import json, os, sys

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\onokp\Desktop\bible\static\data\books\genesis'
for i in range(1, 101):
    p = os.path.join(path, f'{i}.json')
    with open(p, encoding='utf-8') as f:
        u = json.load(f)
    wc = u.get('word-count-original', len(u.get('words', [])))
    sent = u.get('sentence', '')
    words = u.get('words', [])
    print(f'{i:3d} | w={wc:2d} | {sent}')
    print(f'     words: {json.dumps(words, ensure_ascii=False)}')
    print()
