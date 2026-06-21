// Enriched Design Styles — Refero-grade detail for each style
// Adds: type scale, spacing system, border radius, elevation, do/don't guidelines,
// design tokens (CSS variables + Tailwind), popularity, tags, and related styles

export interface TypeScaleStep {
  name: string;
  size: string;
  weight: string;
  lineHeight: string;
  letterSpacing?: string;
  sample: string;
}

export interface SpacingSystem {
  density: 'compact' | 'comfortable' | 'spacious';
  baseUnit: string;
  maxWidth: string;
  sectionGap: string;
  cardPadding: string;
  elementGap: string;
}

export interface BorderRadiusSystem {
  badges: string;
  nav: string;
  inputs: string;
  buttons: string;
  cards: string;
}

export interface ElevationLevel {
  name: string;
  value: string;
  usage: string;
}

export interface DoDontRule {
  do: string;
  dont: string;
}

export interface DesignToken {
  name: string;
  value: string;
  type: 'color' | 'font' | 'spacing' | 'radius' | 'shadow';
}

export interface EnrichedStyle {
  id: string;
  name: string;
  category: string;
  tagline: string;
  description: string;
  mood: string;
  popularity: number;
  tags: string[];
  colors: {
    name: string;
    hex: string;
    usage: string;
  }[];
  neutrals: {
    name: string;
    hex: string;
    usage: string;
  }[];
  fonts: {
    primary: { name: string; weights: string; sizes: string; usage: string; fallback: string };
    secondary?: { name: string; weights: string; sizes: string; usage: string; fallback: string };
  };
  typeScale: TypeScaleStep[];
  spacing: SpacingSystem;
  borderRadius: BorderRadiusSystem;
  elevation: ElevationLevel[];
  guidelines: DoDontRule[];
  characteristics: string[];
  exampleWebsite: string;
  relatedStyleIds: string[];
}

