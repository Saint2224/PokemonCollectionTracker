import re, urllib.parse, urllib.request
H={'User-Agent':'Mozilla/5.0'}
queries=['30th Anniversary Pokemon','Pokemon 30th Anniversary','ME06 Pokemon']
for q in queries:
    u='https://explore.justtcg.com/search?q='+urllib.parse.quote(q)
    t=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=45).read().decode('utf-8','ignore')
    ids=[]
    for p in [r'\\"id\\":\\"(pokemon-[^\\"]+)\\"', r'"id":"(pokemon-[^"]+)"']:
        ids.extend(re.findall(p,t))
    uniq=[]
    for i in ids:
        base=i.split('_',1)[0]
        if base not in uniq:
            uniq.append(base)
    filt=[x for x in uniq if ('anniversary' in x.lower() or 'me06' in x.lower() or '30th' in x.lower())]
    print('\nQ:',q,'all_ids',len(uniq),'filtered',len(filt))
    for x in filt[:120]:
        print(x)
