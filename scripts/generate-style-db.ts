// Style Database Generator — produces 2,000 enriched styles
// Combines: 18 hand-crafted enriched styles + 187 design systems + 
// procedural variations to reach 2,000 total
import { enrichedStyles, type EnrichedStyle } from '../src/data/enrichedStyles';
import { openDesignSystems } from '../src/data/openDesignSystems';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import * as fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Type scale templates by density
const typeScales = {
  compact: [
    { name: 'display', size: '48px', weight: '700', lineHeight: '1.05', letterSpacing: '-0.02em', sample: 'The quick brown fox' },
    { name: 'heading', size: '32px', weight: '600', lineHeight: '1.15', sample: 'The quick brown fox' },
    { name: 'subheading', size: '20px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
    { name: 'body', size: '14px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
    { name: 'caption', size: '12px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
  ],
  comfortable: [
    { name: 'display', size: '64px', weight: '700', lineHeight: '1.05', letterSpacing: '-0.02em', sample: 'The quick brown fox' },
    { name: 'heading', size: '40px', weight: '600', lineHeight: '1.15', sample: 'The quick brown fox' },
    { name: 'subheading', size: '24px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
    { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
    { name: 'caption', size: '14px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
  ],
  spacious: [
    { name: 'display', size: '72px', weight: '300', lineHeight: '1.1', letterSpacing: '-0.02em', sample: 'The quick brown fox' },
    { name: 'heading', size: '48px', weight: '400', lineHeight: '1.2', sample: 'The quick brown fox' },
    { name: 'subheading', size: '24px', weight: '400', lineHeight: '1.35', sample: 'The quick brown fox' },
    { name: 'body', size: '17px', weight: '400', lineHeight: '1.7', sample: 'The quick brown fox' },
    { name: 'caption', size: '13px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
  ],
};

// Color palettes by style archetype
const paletteArchetypes: Record<string, { colors: {name: string, hex: string, usage: string}[], neutrals: {name: string, hex: string, usage: string}[] }> = {
  minimal: {
    colors: [
      { name: 'Accent', hex: '#0066FF', usage: 'Primary actions, links, focus states' },
      { name: 'Black', hex: '#000000', usage: 'Primary text, headings' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas, surfaces' },
      { name: 'Light Gray', hex: '#F5F5F5', usage: 'Secondary surfaces' },
      { name: 'Gray', hex: '#999999', usage: 'Secondary text, borders' },
    ],
    neutrals: [
      { name: 'Ink', hex: '#0A0A0A', usage: 'Primary text' },
      { name: 'Slate', hex: '#444444', usage: 'Secondary text' },
      { name: 'Mist', hex: '#999999', usage: 'Tertiary text' },
      { name: 'Fog', hex: '#E5E5E5', usage: 'Borders' },
      { name: 'Cloud', hex: '#F5F5F5', usage: 'Surfaces' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas' },
    ],
  },
  dark: {
    colors: [
      { name: 'Accent', hex: '#00D4FF', usage: 'Primary accent, glows, CTAs' },
      { name: 'Secondary', hex: '#B026FF', usage: 'Secondary accent, gradients' },
      { name: 'Void', hex: '#0A0A0F', usage: 'Page background' },
      { name: 'Panel', hex: '#14141F', usage: 'Card surfaces' },
      { name: 'Border', hex: '#2A2A3A', usage: 'Borders, dividers' },
    ],
    neutrals: [
      { name: 'Void', hex: '#0A0A0F', usage: 'Background' },
      { name: 'Panel', hex: '#14141F', usage: 'Surfaces' },
      { name: 'Surface', hex: '#1E1E2E', usage: 'Elevated surfaces' },
      { name: 'Border', hex: '#2A2A3A', usage: 'Borders' },
      { name: 'Dim', hex: '#666680', usage: 'Tertiary text' },
      { name: 'Text', hex: '#F0F0F5', usage: 'Primary text' },
    ],
  },
  warm: {
    colors: [
      { name: 'Coral', hex: '#FF6B35', usage: 'Primary accent' },
      { name: 'Amber', hex: '#FFB627', usage: 'Secondary accent' },
      { name: 'Cream', hex: '#FFF3E0', usage: 'Canvas' },
      { name: 'Brown', hex: '#3E2723', usage: 'Primary text' },
      { name: 'Sand', hex: '#D7CCC8', usage: 'Borders' },
    ],
    neutrals: [
      { name: 'Espresso', hex: '#3E2723', usage: 'Primary text' },
      { name: 'Mocha', hex: '#6D4C41', usage: 'Secondary text' },
      { name: 'Sand', hex: '#D7CCC8', usage: 'Borders' },
      { name: 'Cream', hex: '#FFF3E0', usage: 'Surfaces' },
      { name: 'Paper', hex: '#FFFAF0', usage: 'Canvas' },
    ],
  },
  bold: {
    colors: [
      { name: 'Electric', hex: '#FF1493', usage: 'Primary accent, bold statements' },
      { name: 'Cyan', hex: '#00CED1', usage: 'Secondary accent' },
      { name: 'Gold', hex: '#FFD700', usage: 'Tertiary accent' },
      { name: 'Black', hex: '#000000', usage: 'Text, structure' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas' },
    ],
    neutrals: [
      { name: 'Black', hex: '#000000', usage: 'Text' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas' },
      { name: 'Gray', hex: '#888888', usage: 'Secondary text' },
    ],
  },
  editorial: {
    colors: [
      { name: 'Ink', hex: '#1A1A1A', usage: 'Primary text' },
      { name: 'Paper', hex: '#FFFFFF', usage: 'Canvas' },
      { name: 'Accent', hex: '#C9A959', usage: 'Gold accent' },
      { name: 'Red', hex: '#8B0000', usage: 'Editorial marks' },
      { name: 'Cream', hex: '#F4F4F4', usage: 'Surfaces' },
    ],
    neutrals: [
      { name: 'Ink', hex: '#1A1A1A', usage: 'Primary text' },
      { name: 'Smoke', hex: '#555555', usage: 'Secondary text' },
      { name: 'Stone', hex: '#888888', usage: 'Tertiary text' },
      { name: 'Mist', hex: '#D4D4D4', usage: 'Borders' },
      { name: 'Cream', hex: '#F4F4F4', usage: 'Surfaces' },
      { name: 'Paper', hex: '#FFFFFF', usage: 'Canvas' },
    ],
  },
  playful: {
    colors: [
      { name: 'Sunny', hex: '#FFD93D', usage: 'Primary accent' },
      { name: 'Bubblegum', hex: '#FF6B9D', usage: 'Secondary accent' },
      { name: 'Mint', hex: '#6BCB77', usage: 'Success states' },
      { name: 'Sky', hex: '#4D96FF', usage: 'Links, info' },
      { name: 'Cream', hex: '#FFF8E7', usage: 'Canvas' },
    ],
    neutrals: [
      { name: 'Soft Black', hex: '#2D2D2D', usage: 'Primary text' },
      { name: 'Warm Gray', hex: '#6B6B6B', usage: 'Secondary text' },
      { name: 'Light', hex: '#E8E8E8', usage: 'Borders' },
      { name: 'Cream', hex: '#FFF8E7', usage: 'Surfaces' },
      { name: 'White', hex: '#FFFFFF', usage: 'Cards' },
    ],
  },
  technical: {
    colors: [
      { name: 'Signal', hex: '#39FF14', usage: 'Primary accent, active states' },
      { name: 'Dark', hex: '#0D0D0D', usage: 'Background' },
      { name: 'Panel', hex: '#141414', usage: 'Surfaces' },
      { name: 'Amber', hex: '#FFB000', usage: 'Warnings, highlights' },
      { name: 'Red', hex: '#FF3B30', usage: 'Errors' },
    ],
    neutrals: [
      { name: 'Void', hex: '#0D0D0D', usage: 'Background' },
      { name: 'Panel', hex: '#141414', usage: 'Surfaces' },
      { name: 'Surface', hex: '#1A1A1A', usage: 'Elevated' },
      { name: 'Border', hex: '#333333', usage: 'Borders' },
      { name: 'Dim', hex: '#666666', usage: 'Tertiary text' },
      { name: 'Text', hex: '#E4E4E4', usage: 'Primary text' },
    ],
  },
  luxury: {
    colors: [
      { name: 'Gold', hex: '#C9A959', usage: 'Primary accent' },
      { name: 'Onyx', hex: '#1A1A1A', usage: 'Primary text' },
      { name: 'Ivory', hex: '#FFFFF0', usage: 'Canvas' },
      { name: 'Burgundy', hex: '#800020', usage: 'Secondary accent' },
      { name: 'Pearl', hex: '#F8F8F0', usage: 'Surfaces' },
    ],
    neutrals: [
      { name: 'Onyx', hex: '#1A1A1A', usage: 'Primary text' },
      { name: 'Charcoal', hex: '#333333', usage: 'Secondary text' },
      { name: 'Stone', hex: '#888888', usage: 'Tertiary text' },
      { name: 'Pearl', hex: '#F8F8F0', usage: 'Surfaces' },
      { name: 'Ivory', hex: '#FFFFF0', usage: 'Canvas' },
    ],
  },
};

// Font pairings by style
const fontPairings: Record<string, { primary: {name: string, weights: string, sizes: string, usage: string, fallback: string}, secondary?: {name: string, weights: string, sizes: string, usage: string, fallback: string} }> = {
  minimal: { primary: { name: 'Inter', weights: '400, 500, 600, 700', sizes: '12–64px', usage: 'All UI text', fallback: 'system-ui, sans-serif' } },
  dark: { primary: { name: 'Inter', weights: '400, 500, 600', sizes: '12–48px', usage: 'All UI text', fallback: 'system-ui, sans-serif' }, secondary: { name: 'JetBrains Mono', weights: '400, 500', sizes: '12–16px', usage: 'Code, metadata', fallback: 'monospace' } },
  warm: { primary: { name: 'DM Sans', weights: '400, 500, 700', sizes: '12–48px', usage: 'All UI text', fallback: 'system-ui, sans-serif' } },
  bold: { primary: { name: 'Space Grotesk', weights: '400, 700', sizes: '14–72px', usage: 'Display, headings', fallback: 'Arial, sans-serif' }, secondary: { name: 'Inter', weights: '400, 500', sizes: '14–18px', usage: 'Body, UI', fallback: 'system-ui, sans-serif' } },
  editorial: { primary: { name: 'Playfair Display', weights: '400, 700, 900', sizes: '14–72px', usage: 'Headlines, display', fallback: 'Georgia, serif' }, secondary: { name: 'Source Serif Pro', weights: '400, 600', sizes: '14–20px', usage: 'Body text', fallback: 'Georgia, serif' } },
  playful: { primary: { name: 'Fredoka', weights: '400, 500, 600, 700', sizes: '14–56px', usage: 'Display, headings', fallback: 'system-ui, sans-serif' }, secondary: { name: 'Nunito', weights: '400, 600, 700', sizes: '14–18px', usage: 'Body text', fallback: 'system-ui, sans-serif' } },
  technical: { primary: { name: 'JetBrains Mono', weights: '400, 500, 700', sizes: '11–32px', usage: 'All text', fallback: 'SF Mono, monospace' } },
  luxury: { primary: { name: 'Cormorant Garamond', weights: '300, 400, 600', sizes: '14–64px', usage: 'Display, headings', fallback: 'Georgia, serif' }, secondary: { name: 'Montserrat', weights: '300, 400, 500', sizes: '12–18px', usage: 'Body, labels', fallback: 'system-ui, sans-serif' } },
};

// Spacing templates
const spacingTemplates = {
  compact: { density: 'compact' as const, baseUnit: '4px', maxWidth: '1400px', sectionGap: '32px', cardPadding: '16px', elementGap: '8px' },
  comfortable: { density: 'comfortable' as const, baseUnit: '8px', maxWidth: '1200px', sectionGap: '64px', cardPadding: '24px', elementGap: '16px' },
  spacious: { density: 'spacious' as const, baseUnit: '8px', maxWidth: '1080px', sectionGap: '96px', cardPadding: '40px', elementGap: '24px' },
};

// Border radius templates
const radiusTemplates = {
  sharp: { badges: '0px', nav: '0px', inputs: '0px', buttons: '0px', cards: '0px' },
  soft: { badges: '6px', nav: '8px', inputs: '8px', buttons: '8px', cards: '12px' },
  round: { badges: '20px', nav: '16px', inputs: '16px', buttons: '20px', cards: '24px' },
};

// Guideline templates by archetype
function generateGuidelines(archetype: string, accentName: string): {do: string, dont: string}[] {
  const base: Record<string, {do: string, dont: string}[]> = {
    minimal: [
      { do: `Use ${accentName} as the single accent color for all interactive elements`, dont: "Don't introduce multiple accent colors — restraint is the system" },
      { do: 'Use generous whitespace (24-32px padding) to create focus', dont: "Don't pack content tightly — whitespace IS the design" },
      { do: 'Use weight 400 for body and 600-700 for headings', dont: "Don't use decorative fonts — the system is clean and neutral" },
    ],
    dark: [
      { do: 'Keep backgrounds near-black — accent colors need darkness to pop', dont: "Don't use light backgrounds — dark themes are dark-first" },
      { do: `Use ${accentName} sparingly for active states and primary CTAs`, dont: "Don't overuse accent colors — they lose impact when everywhere" },
      { do: 'Use 1px borders in subtle grays for panel separation', dont: "Don't use thick borders — dark UIs are precise and minimal" },
    ],
    warm: [
      { do: 'Use warm color palettes — oranges, ambers, creams', dont: "Don't use cool blues or grays — warmth is the identity" },
      { do: 'Use generous spacing for a relaxed, inviting feel', dont: "Don't create dense layouts — warmth requires room to breathe" },
    ],
    bold: [
      { do: 'Use bold, saturated colors as the primary visual language', dont: "Don't use subtle or muted colors — bold means confident" },
      { do: 'Use weight 700+ for display type — bold is loud', dont: "Don't use light weights — this is not the place for restraint" },
    ],
    editorial: [
      { do: 'Use serif typefaces for headlines — the serif IS the editorial voice', dont: "Don't use sans-serif for body text — the serif defines the style" },
      { do: 'Use narrow column width (max 720px) for articles', dont: "Don't stretch text across full width — print columns are narrow" },
    ],
    playful: [
      { do: 'Use 20-24px border radius — everything should look soft and friendly', dont: "Don't use sharp corners — playful design is round" },
      { do: 'Use bright, warm colors and chunky shadows', dont: "Don't use dark or muted colors — playful is bright and warm" },
    ],
    technical: [
      { do: 'Use monospace throughout — it IS the technical voice', dont: "Don't use proportional fonts — the monospace grid is the design" },
      { do: 'Keep backgrounds near-black — terminal UIs are dark-first', dont: "Don't use light mode — technical interfaces are dark by nature" },
    ],
    luxury: [
      { do: 'Use weight 300 for display — luxury whispers through light type', dont: "Don't use bold weights — luxury is never loud" },
      { do: `Use ${accentName} as the only accent — it signals premium`, dont: "Don't introduce bright or saturated colors — luxury is muted" },
    ],
  };
  return base[archetype] || base.minimal;
}

// Map style tags to archetypes
function styleToArchetype(style: string, tags: string[]): string {
  if (tags.includes('dark')) return 'dark';
  if (style === 'brutalist') return 'bold';
  if (style === 'playful') return 'playful';
  if (style === 'editorial') return 'editorial';
  if (style === 'luxury') return 'luxury';
  if (style === 'technical') return 'technical';
  if (style === 'minimal') return 'minimal';
  if (style === 'bold') return 'bold';
  if (style === 'elegant') return 'minimal';
  return 'minimal';
}

// Generate elevation by archetype
function generateElevation(archetype: string) {
  switch (archetype) {
    case 'dark':
      return [
        { name: 'panel', value: '0 2px 8px rgba(0,0,0,0.4)', usage: 'Card panels' },
        { name: 'border', value: '1px solid #2A2A3A', usage: 'Panel borders' },
        { name: 'glow', value: '0 0 20px rgba(0,212,255,0.15)', usage: 'Active element glow' },
      ];
    case 'bold':
      return [
        { name: 'hard', value: '8px 8px 0px #000000', usage: 'Hard offset shadows' },
        { name: 'border', value: '3px solid #000000', usage: 'Thick borders' },
      ];
    case 'playful':
      return [
        { name: 'chunky', value: '0 6px 0px #2D2D2D', usage: 'Chunky bottom shadow' },
        { name: 'soft', value: '0 4px 12px rgba(0,0,0,0.1)', usage: 'Soft shadow' },
        { name: 'float', value: '0 8px 24px rgba(0,0,0,0.12)', usage: 'Hover state' },
      ];
    case 'luxury':
      return [
        { name: 'none', value: 'none', usage: 'No shadows — luxury is flat' },
        { name: 'hairline', value: '1px solid #C9A959', usage: 'Gold hairlines' },
      ];
    default:
      return [
        { name: 'rest', value: 'none', usage: 'Cards at rest' },
        { name: 'hover', value: '0 2px 8px rgba(0,0,0,0.06)', usage: 'Card hover' },
        { name: 'float', value: '0 8px 24px rgba(0,0,0,0.08)', usage: 'Dropdowns, popovers' },
      ];
  }
}

// Adjective sets for generating variation names
const moodAdjectives = ['Soft', 'Crisp', 'Bold', 'Quiet', 'Warm', 'Cool', 'Dark', 'Light', 'Rich', 'Clean', 'Sharp', 'Smooth', 'Raw', 'Refined', 'Wild', 'Calm', 'Lush', 'Stark', 'Vivid', 'Muted'];
const styleSuffixes = ['Edition', 'Variant', 'Treatment', 'Phase', 'Wave', 'Form', 'Mode', 'Tone', 'Shade', 'Cut'];

// Tag combinations for procedural styles
const tagPool = ['Minimal', 'Clean', 'Modern', 'Dark', 'Light', 'Bold', 'Soft', 'Sharp', 'Warm', 'Cool', 'Grid', 'Typography', 'Gradient', 'Flat', 'Rounded', 'Monospace', 'Serif', 'Geometric', 'Organic', 'Tech', 'Editorial', 'Luxury', 'Playful', 'Brutalist', 'Glass', 'Neon', 'Vintage', 'Futuristic', 'Corporate', 'Creative'];

// Category pool
const categories = ['classic', 'contemporary', 'tech', 'expressive', 'brand'];

function pickRandom<T>(arr: T[], seed: number): T {
  return arr[seed % arr.length];
}

function pickRandomN<T>(arr: T[], n: number, seed: number): T[] {
  const result: T[] = [];
  const used = new Set<number>();
  for (let i = 0; i < n && i < arr.length; i++) {
    const idx = (seed + i * 7) % arr.length;
    if (!used.has(idx)) {
      used.add(idx);
      result.push(arr[idx]);
    }
  }
  return result;
}

function generateHex(seed: number): string {
  const h = (seed * 2654435761) % 0xFFFFFF;
  return '#' + h.toString(16).padStart(6, '0').toUpperCase();
}

// Convert a design system to an enriched style
function systemToEnriched(ds: typeof openDesignSystems[0], index: number): EnrichedStyle {
  const archetype = styleToArchetype(ds.style, ds.tags);
  const palette = paletteArchetypes[archetype] || paletteArchetypes.minimal;
  const fonts = fontPairings[archetype] || fontPairings.minimal;
  const density = archetype === 'dark' || archetype === 'technical' ? 'compact' : archetype === 'luxury' || archetype === 'editorial' ? 'spacious' : 'comfortable';
  const radius = archetype === 'bold' || archetype === 'technical' ? 'sharp' : archetype === 'playful' ? 'round' : 'soft';

  // Override first color with the system's accent color
  const colors = [...palette.colors];
  if (ds.accentColor && ds.accentColor !== '#FFFFFF' && ds.accentColor !== '#ffffff') {
    colors[0] = { name: 'Brand Accent', hex: ds.accentColor, usage: 'Primary brand color, CTAs, active states' };
  }

  // Determine category mapping
  const catMap: Record<string, string> = {
    productivity: 'brand', developer: 'tech', fintech: 'brand', media: 'contemporary',
    creative: 'expressive', enterprise: 'brand', luxury: 'brand', gaming: 'tech',
    editorial: 'classic', modern: 'contemporary',
  };
  const category = catMap[ds.category] || 'contemporary';

  return {
    id: ds.id,
    name: ds.name,
    category,
    tagline: ds.description.split('.')[0] + '.',
    description: ds.description,
    mood: archetype.charAt(0).toUpperCase() + archetype.slice(1) + ', ' + ds.style.charAt(0).toUpperCase() + ds.style.slice(1),
    popularity: Math.max(40, 95 - Math.floor(index / 3)),
    tags: ds.tags.map(t => t.charAt(0).toUpperCase() + t.slice(1)).concat([archetype.charAt(0).toUpperCase() + archetype.slice(1)]),
    colors,
    neutrals: palette.neutrals,
    fonts,
    typeScale: typeScales[density],
    spacing: spacingTemplates[density],
    borderRadius: radiusTemplates[radius],
    elevation: generateElevation(archetype),
    guidelines: generateGuidelines(archetype, colors[0].name),
    characteristics: [ds.style, archetype, density, ds.category].map(s => s.charAt(0).toUpperCase() + s.slice(1)),
    exampleWebsite: ds.category.charAt(0).toUpperCase() + ds.category.slice(1) + ' Product',
    relatedStyleIds: [],
  };
}

// Generate procedural style variations
function generateProceduralStyle(seed: number): EnrichedStyle {
  const archetypeIdx = seed % 8;
  const archetypes = ['minimal', 'dark', 'warm', 'bold', 'editorial', 'playful', 'technical', 'luxury'];
  const archetype = archetypes[archetypeIdx];
  const palette = paletteArchetypes[archetype];
  const fonts = fontPairings[archetype];
  const density = archetype === 'dark' || archetype === 'technical' ? 'compact' : archetype === 'luxury' || archetype === 'editorial' ? 'spacious' : 'comfortable';
  const radius = archetype === 'bold' || archetype === 'technical' ? 'sharp' : archetype === 'playful' ? 'round' : 'soft';

  const adj = pickRandom(moodAdjectives, seed);
  const suffix = pickRandom(styleSuffixes, seed * 3);
  const name = `${adj} ${archetype.charAt(0).toUpperCase() + archetype.slice(1)} ${suffix}`;
  const id = `proc-${seed}-${archetype}-${adj.toLowerCase()}-${suffix.toLowerCase()}`.replace(/[^a-z0-9-]/g, '');

  // Generate unique-ish colors by rotating hue
  const colors = palette.colors.map((c, i) => {
    if (i === 0 && archetype !== 'minimal' && archetype !== 'editorial') {
      return { ...c, hex: generateHex(seed * 7 + i * 31) };
    }
    return c;
  });

  const tags = pickRandomN(tagPool, 4, seed).map(t => t);
  const category = pickRandom(categories, seed * 5);

  return {
    id,
    name,
    category,
    tagline: `${archetype.charAt(0).toUpperCase() + archetype.slice(1)} style with ${adj.toLowerCase()} characteristics`,
    description: `A ${archetype} design approach with ${adj.toLowerCase()} sensibility. Generated as part of the OpenDesignStudio expanded library, this style emphasizes ${tags.slice(0, 3).join(', ').toLowerCase()} aesthetics.`,
    mood: `${adj}, ${archetype.charAt(0).toUpperCase() + archetype.slice(1)}, ${pickRandom(['Confident', 'Focused', 'Expressive', 'Refined', 'Dynamic'], seed * 11)}`,
    popularity: Math.max(20, 80 - (seed % 60)),
    tags,
    colors,
    neutrals: palette.neutrals,
    fonts,
    typeScale: typeScales[density],
    spacing: spacingTemplates[density],
    borderRadius: radiusTemplates[radius],
    elevation: generateElevation(archetype),
    guidelines: generateGuidelines(archetype, colors[0].name),
    characteristics: tags.slice(0, 5),
    exampleWebsite: pickRandom(['SaaS Landing', 'Dashboard', 'Portfolio', 'E-commerce', 'Blog', 'Docs', 'Pricing Page', 'Settings', 'Onboarding', 'Marketing'], seed * 13),
    relatedStyleIds: [],
  };
}

// Main generation
function generateAllStyles(): EnrichedStyle[] {
  const all: EnrichedStyle[] = [];

  // 1. Add the 18 hand-crafted enriched styles
  all.push(...enrichedStyles);

  // 2. Convert the 187 design systems
  openDesignSystems.forEach((ds, i) => {
    // Skip if ID already exists in enriched styles
    if (!all.find(s => s.id === ds.id)) {
      all.push(systemToEnriched(ds, i));
    }
  });

  // 3. Generate procedural styles to reach 2,000
  let seed = 1;
  while (all.length < 2000) {
    const proc = generateProceduralStyle(seed);
    if (!all.find(s => s.id === proc.id)) {
      all.push(proc);
    }
    seed++;
  }

  // Compute related styles (find 3 with same archetype/category)
  all.forEach(style => {
    const related = all
      .filter(s => s.id !== style.id && (s.category === style.category || s.tags.some(t => style.tags.includes(t))))
      .sort((a, b) => {
        const aMatch = a.tags.filter(t => style.tags.includes(t)).length;
        const bMatch = b.tags.filter(t => style.tags.includes(t)).length;
        return bMatch - aMatch;
      })
      .slice(0, 4)
      .map(s => s.id);
    style.relatedStyleIds = related;
  });

  return all;
}

// Generate and write
const allStyles = generateAllStyles();
console.log(`Generated ${allStyles.length} styles`);

// Write as TypeScript
const output = `// Auto-generated style database — ${allStyles.length} styles
// DO NOT EDIT MANUALLY — regenerate with: npx tsx scripts/generate-style-db.ts
import type { EnrichedStyle } from '../src/data/enrichedStyles';

export const styleDatabase: EnrichedStyle[] = ${JSON.stringify(allStyles, null, 0).replace(/"([a-zA-Z_]+)":/g, '$1:')};
`;

fs.writeFileSync(__dirname + '/../src/data/styleDatabase.ts', output);
console.log('Written to src/data/styleDatabase.ts');
console.log(`File size: ${(fs.statSync(__dirname + '/../src/data/styleDatabase.ts').size / 1024).toFixed(0)}KB`);
