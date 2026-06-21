import type { Server } from 'http';
import { createServer } from 'http';
import { enrichedStyles, type EnrichedStyle } from '../src/data/enrichedStyles';
import { generateDesignMd, generateTailwindConfig, generateCssVariables, generateDesignTokens } from '../src/utils/generators';

const PORT = parseInt(process.env.MCP_PORT || '3120', 10);
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function jsonResponse(res: any, data: any, status = 200) {
  res.writeHead(status, { 'Content-Type': 'application/json', ...CORS_HEADERS });
  res.end(JSON.stringify(data));
}

function plainResponse(res: any, data: string, status = 200) {
  res.writeHead(status, { 'Content-Type': 'text/plain', ...CORS_HEADERS });
  res.end(data);
}

function searchStyles(query: string): EnrichedStyle[] {
  const words = query.toLowerCase().split(/\s+/).filter(Boolean);
  if (words.length === 0) return [...enrichedStyles];
  return enrichedStyles.filter(s => {
    const haystack = [
      s.name, s.description, s.tagline, s.mood,
      ...s.tags, ...s.characteristics,
    ].join(' ').toLowerCase();
    return words.every(w => haystack.includes(w));
  });
}

function styleSummary(s: EnrichedStyle) {
  return {
    id: s.id,
    name: s.name,
    category: s.category,
    tagline: s.tagline,
    mood: s.mood,
    popularity: s.popularity,
    tags: s.tags,
    colors: s.colors.map(c => ({ name: c.name, hex: c.hex })),
    fonts: { primary: s.fonts.primary.name, secondary: s.fonts.secondary?.name },
    characteristics: s.characteristics,
  };
}

