// DESIGN.md + Tailwind v4 + CSS Variables generator utilities
import type { EnrichedStyle } from '../data/enrichedStyles';

export function generateDesignMd(style: EnrichedStyle): string {
  const colorsSection = style.colors.map(c => 
    `### ${c.name}\n\`${c.hex}\` — ${c.usage}`
  ).join('\n\n');

  const neutralsSection = style.neutrals.map(n => 
    `### ${n.name}\n\`${n.hex}\` — ${n.usage}`
  ).join('\n\n');

  const typeScaleSection = style.typeScale.map(t => 
    `### ${t.name}\n${t.size} · ${t.weight} · ${t.lineHeight}${t.letterSpacing ? ` · tracking ${t.letterSpacing}` : ''}\n\n> ${t.sample}`
  ).join('\n\n');

  const fontsSection = `
## Fonts

**Primary:** ${style.fonts.primary.name}
- Weights: ${style.fonts.primary.weights}
- Sizes: ${style.fonts.primary.sizes}
- Usage: ${style.fonts.primary.usage}
- Fallback: ${style.fonts.primary.fallback}
${style.fonts.secondary ? `
**Secondary:** ${style.fonts.secondary.name}
- Weights: ${style.fonts.secondary.weights}
- Sizes: ${style.fonts.secondary.sizes}
- Usage: ${style.fonts.secondary.usage}
- Fallback: ${style.fonts.secondary.fallback}` : ''}
`.trim();

  const doDontSection = style.guidelines.map((g, i) => 
    `### Rule ${i + 1}\n\n**Do:** ${g.do}\n\n**Don't:** ${g.dont}`
  ).join('\n\n');

  return `# ${style.name}

> ${style.tagline}

${style.description}

**Mood:** ${style.mood}

## Color Palette

${colorsSection}

## Neutrals

${neutralsSection}

## Typography

### Type Scale

${typeScaleSection}

${fontsSection}

## Spacing & Shape

| Purpose | Value |
| --- | --- |
| Density | ${style.spacing.density} |
| Base unit | ${style.spacing.baseUnit} |
| Max width | ${style.spacing.maxWidth} |
| Section gap | ${style.spacing.sectionGap} |
| Card padding | ${style.spacing.cardPadding} |
| Element gap | ${style.spacing.elementGap} |

### Border Radius

| Element | Value |
| --- | --- |
| Badges | ${style.borderRadius.badges} |
| Nav | ${style.borderRadius.nav} |
| Inputs | ${style.borderRadius.inputs} |
| Buttons | ${style.borderRadius.buttons} |
| Cards | ${style.borderRadius.cards} |

### Elevation

${style.elevation.map(e => `- **${e.name}:** \`${e.value}\` — ${e.usage}`).join('\n')}

## Guidelines

### Do
${style.guidelines.map(g => `- ${g.do}`).join('\n')}

### Don't
${style.guidelines.map(g => `- ${g.dont}`).join('\n')}

## Key Characteristics

${style.characteristics.map(c => `- ${c}`).join('\n')}

## Tags

${style.tags.map(t => `\`${t}\``).join(' ')}

---
*Generated from OpenDesignStudio*
`;
}

export function generateTailwindConfig(style: EnrichedStyle): string {
  const colorEntries = [...style.colors, ...style.neutrals]
    .map(c => `      '${c.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}': '${c.hex}'`)
    .join(',\n');

  const fontFamily = [
    `      'primary': ['${style.fonts.primary.name}', '${style.fonts.primary.fallback}']`,
    style.fonts.secondary ? `      'secondary': ['${style.fonts.secondary.name}', '${style.fonts.secondary.fallback}']` : '',
  ].filter(Boolean).join(',\n');

  const typeScaleEntries = style.typeScale.map(t => {
    const px = parseInt(t.size);
    const rem = (px / 16).toFixed(3);
    return `      '${t.name}': ['${rem}rem', { lineHeight: '${t.lineHeight}', fontWeight: '${t.weight}'${t.letterSpacing ? `, letterSpacing: '${t.letterSpacing}'` : ''} }]`;
  }).join(',\n');

  return `// tailwind.config.js — ${style.name}
