import re
import urllib.parse
import urllib.request

H = {"User-Agent": "Mozilla/5.0"}
QUERIES = [
    "Weedle Chaos Rising",
    "Mega Darkrai ex Pitch Black",
    "Roxie's Performance Chaos Rising",
    "Mega Greninja ex 122/086 Chaos Rising",
]

for q in QUERIES:
    u = "https://explore.justtcg.com/search?q=" + urllib.parse.quote(q)
    t = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40).read().decode("utf-8", "ignore")
    links = re.findall(r'href=["\'](/pokemon/(?:me04-chaos-rising-pokemon|me05-pitch-black-pokemon)/pokemon-[^"\'#?]+)["\']', t)
    uniq = []
    for l in links:
        if l not in uniq:
            uniq.append(l)

    ids = []
    for p in [r'\\"id\\":\\"(pokemon-[^\\"]+)\\"', r'"id":"(pokemon-[^"]+)"']:
        ids.extend(re.findall(p, t))

    print(f"Q: {q}")
    print(f"  links: {len(uniq)} sample={uniq[:5]}")
    print(f"  ids:   {len(ids)} sample={ids[:5]}")
