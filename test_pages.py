import re, urllib.request
base='https://explore.justtcg.com/pokemon/gym-heroes-pokemon'
for p in range(1,9):
    u = base if p==1 else f'{base}?page={p}'
    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
    html=urllib.request.urlopen(req,timeout=30).read().decode('utf-8','ignore')
    links=re.findall(r'href=["\'](/pokemon/gym-heroes-pokemon/pokemon-gym-heroes-[^"\'#?]+)["\']', html)
    uniq=[]
    [uniq.append(x) for x in links if x not in uniq]
    print(p, len(uniq), uniq[:3])
