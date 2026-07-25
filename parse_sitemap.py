import re, urllib.request
u='https://explore.justtcg.com/sitemap.xml'
html=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode('utf-8','ignore')
print('len',len(html))
print('contains gym heroes path?', 'gym-heroes-pokemon' in html)
print('contains gym challenge path?', 'gym-challenge-pokemon' in html)
for pat in [r'https://[^"\']*gym-heroes-pokemon[^"\'\s<]*', r'https://[^"\']*gym-challenge-pokemon[^"\'\s<]*', r'"/pokemon/[^"\']*"']:
    m = re.findall(pat, html)
    print(pat, len(m))
print('first urls:', re.findall(r'https://[^"\'\s<]+', html)[:40])
