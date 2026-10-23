#!/usr/bin/env python3
"""Generate the 25 self-contained visual add-on demos in public/addons/.

Each demo is a standalone HTML page: one add-on applied to a realistic
section, with a small label and a usage hint. No external assets.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from addons_a import ADDONS_A  # noqa: E402
from addons_b import ADDONS_B  # noqa: E402

ADDONS = ADDONS_A + ADDONS_B
OUT = pathlib.Path(__file__).resolve().parent.parent / "public" / "addons"

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:#08090c;color:#eceef2;font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
scrollbar-width:thin;scrollbar-color:#2a3140 #0b0d13;overscroll-behavior:contain;
-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;overflow-x:hidden}
img,svg{max-width:100%}
a,button{font-family:inherit}
::selection{background:#ff6b35;color:#140803}
.demo-tag{position:fixed;top:14px;left:14px;z-index:9000;display:inline-flex;align-items:center;gap:8px;
font:600 9.5px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.18em;text-transform:uppercase;
color:#98a2b6;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:999px;padding:8px 12px;
backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);pointer-events:none}
.demo-tag b{color:#ff8a5c;letter-spacing:.14em}
.demo-hint{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:9000;
font-size:11.5px;line-height:1.45;color:#a2abbd;background:#0b0d13e0;border:1px solid #ffffff17;
padding:9px 15px;border-radius:999px;backdrop-filter:blur(10px);text-align:center;max-width:90vw;pointer-events:none}
::-webkit-scrollbar{width:9px;height:9px}
::-webkit-scrollbar-track{background:#0b0d13}
::-webkit-scrollbar-thumb{background:#2a3140;border-radius:6px}
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{animation-duration:.001ms !important;animation-iteration-count:1 !important;
    transition-duration:.001ms !important;scroll-behavior:auto !important}
}
@media(max-width:600px){.demo-hint{font-size:10.5px;padding:7px 12px}.demo-tag{font-size:8.5px;padding:7px 10px}}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__NAME__ — vivDesign add-on</title>
<style>__BASE__
__CSS__</style>
</head>
<body>
<div class="demo-tag"><b>ADD-ON __NUM__</b> __NAME__</div>
__HTML__
<div class="demo-hint">__HINT__</div>
<script>__JS__</script>
</body>
</html>
"""


def main() -> None:
    ids = [a["id"] for a in ADDONS]
    assert len(ADDONS) == 25, f"expected 25 add-ons, got {len(ADDONS)}"
    assert len(set(ids)) == 25, "duplicate add-on id"
    OUT.mkdir(parents=True, exist_ok=True)
    for i, a in enumerate(ADDONS, 1):
        page = (
            TEMPLATE.replace("__NAME__", a["name"])
            .replace("__NUM__", f"{i:02d}")
            .replace("__BASE__", BASE_CSS)
            .replace("__CSS__", a["css"])
            .replace("__HTML__", a["html"].strip())
            .replace("__HINT__", a["hint"])
            .replace("__JS__", a["js"].strip())
        )
        (OUT / f"{a['id']}.html").write_text(page, encoding="utf-8")
    print(f"wrote {len(ADDONS)} demos to {OUT}")


if __name__ == "__main__":
    main()
