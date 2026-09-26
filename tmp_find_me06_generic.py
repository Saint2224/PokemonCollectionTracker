import re, urllib.parse, urllib.request
H={'User-Agent':'Mozilla/5.0'}
queries=['me06','me 06','30th anniversary','anniversary pokemon me06','pokemon me06 30th']
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
    me=[x for x in uniq if '-me0' in x or '-me' in x]
    print('\nQ',q,'total',len(uniq),'me*',len(me))
    for x in me[:120]:
        print(x)