const server: Server = createServer((req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(204, CORS_HEADERS);
    res.end();
    return;
  }

  const url = new URL(req.url || '/', `http://localhost:${PORT}`);
  const path = url.pathname;

  // MCP-style JSON-RPC endpoint
  if (path === '/mcp' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const rpc = JSON.parse(body);
        const { method, params, id } = rpc;

        switch (method) {
          case 'tools/list':
            return jsonResponse(res, {
              jsonrpc: '2.0',
              id,
              result: {
                tools: [
                  {
                    name: 'search_styles',
                    description: 'Search design styles by keyword, tag, or category',
                    inputSchema: {
                      type: 'object',
                      properties: {
                        query: { type: 'string', description: 'Search query (name, tag, mood, characteristic)' },
                        category: { type: 'string', description: 'Filter by category: classic, contemporary, tech, expressive, brand' },
                        limit: { type: 'number', description: 'Max results (default 10)' },
                      },
                    },
                  },
                  {
                    name: 'get_style',
                    description: 'Get full detail of a specific style by ID',
                    inputSchema: {
                      type: 'object',
                      properties: {
                        id: { type: 'string', description: 'Style ID (e.g. "swiss", "cyberpunk")' },
                      },
                      required: ['id'],
                    },
                  },
                  {
                    name: 'get_design_md',
                    description: 'Generate a DESIGN.md markdown file for a specific style',
                    inputSchema: {
                      type: 'object',
                      properties: {
                        id: { type: 'string', description: 'Style ID' },
                      },
                      required: ['id'],
                    },
                  },
                  {
                    name: 'get_tailwind_config',
                    description: 'Generate a Tailwind CSS config for a specific style',
                    inputSchema: {
                      type: 'object',
                      properties: {
                        id: { type: 'string', description: 'Style ID' },
                      },
                      required: ['id'],
                    },
                  },
                  {
                    name: 'get_css_variables',
                    description: 'Generate CSS custom properties for a specific style',
                    inputSchema: {
                      type: 'object',
                      properties: {
                        id: { type: 'string', description: 'Style ID' },
                      },
                      required: ['id'],
                    },
                  },
                  {
                    name: 'list_all_styles',
                    description: 'List all available design styles with summaries',
                    inputSchema: {
                      type: 'object',
                      properties: {
                        sort: { type: 'string', description: 'Sort by: popular, name, category' },
                      },
                    },
                  },
                ],
              },
            });

          case 'tools/call': {
            const toolName = params?.name;
            const args = params?.arguments || {};

            switch (toolName) {
              case 'search_styles': {
                let results = args.query ? searchStyles(args.query) : [...enrichedStyles];
                if (args.category) results = results.filter(s => s.category === args.category);
                const limit = args.limit || 10;
                results.sort((a, b) => b.popularity - a.popularity);
                return jsonResponse(res, {
                  jsonrpc: '2.0',
                  id,
                  result: {
                    content: [{
                      type: 'text',
                      text: JSON.stringify(results.slice(0, limit).map(styleSummary), null, 2),
                    }],
                  },
                });
              }

              case 'get_style': {
                const style = enrichedStyles.find(s => s.id === args.id);
                if (!style) return jsonResponse(res, { jsonrpc: '2.0', id, error: { code: -32602, message: `Style not found: ${args.id}` } });
                return jsonResponse(res, {
                  jsonrpc: '2.0',
                  id,
                  result: { content: [{ type: 'text', text: JSON.stringify(style, null, 2) }] },
                });
              }

              case 'get_design_md': {
                const style = enrichedStyles.find(s => s.id === args.id);
                if (!style) return jsonResponse(res, { jsonrpc: '2.0', id, error: { code: -32602, message: `Style not found: ${args.id}` } });
                return jsonResponse(res, {
                  jsonrpc: '2.0',
                  id,
                  result: { content: [{ type: 'text', text: generateDesignMd(style) }] },
                });
              }

              case 'get_tailwind_config': {
                const style = enrichedStyles.find(s => s.id === args.id);
                if (!style) return jsonResponse(res, { jsonrpc: '2.0', id, error: { code: -32602, message: `Style not found: ${args.id}` } });
                return jsonResponse(res, {
                  jsonrpc: '2.0',
                  id,
                  result: { content: [{ type: 'text', text: generateTailwindConfig(style) }] },
                });
              }

              case 'get_css_variables': {
                const style = enrichedStyles.find(s => s.id === args.id);
                if (!style) return jsonResponse(res, { jsonrpc: '2.0', id, error: { code: -32602, message: `Style not found: ${args.id}` } });
                return jsonResponse(res, {
                  jsonrpc: '2.0',
                  id,
                  result: { content: [{ type: 'text', text: generateCssVariables(style) }] },
                });
              }

              case 'list_all_styles': {
                let results = [...enrichedStyles];
                if (args.sort === 'name') results.sort((a, b) => a.name.localeCompare(b.name));
                else if (args.sort === 'category') results.sort((a, b) => a.category.localeCompare(b.category));
                else results.sort((a, b) => b.popularity - a.popularity);
                return jsonResponse(res, {
                  jsonrpc: '2.0',
                  id,
                  result: { content: [{ type: 'text', text: JSON.stringify(results.map(styleSummary), null, 2) }] },
                });
              }

              default:
                return jsonResponse(res, { jsonrpc: '2.0', id, error: { code: -32601, message: `Unknown tool: ${toolName}` } });
            }
          }

          default:
            return jsonResponse(res, { jsonrpc: '2.0', id, error: { code: -32601, message: `Unknown method: ${method}` } });
        }
      } catch (e: any) {
        return jsonResponse(res, { jsonrpc: '2.0', id: null, error: { code: -32700, message: `Parse error: ${e.message}` } });
      }
    });
    return;
  }

  // REST endpoints for easy testing
  if (path === '/api/styles' && req.method === 'GET') {
    const query = url.searchParams.get('q') || '';
    const category = url.searchParams.get('category') || '';
    const sort = url.searchParams.get('sort') || 'popular';
    let results = query ? searchStyles(query) : [...enrichedStyles];
    if (category) results = results.filter(s => s.category === category);
    if (sort === 'name') results.sort((a, b) => a.name.localeCompare(b.name));
    else if (sort === 'category') results.sort((a, b) => a.category.localeCompare(b.category));
    else results.sort((a, b) => b.popularity - a.popularity);
    return jsonResponse(res, { total: results.length, styles: results.map(styleSummary) });
  }

  if (path.startsWith('/api/styles/') && req.method === 'GET') {
    const id = path.split('/')[3];
    const style = enrichedStyles.find(s => s.id === id);
    if (!style) return jsonResponse(res, { error: `Style not found: ${id}` }, 404);
    const format = url.searchParams.get('format');
    if (format === 'design-md') return plainResponse(res, generateDesignMd(style));
    if (format === 'tailwind') return plainResponse(res, generateTailwindConfig(style));
    if (format === 'css-vars') return plainResponse(res, generateCssVariables(style));
    if (format === 'tokens') return plainResponse(res, generateDesignTokens(style));
    return jsonResponse(res, style);
  }

  if (path === '/api/health' && req.method === 'GET') {
    return jsonResponse(res, {
      status: 'ok',
      service: 'opendesignstudio-mcp',
      styles: enrichedStyles.length,
      tools: ['search_styles', 'get_style', 'get_design_md', 'get_tailwind_config', 'get_css_variables', 'list_all_styles'],
      endpoints: {
        mcp: 'POST /mcp',
        rest: 'GET /api/styles?q=...&category=...&sort=...',
        detail: 'GET /api/styles/:id',
        export: 'GET /api/styles/:id?format=design-md|tailwind|css-vars|tokens',
      },
    });
  }

  if (path === '/') {
    return plainResponse(res, 'OpenDesignStudio MCP Server\n\nEndpoints:\n  POST /mcp          — MCP JSON-RPC\n  GET  /api/styles   — Search styles\n  GET  /api/styles/:id — Get style detail\n  GET  /api/styles/:id?format=design-md — Export DESIGN.md\n  GET  /api/health   — Health check\n');
  }

  jsonResponse(res, { error: 'Not found' }, 404);
});

server.listen(PORT, () => {
  console.log(`OpenDesignStudio MCP Server running on http://localhost:${PORT}`);
  console.log(`  MCP endpoint: POST http://localhost:${PORT}/mcp`);
  console.log(`  REST endpoint: GET http://localhost:${PORT}/api/styles`);
  console.log(`  Health: GET http://localhost:${PORT}/api/health`);
});

export { server };
