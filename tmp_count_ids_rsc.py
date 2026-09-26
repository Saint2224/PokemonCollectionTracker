import re
from pathlib import Path
t=Path('tmp_me30_rsc.txt').read_text(encoding='utf-8', errors='ignore')
ids = re.findall(r'\\"id\\":\\"(pokemon-[^\\"]+)\\"', t)
if not ids:
    ids = re.findall(r'"id":"(pokemon-[^"]+)"', t)
base=[]
for i in ids:
    b=i.split('_',1)[0]
    if b not in base:
        base.append(b)
print('raw',len(ids),'unique',len(base))
print('prefix me-30th count',sum(1 for b in base if 'pokemon-me-30th-celebration-' in b))
for x in base[:40]:
    print(x)
print('--- tail ---')
for x in base[-40:]:
    print(x)
