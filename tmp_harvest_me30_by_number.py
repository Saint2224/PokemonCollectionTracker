import re, time, urllib.parse, urllib.request, html as ihtml, json
H={'User-Agent':'Mozilla/5.0'}
BASE='https://explore.justtcg.com'
SET_PATH='me-30th-celebration-pokemon'

def get(url, timeout=45):
    return urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=timeout).read().decode('utf-8','ignore')

id_pat1=re.compile(r'\\"id\\":\\"(pokemon-me-30th-celebration-[^\\"]+)\\"')
id_pat2=re.compile(r'"id":"(pokemon-me-30th-celebration-[^"]+)"')
num_rxes=[
    re.compile(r'ME:\s*30th Celebration\s*-\s*(\d{1,3})\s*/\s*(\d{1,3})', re.I),
    re.compile(r'#\s*(\d{1,3})\s*/\s*(\d{1,3})', re.I),
]
name_rx=re.compile(r'<h1[^>]*>(.*?)</h1>', re.I|re.S)

candidates={}
for n in range(1,171):
    qs=[
        f'ME: 30th Celebration {n}/128',
        f'ME: 30th Celebration {n:03d}/128',
        f'{n}/128 ME: 30th Celebration',
        f'ME: 30th Celebration #{n}',
    ]
    found=[]
    for q in qs:
        try:
            u=BASE+'/search?q='+urllib.parse.quote(q)
            t=get(u)
        except Exception:
            continue
        ids=id_pat1.findall(t)+id_pat2.findall(t)
        for i in ids:
            b=i.split('_',1)[0]
            if b not in found:
                found.append(b)
        time.sleep(0.05)
    if found:
        candidates[n]=found

resolved=[]
seen=set()
for n, slugs in candidates.items():
    for slug in slugs:
        if slug in seen:
            continue
        seen.add(slug)
        try:
            d=get(f'{BASE}/pokemon/{SET_PATH}/{slug}')
        except Exception:
            continue
        txt=ihtml.unescape(re.sub(r'<[^>]+>',' ',d))
        txt=re.sub(r'\s+',' ',txt)
        num=None; denom=None
        for rx in num_rxes:
            m=rx.search(txt)
            if m:
                num=int(m.group(1)); denom=int(m.group(2)); break
        nm=''
        hm=name_rx.search(d)
        if hm:
            nm=ihtml.unescape(re.sub(r'<[^>]+>',' ',hm.group(1))).strip()
        if num is None:
            continue
        resolved.append({'num':num,'denom':denom,'slug':slug,'name':nm})
        time.sleep(0.05)

# dedupe by num preferring non-empty name and card-like slugs over product slugs
by_num={}
for r in sorted(resolved, key=lambda x: (x['num'], 0 if any(k in x['slug'] for k in ['-ex-','-gx-','-v-','-vmax-','-vstar-','-rare','-common','-uncommon']) else 1)):
    cur=by_num.get(r['num'])
    if not cur or (not cur['name'] and r['name']):
        by_num[r['num']]=r

out={
    'candidate_numbers':len(candidates),
    'unique_slugs_checked':len(seen),
    'resolved_entries':len(resolved),
    'unique_numbers':len(by_num),
    'min_num':min(by_num.keys()) if by_num else None,
    'max_num':max(by_num.keys()) if by_num else None,
    'numbers':sorted(by_num.keys()),
    'entries':[by_num[k] for k in sorted(by_num.keys())],
}
open('tmp_me30_number_harvest.json','w',encoding='utf-8').write(json.dumps(out,indent=2,ensure_ascii=False))
print(json.dumps({k:out[k] for k in ['candidate_numbers','unique_slugs_checked','resolved_entries','unique_numbers','min_num','max_num']}, indent=2))
print('saved tmp_me30_number_harvest.json')
