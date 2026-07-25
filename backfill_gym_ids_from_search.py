import re
import time
import urllib.parse
import urllib.request
import html as ihtml

INDEX_PATH = 'c:\\Users\\cajun\\OneDrive\\Documents\\Pokemon\\CollectionTracker\\PokemonCollectionTracker\\index.html'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

def parse_cards(array_name):
    m = re.search(rf'const\s+{array_name}\s*=\s*\[(.*?)\];', text, re.S)
    if not m:
        return {}
    block = m.group(1)
    pairs = re.findall(r'\{num:(\d+),name:"([^"]+)"\}', block)
    return {int(n): name for n, name in pairs}

heroes_cards = parse_cards('gymHeroesCards')
challenge_cards = parse_cards('gymChallengeCards')

def current_map_value(sid, num):
    m = re.search(rf'"{sid}-{num}"\s*:\s*(null|"[^"]*")', text)
    if not m:
        return None
    v = m.group(1)
    if v == 'null':
        return None
    return v.strip('"')


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read().decode('utf-8', 'ignore')

def extract_ids_from_search_html(raw_html):
    ids = []
    for pat in [r'\\"id\\":\\"(pokemon-[^\\\"]+)\\"', r'"id":"(pokemon-[^"]+)"']:
        ids.extend(re.findall(pat, raw_html))
    uniq = []
    seen = set()
    for cid in ids:
        base = cid.split('_', 1)[0]
        if base not in seen:
            seen.add(base)
            uniq.append(base)
    return uniq

def parse_detail_for_num(set_path, slug):
    url = f'https://explore.justtcg.com/pokemon/{set_path}/{slug}'
    try:
        raw = get(url)
    except Exception:
        return None
    plain = ihtml.unescape(re.sub(r'<[^>]+>', ' ', raw))
    plain = re.sub(r'\s+', ' ', plain)
    if set_path == 'gym-heroes-pokemon':
        m = re.search(r'Gym Heroes\s*#\s*(\d{1,3})\s*/\s*132', plain, re.I)
    else:
        m = re.search(r'Gym Challenge\s*#\s*(\d{1,3})\s*/\s*132', plain, re.I)
    if not m:
        return None
    return int(m.group(1))

def find_slug_for_card(name, num, set_name, set_prefix, set_path):
    queries = [f'{name} {set_name}', f'{name}']
    for q in queries:
        u = 'https://explore.justtcg.com/search?q=' + urllib.parse.quote(q)
        try:
            raw = get(u)
        except Exception:
            continue

        base_ids = extract_ids_from_search_html(raw)
        candidates = [cid for cid in base_ids if cid.startswith(set_prefix)]

        # Prioritize IDs with the target number in slug.
        candidates.sort(key=lambda c: (f'-{num}-' not in c and not c.endswith(f'-{num}'), len(c)))

        for cid in candidates:
            parsed_num = parse_detail_for_num(set_path, cid)
            if parsed_num == num:
                return cid
        time.sleep(0.08)
    return None

updates = {}

for sid, cards, set_name, set_prefix, set_path in [
    ('gymheroes', heroes_cards, 'Gym Heroes', 'pokemon-gym-heroes-', 'gym-heroes-pokemon'),
    ('gymchallenge', challenge_cards, 'Gym Challenge', 'pokemon-gym-challenge-', 'gym-challenge-pokemon'),
]:
    for num in sorted(cards.keys()):
        if current_map_value(sid, num):
            continue
        slug = find_slug_for_card(cards[num], num, set_name, set_prefix, set_path)
        if slug:
            updates[f'{sid}-{num}'] = slug

new_text = text
replaced = 0
for key, slug in updates.items():
    new_text, n = re.subn(rf'("{re.escape(key)}"\s*:\s*)(null|"[^"]*")', rf'\1"{slug}"', new_text, count=1)
    replaced += n

with open(INDEX_PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(new_text)

# Coverage after update
for sid in ['gymheroes','gymchallenge']:
    pairs = re.findall(rf'"{sid}-(\d+)"\s*:\s*(null|"[^"]*")', new_text)
    mapped = sum(1 for _, v in pairs if v != 'null')
    print(sid, 'mapped', mapped, 'of', len(pairs))

print('new_updates', len(updates), 'replaced', replaced)
