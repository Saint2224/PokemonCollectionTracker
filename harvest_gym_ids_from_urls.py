import re
import json
import html as ihtml
import urllib.request
from urllib.parse import urljoin

SETS = [
    ('gymheroes', 'https://explore.justtcg.com/pokemon/gym-heroes-pokemon', '/pokemon/gym-heroes-pokemon/'),
    ('gymchallenge', 'https://explore.justtcg.com/pokemon/gym-challenge-pokemon', '/pokemon/gym-challenge-pokemon/'),
]

headers = {'User-Agent': 'Mozilla/5.0'}

def get(url):
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=45).read().decode('utf-8', 'ignore')

def extract_slug_and_num(detail_html, sid):
    text = ihtml.unescape(re.sub(r'<[^>]+>', ' ', detail_html))
    text = re.sub(r'\s+', ' ', text)
    slug_match = re.search(r'slug \(v1 id\):\s*([a-z0-9-]+)', text, re.I)
    if sid == 'gymheroes':
        num_match = re.search(r'Gym Heroes\s*#\s*(\d{1,3})\s*/\s*132', text, re.I)
    else:
        num_match = re.search(r'Gym Challenge\s*#\s*(\d{1,3})\s*/\s*132', text, re.I)
    if not slug_match or not num_match:
        return None, None
    return slug_match.group(1), int(num_match.group(1))

found = {}
report = {}

for sid, set_url, path_prefix in SETS:
    html = get(set_url)
    links = re.findall(r'href=["\'](' + re.escape(path_prefix) + r'pokemon-[^"\'#?]+)["\']', html)
    uniq = []
    for l in links:
        if l not in uniq:
            uniq.append(l)

    mapped = {}
    for rel in uniq:
        detail_url = urljoin('https://explore.justtcg.com', rel)
        try:
            dhtml = get(detail_url)
            slug, num = extract_slug_and_num(dhtml, sid)
        except Exception:
            continue

        if slug and num and 1 <= num <= 132 and num not in mapped:
            mapped[num] = slug
            found[f'{sid}-{num}'] = slug

    report[sid] = {
        'set_url': set_url,
        'links_found': len(uniq),
        'mapped_numbers': len(mapped),
        'min_num': min(mapped.keys()) if mapped else None,
        'max_num': max(mapped.keys()) if mapped else None,
        'mapped_numbers_list': sorted(mapped.keys()),
        'missing_under_132_count': len([n for n in range(1, 133) if n not in mapped]),
    }

text = open('index.html', 'r', encoding='utf-8').read()
replaced = 0
for key, slug in found.items():
    new_text, n = re.subn(rf'("{re.escape(key)}"\s*:\s*)(null|"[^"]*")', rf'\1"{slug}"', text, count=1)
    if n:
        replaced += 1
        text = new_text

open('index.html', 'w', encoding='utf-8', newline='').write(text)
open('justtcg_gym_url_scrape_report.json', 'w', encoding='utf-8').write(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
print('total_found', len(found), 'replaced', replaced)
