#!/usr/bin/env python3
"""Build public/catalog.json — one machine-readable index of every component
on vivDesign, with a permanent share URL agents can fetch directly."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://designviv.up.railway.app").rstrip("/")

def url(section, cid):
    return f"{BASE}/#/{section}/{cid}"

def strip_tags(s):
    return re.sub(r"\s+", " ", s).strip() if s else ""

catalog = {"site": "vivDesign", "base_url": BASE, "sections": []}

# ── Design Styles (hydrated dashboard styles + hybrids) ──────────────────────
src = (ROOT / "src/data/designStyles.ts").read_text()
styles = []
for m in re.finditer(r'\{\s*\n\s*id:\s*"([^"]+)",\s*\n\s*name:\s*"([^"]+)"(.*?)\n\s*\}', src, re.S):
    cid, name, body = m.group(1), m.group(2), m.group(3)
    cat = re.search(r'\n\s*category:\s*"([^"]+)"', body)
    mood = re.search(r'\n\s*mood:\s*"([^"]+)"', body)
    styles.append({
        "id": cid, "name": name,
        "category": cat.group(1) if cat else ("mixed" if "parentStyles" in body else "classic"),
        "tagline": mood.group(1) if mood else "",
        "url": url("styles", cid),
    })
catalog["sections"].append({"id": "styles", "name": "Design Styles", "count": len(styles), "items": styles})

# ── Styles DB ────────────────────────────────────────────────────────────────
db = json.loads((ROOT / "public/styles-dataset.json").read_text())
items = []
for s in db:
    items.append({
        "id": s["id"], "name": s["name"], "category": s.get("category", ""),
        "tagline": strip_tags(s.get("tagline", "")),
        "url": url("stylesdb", s["id"]),
        "spec": f"{BASE}/styles-specs/{s['id']}.html",
        **({"prompt": s["agent_prompt"]} if s.get("agent_prompt") else {}),
    })
catalog["sections"].append({"id": "stylesdb", "name": "Styles DB", "count": len(items), "items": items})

# ── Add-ons + Interactive ────────────────────────────────────────────────────
def quoted(line, key):
    m = re.search(rf'"{key}":\s*"((?:[^"\\]|\\.)*)"', line)
    if not m:
        m = re.search(rf"{key}:\s*'((?:[^'\\]|\\.)*)'", line)
    if not m:
        return ""
    try:
        return json.loads(f'"{m.group(1)}"')
    except Exception:
        return m.group(1)

def ts_items(path, section):
    """Parse either the hand-written TS arrays (multi-line objects) or the
    one-object-per-line JSON-ish extra files."""
    src = (ROOT / path).read_text()
    out, seen = [], set()
    # Hand-written objects: n: 1, id: 'x', name: 'X', category: '...', tagline: '...'
    for m in re.finditer(
        r"n:\s*(\d+),\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*"
        r"category:\s*'([^']+)',\s*(?:group:\s*'[^']*',\s*)?tagline:\s*'((?:[^'\\]|\\.)*)'",
        src, re.S):
        n, cid, name, cat, tagline = m.groups()
        if cid in seen:
            continue
        seen.add(cid)
        tail = src[m.end():m.end() + 1200]
        dm = re.search(r"demo:\s*'([^']+)'", tail)
        demo = dm.group(1) if dm else ""
        out.append({
            "id": cid, "name": name, "category": cat,
            "tagline": strip_tags(tagline),
            "url": url(section, cid),
            **({"demo": demo if demo.startswith("http") else BASE + demo} if demo else {}),
        })
    # One-object-per-line JSON-ish files: {"n": 76, "id": "plasma-field", ...}
    for line in src.splitlines():
        if '"id":' not in line or '"name":' not in line:
            continue
        cid, name = quoted(line, "id"), quoted(line, "name")
        if not cid or not name or cid in seen:
            continue
        seen.add(cid)
        demo = quoted(line, "demo")
        out.append({
            "id": cid, "name": name, "category": quoted(line, "category"),
            "tagline": strip_tags(quoted(line, "tagline")),
            "url": url(section, cid),
            **({"demo": demo if demo.startswith("http") else BASE + demo} if demo else {}),
        })
    return out

addons = ts_items("src/data/visualAddons.ts", "addons")
catalog["sections"].append({"id": "addons", "name": "Visual Add-ons", "count": len(addons), "items": addons})

inter = ts_items("src/data/interactiveAddons.ts", "interactive")
for extra in ("src/data/interactiveAddonsExtra.ts", "src/data/interactiveAddonsExtra2.ts"):
    have = {i["id"] for i in inter}
    inter += [i for i in ts_items(extra, "interactive") if i["id"] not in have]
catalog["sections"].append({"id": "interactive", "name": "Interactive", "count": len(inter), "items": inter})

# ── Techniques ───────────────────────────────────────────────────────────────
tech = json.loads((ROOT / "public/techniques-catalog.json").read_text())
items = []
for t in tech:
    demo = t.get("demo_url") or f"/techniques-demos/{t['id']}.html"
    items.append({
        "id": t["id"], "name": t["name"], "category": t.get("domain", ""),
        "level": t.get("level", ""), "tagline": strip_tags(t.get("one_line", "")),
        "url": url("techniques", t["id"]),
        "demo": demo if demo.startswith("http") else BASE + demo,
    })
catalog["sections"].append({"id": "techniques", "name": "Techniques", "count": len(items), "items": items})

# ── Top 200 sites ────────────────────────────────────────────────────────────
def slugify(v):
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", v.lower()))

top = []
for line in (ROOT / "src/data/topSites.ts").read_text().splitlines():
    m = re.match(r"\s*\{ rank: (\d+), name: '(.+?)', url: '(.+?)', category: '(.+?)', description: '(.*)' \},?\s*$", line)
    if not m:
        continue
    rank, name, site_url, cat, desc = m.groups()
    top.append({
        "id": slugify(name), "name": name, "rank": int(rank), "category": cat,
        "tagline": strip_tags(desc), "url": url("top200", slugify(name)),
        "website": site_url,
        "design_md": f"{BASE}/top-sites/{slugify(name)}.md",
    })
catalog["sections"].append({"id": "top200", "name": "Top 200 Sites", "count": len(top), "items": top})

total = sum(s["count"] for s in catalog["sections"])
catalog["total_components"] = total
out = ROOT / "public/catalog.json"
out.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
print(f"wrote {out} — {total} components across {len(catalog['sections'])} sections")
for s in catalog["sections"]:
    print(f"  {s['id']}: {s['count']}")
