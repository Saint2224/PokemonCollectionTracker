import re, json, time, html
import urllib.request
from urllib.parse import urljoin

HEAD={'User-Agent':'Mozilla/5.0'}

def get(url, retries=6):
    last=None
    for i in range(retries):
        try:
            req=urllib.request.Request(url, headers=HEAD)
            return urllib.request.urlopen(req, timeout=45).read().decode('utf-8','ignore')
        except Exception as e:
            last=e
            time.sleep(0.6*(i+1))
    raise last

SETS=[
    ('chaosrising','Chaos Rising','https://explore.justtcg.com/pokemon/me04-chaos-rising-pokemon','/pokemon/me04-chaos-rising-pokemon/'),
    ('pitchblack','Pitch Black','https://explore.justtcg.com/pokemon/me05-pitch-black-pokemon','/pokemon/me05-pitch-black-pokemon/'),
]

result={}
report={}

for sid,set_name,base,prefix in SETS:
    links=[]
    for page in range(1,9):
        u = base if page==1 else f'{base}?page={page}'
        try:
            t=get(u)
        except Exception as e:
            report.setdefault(sid,{})[f'page_{page}_err']=str(e)
            continue
        found=re.findall(r'href=["\'](' + re.escape(prefix) + r'pokemon-[^"\'#?]+)["\']', t)
        if not found and page > 1:
            break
        for f in found:
            if f not in links:
                links.append(f)

    mapped={}
    for rel in links:
        slug = rel.rsplit('/',1)[-1]
        detail=urljoin('https://explore.justtcg.com', rel)
        try:
            d=get(detail)
        except Exception:
            continue
        tx=html.unescape(re.sub(r'<[^>]+>',' ', d))
        tx=re.sub(r'\s+',' ', tx)
        m=re.search(re.escape(set_name) + r'\s*#\s*(\d{1,3})\s*(?:/\s*\d{1,3})?', tx, re.I)
        num=None
        if m:
            num=int(m.group(1))
        else:
            m2=re.search(r'-(\d{1,3})-(\d{3})-', slug)
            if m2:
                num=int(m2.group(1))
            else:
                m3=re.search(r'-(\d{3})(\d{3})-', slug)
                if m3:
                    num=int(m3.group(1).lstrip('0') or '0')

        if num and 1 <= num <= 200:
            key=f'{sid}-{num}'
            if key not in mapped:
                mapped[key]=slug

    result.update(mapped)
    nums=sorted(int(k.split('-')[1]) for k in mapped)
    report[sid]={
        'links_collected': len(links),
        'mapped': len(mapped),
        'min_num': nums[0] if nums else None,
        'max_num': nums[-1] if nums else None,
    }

with open('tmp_new_set_mapping.json','w',encoding='utf-8') as f:
    json.dump(result,f,indent=2)
with open('tmp_new_set_mapping_report.json','w',encoding='utf-8') as f:
    json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
print('total mapped',len(result))
