import re, urllib.request
url='https://explore.justtcg.com/pokemon/gym-heroes-pokemon/pokemon-gym-heroes-brock-s-rhydon-holo-rare'
html=urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=40).read().decode('utf-8','ignore')
print('len',len(html))
print('slug found', bool(re.search(r'slug \(v1 id\):\s*([a-z0-9-]+)', html, re.I)))
print('num found', bool(re.search(r'#\s*(\d{1,3})\s*/\s*132', html)))
for pat in [r'slug \(v1 id\):', r'ID:', r'/132', r'Brock']:
    i = re.search(pat, html, re.I)
    print(pat, 'idx', i.start() if i else None)
