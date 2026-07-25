import urllib.parse
import urllib.request
import re
import html as ihtml

q = "Brock's Onix Gym Heroes"
u = 'https://explore.justtcg.com/search?q=' + urllib.parse.quote(q)
t = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read().decode('utf-8', 'ignore')
tx = ihtml.unescape(re.sub(r'<[^>]+>', ' ', t))
tx = re.sub(r'\s+', ' ', tx)
links = re.findall(r'href=["\'](/pokemon/gym-heroes-pokemon/pokemon-gym-heroes-[^"\'#?]+)["\']', t)
print('url', u, 'len', len(t), 'links', len(links))
print('sample', links[:12])
idx = tx.find('Search Results')
print('snippet', tx[idx:idx+700] if idx >= 0 else tx[:700])
