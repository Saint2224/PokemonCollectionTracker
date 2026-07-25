import re, urllib.request
u='https://explore.justtcg.com/pokemon/gym-heroes-pokemon'
html=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode('utf-8','ignore')
for pat in [r'page=\d+', r'next', r'__NEXT_DATA__', r'products', r'graphql', r'api/']:
    m=re.search(pat, html, re.I)
    print(pat, bool(m))
print('page links sample:', re.findall(r'href=["\']([^"\']*page=\d+[^"\']*)["\']', html)[:20])
print('contains _next/data:', '_next/data' in html)
print('contains application/ld+json:', 'application/ld+json' in html)
