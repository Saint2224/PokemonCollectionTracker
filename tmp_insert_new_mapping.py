import re
from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

found_chaos = {
87:'pokemon-me04-chaos-rising-chespin-087-086-illustration-rare',88:'pokemon-me04-chaos-rising-froakie-088-086-illustration-rare',89:'pokemon-me04-chaos-rising-frogadier-089-086-illustration-rare',90:'pokemon-me04-chaos-rising-ampharos-090-086-illustration-rare',91:'pokemon-me04-chaos-rising-xerneas-091-086-illustration-rare',92:'pokemon-me04-chaos-rising-claydol-092-086-illustration-rare',93:'pokemon-me04-chaos-rising-crobat-093-086-illustration-rare',94:'pokemon-me04-chaos-rising-metang-094-086-illustration-rare',95:'pokemon-me04-chaos-rising-sliggoo-095-086-illustration-rare',96:'pokemon-me04-chaos-rising-tauros-096-086-illustration-rare',98:'pokemon-me04-chaos-rising-beedrill-ex-098-086-ultra-rare',99:'pokemon-me04-chaos-rising-mega-pyroar-ex-099-086-ultra-rare',100:'pokemon-me04-chaos-rising-mega-greninja-ex-100-086-ultra-rare',101:'pokemon-me04-chaos-rising-mega-floette-ex-101-086-ultra-rare',103:'pokemon-me04-chaos-rising-cobalion-ex-103-086-ultra-rare',104:'pokemon-me04-chaos-rising-mega-dragalge-ex-104-086-ultra-rare',105:'pokemon-me04-chaos-rising-cinccino-ex-105-086-ultra-rare',112:'pokemon-me04-chaos-rising-roxie-s-performance-112-086-ultra-rare',113:'pokemon-me04-chaos-rising-special-red-card-113-086-ultra-rare',116:'pokemon-me04-chaos-rising-mega-greninja-ex-116-086-special-illustration-rare',117:'pokemon-me04-chaos-rising-mega-floette-ex-117-086-special-illustration-rare',118:'pokemon-me04-chaos-rising-mega-dragalge-ex-118-086-special-illustration-rare',119:'pokemon-me04-chaos-rising-cinccino-ex-119-086-special-illustration-rare',120:'pokemon-me04-chaos-rising-az-s-tranquility-120-086-special-illustration-rare',121:'pokemon-me04-chaos-rising-roxie-s-performance-121-086-special-illustration-rare',122:'pokemon-me04-chaos-rising-mega-greninja-ex-122-086-mega-hyper-rare'
}
found_pitch = {
85:'pokemon-me05-pitch-black-fomantis-085-084-illustration-rare',86:'pokemon-me05-pitch-black-armarouge-086-084-illustration-rare',87:'pokemon-me05-pitch-black-goldeen-087-084-illustration-rare',88:'pokemon-me05-pitch-black-primarina-088-084-illustration-rare',89:'pokemon-me05-pitch-black-manectric-089-084-illustration-rare',90:'pokemon-me05-pitch-black-slowbro-090-084-illustration-rare',91:'pokemon-me05-pitch-black-dhelmise-091-084-illustration-rare',94:'pokemon-me05-pitch-black-toucannon-094-084-illustration-rare',97:'pokemon-me05-pitch-black-wailord-ex-097-084-ultra-rare',98:'pokemon-me05-pitch-black-mega-zeraora-ex-098-084-ultra-rare',99:'pokemon-me05-pitch-black-mega-chandelure-ex-099084-ultra-rare',101:'pokemon-me05-pitch-black-mega-darkrai-ex-101-084-ultra-rare',102:'pokemon-me05-pitch-black-morpeko-ex-102-084-ultra-rare',103:'pokemon-me05-pitch-black-mega-excadrill-ex-103-084-ultra-rare',106:'pokemon-me05-pitch-black-dark-bell-106084-ultra-rare',108:'pokemon-me05-pitch-black-gladion-s-final-battle-108-084-ultra-rare',109:'pokemon-me05-pitch-black-gwynn-109-084-ultra-rare',111:'pokemon-me05-pitch-black-misty-s-vitality-111-084-ultra-rare',114:'pokemon-me05-pitch-black-mega-zeraora-ex-114-084-special-illustration-rare',115:'pokemon-me05-pitch-black-mega-chandelure-ex-115084-special-illustration-rare',116:'pokemon-me05-pitch-black-mega-darkrai-ex-116084-special-illustration-rare',117:'pokemon-me05-pitch-black-morpeko-ex-117-084-special-illustration-rare',118:'pokemon-me05-pitch-black-gladion-s-final-battle-118084-special-illustration-rare',119:'pokemon-me05-pitch-black-gwynn-119084-special-illustration-rare',120:'pokemon-me05-pitch-black-mega-darkrai-ex-120084-mega-hyper-rare'
}

# Remove prior chaos/pitch mapping entries if present.
text = re.sub(r'\n\s*"chaosrising-\d+":\s*(?:null|"[^"]*"),?', '', text)
text = re.sub(r'\n\s*"pitchblack-\d+":\s*(?:null|"[^"]*"),?', '', text)

lines = []
for i in range(1, 123):
    v = found_chaos.get(i)
    lines.append(f'    "chaosrising-{i}": "{v}",' if v else f'    "chaosrising-{i}": null,')
for i in range(1, 121):
    v = found_pitch.get(i)
    tail = ',' if i < 120 else ''
    lines.append(f'    "pitchblack-{i}": "{v}"{tail}' if v else f'    "pitchblack-{i}": null{tail}')
block = '\n'.join(lines)

marker = '\n};\n    // PASTE YOUR ARRAYS HERE'
if marker not in text:
    raise SystemExit('Could not find mapping end marker')
text = text.replace(marker, '\n' + block + marker, 1)

path.write_text(text, encoding='utf-8', newline='')
print('Inserted chaosrising/pitchblack mapping entries')
