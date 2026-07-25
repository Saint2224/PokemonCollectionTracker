import re
text=open('index.html','r',encoding='utf-8').read()
for sid in ['gymheroes','gymchallenge']:
    pairs=re.findall(rf'"{sid}-(\d+)"\s*:\s*(null|"[^"]*")', text)
    total=len(pairs)
    mapped=sum(1 for _,v in pairs if v!='null')
    missing=[int(n) for n,v in pairs if v=='null']
    print(sid, 'total', total, 'mapped', mapped, 'missing', total-mapped)
    print('missing sample', missing[:25])
