import re, json
from pathlib import Path
p=Path(r'c:/Users/cajun/AppData/Roaming/Code/User/workspaceStorage/d7253fdd2d5ca2881dc3a2edd6ebc9c1/GitHub.copilot-chat/chat-session-resources/5cad80b4-d75b-4ac0-b9a3-1cfdba2d0db3/call_Bpq7CTqg1DszyljxE2W89jJH__vscode-1790406603335/content.txt')
t=p.read_text(encoding='utf-8', errors='ignore')
pat=r"- 'link \"(\d+) (.+?) ME: 30th Celebration Classic Collection - ([^\"$]+?) \$[^\"]*\" \[ref=[^\]]+\][\s\S]*?- /url: (/pokemon/me-30th-celebration-classic-collection-pokemon/([^\n]+))"
links=re.findall(pat, t)
print('matches',len(links))
rows=[]; seen=set()
for rank,name,num,href,slug in links:
    r=int(rank)
    if r in seen: continue
    seen.add(r)
    rows.append({'num':r,'name':name.strip(),'collector':num.strip(),'slug':slug.strip()})
rows.sort(key=lambda x:x['num'])
print('rows',len(rows))
for r in rows[:10]: print(r)
for r in rows[-5:]: print(r)