export const enrichedStyles: EnrichedStyle[] = [
  {
    id: 'swiss',
    name: 'Swiss / International Style',
    category: 'classic',
    tagline: 'Grid-based precision with objective clarity',
    description: 'Grid-based precision with clean sans-serif typography. Objective clarity meets mathematical layouts. Think Helvetica, asymmetric balance, and content that speaks for itself.',
    mood: 'Professional, Objective, Timeless',
    popularity: 92,
    tags: ['Minimal', 'Grid', 'Clean', 'Typography'],
    colors: [
      { name: 'Swiss Red', hex: '#FF3B30', usage: 'Single accent for CTAs, active states, and focal emphasis' },
      { name: 'Pure Black', hex: '#000000', usage: 'Primary text, headings, structural elements' },
      { name: 'Paper White', hex: '#FFFFFF', usage: 'Page background, card surfaces' },
      { name: 'Light Gray', hex: '#F5F5F5', usage: 'Secondary surfaces, subtle backgrounds' },
      { name: 'Charcoal', hex: '#1A1A1A', usage: 'Secondary text, borders, dividers' },
    ],
    neutrals: [
      { name: 'Ink', hex: '#0A0A0A', usage: 'Primary text' },
      { name: 'Smoke', hex: '#6B6B6B', usage: 'Secondary text' },
      { name: 'Mist', hex: '#D4D4D4', usage: 'Tertiary text, borders' },
      { name: 'Fog', hex: '#F5F5F5', usage: 'Surface backgrounds' },
      { name: 'Paper', hex: '#FFFFFF', usage: 'Canvas' },
    ],
    fonts: {
      primary: { name: 'Helvetica Now Display', weights: '400, 500, 700', sizes: '12–72px', usage: 'All UI text — headings, body, navigation, buttons', fallback: 'Helvetica, Arial, sans-serif' },
      secondary: { name: 'Inter', weights: '400, 500, 600', sizes: '13–48px', usage: 'Body text, captions, metadata', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '72px', weight: '700', lineHeight: '1', letterSpacing: '-0.03em', sample: 'The quick brown fox' },
      { name: 'heading-lg', size: '48px', weight: '700', lineHeight: '1.05', letterSpacing: '-0.02em', sample: 'The quick brown fox' },
      { name: 'heading', size: '32px', weight: '500', lineHeight: '1.2', sample: 'The quick brown fox' },
      { name: 'subheading', size: '20px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body-lg', size: '18px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '14px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
      { name: 'label', size: '12px', weight: '500', lineHeight: '1.4', letterSpacing: '0.02em', sample: 'THE QUICK BROWN FOX' },
    ],
    spacing: { density: 'comfortable', baseUnit: '8px', maxWidth: '1200px', sectionGap: '80px', cardPadding: '32px', elementGap: '16px' },
    borderRadius: { badges: '0px', nav: '0px', inputs: '0px', buttons: '0px', cards: '0px' },
    elevation: [
      { name: 'flat', value: 'none', usage: 'All surfaces — Swiss style rejects shadows' },
      { name: 'border', value: '1px solid #D4D4D4', usage: 'Card edges, dividers' },
      { name: 'hairline', value: '0.5px solid #1A1A1A', usage: 'Typography underlines, precise dividers' },
    ],
    guidelines: [
      { do: 'Use a strict 12-column grid for all layouts — the grid is the design', dont: 'Don\'t add decorative shadows or rounded corners — Swiss style is sharp and flat' },
      { do: 'Use one accent color (Swiss Red) sparingly for a single focal point per section', dont: 'Don\'t introduce multiple accent colors — restraint is the system' },
      { do: 'Use Helvetica at weight 700 for display, 400 for body — the weight contrast IS the hierarchy', dont: 'Don\'t use decorative or script fonts — the typeface must be invisible' },
      { do: 'Embrace asymmetric balance — left-aligned content with intentional negative space', dont: 'Don\'t center everything — centered layouts lose the mathematical precision' },
      { do: 'Use mathematical proportions (1:1.618, 1:1.414) for spacing and sizing', dont: 'Don\'t use arbitrary spacing values — every measurement should be calculated' },
    ],
    characteristics: ['Strict grid systems', 'Asymmetric layouts', 'Sans-serif typography', 'Negative space', 'Objective photography'],
    exampleWebsite: 'Architecture Firm',
    relatedStyleIds: ['modernism', 'minimalism', 'swisstypography', 'cleanui'],
  },
  {
    id: 'modernism',
    name: 'Modernism',
    category: 'classic',
    tagline: 'Form follows function. Extreme minimalism.',
    description: 'Form follows function. Extreme minimalism where every element must justify its existence. Rejection of ornamentation in favor of honest, functional design.',
    mood: 'Pure, Honest, Essential',
    popularity: 78,
    tags: ['Minimal', 'Functional', 'Clean'],
    colors: [
      { name: 'Black', hex: '#000000', usage: 'Primary text, structural elements' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas, surfaces' },
      { name: 'Silver', hex: '#C0C0C0', usage: 'Dividers, subtle borders' },
      { name: 'Graphite', hex: '#333333', usage: 'Secondary text, icons' },
      { name: 'Smoke', hex: '#E8E8E8', usage: 'Background surfaces, cards' },
    ],
    neutrals: [
      { name: 'Absolute', hex: '#000000', usage: 'Primary text' },
      { name: 'Concrete', hex: '#333333', usage: 'Secondary text' },
      { name: 'Steel', hex: '#6B6B6B', usage: 'Tertiary text' },
      { name: 'Ash', hex: '#C0C0C0', usage: 'Borders' },
      { name: 'Vapor', hex: '#E8E8E8', usage: 'Surfaces' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas' },
    ],
    fonts: {
      primary: { name: 'Grotesk Nova', weights: '300, 400, 500', sizes: '12–64px', usage: 'All UI text', fallback: 'Helvetica, Arial, sans-serif' },
      secondary: { name: 'Inter', weights: '400, 500', sizes: '14–18px', usage: 'Body text', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '64px', weight: '300', lineHeight: '1.1', letterSpacing: '-0.02em', sample: 'The quick brown fox' },
      { name: 'heading', size: '40px', weight: '400', lineHeight: '1.15', sample: 'The quick brown fox' },
      { name: 'subheading', size: '24px', weight: '400', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '13px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'spacious', baseUnit: '8px', maxWidth: '1280px', sectionGap: '96px', cardPadding: '40px', elementGap: '24px' },
    borderRadius: { badges: '0px', nav: '0px', inputs: '0px', buttons: '0px', cards: '0px' },
    elevation: [
      { name: 'none', value: 'none', usage: 'No shadows — depth comes from spacing and contrast' },
      { name: 'hairline', value: '1px solid #E8E8E8', usage: 'Minimal borders' },
    ],
    guidelines: [
      { do: 'Use weight 300 for display — light type conveys confidence through restraint', dont: 'Don\'t use bold weights for headlines — modernism whispers, it doesn\'t shout' },
      { do: 'Limit palette to black, white, and one neutral gray — color is decoration', dont: 'Don\'t introduce accent colors — the system is monochrome' },
      { do: 'Give elements 2x more space than feels necessary — modernism breathes', dont: 'Don\'t crowd the layout — if it feels tight, double the spacing' },
      { do: 'Use full-bleed imagery with no borders or rounded corners', dont: 'Don\'t frame images decoratively — let them sit on the canvas naturally' },
    ],
    characteristics: ['Function over form', 'Minimal ornamentation', 'Honest materials', 'Simplified geometry', 'Clean lines'],
    exampleWebsite: 'Design Studio',
    relatedStyleIds: ['swiss', 'minimalism', 'cleanui', 'bauhaus'],
  },
  {
    id: 'bauhaus',
    name: 'Bauhaus',
    category: 'classic',
    tagline: 'Art meets industry. Primary colors, geometric forms.',
    description: 'The marriage of art and industry. Geometric forms, primary colors, and the belief that design should serve humanity. Craftsmanship meets industrial production.',
    mood: 'Revolutionary, Geometric, Industrial',
    popularity: 81,
    tags: ['Geometric', 'Bold', 'Primary Colors', 'Artistic'],
    colors: [
      { name: 'Bauhaus Red', hex: '#FF0000', usage: 'Primary accent, CTAs, focal elements' },
      { name: 'Bauhaus Blue', hex: '#0000FF', usage: 'Secondary accent, links, navigation' },
      { name: 'Bauhaus Yellow', hex: '#FFFF00', usage: 'Tertiary accent, highlights, badges' },
      { name: 'Black', hex: '#000000', usage: 'Text, structural geometry' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas, negative space' },
    ],
    neutrals: [
      { name: 'Black', hex: '#000000', usage: 'Text, structure' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas' },
      { name: 'Gray', hex: '#888888', usage: 'Secondary text' },
    ],
    fonts: {
      primary: { name: 'Bauhaus93', weights: '400, 700', sizes: '14–72px', usage: 'Display, headings', fallback: 'Arial, sans-serif' },
      secondary: { name: 'Work Sans', weights: '400, 500, 600', sizes: '13–18px', usage: 'Body, UI text', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '72px', weight: '700', lineHeight: '0.95', sample: 'The quick brown fox' },
      { name: 'heading', size: '42px', weight: '700', lineHeight: '1.1', sample: 'The quick brown fox' },
      { name: 'subheading', size: '24px', weight: '400', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'label', size: '12px', weight: '500', lineHeight: '1.4', letterSpacing: '0.05em', sample: 'THE QUICK BROWN FOX' },
    ],
    spacing: { density: 'comfortable', baseUnit: '8px', maxWidth: '1200px', sectionGap: '80px', cardPadding: '32px', elementGap: '16px' },
    borderRadius: { badges: '0px', nav: '0px', inputs: '0px', buttons: '0px', cards: '0px' },
    elevation: [
      { name: 'flat', value: 'none', usage: 'Flat surfaces — geometry defines hierarchy' },
      { name: 'block', value: '4px 4px 0px #000000', usage: 'Hard offset shadows for geometric emphasis' },
    ],
    guidelines: [
      { do: 'Use primary colors (red, blue, yellow) as the only accent palette', dont: 'Don\'t use secondary or tertiary colors — the system is primary only' },
      { do: 'Build layouts from circles, squares, and triangles — geometric forms are the vocabulary', dont: 'Don\'t use organic shapes or freeform curves — geometry is the point' },
      { do: 'Use Bauhaus93 for display type — it IS the identity', dont: 'Don\'t substitute with generic sans-serifs for headlines' },
      { do: 'Apply hard offset shadows (4px 4px 0px) for depth — no soft blurs', dont: 'Don\'t use soft drop shadows — Bauhaus shadows are graphic, not atmospheric' },
    ],
    characteristics: ['Geometric shapes', 'Primary colors', 'Form follows function', 'Industrial materials', 'Functional furniture integration'],
    exampleWebsite: 'Furniture Brand',
    relatedStyleIds: ['swiss', 'modernism', 'retro', 'maximalism'],
  },
  {
    id: 'minimalism',
    name: 'Minimalism',
    category: 'classic',
    tagline: 'Extreme restraint. Clarity through reduction.',
    description: 'Extreme restraint as a design philosophy. Clarity through reduction. When you remove everything unnecessary, the essential becomes undeniable.',
    mood: 'Pure, Refined, Essential',
    popularity: 95,
    tags: ['Minimal', 'Clean', 'Whitespace', 'Refined'],
    colors: [
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas, primary surface' },
      { name: 'Black', hex: '#000000', usage: 'Primary text, maximal contrast' },
      { name: 'Off-White', hex: '#F8F8F8', usage: 'Secondary surfaces, cards' },
      { name: 'Light Gray', hex: '#E0E0E0', usage: 'Borders, dividers' },
      { name: 'Dark Gray', hex: '#333333', usage: 'Secondary text' },
    ],
    neutrals: [
      { name: 'Pure Black', hex: '#000000', usage: 'Primary text' },
      { name: 'Charcoal', hex: '#333333', usage: 'Secondary text' },
      { name: 'Gray', hex: '#888888', usage: 'Tertiary text' },
      { name: 'Light Gray', hex: '#E0E0E0', usage: 'Borders' },
      { name: 'Off-White', hex: '#F8F8F8', usage: 'Surfaces' },
      { name: 'Pure White', hex: '#FFFFFF', usage: 'Canvas' },
    ],
    fonts: {
      primary: { name: 'Söhne', weights: '300, 400, 500', sizes: '12–64px', usage: 'All UI text', fallback: 'Inter, system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '64px', weight: '300', lineHeight: '1.1', letterSpacing: '-0.02em', sample: 'The quick brown fox' },
      { name: 'heading', size: '36px', weight: '400', lineHeight: '1.2', sample: 'The quick brown fox' },
      { name: 'subheading', size: '20px', weight: '400', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.7', sample: 'The quick brown fox' },
      { name: 'caption', size: '13px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'spacious', baseUnit: '8px', maxWidth: '1080px', sectionGap: '120px', cardPadding: '48px', elementGap: '24px' },
    borderRadius: { badges: '0px', nav: '0px', inputs: '2px', buttons: '2px', cards: '0px' },
    elevation: [
      { name: 'none', value: 'none', usage: 'No shadows — hierarchy through whitespace and typography' },
      { name: 'hairline', value: '1px solid #E0E0E0', usage: 'Minimal borders only when necessary' },
    ],
    guidelines: [
      { do: 'Use weight 300 for display and 400 for body — lightness conveys luxury', dont: 'Don\'t use weights above 500 — boldness is noise' },
      { do: 'Limit to 2-3 colors total — black, white, and maybe one neutral', dont: 'Don\'t add accent colors — the absence of color IS the design' },
      { do: 'Use 120px+ section gaps — whitespace is the primary design element', dont: 'Don\'t reduce spacing to fit more content — if it doesn\'t fit, remove content' },
      { do: 'Let single elements dominate each screen — one hero, one message', dont: 'Don\'t create competing focal points — minimalism is singular focus' },
      { do: 'Use 2px border radius max — sharpness communicates precision', dont: 'Don\'t round corners beyond 4px — softness undermines the purity' },
    ],
    characteristics: ['Extreme reduction', 'Maximum whitespace', 'Limited palette', 'Essential only', 'Visual silence'],
    exampleWebsite: 'Luxury Brand',
    relatedStyleIds: ['modernism', 'swiss', 'cleanui', 'luxury'],
  },
  {
    id: 'editorial',
    name: 'Editorial / Print-Inspired',
    category: 'classic',
    tagline: 'Magazine-quality layouts with dramatic hierarchy',
    description: 'Magazine-quality layouts translated to screen. Strong hierarchy, serif typography, and the drama of print design meets digital interactivity.',
    mood: 'Sophisticated, Editorial, Dramatic',
    popularity: 87,
    tags: ['Editorial', 'Serif', 'Magazine', 'Typography'],
    colors: [
      { name: 'Ink Black', hex: '#1A1A1A', usage: 'Primary text, headlines' },
      { name: 'Paper', hex: '#FFFFFF', usage: 'Canvas, article backgrounds' },
      { name: 'Gold', hex: '#C9A959', usage: 'Accent, pull quotes, decorative elements' },
      { name: 'Deep Red', hex: '#8B0000', usage: 'Secondary accent, editorial marks' },
      { name: 'Cream', hex: '#F4F4F4', usage: 'Section backgrounds, sidebars' },
    ],
    neutrals: [
      { name: 'Ink', hex: '#1A1A1A', usage: 'Primary text' },
      { name: 'Smoke', hex: '#5A5A5A', usage: 'Secondary text' },
      { name: 'Stone', hex: '#8A8A8A', usage: 'Tertiary text, captions' },
      { name: 'Mist', hex: '#D4D4D4', usage: 'Borders, dividers' },
      { name: 'Cream', hex: '#F4F4F4', usage: 'Surfaces' },
      { name: 'Paper', hex: '#FFFFFF', usage: 'Canvas' },
    ],
    fonts: {
      primary: { name: 'Playfair Display', weights: '400, 700, 900', sizes: '14–72px', usage: 'Headlines, display, pull quotes', fallback: 'Georgia, serif' },
      secondary: { name: 'Source Serif Pro', weights: '400, 600', sizes: '14–20px', usage: 'Body text, articles', fallback: 'Georgia, serif' },
    },
    typeScale: [
      { name: 'display', size: '72px', weight: '900', lineHeight: '0.95', letterSpacing: '-0.02em', sample: 'The quick brown fox' },
      { name: 'heading-lg', size: '48px', weight: '700', lineHeight: '1.05', sample: 'The quick brown fox' },
      { name: 'heading', size: '32px', weight: '700', lineHeight: '1.15', sample: 'The quick brown fox' },
      { name: 'subheading', size: '22px', weight: '400', lineHeight: '1.35', sample: 'The quick brown fox' },
      { name: 'body', size: '17px', weight: '400', lineHeight: '1.7', sample: 'The quick brown fox' },
      { name: 'caption', size: '13px', weight: '600', lineHeight: '1.4', letterSpacing: '0.03em', sample: 'THE QUICK BROWN FOX' },
    ],
    spacing: { density: 'comfortable', baseUnit: '8px', maxWidth: '720px', sectionGap: '64px', cardPadding: '32px', elementGap: '16px' },
    borderRadius: { badges: '0px', nav: '0px', inputs: '0px', buttons: '0px', cards: '0px' },
    elevation: [
      { name: 'flat', value: 'none', usage: 'No shadows — print aesthetic' },
      { name: 'rule', value: '1px solid #1A1A1A', usage: 'Horizontal rules between sections' },
    ],
    guidelines: [
      { do: 'Use serif typefaces throughout — Playfair for display, Source Serif for body', dont: 'Don\'t use sans-serif for body text — the serif IS the editorial voice' },
      { do: 'Use a narrow column width (max 720px) for articles — readability is paramount', dont: 'Don\'t stretch text across full width — print columns are narrow' },
      { do: 'Use drop caps, pull quotes, and horizontal rules as structural decoration', dont: 'Don\'t use cards or boxes — editorial design uses typography, not containers' },
      { do: 'Apply weight 900 for display headlines — dramatic contrast is the point', dont: 'Don\'t use light weights for headlines — editorial is bold and theatrical' },
      { do: 'Use gold (#C9A959) as a single decorative accent for pull quotes and marks', dont: 'Don\'t introduce multiple accent colors — one decorative color only' },
    ],
    characteristics: ['Strong hierarchy', 'Serif typography', 'Editorial layouts', 'Dramatic contrasts', 'White space as design'],
    exampleWebsite: 'Fashion Magazine',
    relatedStyleIds: ['editorialmax', 'luxury', 'typographic', 'swisstypography'],
  },
  {
    id: 'flat',
    name: 'Flat Design',
    category: 'contemporary',
    tagline: 'No depth, no shadows — pure shape and color',
    description: 'No depth, no shadows, just pure shape and color. Flat design strips away skeuomorphism to reveal the essence of digital interfaces.',
    mood: 'Clean, Modern, Approachable',
    popularity: 73,
    tags: ['Flat', 'Colorful', 'Modern', '2D'],
    colors: [
      { name: 'Ocean Blue', hex: '#3498DB', usage: 'Primary actions, links' },
      { name: 'Coral Red', hex: '#E74C3C', usage: 'Errors, destructive actions' },
      { name: 'Emerald', hex: '#2ECC71', usage: 'Success states, confirmations' },
      { name: 'Golden', hex: '#F1C40F', usage: 'Warnings, highlights' },
      { name: 'Amethyst', hex: '#9B59B6', usage: 'Secondary accent, tags' },
    ],
    neutrals: [
      { name: 'Dark', hex: '#2C3E50', usage: 'Primary text' },
      { name: 'Gray', hex: '#7F8C8D', usage: 'Secondary text' },
      { name: 'Silver', hex: '#BDC3C7', usage: 'Borders' },
      { name: 'Cloud', hex: '#ECF0F1', usage: 'Surfaces' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas' },
    ],
    fonts: {
      primary: { name: 'Proxima Nova', weights: '400, 600, 700', sizes: '12–48px', usage: 'All UI text', fallback: 'system-ui, sans-serif' },
      secondary: { name: 'Open Sans', weights: '400, 600', sizes: '14–18px', usage: 'Body text', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '48px', weight: '700', lineHeight: '1.1', sample: 'The quick brown fox' },
      { name: 'heading', size: '32px', weight: '600', lineHeight: '1.2', sample: 'The quick brown fox' },
      { name: 'subheading', size: '20px', weight: '600', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '14px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'comfortable', baseUnit: '8px', maxWidth: '1200px', sectionGap: '64px', cardPadding: '24px', elementGap: '16px' },
    borderRadius: { badges: '12px', nav: '8px', inputs: '8px', buttons: '8px', cards: '12px' },
    elevation: [
      { name: 'none', value: 'none', usage: 'No shadows — flat is flat' },
      { name: 'border', value: '1px solid #BDC3C7', usage: 'Card and input borders' },
    ],
    guidelines: [
      { do: 'Use bold, saturated colors as the primary visual language', dont: 'Don\'t use subtle or muted colors — flat design is confident and bright' },
      { do: 'Use solid color fills for buttons and cards — no gradients', dont: 'Don\'t add gradients or textures — flat means flat' },
      { do: 'Use 8-12px border radius for a friendly, approachable feel', dont: 'Don\'t use sharp corners — flat design is friendly, not harsh' },
      { do: 'Use simple iconography with solid fills — no outline icons', dont: 'Don\'t mix filled and outlined icons — consistency is key' },
    ],
    characteristics: ['No depth/shadows', 'Simple shapes', 'Bold colors', '2D elements', 'Clean icons'],
    exampleWebsite: 'Mobile App',
    relatedStyleIds: ['material', 'cleanui', 'playful', 'brutalist'],
  },
  {
    id: 'glassmorphism',
    name: 'Glassmorphism',
    category: 'contemporary',
    tagline: 'Frosted glass aesthetics with translucent depth',
    description: 'Frosted glass aesthetics with translucency and depth. Layers that float, blur that adds mystery, and transparency as design element.',
    mood: 'Ethereal, Modern, Sleek',
    popularity: 84,
    tags: ['Glass', 'Blur', 'Translucent', 'Modern', 'Gradient'],
    colors: [
      { name: 'White', hex: '#FFFFFF', usage: 'Glass surfaces, text on dark' },
      { name: 'Indigo', hex: '#667EEA', usage: 'Primary accent, gradient start' },
      { name: 'Violet', hex: '#764BA2', usage: 'Secondary accent, gradient end' },
      { name: 'Dark', hex: '#000000', usage: 'Background, text on glass' },
      { name: 'Mist', hex: '#F0F0F0', usage: 'Light surfaces' },
    ],
    neutrals: [
      { name: 'Void', hex: '#000000', usage: 'Background behind glass' },
      { name: 'Shadow', hex: '#1A1A2E', usage: 'Dark surface' },
      { name: 'Mist', hex: '#F0F0F0', usage: 'Light surface' },
      { name: 'White', hex: '#FFFFFF', usage: 'Glass surface' },
    ],
    fonts: {
      primary: { name: 'SF Pro Display', weights: '400, 500, 600', sizes: '12–48px', usage: 'All UI text', fallback: 'system-ui, sans-serif' },
      secondary: { name: 'SF Pro Text', weights: '400, 500', sizes: '14–18px', usage: 'Body text', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '48px', weight: '600', lineHeight: '1.1', sample: 'The quick brown fox' },
      { name: 'heading', size: '32px', weight: '600', lineHeight: '1.2', sample: 'The quick brown fox' },
      { name: 'subheading', size: '20px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '13px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'comfortable', baseUnit: '8px', maxWidth: '1200px', sectionGap: '64px', cardPadding: '32px', elementGap: '16px' },
    borderRadius: { badges: '12px', nav: '16px', inputs: '12px', buttons: '12px', cards: '24px' },
    elevation: [
      { name: 'glass', value: '0 8px 32px rgba(0,0,0,0.3)', usage: 'Glass cards with backdrop-blur' },
      { name: 'float', value: '0 4px 16px rgba(0,0,0,0.15)', usage: 'Floating elements' },
      { name: 'deep', value: '0 16px 48px rgba(0,0,0,0.4)', usage: 'Modals, overlays' },
    ],
    guidelines: [
      { do: 'Use backdrop-filter: blur(12px) on glass surfaces — it\'s the defining property', dont: 'Don\'t use solid backgrounds on cards — glass requires translucency' },
      { do: 'Layer multiple glass surfaces at different opacities for depth', dont: 'Don\'t use a single glass layer — the effect needs stacking' },
      { do: 'Use vibrant gradient backgrounds behind glass — the blur reveals the colors', dont: 'Don\'t use plain backgrounds — glassmorphism needs colorful blurs to work' },
      { do: 'Use 16-24px border radius — glass surfaces are soft and rounded', dont: 'Don\'t use sharp corners — glass is organic and flowing' },
      { do: 'Add a 1px semi-transparent white border to glass edges for the frosted effect', dont: 'Don\'t use solid borders — the edge should be a subtle light refraction' },
    ],
    characteristics: ['Frosted glass effect', 'Translucency', 'Depth layering', 'Blur backgrounds', 'Floating elements'],
    exampleWebsite: 'Music Player',
    relatedStyleIds: ['flat', 'neumorphism', 'modernism', 'cleanui'],
  },
  {
    id: 'brutalist',
    name: 'Brutalist Web Design',
    category: 'contemporary',
    tagline: 'Raw, unpolished, intentionally harsh anti-design',
    description: 'Raw, unpolished, intentionally harsh. Anti-design that rejects convention. Large type, bold colors, and the beauty of exposed structure.',
    mood: 'Raw, Bold, Unapologetic',
    popularity: 69,
    tags: ['Brutalist', 'Raw', 'Bold', 'High Contrast'],
    colors: [
      { name: 'Warning Red', hex: '#FF0000', usage: 'Alarms, critical emphasis, harsh contrast' },
      { name: 'Caution Yellow', hex: '#FFFF00', usage: 'Highlights, badges, brutalist accents' },
      { name: 'Black', hex: '#000000', usage: 'Text, borders, structural elements' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas, contrast' },
      { name: 'Link Blue', hex: '#0000FF', usage: 'Links, interactive elements' },
    ],
    neutrals: [
      { name: 'Black', hex: '#000000', usage: 'Text, structure' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas' },
      { name: 'Gray', hex: '#888888', usage: 'Rare secondary text' },
    ],
    fonts: {
      primary: { name: 'Space Mono', weights: '400, 700', sizes: '12–96px', usage: 'All text — monospace is the brutalist voice', fallback: 'Courier New, monospace' },
      secondary: { name: 'JetBrains Mono', weights: '400, 700', sizes: '12–48px', usage: 'Code, labels', fallback: 'monospace' },
    },
    typeScale: [
      { name: 'display', size: '96px', weight: '700', lineHeight: '0.9', sample: 'THE QUICK BROWN FOX' },
      { name: 'heading', size: '48px', weight: '700', lineHeight: '1', sample: 'THE QUICK BROWN FOX' },
      { name: 'subheading', size: '24px', weight: '700', lineHeight: '1.1', sample: 'THE QUICK BROWN FOX' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
      { name: 'label', size: '12px', weight: '700', lineHeight: '1.3', letterSpacing: '0.1em', sample: 'THE QUICK BROWN FOX' },
    ],
    spacing: { density: 'compact', baseUnit: '4px', maxWidth: '1400px', sectionGap: '32px', cardPadding: '16px', elementGap: '8px' },
    borderRadius: { badges: '0px', nav: '0px', inputs: '0px', buttons: '0px', cards: '0px' },
    elevation: [
      { name: 'none', value: 'none', usage: 'No soft shadows' },
      { name: 'hard', value: '8px 8px 0px #000000', usage: 'Hard offset shadows — no blur' },
      { name: 'border', value: '3px solid #000000', usage: 'Thick black borders' },
    ],
    guidelines: [
      { do: 'Use thick black borders (3-4px) on everything — borders ARE the design', dont: 'Don\'t use subtle borders or hairlines — brutalist borders are THICK' },
      { do: 'Use hard offset shadows (8px 8px 0px) — no blur, no softness', dont: 'Don\'t use soft drop shadows — brutalist shadows are graphic blocks' },
      { do: 'Use monospace type at extreme sizes — 96px+ for display', dont: 'Don\'t use elegant serif or refined sans-serif — brutalism is raw' },
      { do: 'Use high-contrast primary colors (red, yellow, blue) with no gradients', dont: 'Don\'t use pastels or muted tones — colors should clash' },
      { do: 'Break the grid intentionally — misaligned elements are deliberate', dont: 'Don\'t align everything perfectly — controlled chaos is the point' },
    ],
    characteristics: ['Raw aesthetics', 'Large typography', 'Bold colors', 'Exposed structure', 'Anti-convention'],
    exampleWebsite: 'Art Gallery',
    relatedStyleIds: ['flat', 'maximalism', 'cyberpunk', 'experimental'],
  },
  {
    id: 'cleanui',
    name: 'Minimal UI / Clean UI',
    category: 'contemporary',
    tagline: 'High whitespace, restrained color, absolute clarity',
    description: 'High whitespace, restrained color, and absolute clarity. Every pixel earns its place. The sophistication of saying less.',
    mood: 'Clear, Focused, Sophisticated',
    popularity: 89,
    tags: ['Clean', 'Minimal', 'SaaS', 'Whitespace'],
    colors: [
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas, primary surface' },
      { name: 'Off-White', hex: '#F8F9FA', usage: 'Secondary surfaces' },
      { name: 'Dark', hex: '#212529', usage: 'Primary text' },
      { name: 'Border', hex: '#DEE2E6', usage: 'Subtle dividers, borders' },
      { name: 'Accent Cyan', hex: '#0DCAF0', usage: 'Single accent for CTAs' },
    ],
    neutrals: [
      { name: 'Ink', hex: '#212529', usage: 'Primary text' },
      { name: 'Slate', hex: '#495057', usage: 'Secondary text' },
      { name: 'Gray', hex: '#868E96', usage: 'Tertiary text' },
      { name: 'Silver', hex: '#CED4DA', usage: 'Borders' },
      { name: 'Cloud', hex: '#F8F9FA', usage: 'Surfaces' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas' },
    ],
    fonts: {
      primary: { name: 'DM Sans', weights: '400, 500, 700', sizes: '12–48px', usage: 'All UI text', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '48px', weight: '700', lineHeight: '1.1', letterSpacing: '-0.02em', sample: 'The quick brown fox' },
      { name: 'heading', size: '32px', weight: '700', lineHeight: '1.2', sample: 'The quick brown fox' },
      { name: 'subheading', size: '20px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '14px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'comfortable', baseUnit: '4px', maxWidth: '1200px', sectionGap: '64px', cardPadding: '24px', elementGap: '12px' },
    borderRadius: { badges: '6px', nav: '8px', inputs: '8px', buttons: '8px', cards: '12px' },
    elevation: [
      { name: 'rest', value: 'none', usage: 'Cards at rest — no shadow' },
      { name: 'hover', value: '0 2px 8px rgba(0,0,0,0.06)', usage: 'Card hover state — subtle lift' },
      { name: 'float', value: '0 8px 24px rgba(0,0,0,0.08)', usage: 'Dropdowns, popovers' },
    ],
    guidelines: [
      { do: 'Use generous whitespace (24-32px padding) to create focus', dont: 'Don\'t pack content tightly — whitespace IS the design' },
      { do: 'Use a single accent color for all interactive elements', dont: 'Don\'t introduce multiple accent colors — restraint is the system' },
      { do: 'Use 8-12px border radius for soft, approachable UI', dont: 'Don\'t use sharp corners or fully rounded pills — 8-12px is the sweet spot' },
      { do: 'Apply subtle shadows only on hover (0 2px 8px rgba(0,0,0,0.06))', dont: 'Don\'t use heavy shadows at rest — subtlety is sophistication' },
      { do: 'Use DM Sans throughout — it\'s clean, geometric, and neutral', dont: 'Don\'t mix font families — one font, weight variations only' },
    ],
    characteristics: ['Generous whitespace', 'Restrained colors', 'Clear hierarchy', 'Focused content', 'Invisible UI'],
    exampleWebsite: 'SaaS Dashboard',
    relatedStyleIds: ['minimalism', 'flat', 'swiss', 'modernism'],
  },
  {
    id: 'neumorphism',
    name: 'Neumorphism',
    category: 'contemporary',
    tagline: 'Soft shadows create subtle tactile depth',
    description: 'Soft shadows create subtle depth. Elements that appear to extrude from the background. Tactile surfaces that beg to be touched.',
    mood: 'Soft, Tactile, Calm',
    popularity: 64,
    tags: ['Soft', 'Tactile', 'Shadow', 'Calming'],
    colors: [
      { name: 'Surface', hex: '#E0E5EC', usage: 'Background canvas — everything sits on this' },
      { name: 'Soft Blue', hex: '#A3B1C6', usage: 'Secondary accent, pressed states' },
      { name: 'White', hex: '#FFFFFF', usage: 'Light shadow source' },
      { name: 'Dark', hex: '#2D3436', usage: 'Primary text' },
      { name: 'Medium Gray', hex: '#636E72', usage: 'Secondary text, icons' },
    ],
    neutrals: [
      { name: 'Dark', hex: '#2D3436', usage: 'Primary text' },
      { name: 'Gray', hex: '#636E72', usage: 'Secondary text' },
      { name: 'Soft', hex: '#A3B1C6', usage: 'Tertiary, borders' },
      { name: 'Surface', hex: '#E0E5EC', usage: 'Canvas — the key neumorphic color' },
      { name: 'White', hex: '#FFFFFF', usage: 'Shadow light source' },
    ],
    fonts: {
      primary: { name: 'Circular', weights: '400, 500, 700', sizes: '12–32px', usage: 'All UI text', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '32px', weight: '700', lineHeight: '1.2', sample: 'The quick brown fox' },
      { name: 'heading', size: '24px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'subheading', size: '18px', weight: '500', lineHeight: '1.4', sample: 'The quick brown fox' },
      { name: 'body', size: '15px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '13px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'comfortable', baseUnit: '8px', maxWidth: '1080px', sectionGap: '48px', cardPadding: '24px', elementGap: '16px' },
    borderRadius: { badges: '8px', nav: '12px', inputs: '12px', buttons: '12px', cards: '20px' },
    elevation: [
      { name: 'raised', value: '8px 8px 16px #BEBFC1, -8px -8px 16px #FFFFFF', usage: 'Extruded elements — dual shadow is the neumorphic signature' },
      { name: 'pressed', value: 'inset 4px 4px 8px #BEBFC1, inset -4px -4px 8px #FFFFFF', usage: 'Active/pressed states — inset dual shadow' },
      { name: 'flat', value: 'none', usage: 'Background elements' },
    ],
    guidelines: [
      { do: 'Use dual shadows (light top-left, dark bottom-right) on the same surface color', dont: 'Don\'t use different background colors for elements — neumorphism is monochromatic' },
      { do: 'Use inset shadows for pressed/active states', dont: 'Don\'t use color changes for active states — depth change IS the state' },
      { do: 'Keep the surface color consistent across the entire UI', dont: 'Don\'t vary the background — the illusion breaks' },
      { do: 'Use 12-20px border radius — soft rounded forms match the soft shadows', dont: 'Don\'t use sharp corners — they fight the tactile softness' },
      { do: 'Limit color to subtle accents — neumorphism is about depth, not color', dont: 'Don\'t use bold saturated colors — they break the calm' },
    ],
    characteristics: ['Soft shadows', 'Subtle depth', 'Tactile feel', 'Monochrome palette', 'Embossed elements'],
    exampleWebsite: 'Smart Home App',
    relatedStyleIds: ['glassmorphism', 'cleanui', 'flat', 'minimalism'],
  },
  {
    id: 'cyberpunk',
    name: 'Cyberpunk',
    category: 'tech',
    tagline: 'Neon, glitch, dystopian future aesthetic',
    description: 'Neon colors on dark backgrounds, glitch effects, and dystopian future vibes. For products that want to feel like they\'re from 2077.',
    mood: 'Neon, Dystopian, Electric',
    popularity: 76,
    tags: ['Neon', 'Dark', 'Glitch', 'Futuristic', 'Cyberpunk'],
    colors: [
      { name: 'Neon Cyan', hex: '#00F0FF', usage: 'Primary neon accent, glows, active states' },
      { name: 'Neon Magenta', hex: '#FF00FF', usage: 'Secondary neon, error states, highlights' },
      { name: 'Void Black', hex: '#0A0A0F', usage: 'Page background — deepest dark' },
      { name: 'Surface Dark', hex: '#14141F', usage: 'Card surfaces, panels' },
      { name: 'Neon Green', hex: '#39FF14', usage: 'Success, terminal text, data' },
    ],
    neutrals: [
      { name: 'Void', hex: '#0A0A0F', usage: 'Background' },
      { name: 'Panel', hex: '#14141F', usage: 'Surfaces' },
      { name: 'Steel', hex: '#1E1E2E', usage: 'Elevated surfaces' },
      { name: 'Border', hex: '#2A2A3A', usage: 'Borders, dividers' },
      { name: 'Fog', hex: '#8A8A9A', usage: 'Secondary text' },
      { name: 'White', hex: '#F0F0F5', usage: 'Primary text' },
    ],
    fonts: {
      primary: { name: 'Orbitron', weights: '400, 700, 900', sizes: '12–72px', usage: 'Display, headings — futuristic geometric', fallback: 'Arial, sans-serif' },
      secondary: { name: 'Rajdhani', weights: '400, 500, 600', sizes: '13–24px', usage: 'Body, UI text — condensed tech feel', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '72px', weight: '900', lineHeight: '0.95', letterSpacing: '0.02em', sample: 'THE QUICK BROWN FOX' },
      { name: 'heading', size: '40px', weight: '700', lineHeight: '1.1', sample: 'THE QUICK BROWN FOX' },
      { name: 'subheading', size: '24px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'label', size: '12px', weight: '600', lineHeight: '1.4', letterSpacing: '0.15em', sample: 'THE QUICK BROWN FOX' },
    ],
    spacing: { density: 'compact', baseUnit: '4px', maxWidth: '1400px', sectionGap: '48px', cardPadding: '20px', elementGap: '12px' },
    borderRadius: { badges: '0px', nav: '4px', inputs: '4px', buttons: '4px', cards: '4px' },
    elevation: [
      { name: 'neon', value: '0 0 20px rgba(0,240,255,0.3)', usage: 'Neon glow on active elements' },
      { name: 'panel', value: '0 4px 20px rgba(0,0,0,0.5)', usage: 'Card panels' },
      { name: 'deep', value: '0 0 40px rgba(255,0,255,0.2)', usage: 'Hero elements, dramatic glows' },
    ],
    guidelines: [
      { do: 'Use neon colors with text-shadow glows for the electric effect', dont: 'Don\'t use neon colors without glow — flat neon loses the effect' },
      { do: 'Keep backgrounds near-black (#0A0A0F) — neon needs darkness to pop', dont: 'Don\'t use light backgrounds — cyberpunk is dark-first' },
      { do: 'Use Orbitron for display and Rajdhani for body — the futuristic feel is in the fonts', dont: 'Don\'t use generic sans-serifs — the typeface IS the futurism' },
      { do: 'Add subtle glitch animations (clip-path, transform) on hover', dont: 'Don\'t overuse glitch effects — they lose impact when constant' },
      { do: 'Use thin borders (1px) in neon colors for panel edges', dont: 'Don\'t use thick borders — cyberpunk is precise and thin' },
    ],
    characteristics: ['Neon colors', 'Dark backgrounds', 'Glitch effects', 'Futuristic fonts', 'Grid overlays'],
    exampleWebsite: 'Gaming Platform',
    relatedStyleIds: ['futurism', 'terminal', 'brutalist', 'data'],
  },
  {
    id: 'terminal',
    name: 'Terminal / CLI',
    category: 'tech',
    tagline: 'Monospace, data-dense, command-center aesthetic',
    description: 'Monospace-heavy, data-dense, dark backgrounds. Designed for power users who live in the terminal. Command-line aesthetics translated to web.',
    mood: 'Technical, Dense, Command-Center',
    popularity: 71,
    tags: ['Terminal', 'Monospace', 'Dark', 'Developer', 'CLI'],
    colors: [
      { name: 'Terminal Green', hex: '#39FF14', usage: 'Primary accent, active states, success' },
      { name: 'Void', hex: '#0D0D0D', usage: 'Page background — deepest dark' },
      { name: 'Panel', hex: '#141414', usage: 'Card surfaces, terminal windows' },
      { name: 'Amber', hex: '#FFB000', usage: 'Warnings, highlights, cursor' },
      { name: 'Error Red', hex: '#FF3B30', usage: 'Errors, destructive actions' },
    ],
    neutrals: [
      { name: 'Void', hex: '#0D0D0D', usage: 'Background' },
      { name: 'Panel', hex: '#141414', usage: 'Surfaces' },
      { name: 'Surface', hex: '#1A1A1A', usage: 'Elevated surfaces' },
      { name: 'Border', hex: '#333333', usage: 'Borders' },
      { name: 'Dim', hex: '#666666', usage: 'Tertiary text' },
      { name: 'Text', hex: '#E4E4E4', usage: 'Primary text' },
    ],
    fonts: {
      primary: { name: 'JetBrains Mono', weights: '400, 500, 700', sizes: '11–32px', usage: 'All text — monospace throughout', fallback: 'SF Mono, monospace' },
      secondary: { name: 'SF Mono', weights: '400, 500', sizes: '12–16px', usage: 'Secondary code, metadata', fallback: 'monospace' },
    },
    typeScale: [
      { name: 'display', size: '32px', weight: '700', lineHeight: '1.1', sample: 'THE QUICK BROWN FOX' },
      { name: 'heading', size: '24px', weight: '500', lineHeight: '1.2', sample: 'The quick brown fox' },
      { name: 'subheading', size: '18px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '14px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '12px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'compact', baseUnit: '4px', maxWidth: '1280px', sectionGap: '32px', cardPadding: '16px', elementGap: '8px' },
    borderRadius: { badges: '2px', nav: '4px', inputs: '4px', buttons: '4px', cards: '4px' },
    elevation: [
      { name: 'panel', value: '0 2px 8px rgba(0,0,0,0.4)', usage: 'Terminal panels' },
      { name: 'border', value: '1px solid #333333', usage: 'Panel borders' },
      { name: 'focus', value: '0 0 0 1px #39FF14', usage: 'Focus rings — terminal green' },
    ],
    guidelines: [
      { do: 'Use monospace throughout — it IS the terminal voice', dont: 'Don\'t use proportional fonts — the monospace grid is the design' },
      { do: 'Use terminal green (#39FF14) for active states and accents', dont: 'Don\'t use multiple accent colors — green + amber + red is the full palette' },
      { do: 'Keep backgrounds near-black — terminal UIs are dark-first', dont: 'Don\'t use light mode — terminals are dark by nature' },
      { do: 'Use 1px borders in #333 for panel separation', dont: 'Don\'t use thick borders — terminals are precise and minimal' },
      { do: 'Display data in tabular monospace format — alignment is automatic', dont: 'Don\'t use variable-width cards — monospace alignment is the advantage' },
    ],
    characteristics: ['Monospace typography', 'Dark backgrounds', 'Data-dense layouts', 'CLI aesthetics', 'Green-on-black'],
    exampleWebsite: 'Developer Tool',
    relatedStyleIds: ['cyberpunk', 'data', 'algorithmic', 'futurism'],
  },
  {
    id: 'luxury',
    name: 'Luxury',
    category: 'brand',
    tagline: 'Premium, exclusive, refined elegance',
    description: 'Premium materials, gold accents, and the confidence of brands that don\'t need to shout. Luxury design whispers. Every detail is intentional.',
    mood: 'Premium, Exclusive, Refined',
    popularity: 83,
    tags: ['Luxury', 'Premium', 'Gold', 'Elegant'],
    colors: [
      { name: 'Champagne Gold', hex: '#C9A959', usage: 'Primary accent — gold for luxury signaling' },
      { name: 'Onyx', hex: '#1A1A1A', usage: 'Primary text, dark surfaces' },
      { name: 'Ivory', hex: '#FFFFF0', usage: 'Canvas, light surfaces' },
      { name: 'Burgundy', hex: '#800020', usage: 'Secondary accent, editorial marks' },
      { name: 'Pearl', hex: '#F8F8F0', usage: 'Card surfaces, backgrounds' },
    ],
    neutrals: [
      { name: 'Onyx', hex: '#1A1A1A', usage: 'Primary text' },
      { name: 'Charcoal', hex: '#333333', usage: 'Secondary text' },
      { name: 'Stone', hex: '#888888', usage: 'Tertiary text' },
      { name: 'Pearl', hex: '#F8F8F0', usage: 'Surfaces' },
      { name: 'Ivory', hex: '#FFFFF0', usage: 'Canvas' },
    ],
    fonts: {
      primary: { name: 'Cormorant Garamond', weights: '300, 400, 600', sizes: '14–64px', usage: 'Display, headings — refined serif', fallback: 'Georgia, serif' },
      secondary: { name: 'Montserrat', weights: '300, 400, 500', sizes: '12–18px', usage: 'Body, labels — clean sans-serif', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '64px', weight: '300', lineHeight: '1.1', letterSpacing: '-0.01em', sample: 'The quick brown fox' },
      { name: 'heading', size: '40px', weight: '400', lineHeight: '1.2', sample: 'The quick brown fox' },
      { name: 'subheading', size: '22px', weight: '300', lineHeight: '1.35', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '300', lineHeight: '1.8', sample: 'The quick brown fox' },
      { name: 'label', size: '11px', weight: '500', lineHeight: '1.4', letterSpacing: '0.15em', sample: 'THE QUICK BROWN FOX' },
    ],
    spacing: { density: 'spacious', baseUnit: '8px', maxWidth: '1080px', sectionGap: '96px', cardPadding: '40px', elementGap: '24px' },
    borderRadius: { badges: '0px', nav: '0px', inputs: '2px', buttons: '2px', cards: '2px' },
    elevation: [
      { name: 'none', value: 'none', usage: 'No shadows — luxury is flat and confident' },
      { name: 'hairline', value: '1px solid #C9A959', usage: 'Gold hairlines for separators' },
    ],
    guidelines: [
      { do: 'Use weight 300 for display — luxury whispers through light type', dont: 'Don\'t use bold weights — luxury is never loud' },
      { do: 'Use gold (#C9A959) as the only accent — it signals premium globally', dont: 'Don\'t introduce bright or saturated colors — luxury is muted' },
      { do: 'Use generous spacing (96px+ section gaps) — space conveys exclusivity', dont: 'Don\'t crowd content — luxury needs room to breathe' },
      { do: 'Use Cormorant Garamond for display — the serif communicates heritage', dont: 'Don\'t use geometric sans-serifs for headlines — they feel techy, not luxurious' },
      { do: 'Use wide letter-spacing (0.15em) on labels and CTAs — it feels considered', dont: 'Don\'t use tight tracking on small text — spacing is a luxury signal' },
    ],
    characteristics: ['Premium materials', 'Gold accents', 'Refined typography', 'Generous whitespace', 'Heritage feel'],
    exampleWebsite: 'Luxury Fashion',
    relatedStyleIds: ['editorial', 'minimalism', 'modernism', 'corporate'],
  },
  {
    id: 'maximalism',
    name: 'Maximalism',
    category: 'expressive',
    tagline: 'More is more. Bold, dense, unapologetically rich.',
    description: 'More is more. Bold colors, dense visuals, and expressive chaos. The antidote to minimalist fatigue. Unapologetically rich and layered.',
    mood: 'Bold, Expressive, Chaotic',
    popularity: 62,
    tags: ['Maximalist', 'Bold', 'Colorful', 'Expressive', 'Dense'],
    colors: [
      { name: 'Hot Pink', hex: '#FF1493', usage: 'Primary accent, bold statements' },
      { name: 'Teal', hex: '#00CED1', usage: 'Secondary accent, contrast' },
      { name: 'Gold', hex: '#FFD700', usage: 'Tertiary accent, highlights' },
      { name: 'Deep Magenta', hex: '#8B008B', usage: 'Quaternary, depth' },
      { name: 'Orange Red', hex: '#FF4500', usage: 'Energy, urgency, CTAs' },
    ],
    neutrals: [
      { name: 'Black', hex: '#000000', usage: 'Text, structure' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas, contrast' },
    ],
    fonts: {
      primary: { name: 'Casablanca', weights: '400, 700, 900', sizes: '14–96px', usage: 'Display — bold and theatrical', fallback: 'Impact, sans-serif' },
      secondary: { name: 'Cooper Black', weights: '400, 700', sizes: '14–48px', usage: 'Headings, body — chunky and friendly', fallback: 'Georgia, serif' },
    },
    typeScale: [
      { name: 'display', size: '96px', weight: '900', lineHeight: '0.9', sample: 'THE QUICK BROWN FOX' },
      { name: 'heading', size: '56px', weight: '900', lineHeight: '0.95', sample: 'THE QUICK BROWN FOX' },
      { name: 'subheading', size: '28px', weight: '700', lineHeight: '1.1', sample: 'The quick brown fox' },
      { name: 'body', size: '18px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
      { name: 'caption', size: '14px', weight: '700', lineHeight: '1.3', sample: 'THE QUICK BROWN FOX' },
    ],
    spacing: { density: 'compact', baseUnit: '4px', maxWidth: '1400px', sectionGap: '32px', cardPadding: '16px', elementGap: '8px' },
    borderRadius: { badges: '24px', nav: '16px', inputs: '16px', buttons: '24px', cards: '32px' },
    elevation: [
      { name: 'block', value: '8px 8px 0px #000000', usage: 'Hard offset shadows — graphic and bold' },
      { name: 'stack', value: '0 4px 0px #FF1493, 0 8px 0px #00CED1', usage: 'Stacked color shadows for maximum impact' },
    ],
    guidelines: [
      { do: 'Use 5+ colors per layout — maximalism celebrates abundance', dont: 'Don\'t limit your palette — more colors, more energy' },
      { do: 'Use weight 900 for display — maximalist type is LOUD', dont: 'Don\'t use light or thin weights — this is not the place for restraint' },
      { do: 'Layer patterns, textures, and imagery densely', dont: 'Don\'t leave large empty spaces — fill the canvas' },
      { do: 'Use 24-32px border radius and hard offset shadows', dont: 'Don\'t use subtle shadows — maximalist shadows are graphic blocks' },
      { do: 'Mix font families — Casablanca + Cooper Black is intentionally eclectic', dont: 'Don\'t use a single font family — variety is the point' },
    ],
    characteristics: ['Bold colors', 'Dense layouts', 'Expressive typography', 'Layered visuals', 'Anti-minimalist'],
    exampleWebsite: 'Creative Agency',
    relatedStyleIds: ['bauhaus', 'brutalist', 'psychedelic', 'collage'],
  },
  {
    id: 'corporate',
    name: 'Corporate',
    category: 'brand',
    tagline: 'Safe, professional, trustworthy',
    description: 'Safe, professional, and brand-aligned. Structured grids, conservative palettes, and the visual language of business. Trust through consistency.',
    mood: 'Professional, Trustworthy, Structured',
    popularity: 70,
    tags: ['Corporate', 'Professional', 'Business', 'Trust'],
    colors: [
      { name: 'Corporate Blue', hex: '#0052CC', usage: 'Primary brand color, CTAs, links' },
      { name: 'Dark Navy', hex: '#091E42', usage: 'Primary text, headings' },
      { name: 'Light Blue', hex: '#DEEBFF', usage: 'Backgrounds, hover states' },
      { name: 'Green', hex: '#36B37E', usage: 'Success, positive metrics' },
      { name: 'Light Gray', hex: '#F4F5F7', usage: 'Surface backgrounds, cards' },
    ],
    neutrals: [
      { name: 'Navy', hex: '#091E42', usage: 'Primary text' },
      { name: 'Slate', hex: '#42526E', usage: 'Secondary text' },
      { name: 'Gray', hex: '#6B778C', usage: 'Tertiary text' },
      { name: 'Border', hex: '#DFE1E6', usage: 'Borders' },
      { name: 'Surface', hex: '#F4F5F7', usage: 'Card backgrounds' },
      { name: 'White', hex: '#FFFFFF', usage: 'Canvas' },
    ],
    fonts: {
      primary: { name: 'Inter', weights: '400, 500, 600, 700', sizes: '12–48px', usage: 'All UI text — the corporate standard', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '48px', weight: '700', lineHeight: '1.1', letterSpacing: '-0.02em', sample: 'The quick brown fox' },
      { name: 'heading', size: '32px', weight: '600', lineHeight: '1.2', sample: 'The quick brown fox' },
      { name: 'subheading', size: '20px', weight: '600', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '14px', weight: '400', lineHeight: '1.5', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'comfortable', baseUnit: '8px', maxWidth: '1200px', sectionGap: '64px', cardPadding: '24px', elementGap: '16px' },
    borderRadius: { badges: '4px', nav: '6px', inputs: '6px', buttons: '6px', cards: '8px' },
    elevation: [
      { name: 'rest', value: 'none', usage: 'Cards at rest' },
      { name: 'hover', value: '0 2px 4px rgba(0,0,0,0.08)', usage: 'Card hover' },
      { name: 'raised', value: '0 4px 12px rgba(0,0,0,0.1)', usage: 'Sticky nav, dropdowns' },
    ],
    guidelines: [
      { do: 'Use Corporate Blue (#0052CC) as the single brand accent', dont: 'Don\'t use multiple brand colors — consistency builds trust' },
      { do: 'Use Inter throughout — it\'s the corporate standard', dont: 'Don\'t use display fonts or experimental typefaces — corporate is safe' },
      { do: 'Use 6-8px border radius — professional but not harsh', dont: 'Don\'t use fully rounded corners — they feel too casual' },
      { do: 'Keep shadows subtle (rgba 0.08 max) — professionalism is understated', dont: 'Don\'t use dramatic shadows — they undermine trust' },
      { do: 'Use consistent component patterns — same button, same card, everywhere', dont: 'Don\'t vary component styles — consistency IS the corporate design' },
    ],
    characteristics: ['Structured grids', 'Conservative palette', 'Professional typography', 'Trust signals', 'Consistent components'],
    exampleWebsite: 'Enterprise Software',
    relatedStyleIds: ['cleanui', 'swiss', 'flat', 'luxury'],
  },
  {
    id: 'futurism',
    name: 'Futurism',
    category: 'tech',
    tagline: 'Tech-forward, neon-accented, sci-fi aesthetic',
    description: 'Technology-driven design with neon accents, HUD elements, and sci-fi aesthetics. For products that want to feel like they\'re from the future.',
    mood: 'Futuristic, Tech-Forward, Sci-Fi',
    popularity: 68,
    tags: ['Futuristic', 'Neon', 'HUD', 'Sci-Fi', 'Tech'],
    colors: [
      { name: 'Electric Blue', hex: '#00D4FF', usage: 'Primary accent, HUD elements, glows' },
      { name: 'Deep Space', hex: '#0A0E27', usage: 'Page background — deep dark blue' },
      { name: 'Panel', hex: '#131A36', usage: 'Card surfaces, HUD panels' },
      { name: 'Neon Purple', hex: '#B026FF', usage: 'Secondary accent, gradients' },
      { name: 'Cyan Glow', hex: '#00FFC8', usage: 'Active states, data viz' },
    ],
    neutrals: [
      { name: 'Space', hex: '#0A0E27', usage: 'Background' },
      { name: 'Panel', hex: '#131A36', usage: 'Surfaces' },
      { name: 'Border', hex: '#1E2940', usage: 'Borders' },
      { name: 'Dim', hex: '#4A5568', usage: 'Tertiary text' },
      { name: 'Mist', hex: '#A0AEC0', usage: 'Secondary text' },
      { name: 'White', hex: '#F7FAFC', usage: 'Primary text' },
    ],
    fonts: {
      primary: { name: 'Orbitron', weights: '400, 500, 700, 900', sizes: '12–64px', usage: 'Display, headings — geometric futuristic', fallback: 'Arial, sans-serif' },
      secondary: { name: 'Rajdhani', weights: '400, 500, 600', sizes: '13–20px', usage: 'Body, UI — condensed tech', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '64px', weight: '900', lineHeight: '1', letterSpacing: '0.02em', sample: 'THE QUICK BROWN FOX' },
      { name: 'heading', size: '40px', weight: '700', lineHeight: '1.1', sample: 'THE QUICK BROWN FOX' },
      { name: 'subheading', size: '22px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'label', size: '11px', weight: '600', lineHeight: '1.4', letterSpacing: '0.2em', sample: 'THE QUICK BROWN FOX' },
    ],
    spacing: { density: 'compact', baseUnit: '4px', maxWidth: '1400px', sectionGap: '48px', cardPadding: '20px', elementGap: '12px' },
    borderRadius: { badges: '4px', nav: '4px', inputs: '4px', buttons: '4px', cards: '8px' },
    elevation: [
      { name: 'glow', value: '0 0 20px rgba(0,212,255,0.25)', usage: 'HUD elements with electric glow' },
      { name: 'panel', value: '0 4px 24px rgba(0,0,0,0.4)', usage: 'Card panels' },
      { name: 'border-glow', value: '0 0 0 1px rgba(0,212,255,0.3), 0 0 12px rgba(0,212,255,0.15)', usage: 'Active panel borders' },
    ],
    guidelines: [
      { do: 'Use Orbitron for display — geometric letterforms signal future-tech', dont: 'Don\'t use humanist sans-serifs — they feel too present-day' },
      { do: 'Use electric blue (#00D4FF) with glow effects for HUD-style accents', dont: 'Don\'t use flat colors — futurism needs glow and light' },
      { do: 'Keep backgrounds deep dark blue (#0A0E27) — not pure black', dont: 'Don\'t use pure black — the slight blue tint adds depth' },
      { do: 'Use HUD-style UI elements: rings, data readouts, scan lines', dont: 'Don\'t use standard cards and forms — futurism needs custom UI' },
      { do: 'Add subtle animated grid overlays and scanline effects', dont: 'Don\'t keep everything static — futurism has gentle motion' },
    ],
    characteristics: ['Neon accents', 'HUD elements', 'Dark backgrounds', 'Geometric fonts', 'Glow effects'],
    exampleWebsite: 'Tech Startup',
    relatedStyleIds: ['cyberpunk', 'terminal', 'data', 'algorithmic'],
  },
  {
    id: 'playful',
    name: 'Playful',
    category: 'brand',
    tagline: 'Friendly, rounded, joyful with chunky elements',
    description: 'Friendly, rounded, and full of personality. Chunky shadows, bright colors, and a sense of joy. For products that want to feel like a friend.',
    mood: 'Friendly, Joyful, Approachable',
    popularity: 75,
    tags: ['Playful', 'Friendly', 'Rounded', 'Colorful', 'Fun'],
    colors: [
      { name: 'Sunny', hex: '#FFD93D', usage: 'Primary accent — joy and energy' },
      { name: 'Bubblegum', hex: '#FF6B9D', usage: 'Secondary accent — fun and friendly' },
      { name: 'Mint', hex: '#6BCB77', usage: 'Success, positive states' },
      { name: 'Sky', hex: '#4D96FF', usage: 'Links, info states' },
      { name: 'Cream', hex: '#FFF8E7', usage: 'Canvas — warm and soft' },
    ],
    neutrals: [
      { name: 'Soft Black', hex: '#2D2D2D', usage: 'Primary text — not harsh black' },
      { name: 'Warm Gray', hex: '#6B6B6B', usage: 'Secondary text' },
      { name: 'Light', hex: '#E8E8E8', usage: 'Borders' },
      { name: 'Cream', hex: '#FFF8E7', usage: 'Surfaces' },
      { name: 'White', hex: '#FFFFFF', usage: 'Cards' },
    ],
    fonts: {
      primary: { name: 'Fredoka', weights: '400, 500, 600, 700', sizes: '14–56px', usage: 'Display, headings — rounded and friendly', fallback: 'system-ui, sans-serif' },
      secondary: { name: 'Nunito', weights: '400, 600, 700', sizes: '14–18px', usage: 'Body text — soft and readable', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '56px', weight: '700', lineHeight: '1', sample: 'The quick brown fox' },
      { name: 'heading', size: '36px', weight: '600', lineHeight: '1.1', sample: 'The quick brown fox' },
      { name: 'subheading', size: '22px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '14px', weight: '600', lineHeight: '1.4', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'comfortable', baseUnit: '8px', maxWidth: '1080px', sectionGap: '48px', cardPadding: '24px', elementGap: '16px' },
    borderRadius: { badges: '20px', nav: '16px', inputs: '16px', buttons: '20px', cards: '24px' },
    elevation: [
      { name: 'chunky', value: '0 6px 0px #2D2D2D', usage: 'Chunky bottom shadow — the playful signature' },
      { name: 'soft', value: '0 4px 12px rgba(0,0,0,0.1)', usage: 'Soft shadow for secondary elements' },
      { name: 'float', value: '0 8px 24px rgba(0,0,0,0.12)', usage: 'Hover state — elements float up' },
    ],
    guidelines: [
      { do: 'Use Fredoka for display — rounded letterforms are inherently friendly', dont: 'Don\'t use sharp geometric fonts — they feel cold' },
      { do: 'Use 20-24px border radius — everything should look soft and huggable', dont: 'Don\'t use sharp corners — playful design is round' },
      { do: 'Use chunky shadows (0 6px 0px) for buttons and cards', dont: 'Don\'t use soft blurred shadows — chunky is the playful signature' },
      { do: 'Use bright, warm colors — yellow, pink, mint, sky blue', dont: 'Don\'t use dark or muted colors — playful is bright and warm' },
      { do: 'Add bounce animations on hover (scale 1.05, 200ms)', dont: 'Don\'t use linear or ease-in-out — playful needs bounce' },
    ],
    characteristics: ['Friendly shapes', 'Bright colors', 'Rounded corners', 'Chunky shadows', 'Joyful animations'],
    exampleWebsite: 'Educational App',
    relatedStyleIds: ['flat', 'duolingo', 'cleanui', 'maximalism'],
  },
  {
    id: 'retro',
    name: 'Retro / 70s-80s',
    category: 'brand',
    tagline: 'Nostalgic vibes with warm sunset palettes',
    description: 'Nostalgic design inspired by the 70s and 80s. Warm sunset gradients, geometric patterns, and the confident excess of a bygone era.',
    mood: 'Nostalgic, Warm, Confident',
    popularity: 66,
    tags: ['Retro', 'Nostalgic', '70s', '80s', 'Warm'],
    colors: [
      { name: 'Sunset Orange', hex: '#FF6B35', usage: 'Primary accent — warm sunset' },
      { name: 'Mustard', hex: '#FFB627', usage: 'Secondary accent — 70s warmth' },
      { name: 'Rust', hex: '#B85C38', usage: 'Tertiary — earthy retro tone' },
      { name: 'Cream', hex: '#FFF3E0', usage: 'Canvas — warm paper' },
      { name: 'Deep Brown', hex: '#3E2723', usage: 'Primary text — warm dark' },
    ],
    neutrals: [
      { name: 'Espresso', hex: '#3E2723', usage: 'Primary text' },
      { name: 'Mocha', hex: '#6D4C41', usage: 'Secondary text' },
      { name: 'Sand', hex: '#D7CCC8', usage: 'Borders' },
      { name: 'Cream', hex: '#FFF3E0', usage: 'Surfaces' },
      { name: 'Paper', hex: '#FFFAF0', usage: 'Canvas' },
    ],
    fonts: {
      primary: { name: 'Abril Fatface', weights: '400', sizes: '24–72px', usage: 'Display — retro dramatic serif', fallback: 'Georgia, serif' },
      secondary: { name: 'Work Sans', weights: '400, 500, 600', sizes: '14–18px', usage: 'Body, UI', fallback: 'system-ui, sans-serif' },
    },
    typeScale: [
      { name: 'display', size: '72px', weight: '400', lineHeight: '0.95', sample: 'The quick brown fox' },
      { name: 'heading', size: '42px', weight: '400', lineHeight: '1.05', sample: 'The quick brown fox' },
      { name: 'subheading', size: '24px', weight: '500', lineHeight: '1.3', sample: 'The quick brown fox' },
      { name: 'body', size: '16px', weight: '400', lineHeight: '1.6', sample: 'The quick brown fox' },
      { name: 'caption', size: '13px', weight: '500', lineHeight: '1.4', sample: 'The quick brown fox' },
    ],
    spacing: { density: 'comfortable', baseUnit: '8px', maxWidth: '1200px', sectionGap: '64px', cardPadding: '28px', elementGap: '16px' },
    borderRadius: { badges: '0px', nav: '0px', inputs: '0px', buttons: '0px', cards: '0px' },
    elevation: [
      { name: 'flat', value: 'none', usage: 'No shadows — retro is print-inspired' },
      { name: 'hard', value: '6px 6px 0px #3E2723', usage: 'Hard offset shadows in warm brown' },
    ],
    guidelines: [
      { do: 'Use warm sunset colors — orange, mustard, rust, cream', dont: 'Don\'t use cool blues or greens — retro is warm-only' },
      { do: 'Use Abril Fatface for display — the retro serif is the identity', dont: 'Don\'t use modern geometric sans-serifs — they break the era' },
      { do: 'Use hard offset shadows in warm brown (#3E2723)', dont: 'Don\'t use soft gray shadows — retro shadows are solid and warm' },
      { do: 'Keep borders sharp (0px radius) — retro design is angular', dont: 'Don\'t use rounded corners — the 70s/80s were sharp' },
      { do: 'Use geometric patterns (stripes, chevrons, sun rays) as decoration', dont: 'Don\'t use subtle textures — retro patterns are bold and geometric' },
    ],
    characteristics: ['Nostalgic palettes', 'Warm tones', 'Geometric patterns', 'Retro typography', 'Sunset gradients'],
    exampleWebsite: 'Lifestyle Brand',
    relatedStyleIds: ['bauhaus', 'maximalism', 'editorial', 'handcrafted'],
  },
];

// Category metadata for filters
export const enrichedCategories = [
  { id: 'all', name: 'All Styles', icon: '🎨' },
  { id: 'classic', name: 'Classic & Timeless', icon: '🏛️' },
  { id: 'contemporary', name: 'Contemporary & Digital', icon: '💻' },
  { id: 'tech', name: 'Tech & Futuristic', icon: '🚀' },
  { id: 'expressive', name: 'Expressive & Artistic', icon: '🎭' },
  { id: 'brand', name: 'Brand & Identity', icon: '⭐' },
];

// Sort options
export const sortOptions = [
  { id: 'popular', name: 'Popular' },
  { id: 'name', name: 'A-Z' },
  { id: 'category', name: 'Category' },
];

// Tag filter options (derived from styles)
export const allTags = [...new Set(enrichedStyles.flatMap(s => s.tags))].sort();
