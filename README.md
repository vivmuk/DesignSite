# vivDesign

Design reference site: design styles, a 150-entry style database, visual add-ons,
interactive playgrounds, front-end techniques, and 200 real-site teardowns.

## Permanent component links

Every card and detail page has a **🔗 Copy link** control. Links use a stable hash route:

```
https://designviv.up.railway.app/#/<section>/<id>
```

| Section | Count | Route |
|---|---|---|
| Design Styles | 38 | `#/styles/<id>` |
| Styles DB | 150 | `#/stylesdb/<id>` |
| Visual Add-ons | 25 | `#/addons/<id>` |
| Interactive | 125 | `#/interactive/<id>` |
| Techniques | 226+ | `#/techniques/<id>` |
| Top 200 Sites | 200 | `#/top200/<site-slug>` |

Every link resolves straight to that component, survives reload, and is safe to
hand to an agent.

## Agent catalog

`https://designviv.up.railway.app/catalog.json` is a single JSON index of every
component: `id`, `name`, `category`, `tagline`, share `url`, and where available
`demo`, `spec`, `prompt`, and `design_md` URLs. Regenerate it after changing data:

```bash
python3 scripts/build_catalog.py
```

## Railway deployment trigger
