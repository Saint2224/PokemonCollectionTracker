import re
import time
import urllib.parse
import urllib.request
import html as ihtml
import json

INDEX_PATH = r'c:\Users\cajun\OneDrive\Documents\Pokemon\CollectionTracker\PokemonCollectionTracker\index.html'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    text = f.read()


def parse_cards(array_name):
    m = re.search(rf'const\s+{array_name}\s*=\s*\[(.*?)\];', text, re.S)
    if not m:
        return {}
    block = m.group(1)
    pairs = re.findall(r'\{num:(\d+),name:"([^"]+)"\}', block)
    cards = {}
    for n, name in pairs:
        cards[int(n)] = name
    return cards


def current_map_value(sid, num):
    m = re.search(rf'"{sid}-{num}"\s*:\s*(null|"[^"]*")', text)
    if not m:
        return None
    v = m.group(1)
    return None if v == 'null' else v.strip('"')


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read().decode('utf-8', 'ignore')


def extract_ids_from_search_html(raw_html):
    ids = []
    for pat in [r'\\"id\\":\\"(pokemon-[^\\"]+)\\"', r'"id":"(pokemon-[^"]+)"']:
        ids.extend(re.findall(pat, raw_html))

    uniq = []
    seen = set()
    for cid in ids:
        base = cid.split('_', 1)[0]
        if base not in seen:
            seen.add(base)
            uniq.append(base)
    return uniq


def parse_detail_for_num(set_title, denom, slug, set_path, cache):
    if slug in cache:
        return cache[slug]
    url = f'https://explore.justtcg.com/pokemon/{set_path}/{slug}'
    try:
        raw = get(url)
    except Exception:
        cache[slug] = None
        return None

    plain = ihtml.unescape(re.sub(r'<[^>]+>', ' ', raw))
    plain = re.sub(r'\s+', ' ', plain)

    # Common pattern on JustTCG details: card title includes number like 121/086 or 116/084
    m = re.search(rf'(\d{{1,3}})\s*/\s*0?{denom}', plain)
    if m:
        cache[slug] = int(m.group(1))
        return cache[slug]

    # Fallback pattern if explicit set title + hash appears.
    m2 = re.search(rf'{re.escape(set_title)}\s*#\s*(\d{{1,3}})\s*/\s*0?{denom}', plain, re.I)
    if m2:
        cache[slug] = int(m2.group(1))
        return cache[slug]

    cache[slug] = None
    return None


def slug_number_matches(slug, target_num, denom):
    m = re.search(rf'-(\d{{3}})-0?{denom}(?:-|$)', slug)
    if m and int(m.group(1)) == target_num:
        return True
    m2 = re.search(rf'-(\d{{3}})0?{denom}(?:-|$)', slug)
    if m2 and int(m2.group(1)) == target_num:
        return True
    return False


def find_slug_for_card(name, num, set_name, set_prefix, set_path, denom, detail_cache):
    queries = [
        f'{name} {set_name} {num}/{denom}',
        f'{name} {set_name} {num:03d}/{denom:03d}',
        f'{name} {set_name} {num}',
        f'{name} {set_name}',
        f'{name}'
    ]

    for q in queries:
        u = 'https://explore.justtcg.com/search?q=' + urllib.parse.quote(q)
        try:
            raw = get(u)
        except Exception:
            continue

        base_ids = extract_ids_from_search_html(raw)
        candidates = [cid for cid in base_ids if cid.startswith(set_prefix)]
        if not candidates:
            continue

        # Prioritize candidates where slug itself encodes target number.
        candidates.sort(key=lambda c: (0 if slug_number_matches(c, num, denom) else 1, len(c)))

        for cid in candidates:
            if slug_number_matches(cid, num, denom):
                return cid

            parsed_num = parse_detail_for_num(set_name, denom, cid, set_path, detail_cache)
            if parsed_num == num:
                return cid

        time.sleep(0.08)

    return None


chaos_cards = parse_cards('chaosRisingCards')
pitch_cards = parse_cards('pitchBlackCards')

updates = {}
report = {}
detail_cache = {}

for sid, cards, set_name, set_prefix, set_path, denom in [
    ('chaosrising', chaos_cards, 'Chaos Rising', 'pokemon-me04-chaos-rising-', 'me04-chaos-rising-pokemon', 86),
    ('pitchblack', pitch_cards, 'Pitch Black', 'pokemon-me05-pitch-black-', 'me05-pitch-black-pokemon', 84),
]:
    mapped_before = 0
    mapped_after = 0
    attempted = 0
    found_now = 0

    for num in sorted(cards.keys()):
        attempted += 1
        existing = current_map_value(sid, num)
        if existing:
            mapped_before += 1
            mapped_after += 1
            continue

        slug = find_slug_for_card(cards[num], num, set_name, set_prefix, set_path, denom, detail_cache)
        if slug:
            updates[f'{sid}-{num}'] = slug
            mapped_after += 1
            found_now += 1

        time.sleep(0.10)

    report[sid] = {
        'attempted': attempted,
        'mapped_before': mapped_before,
        'newly_found': found_now,
        'mapped_after_estimate': mapped_after,
        'missing_after_estimate': attempted - mapped_after,
    }

new_text = text
replaced = 0
for key, slug in updates.items():
    new_text, n = re.subn(rf'("{re.escape(key)}"\s*:\s*)(null|"[^"]*")', rf'\1"{slug}"', new_text, count=1)
    replaced += n

with open(INDEX_PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(new_text)

for sid in ['chaosrising', 'pitchblack']:
    pairs = re.findall(rf'"{sid}-(\d+)"\s*:\s*(null|"[^"]*")', new_text)
    mapped = sum(1 for _, v in pairs if v != 'null')
    report[sid]['mapped_after_actual'] = mapped
    report[sid]['total_keys'] = len(pairs)
    report[sid]['missing_after_actual'] = len(pairs) - mapped

report['updates_written'] = len(updates)
report['replaced'] = replaced

with open('tmp_newset_backfill_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print(json.dumps(report, indent=2))
