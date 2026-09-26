import re
from pathlib import Path
t=Path('tmp_me30_rsc.txt').read_text(encoding='utf-8', errors='ignore')
# pull likely API-like paths/urls
patterns=[r'https://api\.justtcg\.com[^"\s<]+', r'/api/[^"\s<]+', r'cards\?[^"\s<]+', r'_rsc=[A-Za-z0-9_-]+']
for p in patterns:
    m=sorted(set(re.findall(p,t)))
    print('\nPAT',p,'count',len(m))
    for x in m[:40]:
        print(x)
# look for serialized objects around card counts
for kw in ['170 cards','card_count','cards_count','cardsCount','total','limit','offset','cursor','pageSize','hasMore']:
    i=t.lower().find(kw.lower())
    if i!=-1:
        print('\nKW',kw,'at',i)
        print(t[max(0,i-180):i+260])
