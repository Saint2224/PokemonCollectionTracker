import hashlib, urllib.request
urls = {
 'chaos_front':'https://images.scrydex.com/pokemon/me4-1/small',
 'classic_1':'https://images.scrydex.com/pokemon/pokemon-me-30th-celebration-classic-collection-lugia-classic-collection/small',
 'classic_28':'https://images.scrydex.com/pokemon/pokemon-me-30th-celebration-classic-collection-zacian-v-classic-collection/small',
 'classic_29':'https://images.scrydex.com/pokemon/pokemon-me-30th-celebration-classic-collection-genesect-ex-team-plasma-classic-collection/small',
 'classic_30':'https://images.scrydex.com/pokemon/pokemon-me-30th-celebration-classic-collection-buzzwole-gx-classic-collection/small',
 'main_1':'https://images.scrydex.com/pokemon/pokemon-me-30th-celebration-mew-grgb-holo-rare/small',
 'main_22':'https://images.scrydex.com/pokemon/pokemon-me-30th-celebration-mew-ex-152-128-special-illustration-rare/small',
}
for k,u in urls.items():
    try:
        b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
        h=hashlib.sha256(b).hexdigest()[:16]
        print(k, len(b), h)
    except Exception as e:
        print(k, 'ERR', e)
