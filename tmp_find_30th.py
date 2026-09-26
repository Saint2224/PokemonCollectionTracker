import re, urllib.parse, urllib.request
H={'User-Agent':'Mozilla/5.0'}
queries=[
    '30th Anniversary Pokemon',
    'Pokemon 30th Anniversary',
    '30th Anniversary set pokemon',
    'ME06 Pokemon',
]
for q in queries:
    u='https://explore.justtcg.com/search?q='+urllib.parse.quote(q)
    t=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=45).read().decode('utf-8','ignore')
    links=re.findall(r'href=["\'](/pokemon/[^"\'#?]+)["\']',t)
    uniq=[]
    for l in links:
        if l not in uniq:
            uniq.append(l)
    print('\nQ:',q)
    print('len',len(t),'unique links',len(uniq))
    for l in uniq[:50]:
        print(l)
    print('contains anniversary?', 'anniversary' in t.lower())
