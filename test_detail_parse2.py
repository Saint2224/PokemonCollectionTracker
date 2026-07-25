import re, urllib.request, html as ihtml
url='https://explore.justtcg.com/pokemon/gym-heroes-pokemon/pokemon-gym-heroes-brock-s-rhydon-holo-rare'
raw=urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=40).read().decode('utf-8','ignore')
text=ihtml.unescape(re.sub(r'<[^>]+>',' ', raw))
text=re.sub(r'\s+',' ', text)
m1=re.search(r'slug \(v1 id\):\s*([a-z0-9-]+)', text, re.I)
m2=re.search(r'Gym Heroes\s*#\s*(\d{1,3})\s*/\s*132', text, re.I)
print('slug', m1.group(1) if m1 else None)
print('num', m2.group(1) if m2 else None)
print('text sample around slug:', text[text.lower().find('slug (v1 id)')-40:text.lower().find('slug (v1 id)')+120])
