import re
from pathlib import Path
p=Path(r'c:/Users/cajun/AppData/Roaming/Code/User/workspaceStorage/d7253fdd2d5ca2881dc3a2edd6ebc9c1/GitHub.copilot-chat/chat-session-resources/5cad80b4-d75b-4ac0-b9a3-1cfdba2d0db3/call_Bpq7CTqg1DszyljxE2W89jJH__vscode-1790406603335/content.txt')
t=p.read_text(encoding='utf-8', errors='ignore')
pat=r"- 'link \"(\d+) (.+?) ME: 30th Celebration Classic Collection - ([^\"$]+?) \$[^\"]*\" \[ref=[^\]]+\][\s\S]*?- /url: (/pokemon/me-30th-celebration-classic-collection-pokemon/([^\n]+))"
rows=[]; seen=set()
for rank,name,num,href,slug in re.findall(pat, t):
    r=int(rank)
    if r in seen: continue
    seen.add(r)
    name=name.replace('"','\\"')
    numtxt=num.strip().replace('"','\\"')
    rows.append((r,name,numtxt,slug.strip()))
rows.sort(key=lambda x:x[0])
print('const thirtyAnniversaryCards = [')
for r,name,numtxt,slug in rows:
    print(f'    {{num:{r},name:"{name}",collectorNum:"{numtxt}",imageToken:"{slug}"}},')
print('];')
