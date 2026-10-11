// OpenDesignStudio Styles API — Deno + Postgres
// Serves: /health, /styles, /styles/:id, /styles/:id/spec, /styles/:id/prompt, /styles/:id/html, /styles/:id/image, /search?q=&category=&technique=&component=
// Data source: `styles` table (seeded from dataset.json + merged legacy sources)
// CORS: fully open (agents from anywhere)

import postgres from "https://deno.land/x/postgresjs@v3.4.5/mod.js";

const DATABASE_URL = Deno.env.get("DATABASE_URL") || "postgresql://postgres:postgres@localhost:5432/railway";
const PORT = Number(Deno.env.get("PORT") || 8000);

const sql = postgres(DATABASE_URL, { max: 5, idle_timeout: 20 });

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

function j(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "Content-Type": "application/json", ...CORS },
  });
}

async function getStyles(filters: {
  category?: string; technique?: string; component?: string; q?: string; limit?: number; offset?: number;
}) {
  const limit = Math.min(filters.limit ?? 50, 500);
  const offset = filters.offset ?? 0;
  // Compose with tagged templates only
  let rows;
  if (filters.category) {
    rows = await sql`SELECT * FROM styles WHERE category = ${filters.category} ORDER BY source='core' DESC, n ASC LIMIT ${limit} OFFSET ${offset}`;
  } else if (filters.technique) {
    rows = await sql`SELECT * FROM styles WHERE techniques ? ${filters.technique} ORDER BY source='core' DESC, n ASC LIMIT ${limit} OFFSET ${offset}`;
  } else if (filters.component) {
    rows = await sql`SELECT * FROM styles WHERE component_focus ? ${filters.component} ORDER BY source='core' DESC, n ASC LIMIT ${limit} OFFSET ${offset}`;
  } else if (filters.q) {
    const like = "%" + filters.q.toLowerCase() + "%";
    rows = await sql`SELECT * FROM styles WHERE lower(name) LIKE ${like} OR lower(intent) LIKE ${like} OR lower(description) LIKE ${like} OR lower(agent_prompt) LIKE ${like} OR lower(category) LIKE ${like} ORDER BY source='core' DESC, n ASC LIMIT ${limit} OFFSET ${offset}`;
  } else {
    rows = await sql`SELECT * FROM styles ORDER BY source='core' DESC, n ASC LIMIT ${limit} OFFSET ${offset}`;
  }
  return rows;
}

async function handler(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const path = url.pathname;
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });

  try {
    if (path === "/health") {
      const [{ count }] = await sql`SELECT count(*)::int AS count FROM styles`;
      return j({ ok: true, v: "v2-patched", styles: count, time: new Date().toISOString() });
    }

    if (path === "/styles") {
      const rows = await getStyles({
        category: url.searchParams.get("category") ?? undefined,
        technique: url.searchParams.get("technique") ?? undefined,
        component: url.searchParams.get("component") ?? undefined,
        q: url.searchParams.get("q") ?? undefined,
        limit: url.searchParams.get("limit") ? Number(url.searchParams.get("limit")) : undefined,
        offset: url.searchParams.get("offset") ? Number(url.searchParams.get("offset")) : undefined,
      });
      // list view: strip heavy fields unless ?full=1
      if (url.searchParams.get("full") !== "1") {
        return j(rows.map((r: Record<string, unknown>) => ({
          n: r.n, id: r.id, name: r.name, category: r.category, tagline: r.tagline,
          techniques: r.techniques, best_for: r.best_for, component_focus: r.component_focus,
          palette: r.palette, image_url: `https://designviv.up.railway.app/styles-images/${r.id}.png`,
          spec_url: `https://designviv.up.railway.app/styles-specs/${r.id}.html`,
        })));
      }
      return j(rows);
    }

    const m = path.match(/^\/styles\/([a-z0-9-]+)(\/(spec|prompt|html|image))?$/);
    if (m) {
      const id = m[1];
      const [row] = await sql`SELECT * FROM styles WHERE id = ${id} LIMIT 1`;
      if (!row) return j({ error: "not found", id }, 404);
      const view = m[3];
      if (view === "prompt") return j({ id: row.id, name: row.name, agent_prompt: row.agent_prompt, palette: row.palette, fonts: row.fonts, tech_stack: row.tech_stack });
      if (view === "html") return new Response(row.html_shell, { headers: { "Content-Type": "text/html", ...CORS } });
      if (view === "image") {
        const imageUrl = `https://designviv.up.railway.app/styles-images/${row.id}.png`;
        return Response.redirect(imageUrl, 302);
      }
      if (view === "spec") return Response.redirect(`https://designviv.up.railway.app/styles-specs/${row.id}.html`, 302);
      return j(row); // full record incl. agent_prompt + html_shell
    }

    if (path === "/search") {
      const q = url.searchParams.get("q") ?? "";
      const rows = await getStyles({ q, limit: Number(url.searchParams.get("limit") ?? 20) });
      return j({ query: q, count: rows.length, results: rows.map((r: Record<string, unknown>) => ({ id: r.id, name: r.name, category: r.category, tagline: r.tagline })) });
    }

    if (path === "/techniques") {
      const rows = await sql`SELECT id,name,domain,level,one_line,why_pro,demo_idea,libraries,spec_url FROM techniques ORDER BY domain, id`;
      return j(rows);
    }
    if (path.startsWith("/techniques/") && path.endsWith("/prompt")) {
      const tid = path.slice("/techniques/".length, -"/prompt".length);
      const rows = await sql`SELECT id,name,level,domain,demo_idea,agent_prompt FROM techniques WHERE id = ${tid} LIMIT 1`;
      if (!rows.length) return new Response(JSON.stringify({ error: "not found" }), { status: 404, headers: cors });
      const r0 = rows[0];
      return j({ id: r0.id, name: r0.name, level: r0.level, domain: r0.domain,
        demo_idea: r0.demo_idea, agent_prompt: r0.agent_prompt,
        demo_url: `https://designviv.up.railway.app/techniques-demos/${r0.id}.html` });
    }

    if (path === "/legacy") {
      const kind = url.searchParams.get("kind") ?? undefined;
      let rows;
      const limit = Math.min(Number(url.searchParams.get("limit") ?? 50), 500);
      if (kind) {
        rows = await sql`SELECT uid,kind,name,category,palette,summary,source_url FROM legacy_styles WHERE kind = ${kind} ORDER BY uid LIMIT ${limit}`;
      } else if (url.searchParams.get("q")) {
        const like = "%" + (url.searchParams.get("q") || "").toLowerCase() + "%";
        rows = await sql`SELECT uid,kind,name,category,palette,summary,source_url FROM legacy_styles WHERE lower(name) LIKE ${like} OR lower(summary) LIKE ${like} ORDER BY uid LIMIT ${limit}`;
      } else {
        rows = await sql`SELECT uid,kind,name,category,palette,summary,source_url FROM legacy_styles ORDER BY kind, uid LIMIT ${limit}`;
      }
      return j({ count: rows.length, results: rows });
    }

    if (path === "/vocab") {
      return j({
        categories: ["classic","contemporary","dark-tech","immersive-3d","scrollcraft","expressive","luxe-brand","data-pro","cultural","component-kit"],
      });
    }

    return j({ error: "unknown path", hint: "try /styles, /styles/{id}, /styles/{id}/prompt, /styles/{id}/html, /search?q=", }, 404);
  } catch (e) {
    return j({ error: String(e) }, 500);
  }
}

Deno.serve({ port: PORT }, handler);
