import { useState, useMemo } from 'react';
import { enrichedStyles, enrichedCategories, sortOptions, allTags, type EnrichedStyle } from '../data/enrichedStyles';

interface ExploreTabProps {
  onSelectStyle: (style: EnrichedStyle) => void;
}

export function ExploreTab({ onSelectStyle }: ExploreTabProps) {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');
  const [sortBy, setSortBy] = useState('popular');
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [showTags, setShowTags] = useState(false);

  const filtered = useMemo(() => {
    let items = [...enrichedStyles];

    if (category !== 'all') {
      items = items.filter(s => s.category === category);
    }

    if (activeTag) {
      items = items.filter(s => s.tags.includes(activeTag));
    }

    if (search) {
      const q = search.toLowerCase();
      items = items.filter(s =>
        s.name.toLowerCase().includes(q) ||
        s.description.toLowerCase().includes(q) ||
        s.tagline.toLowerCase().includes(q) ||
        s.tags.some(t => t.toLowerCase().includes(q)) ||
        s.characteristics.some(c => c.toLowerCase().includes(q))
      );
    }

    switch (sortBy) {
      case 'popular':
        items.sort((a, b) => b.popularity - a.popularity);
        break;
      case 'name':
        items.sort((a, b) => a.name.localeCompare(b.name));
        break;
      case 'category':
        items.sort((a, b) => a.category.localeCompare(b.category) || a.name.localeCompare(b.name));
        break;
    }

    return items;
  }, [search, category, sortBy, activeTag]);

  return (
    <div className="explore-tab">
      {/* Search Bar */}
      <div className="explore-search-bar">
        <input
          type="text"
          className="explore-search-input"
          placeholder="Search 2,000+ design styles…"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <button className="explore-tag-toggle" onClick={() => setShowTags(!showTags)}>
          🏷️ Tags
        </button>
      </div>

      {/* Category Filters */}
      <div className="explore-categories">
        {enrichedCategories.map(cat => (
          <button
            key={cat.id}
            className={`explore-cat-btn ${category === cat.id ? 'active' : ''}`}
            onClick={() => setCategory(cat.id)}
          >
            <span className="cat-icon">{cat.icon}</span>
            <span>{cat.name}</span>
          </button>
        ))}
      </div>

      {/* Tag Filters */}
      {showTags && (
        <div className="explore-tags-panel">
          {allTags.map(tag => (
            <button
              key={tag}
              className={`explore-tag-chip ${activeTag === tag ? 'active' : ''}`}
              onClick={() => setActiveTag(activeTag === tag ? null : tag)}
            >
              {tag}
            </button>
          ))}
        </div>
      )}

      {/* Sort + Count */}
      <div className="explore-meta">
        <span className="explore-count">{filtered.length} styles</span>
        <div className="explore-sort">
          {sortOptions.map(opt => (
            <button
              key={opt.id}
              className={`sort-btn ${sortBy === opt.id ? 'active' : ''}`}
              onClick={() => setSortBy(opt.id)}
            >
              {opt.name}
            </button>
          ))}
        </div>
      </div>

      {/* Style Card Grid */}
      <div className="explore-grid">
        {filtered.map(style => (
          <StyleCard key={style.id} style={style} onClick={() => onSelectStyle(style)} />
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="explore-empty">
          <p>No styles match your search.</p>
          <button onClick={() => { setSearch(''); setCategory('all'); setActiveTag(null); }}>
            Clear filters
          </button>
        </div>
      )}
    </div>
  );
}

function StyleCard({ style, onClick }: { style: EnrichedStyle; onClick: () => void }) {
  const primary = style.colors[0];
  const secondary = style.colors[1] || style.neutrals[0];
  const accent = style.colors[2] || style.colors[0];

  // Generate a mini preview using the style's palette
  const previewStyle: React.CSSProperties = {
    background: style.neutrals.find(n => n.name.toLowerCase().includes('paper') || n.name.toLowerCase().includes('white') || n.name.toLowerCase().includes('canvas'))?.hex || '#ffffff',
  };

  const isDark = style.tags.includes('Dark') || style.tags.includes('Terminal') || style.tags.includes('Cyberpunk');

  return (
    <div className="style-card-explore" onClick={onClick} style={previewStyle}>
      {/* Mini Preview */}
      <div className="card-mini-preview" style={{
        background: isDark
          ? style.neutrals.find(n => n.name.toLowerCase().includes('void') || n.name.toLowerCase().includes('dark') || n.name.toLowerCase().includes('panel'))?.hex || '#0a0a0f'
          : style.neutrals.find(n => n.name.toLowerCase().includes('paper') || n.name.toLowerCase().includes('white') || n.name.toLowerCase().includes('cream'))?.hex || '#ffffff',
      }}>
        <div className="mini-nav-bar" style={{ borderBottom: `1px solid ${isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)'}` }}>
          <div className="mini-logo" style={{ background: primary.hex, borderRadius: style.borderRadius.buttons }} />
          <div className="mini-nav-links">
            <div className="mini-nav-link" style={{ background: isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.08)' }} />
            <div className="mini-nav-link" style={{ background: isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.08)' }} />
            <div className="mini-nav-cta" style={{ background: primary.hex, borderRadius: style.borderRadius.buttons }} />
          </div>
        </div>
        <div className="mini-hero-area">
          <div className="mini-hero-title" style={{ background: isDark ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.7)', borderRadius: '2px' }} />
          <div className="mini-hero-sub" style={{ background: isDark ? 'rgba(255,255,255,0.25)' : 'rgba(0,0,0,0.2)', borderRadius: '2px' }} />
          <div className="mini-hero-btn" style={{ background: primary.hex, borderRadius: style.borderRadius.buttons }} />
        </div>
        <div className="mini-cards-row">
          {[0, 1, 2].map(i => (
            <div key={i} className="mini-card-item" style={{
              background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.04)',
              border: `1px solid ${isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)'}`,
              borderRadius: style.borderRadius.cards,
            }}>
              <div className="mini-card-icon" style={{ background: i === 0 ? primary.hex : i === 1 ? secondary.hex : accent.hex, borderRadius: '50%' }} />
              <div className="mini-card-line" style={{ background: isDark ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.15)' }} />
              <div className="mini-card-line short" style={{ background: isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.1)' }} />
            </div>
          ))}
        </div>
      </div>

      {/* Card Info */}
      <div className="card-info">
        <div className="card-header">
          <h3 className="card-title">{style.name}</h3>
          <span className="card-popularity" title="Popularity score">🔥 {style.popularity}</span>
        </div>
        <p className="card-tagline">{style.tagline}</p>
        <div className="card-tags">
          {style.tags.slice(0, 4).map(tag => (
            <span key={tag} className="card-tag">{tag}</span>
          ))}
        </div>
        <div className="card-swatches">
          {style.colors.slice(0, 5).map((c, i) => (
            <div key={i} className="card-swatch" style={{ background: c.hex }} title={`${c.name} — ${c.hex}`} />
          ))}
        </div>
        <div className="card-cta">
          View details →
        </div>
      </div>
    </div>
  );
}
