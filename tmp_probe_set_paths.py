import urllib.request, re
H={'User-Agent':'Mozilla/5.0'}
paths=[
 '30th-anniversary-pokemon',
 'me06-30th-anniversary-pokemon',
 'me6-30th-anniversary-pokemon',
 '30th-anniversary-celebration-pokemon',
 'anniversary-30th-pokemon',
 'me06-thirtieth-anniversary-pokemon',
 'me06-30th-anniversary-set-pokemon',
]
for p in paths:
    u='https://explore.justtcg.com/pokemon/'+p
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=45)
        t=r.read().decode('utf-8','ignore')
        ids=[]
        for pat in [r'\\"id\\":\\"(pokemon-[^\\"]+)\\"', r'"id":"(pokemon-[^"]+)"']:
            ids += re.findall(pat,t)
        print('\n',p,'status',getattr(r,'status',None),'len',len(t),'ids',len(ids),'anniv?',('anniversary' in t.lower()))
        if ids:
            seen=[]
            for i in ids:
                i=i.split('_',1)[0]
                if i not in seen: seen.append(i)
            for x in seen[:12]: print(' ',x)
    except Exception as e:
        print('\n',p,'ERR',e)
