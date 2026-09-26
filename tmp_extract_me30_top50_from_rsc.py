import re
import html
from pathlib import Path

text = Path('tmp_me30_rsc.txt').read_text(encoding='utf-8', errors='ignore')

# Extract each set item anchor block
anchor_re = re.compile(
    r'<a href="/pokemon/me-30th-celebration-pokemon/(?P<slug>pokemon-me-30th-celebration-[^"]+)">(?P<body>.*?)</a>',
    re.S,
)
rank_re = re.compile(r'text-xs font-mono tabular-nums">(\d+)</div>')
title_re = re.compile(r'<h3[^>]*title="([^"]+)">')
collector_re = re.compile(r'title="ME: 30th Celebration">ME: 30th Celebration<span[^>]*> - <!-- -->([^<]+)</span>')

rows = []
seen = set()
for m in anchor_re.finditer(text):
    slug = m.group('slug')
    if slug in seen:
        continue
    seen.add(slug)
    body = m.group('body')

    rm = rank_re.search(body)
    tm = title_re.search(body)
    cm = collector_re.search(body)

    if not rm or not tm:
        continue

    rank = int(rm.group(1))
    name = html.unescape(tm.group(1)).strip()
    collector = html.unescape(cm.group(1)).strip() if cm else 'N/A'

    rows.append({
        'num': rank,
        'name': name,
        'collectorNum': collector,
        'imageToken': slug,
    })

rows.sort(key=lambda r: r['num'])

out_lines = []
out_lines.append('const thirtyAnniversaryMainCards = [')
for r in rows:
    nm = r['name'].replace('\\', '\\\\').replace('"', '\\"')
    cn = r['collectorNum'].replace('\\', '\\\\').replace('"', '\\"')
    it = r['imageToken'].replace('\\', '\\\\').replace('"', '\\"')
    out_lines.append(f'    {{num:{r["num"]},name:"{nm}",collectorNum:"{cn}",imageToken:"{it}"}},')
out_lines.append('];')

Path('tmp_me30_top50_array.txt').write_text('\n'.join(out_lines), encoding='utf-8')
Path('tmp_me30_top50_rows.json').write_text(__import__('json').dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'rows={len(rows)}')
