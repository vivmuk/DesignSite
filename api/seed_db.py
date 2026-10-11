#!/usr/bin/env python3
"""Seed the styles DB from dataset.json + merge legacy DesignSite data.

Creates:
- styles table: the 100 authored styles (source='core')
- legacy_styles table: the existing 2000 designStyles + 176 systems + 141 skills + 200 top-sites (source='legacy')
All rows carry agent_prompt + palette + fonts so /search covers everything.
"""
import json, os, sys

import psycopg2
from psycopg2.extras import Json, execute_values

DSN = os.environ.get("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/railway"

CORE_SCHEMA = """
CREATE TABLE IF NOT EXISTS styles (
  n INT PRIMARY KEY,
  id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  tagline TEXT,
  description TEXT,
  intent TEXT,
  palette JSONB,
  fonts JSONB,
  motion JSONB,
  signature_elements JSONB,
  component_focus JSONB,
  tech_stack JSONB,
  techniques JSONB,
  best_for JSONB,
  image_prompt TEXT,
  agent_prompt TEXT,
  html_shell TEXT,
  image_url TEXT,
  spec_url TEXT,
  source TEXT DEFAULT 'core',
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS styles_category_idx ON styles(category);
CREATE INDEX IF NOT EXISTS styles_techniques_idx ON styles USING GIN(techniques);
CREATE INDEX IF NOT EXISTS styles_component_idx ON styles USING GIN(component_focus);
CREATE TABLE IF NOT EXISTS legacy_styles (
  uid TEXT PRIMARY KEY,
  kind TEXT NOT NULL,          -- design_style | system | skill | top_site
  name TEXT NOT NULL,
  category TEXT,
  palette JSONB,
  summary TEXT,
  details JSONB,
  source_url TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legacy_kind_idx ON legacy_styles(kind);
"""

def upsert_core(cur, rows):
    execute_values(cur, """
    INSERT INTO styles (n,id,name,category,tagline,description,intent,palette,fonts,motion,
      signature_elements,component_focus,tech_stack,techniques,best_for,image_prompt,agent_prompt,
      html_shell,image_url,spec_url,source)
    VALUES %s
    ON CONFLICT (n) DO UPDATE SET
      id=EXCLUDED.id, name=EXCLUDED.name, category=EXCLUDED.category, tagline=EXCLUDED.tagline,
      description=EXCLUDED.description, intent=EXCLUDED.intent, palette=EXCLUDED.palette,
      fonts=EXCLUDED.fonts, motion=EXCLUDED.motion, signature_elements=EXCLUDED.signature_elements,
      component_focus=EXCLUDED.component_focus, tech_stack=EXCLUDED.tech_stack,
      techniques=EXCLUDED.techniques, best_for=EXCLUDED.best_for, image_prompt=EXCLUDED.image_prompt,
      agent_prompt=EXCLUDED.agent_prompt, html_shell=EXCLUDED.html_shell,
      image_url=EXCLUDED.image_url, spec_url=EXCLUDED.spec_url, source=EXCLUDED.source
    """, rows, page_size=50)

def upsert_legacy(cur, rows):
    execute_values(cur, """
    INSERT INTO legacy_styles (uid,kind,name,category,palette,summary,details,source_url)
    VALUES %s
    ON CONFLICT (uid) DO UPDATE SET
      name=EXCLUDED.name, category=EXCLUDED.category, palette=EXCLUDED.palette,
      summary=EXCLUDED.summary, details=EXCLUDED.details, source_url=EXCLUDED.source_url
    """, rows, page_size=200)

def main():
    repo = os.environ.get("REPO_DIR", "/tmp/DesignSite")
    data_dir = os.environ.get("DATA_DIR", "/tmp/stylesdb")

    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    cur.execute(CORE_SCHEMA)
    conn.commit()

    # 1) core: the 100 authored styles
    dataset_path = os.path.join(data_dir, "dataset.json")
    if os.path.exists(dataset_path):
        ds = json.load(open(dataset_path))
        rows = []
        for s in ds:
            rows.append((
                s["n"], s["id"], s["name"], s["category"], s.get("tagline"), s.get("description"),
                s.get("intent"), Json(s.get("palette")), Json(s.get("fonts")), Json(s.get("motion")),
                Json(s.get("signature_elements")), Json(s.get("component_focus")), Json(s.get("tech_stack")),
                Json(s.get("techniques")), Json(s.get("best_for")), s.get("image_prompt"),
                s.get("agent_prompt"), s.get("html_shell"),
                f"https://designviv.up.railway.app/styles-images/{s['id']}.png",
                f"https://designviv.up.railway.app/styles-specs/{s['id']}.html",
                "core",
            ))
        upsert_core(cur, rows)
        conn.commit()
        print(f"core: {len(rows)} styles upserted")
    else:
        print("WARN: dataset.json not found — core styles skipped")

    # 2) legacy: existing site data
    legacy = []
    # a) design styles (2000) from src/data/designStyles.ts + enrichedStyles.ts
    try:
        sys.path.insert(0, repo)
        # parse the TS arrays with a regex-free approach: they are valid JSON-ish; use node instead
        out = os.popen(f"""cd {repo} && node -e "
const fs = require('fs');
function extract(file, varName) {{
  const src = fs.readFileSync(file, 'utf8');
  const m = src.match(new RegExp('export const ' + varName + '[^=]*= (\\\\[[\\\\s\\\\S]*?\\\\n\\\\]);'));
  if (!m) return [];
  try {{ return eval('(' + m[1] + ')'); }} catch(e) {{ console.error(file, String(e).slice(0,80)); return []; }}
}}
const styles = extract('src/data/designStyles.ts', 'designStyles');
const enriched = extract('src/data/enrichedStyles.ts', 'enrichedStyles');
const systems = extract('src/data/openDesignSystems.ts', 'openDesignSystems');
const skills = extract('src/data/openDesignSkills.ts', 'openDesignSkills');
console.log(JSON.stringify({{styles, enriched, systems, skills}}));
" """).read()
        d = json.loads(out)
        for s in d["styles"]:
            legacy.append((f"style:{s.get('id', s.get('name'))}", "design_style", s.get("name",""),
                           s.get("category"), Json(s.get("palette") or s.get("colors")),
                           s.get("description") or s.get("intent"), Json(s), None))
        for s in d["systems"]:
            legacy.append((f"sys:{s.get('id')}", "system", s.get("name",""), s.get("category"),
                           Json({"bg": s.get("bgColor"), "accent": s.get("accentColor"), "fg": s.get("textColor")}),
                           s.get("description"), Json(s),
                           f"https://designviv.up.railway.app/showcase/systems/{s.get('id')}.html"))
        for s in d["skills"]:
            legacy.append((f"skill:{s.get('id')}", "skill", s.get("name",""), s.get("category"),
                           None, s.get("description"), Json(s),
                           f"https://designviv.up.railway.app/showcase/skills/{s.get('id')}.html"))
    except Exception as e:
        print("legacy ts parse WARN:", e)

    # b) top sites from public/top-sites/sites.json
    try:
        sites = json.load(open(os.path.join(repo, "public/top-sites/sites.json")))
        for s in sites:
            legacy.append((f"site:{s.get('name', s.get('rank'))}", "top_site", s.get("name",""),
                           s.get("category"), Json({"colors": s.get("colors"), "fonts": s.get("fonts")}),
                           s.get("description"), Json(s),
                           f"https://designviv.up.railway.app/top-sites/{s.get('designMdPath','')}"))
    except Exception as e:
        print("sites WARN:", e)

    if legacy:
        upsert_legacy(cur, legacy)
        conn.commit()
        print(f"legacy: {len(legacy)} rows upserted")

    # counts
    cur.execute("SELECT count(*) FROM styles")
    print("styles:", cur.fetchone()[0])
    cur.execute("SELECT kind, count(*) FROM legacy_styles GROUP BY kind")
    print("legacy:", cur.fetchall())
    conn.close()

if __name__ == "__main__":
    main()
