import json
import re
import time
import html as ihtml
import urllib.parse
import urllib.request
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}

SETS = {
    "chaosrising": {
        "title": "Chaos Rising",
        "path": "me04-chaos-rising-pokemon",
        "denom": 86,
        "array_name": "chaosRisingCards",
        "max_num": 122,
    },
    "pitchblack": {
        "title": "Pitch Black",
        "path": "me05-pitch-black-pokemon",
        "denom": 84,
        "array_name": "pitchBlackCards",
        "max_num": 120,
    },
}

INDEX = Path("index.html")
OUT_MAP = Path("tmp_new_set_mapping.json")
OUT_REPORT = Path("tmp_new_set_mapping_report.json")


def get(url: str, retries: int = 5, pause: float = 0.35) -> str:
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "ignore")
        except Exception as e:
            last = e
            time.sleep(pause * (i + 1))
    raise last


def parse_cards_from_index(text: str, array_name: str):
    m = re.search(rf"const\s+{re.escape(array_name)}\s*=\s*\[(.*?)\];", text, re.S)
    if not m:
        return []
    body = m.group(1)
    pairs = re.findall(r"\{num:(\d+),name:\\?\"((?:[^\\\"]|\\.)*)\\?\"", body)
    cards = []
    for num_s, name_raw in pairs:
        name = bytes(name_raw, "utf-8").decode("unicode_escape")
        cards.append({"num": int(num_s), "name": name})
    return cards


def extract_ids_from_search(html: str):
    ids = []
    # Most reliable source in current pages: escaped JSON chunks containing id fields.
    for pat in [r'\\\\\"id\\\\\":\\\\\"(pokemon-[^\\\\\"]+)\\\\\"', r'\"id\":\"(pokemon-[^\"]+)\"']:
        ids.extend(re.findall(pat, html))
    # Dedup preserving order
    out = []
    for i in ids:
        base = i.split("_", 1)[0]  # drop condition/finish suffix variants
        if base not in out:
            out.append(base)
    return out


def parse_num_from_detail(detail_html: str, title: str, denom: int):
    text = ihtml.unescape(re.sub(r"<[^>]+>", " ", detail_html))
    text = re.sub(r"\s+", " ", text)
    rx = re.search(rf"{re.escape(title)}\s*#\s*(\d{{1,3}})\s*/\s*{denom}", text, re.I)
    if rx:
        return int(rx.group(1))
    rx2 = re.search(rf"{re.escape(title)}\s*#\s*(\d{{1,3}})\s*/\s*{str(denom).zfill(3)}", text, re.I)
    if rx2:
        return int(rx2.group(1))
    return None


def main():
    text = INDEX.read_text(encoding="utf-8")

    existing_map = {}
    for sid, cfg in SETS.items():
        for n in range(1, cfg["max_num"] + 1):
            k = f"{sid}-{n}"
            m = re.search(rf'"{re.escape(k)}"\s*:\s*(null|"[^"]*")', text)
            if not m:
                existing_map[k] = None
            else:
                v = m.group(1)
                existing_map[k] = None if v == "null" else v.strip('"')

    scraped = {}
    report = {}
    detail_cache = {}

    for sid, cfg in SETS.items():
        cards = parse_cards_from_index(text, cfg["array_name"])
        mapped = 0
        by_detail = 0
        missing = []
        changed = []

        for card in cards:
            key = f"{sid}-{card['num']}"
            num = card["num"]
            name = card["name"]

            queries = [
                f"{name} {cfg['title']} {num}/{cfg['denom']}",
                f"{name} {cfg['title']} {num:03d}/{cfg['denom']:03d}",
                f"{cfg['title']} {name} #{num}",
            ]

            chosen = None
            reason = None

            for q in queries:
                try:
                    search_html = get("https://explore.justtcg.com/search?q=" + urllib.parse.quote(q))
                except Exception:
                    continue

                candidates = extract_ids_from_search(search_html)
                # Keep only set-specific slugs.
                candidates = [c for c in candidates if c.startswith(f"pokemon-{cfg['path']}-")]
                if not candidates:
                    continue

                for slug in candidates:
                    if slug in detail_cache:
                        detail_num = detail_cache[slug]
                    else:
                        try:
                            d = get(f"https://explore.justtcg.com/pokemon/{cfg['path']}/{slug}")
                            detail_num = parse_num_from_detail(d, cfg["title"], cfg["denom"])
                        except Exception:
                            detail_num = None
                        detail_cache[slug] = detail_num

                    if detail_num == num:
                        chosen = slug
                        reason = "detail-number"
                        break

                if chosen:
                    break

                # Fallback to strict slug-number pattern if detail parser fails.
                for slug in candidates:
                    m = re.search(rf"-(\d{{3}})-{cfg['denom']:03d}(?:-|$)", slug)
                    if m and int(m.group(1)) == num:
                        chosen = slug
                        reason = "slug-number"
                        break
                    m2 = re.search(rf"-(\d{{3}}){cfg['denom']:03d}(?:-|$)", slug)
                    if m2 and int(m2.group(1)) == num:
                        chosen = slug
                        reason = "slug-number"
                        break
                if chosen:
                    break

                time.sleep(0.08)

            scraped[key] = chosen
            if chosen:
                mapped += 1
                if reason == "detail-number":
                    by_detail += 1
            else:
                missing.append(key)

            if existing_map.get(key) != chosen:
                changed.append({"key": key, "existing": existing_map.get(key), "scraped": chosen})

            time.sleep(0.10)

        report[sid] = {
            "total": len(cards),
            "mapped": mapped,
            "verifiedByDetail": by_detail,
            "missing": len(cards) - mapped,
            "changed": len(changed),
            "missingSample": missing[:25],
            "changedSample": changed[:25],
        }

    OUT_MAP.write_text(json.dumps(scraped, indent=2), encoding="utf-8")
    OUT_REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