export default {
  theme: {
    extend: {
      colors: {
${colorEntries}
      },
      fontFamily: {
${fontFamily}
      },
      fontSize: {
${typeScaleEntries}
      },
      borderRadius: {
        badge: '${style.borderRadius.badges}',
        nav: '${style.borderRadius.nav}',
        input: '${style.borderRadius.inputs}',
        btn: '${style.borderRadius.buttons}',
        card: '${style.borderRadius.cards}',
      },
      spacing: {
        section: '${style.spacing.sectionGap}',
        card: '${style.spacing.cardPadding}',
        element: '${style.spacing.elementGap}',
      },
      maxWidth: {
        container: '${style.spacing.maxWidth}',
      },
      boxShadow: {
${style.elevation.filter(e => e.value !== 'none').map((e, i) => `        'elevation-${i + 1}': '${e.value}'`).join(',\n')}
      },
    },
  },
};
`;
}

export function generateCssVariables(style: EnrichedStyle): string {
  const colorVars = style.colors.map(c => 
    `  --color-${c.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}: ${c.hex};`
  ).join('\n');

  const neutralVars = style.neutrals.map(n => 
    `  --color-${n.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}: ${n.hex};`
  ).join('\n');

  const typeVars = style.typeScale.map(t => {
    const px = parseInt(t.size);
    const rem = (px / 16).toFixed(3);
    return `  --text-${t.name}: ${rem}rem;
  --text-${t.name}-weight: ${t.weight};
  --text-${t.name}-line-height: ${t.lineHeight};${t.letterSpacing ? `\n  --text-${t.name}-tracking: ${t.letterSpacing};` : ''}`;
  }).join('\n');

  const radiusVars = `  --radius-badge: ${style.borderRadius.badges};
  --radius-nav: ${style.borderRadius.nav};
  --radius-input: ${style.borderRadius.inputs};
  --radius-btn: ${style.borderRadius.buttons};
  --radius-card: ${style.borderRadius.cards};`;

  const spacingVars = `  --space-base: ${style.spacing.baseUnit};
  --space-section: ${style.spacing.sectionGap};
  --space-card: ${style.spacing.cardPadding};
  --space-element: ${style.spacing.elementGap};
  --max-width: ${style.spacing.maxWidth};`;

  const shadowVars = style.elevation
    .filter(e => e.value !== 'none')
    .map((e, i) => `  --shadow-${i + 1}: ${e.value};`)
    .join('\n');

  const fontVars = `  --font-primary: '${style.fonts.primary.name}', ${style.fonts.primary.fallback};${style.fonts.secondary ? `\n  --font-secondary: '${style.fonts.secondary.name}', ${style.fonts.secondary.fallback};` : ''}`;

  return `:root {
  /* ${style.name} — CSS Variables */

  /* Colors */
${colorVars}

  /* Neutrals */
${neutralVars}

  /* Typography */
${typeVars}

  /* Fonts */
${fontVars}

  /* Border Radius */
${radiusVars}

  /* Spacing */
${spacingVars}

${shadowVars ? `  /* Elevation */\n${shadowVars}\n` : ''}}
`;
}

export function generateDesignTokens(style: EnrichedStyle): string {
  const tokens = [
    ...style.colors.map(c => ({ name: `color.${c.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}`, value: c.hex, type: 'color' as const })),
    ...style.neutrals.map(n => ({ name: `color.${n.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}`, value: n.hex, type: 'color' as const })),
    ...style.typeScale.map(t => ({ name: `type.${t.name}.size`, value: t.size, type: 'font' as const })),
    ...style.typeScale.map(t => ({ name: `type.${t.name}.weight`, value: t.weight, type: 'font' as const })),
    ...style.typeScale.map(t => ({ name: `type.${t.name}.lineHeight`, value: t.lineHeight, type: 'font' as const })),
  ];

  return JSON.stringify({
    $schema: 'https://design-tokens.org/format.json',
    name: style.name,
    description: style.tagline,
    tokens: tokens.reduce((acc, t) => {
      acc[t.name] = { value: t.value, type: t.type };
      return acc;
    }, {} as Record<string, { value: string; type: string }>),
  }, null, 2);
}
