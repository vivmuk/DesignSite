import { useState } from 'react';
import type { EnrichedStyle } from '../data/enrichedStyles';
import { enrichedStyles } from '../data/enrichedStyles';
import { generateDesignMd, generateTailwindConfig, generateCssVariables, generateDesignTokens } from '../utils/generators';

interface StyleDetailPageProps {
  style: EnrichedStyle;
  onBack: () => void;
  onSelectStyle: (style: EnrichedStyle) => void;
}

type ExportFormat = 'design-md' | 'tailwind' | 'css-vars' | 'tokens';

export function StyleDetailPage({ style, onBack, onSelectStyle }: StyleDetailPageProps) {
  const [activeFormat, setActiveFormat] = useState<ExportFormat>('design-md');
  const [copied, setCopied] = useState(false);
  const [copiedColor, setCopiedColor] = useState<string | null>(null);

  const exportContent = {
    'design-md': generateDesignMd(style),
    'tailwind': generateTailwindConfig(style),
    'css-vars': generateCssVariables(style),
    'tokens': generateDesignTokens(style),
  };

  const relatedStyles = style.relatedStyleIds
    .map(id => enrichedStyles.find(s => s.id === id))
    .filter(Boolean) as EnrichedStyle[];

  const handleCopy = () => {
    navigator.clipboard.writeText(exportContent[activeFormat]);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleCopyColor = (hex: string) => {
    navigator.clipboard.writeText(hex);
    setCopiedColor(hex);
    setTimeout(() => setCopiedColor(null), 1500);
  };

  const isDark = style.tags.includes('Dark') || style.tags.includes('Terminal') || style.tags.includes('Cyberpunk');

  return (
    <div className="style-detail-page">
      {/* Back button */}
      <button className="detail-back" onClick={onBack}>
        ← Back to Explore
      </button>

      {/* Header */}
      <header className="detail-header">
        <div className="detail-header-info">
          <h1>{style.name}</h1>
          <p className="detail-tagline">{style.tagline}</p>
          <p className="detail-mood">{style.mood}</p>
          <div className="detail-tags">
            {style.tags.map(tag => (
              <span key={tag} className="detail-tag">{tag}</span>
            ))}
          </div>
        </div>
        <div className="detail-header-preview" style={{
          background: isDark
            ? style.neutrals.find(n => n.name.toLowerCase().includes('void') || n.name.toLowerCase().includes('dark') || n.name.toLowerCase().includes('panel'))?.hex || '#0a0a0f'
            : style.neutrals.find(n => n.name.toLowerCase().includes('paper') || n.name.toLowerCase().includes('white') || n.name.toLowerCase().includes('canvas'))?.hex || '#ffffff',
          borderRadius: style.borderRadius.cards,
          border: `1px solid ${isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)'}`,
        }}>
          <div className="detail-mini-nav">
            <div className="detail-mini-logo" style={{ background: style.colors[0].hex, borderRadius: style.borderRadius.buttons }} />
            <div className="detail-mini-cta" style={{ background: style.colors[0].hex, borderRadius: style.borderRadius.buttons }} />
          </div>
          <div className="detail-mini-hero">
            <div className="detail-mini-h1" style={{ background: isDark ? 'rgba(255,255,255,0.6)' : 'rgba(0,0,0,0.6)', borderRadius: '2px' }} />
            <div className="detail-mini-h1 short" style={{ background: isDark ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.3)', borderRadius: '2px' }} />
            <div className="detail-mini-btn" style={{ background: style.colors[0].hex, borderRadius: style.borderRadius.buttons }} />
          </div>
        </div>
      </header>

      {/* Description */}
      <section className="detail-section">
        <p className="detail-description">{style.description}</p>
      </section>

      {/* Color Palette */}
      <section className="detail-section">
        <h2 className="detail-section-title">Color Palette</h2>
        <div className="detail-color-grid">
          {style.colors.map((color, i) => (
            <div key={i} className="detail-color-card" onClick={() => handleCopyColor(color.hex)}>
              <div className="detail-color-swatch" style={{ background: color.hex }} />
              <div className="detail-color-info">
                <span className="detail-color-name">{color.name}</span>
                <span className="detail-color-hex">{copiedColor === color.hex ? '✓ Copied!' : color.hex}</span>
                <span className="detail-color-usage">{color.usage}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Neutrals */}
      <section className="detail-section">
        <h2 className="detail-section-title">Neutrals</h2>
        <div className="detail-neutral-row">
          {style.neutrals.map((n, i) => (
            <div key={i} className="detail-neutral-chip" onClick={() => handleCopyColor(n.hex)}>
              <div className="detail-neutral-swatch" style={{ background: n.hex }} />
              <span className="detail-neutral-name">{n.name}</span>
              <span className="detail-neutral-hex">{copiedColor === n.hex ? '✓' : n.hex}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Typography */}
      <section className="detail-section">
        <h2 className="detail-section-title">Typography</h2>
        <div className="detail-fonts">
          <div className="detail-font-card">
            <span className="detail-font-label">Primary Font</span>
            <span className="detail-font-name">{style.fonts.primary.name}</span>
            <span className="detail-font-meta">Weights: {style.fonts.primary.weights}</span>
            <span className="detail-font-meta">Sizes: {style.fonts.primary.sizes}</span>
            <span className="detail-font-usage">{style.fonts.primary.usage}</span>
          </div>
          {style.fonts.secondary && (
            <div className="detail-font-card">
              <span className="detail-font-label">Secondary Font</span>
              <span className="detail-font-name">{style.fonts.secondary.name}</span>
              <span className="detail-font-meta">Weights: {style.fonts.secondary.weights}</span>
              <span className="detail-font-meta">Sizes: {style.fonts.secondary.sizes}</span>
              <span className="detail-font-usage">{style.fonts.secondary.usage}</span>
            </div>
          )}
        </div>

        {/* Type Scale */}
        <h3 className="detail-subsection-title">Type Scale</h3>
        <div className="detail-type-scale">
          {style.typeScale.map((step, i) => (
            <div key={i} className="detail-type-step">
              <div className="detail-type-info">
                <span className="detail-type-name">{step.name}</span>
                <span className="detail-type-meta">{step.size} · {step.weight} · {step.lineHeight}{step.letterSpacing ? ` · ${step.letterSpacing}` : ''}</span>
              </div>
              <div className="detail-type-sample" style={{
                fontFamily: `${style.fonts.primary.name}, ${style.fonts.primary.fallback}`,
                fontSize: `clamp(14px, ${parseInt(step.size) * 0.4}px, ${step.size})`,
                fontWeight: step.weight as any,
                lineHeight: step.lineHeight,
                letterSpacing: step.letterSpacing || 'normal',
              }}>
                {step.sample}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Spacing & Shape */}
      <section className="detail-section">
        <h2 className="detail-section-title">Spacing & Shape</h2>
        <div className="detail-spacing-grid">
          <div className="detail-spacing-item">
            <span className="detail-spacing-label">Density</span>
            <span className="detail-spacing-value">{style.spacing.density}</span>
          </div>
          <div className="detail-spacing-item">
            <span className="detail-spacing-label">Base Unit</span>
            <span className="detail-spacing-value">{style.spacing.baseUnit}</span>
          </div>
          <div className="detail-spacing-item">
            <span className="detail-spacing-label">Max Width</span>
            <span className="detail-spacing-value">{style.spacing.maxWidth}</span>
          </div>
          <div className="detail-spacing-item">
            <span className="detail-spacing-label">Section Gap</span>
            <span className="detail-spacing-value">{style.spacing.sectionGap}</span>
          </div>
          <div className="detail-spacing-item">
            <span className="detail-spacing-label">Card Padding</span>
            <span className="detail-spacing-value">{style.spacing.cardPadding}</span>
          </div>
          <div className="detail-spacing-item">
            <span className="detail-spacing-label">Element Gap</span>
            <span className="detail-spacing-value">{style.spacing.elementGap}</span>
          </div>
        </div>

        <h3 className="detail-subsection-title">Border Radius</h3>
        <div className="detail-radius-row">
          {Object.entries(style.borderRadius).map(([key, val]) => (
            <div key={key} className="detail-radius-item">
              <div className="detail-radius-preview" style={{ borderRadius: val }} />
              <span className="detail-radius-key">{key}</span>
              <span className="detail-radius-val">{val}</span>
            </div>
          ))}
        </div>

        <h3 className="detail-subsection-title">Elevation</h3>
        <div className="detail-elevation-list">
          {style.elevation.map((e, i) => (
            <div key={i} className="detail-elevation-item">
              <div className="detail-elevation-preview" style={{ boxShadow: e.value === 'none' ? undefined : e.value, border: e.value === 'none' ? '1px solid rgba(128,128,128,0.2)' : 'none' }}>
                <span>{e.name}</span>
              </div>
              <div className="detail-elevation-info">
                <span className="detail-elevation-name">{e.name}</span>
                <code className="detail-elevation-value">{e.value}</code>
                <span className="detail-elevation-usage">{e.usage}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Do / Don't Guidelines */}
      <section className="detail-section">
        <h2 className="detail-section-title">Guidelines</h2>
        <div className="detail-guidelines">
          {style.guidelines.map((rule, i) => (
            <div key={i} className="detail-guideline-pair">
              <div className="detail-guideline do">
                <span className="guideline-badge do-badge">✓ Do</span>
                <p>{rule.do}</p>
              </div>
              <div className="detail-guideline dont">
                <span className="guideline-badge dont-badge">✗ Don't</span>
                <p>{rule.dont}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Export Section */}
      <section className="detail-section">
        <h2 className="detail-section-title">Export</h2>
        <div className="detail-export">
          <div className="export-format-tabs">
            <button className={`export-tab ${activeFormat === 'design-md' ? 'active' : ''}`} onClick={() => setActiveFormat('design-md')}>
              DESIGN.md
            </button>
            <button className={`export-tab ${activeFormat === 'tailwind' ? 'active' : ''}`} onClick={() => setActiveFormat('tailwind')}>
              Tailwind v4
            </button>
            <button className={`export-tab ${activeFormat === 'css-vars' ? 'active' : ''}`} onClick={() => setActiveFormat('css-vars')}>
              CSS Variables
            </button>
            <button className={`export-tab ${activeFormat === 'tokens' ? 'active' : ''}`} onClick={() => setActiveFormat('tokens')}>
              Design Tokens
            </button>
          </div>
          <div className="export-preview">
            <div className="export-header">
              <span className="export-filename">
                {activeFormat === 'design-md' ? 'DESIGN.md' : activeFormat === 'tailwind' ? 'tailwind.config.js' : activeFormat === 'css-vars' ? 'tokens.css' : 'tokens.json'}
              </span>
              <button className="export-copy-btn" onClick={handleCopy}>
                {copied ? '✓ Copied!' : '📋 Copy'}
              </button>
            </div>
            <pre className="export-code"><code>{exportContent[activeFormat]}</code></pre>
          </div>
        </div>
      </section>

      {/* Characteristics */}
      <section className="detail-section">
        <h2 className="detail-section-title">Key Characteristics</h2>
        <div className="detail-characteristics">
          {style.characteristics.map((char, i) => (
            <span key={i} className="detail-characteristic">{char}</span>
          ))}
        </div>
      </section>

      {/* Related Styles */}
      {relatedStyles.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-section-title">More like this</h2>
          <div className="detail-related-grid">
            {relatedStyles.map(rs => (
              <div key={rs.id} className="detail-related-card" onClick={() => onSelectStyle(rs)}>
                <div className="related-swatches">
                  {rs.colors.slice(0, 4).map((c, i) => (
                    <div key={i} className="related-swatch" style={{ background: c.hex }} />
                  ))}
                </div>
                <span className="related-name">{rs.name}</span>
                <span className="related-tagline">{rs.tagline}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
