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
  const conds: string[] = [];
  const params: unknown[] = [];
  if (filters.category) { params.push(filters.category); conds.push(`category = $${params.length}`); }
  if (filters.technique) { params.push(filters.technique); conds.push(`techniques ? $${params.length}`); }
  if (filters.component) { params.push(filters.component); conds.push(`component_focus ? $${params.length}`); }
  if (filters.q) {
    params.push(`%${filters.q.toLowerCase()}%`);
    const n = params.length;
    conds.push(`(lower(name) LIKE $${n} OR lower(intent) LIKE $${n} OR lower(description) LIKE $${n} OR lower(agent_prompt) LIKE $${n} OR lower(source::text) LIKE $${n})`);
  }
  const where = conds.length ? `WHERE ${conds.join(" AND ")}` : "";
  const limit = Math.min(filters.limit ?? 50, 500);
  const offset = filters.offset ?? 0;
  params.push(limit); const lim = `$${params.length}`;
  params.push(offset); const off = `$${params.length}`;
  return await sql(
    `SELECT * FROM styles ${where} ORDER BY source='core' DESC, n ASC LIMIT ${lim} OFFSET ${off}`,
    params as string[]
  );
}

async function handler(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const path = url.pathname;
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });

  try {
    if (path === "/health") {
      const [{ count }] = await sql`SELECT count(*)::int AS count FROM styles`;
      return j({ ok: true, styles: count, time: new Date().toISOString() });
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
