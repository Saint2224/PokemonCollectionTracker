import re, urllib.request, urllib.parse
H={'User-Agent':'Mozilla/5.0'}
base='https://explore.justtcg.com/pokemon/me-30th-celebration-pokemon'
variants=[
    '?_rsc=1',
    '?limit=200&_rsc=1',
    '?pageSize=200&_rsc=1',
    '?perPage=200&_rsc=1',
    '?take=200&_rsc=1',
    '?count=200&_rsc=1',
    '?offset=0&limit=200&_rsc=1',
    '?sort=rank&limit=200&_rsc=1',
    '?view=all&_rsc=1',
    '?all=1&_rsc=1',
]
pat1=re.compile(r'\\"id\\":\\"(pokemon-me-30th-celebration-[^\\"]+)\\"')
pat2=re.compile(r'"id":"(pokemon-me-30th-celebration-[^"]+)"')
for q in variants:
    u=base+q
    try:
        t=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=45).read().decode('utf-8','ignore')
        ids=pat1.findall(t)+pat2.findall(t)
        uniq=[]
        for i in ids:
            b=i.split('_',1)[0]
            if b not in uniq:
                uniq.append(b)
        print(q, 'len',len(t),'uniq',len(uniq))
    except Exception as e:
        print(q, 'ERR', e)
