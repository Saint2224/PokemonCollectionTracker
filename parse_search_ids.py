import urllib.parse, urllib.request, re
q = "Brock's Onix Gym Heroes"
u = 'https://explore.justtcg.com/search?q=' + urllib.parse.quote(q)
t = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=40).read().decode('utf-8','ignore')
patterns = [r'\\"id\\":\\"(pokemon-[^\\\"]+)\\"', r'"id":"(pokemon-[^"]+)"']
ids=[]
for p in patterns:
    ids += re.findall(p,t)
seen=[]
for x in ids:
    if x not in seen:
        seen.append(x)
print('ids',len(seen))
print(seen[:30])
print('contains gym heroes onix?', any('gym-heroes' in i and 'onix' in i for i in seen))
