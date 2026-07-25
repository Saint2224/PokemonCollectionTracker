import re
import urllib.request

urls = [
    'https://explore.justtcg.com/pokemon/gym-challenge-pokemon',
    'https://explore.justtcg.com/pokemon/gym-heroes-pokemon',
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'ignore')
    links = re.findall(r'href=["\'](/pokemon/[^"\'#?]+)["\']', html)
    uniq = []
    for l in links:
        if l not in uniq:
            uniq.append(l)
    print('\nURL', u, 'len', len(html), 'links', len(links), 'unique', len(uniq))
    print('sample:', uniq[:20])
