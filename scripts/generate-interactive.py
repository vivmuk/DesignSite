#!/usr/bin/env python3
"""Generate self-contained interactive demos into public/interactive/."""
import pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from interactive_a import ADDONS_A
from interactive_b import ADDONS_B
from interactive_c import ADDONS_C

ADDONS = ADDONS_A + ADDONS_B + ADDONS_C

BASE = """
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0;padding:0;min-height:100%}
body{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:#eef1f7;
-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
canvas{display:block}
button,input{font-family:inherit}
::selection{background:#ff6b3555}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{name} — Interactive</title>
<style>{base}{css}</style>
</head>
<body>
{html}
<script>
{js}
</script>
</body>
</html>
"""

def main():
    out = pathlib.Path("public/interactive")
    out.mkdir(parents=True, exist_ok=True)
    seen = set()
    for a in ADDONS:
        assert a["id"] not in seen, f"duplicate id {a['id']}"
        seen.add(a["id"])
        page = TEMPLATE.format(base=BASE, css=a["css"].strip(), html=a["html"].strip(), js=a["js"].strip(), name=a["name"])
        (out / f"{a['id']}.html").write_text(page)
        # structural checks
        assert page.count("<style>") == 1 and page.count("<script>") == 1, a["id"]
        assert "</script>" not in a["js"], a["id"]
    print(f"wrote {len(ADDONS)} interactive demos to {out}")
    print("ids:", ", ".join(a["id"] for a in ADDONS))

if __name__ == "__main__":
    main()
