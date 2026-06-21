import { useState, useMemo, useEffect } from 'react';
import { topSites, type TopSite } from '../data/topSites';

export interface SiteData {
  rank: number;
  name: string;
  url: string;
  category: string;
  description: string;
  colors: string[];
  fonts: string[];
  themeColor: string;
  isDark: boolean;
  title: string;
  screenshotUrl: string;
  designMdPath: string;
  error?: string;
}

interface Top200TabProps {
  onSelectSite: (site: SiteData) => void;
}

const CATEGORIES = [
  { id: 'all', name: 'All Sites', icon: '🌐' },
  { id: 'tech', name: 'Tech & AI', icon: '🤖' },
  { id: 'developer', name: 'Developer', icon: '💻' },
  { id: 'media', name: 'Media & Streaming', icon: '📺' },
  { id: 'social', name: 'Social', icon: '💬' },
  { id: 'ecommerce', name: 'E-commerce', icon: '🛒' },
  { id: 'fintech', name: 'Fintech', icon: '💳' },
  { id: 'productivity', name: 'Productivity', icon: '📊' },
  { id: 'travel', name: 'Travel & Food', icon: '✈️' },
  { id: 'automotive', name: 'Automotive', icon: '🚗' },
  { id: 'design', name: 'Design', icon: '🎨' },
  { id: 'education', name: 'Education', icon: '📚' },
  { id: 'health', name: 'Health', icon: '🏥' },
  { id: 'gaming', name: 'Gaming', icon: '🎮' },
  { id: 'business', name: 'Business', icon: '💼' },
  { id: 'reference', name: 'Reference', icon: '📖' },
  { id: 'realestate', name: 'Real Estate', icon: '🏠' },
];

const PAGE_SIZE = 24;

export function Top200Tab({ onSelectSite }: Top200TabProps) {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const [sitesData, setSitesData] = useState<Record<string, SiteData>>({});
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Load scraped site data
  useEffect(() => {
    fetch('/top-sites/sites.json')
      .then(res => res.json())
      .then((data: SiteData[]) => {
        const map: Record<string, SiteData> = {};
        data.forEach((s) => {
          const key = s.name.toLowerCase().replace(/[^a-z0-9]/g, '-');
          map[key] = s;
        });
        setSitesData(map);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  useEffect(() => { setVisibleCount(PAGE_SIZE); }, [search, category]);

  const filtered = useMemo(() => {
    let items = [...topSites];

    if (category !== 'all') {
      items = items.filter(s => s.category === category);
    }

    if (search) {
      const q = search.toLowerCase();
      items = items.filter(s =>
        s.name.toLowerCase().includes(q) ||
        s.description.toLowerCase().includes(q) ||
        s.category.toLowerCase().includes(q)
      );
    }

    return items;
  }, [search, category]);

  const visible = filtered.slice(0, visibleCount);
  const hasMore = visibleCount < filtered.length;

  return (
    <div className="top200-tab">
      {/* Header */}
      <div className="top200-header">
        <h1 className="top200-title">Top 200 Sites</h1>
        <p className="top200-subtitle">
          Real UI design data extracted from the world's most visited websites.
          Each card includes screenshots, DESIGN.md, colors, and fonts.
        </p>
      </div>

      {/* Search */}
      <div className="top200-search-bar">
        <input
          type="text"
          className="top200-search-input"
          placeholder="Search 200 sites…"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <div className="top200-view-toggle">
          <button className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`} onClick={() => setViewMode('grid')}>▦</button>
          <button className={`view-btn ${viewMode === 'list' ? 'active' : ''}`} onClick={() => setViewMode('list')}>☰</button>
        </div>
      </div>

      {/* Categories */}
      <div className="top200-categories">
        {CATEGORIES.map(cat => (
          <button
            key={cat.id}
            className={`top200-cat-btn ${category === cat.id ? 'active' : ''}`}
            onClick={() => setCategory(cat.id)}
          >
            <span>{cat.icon}</span>
            <span>{cat.name}</span>
          </button>
        ))}
      </div>

      {/* Count */}
      <div className="top200-meta">
        <span className="top200-count">
          {loading ? 'Loading extracted data…' : `${filtered.length} sites`}
        </span>
      </div>

      {/* Grid */}
      {viewMode === 'grid' ? (
        <div className="top200-grid">
          {visible.map(site => (
            <SiteCard
              key={site.rank}
              site={site}
              data={sitesData[site.name.toLowerCase().replace(/[^a-z0-9]/g, '-')]}
              onClick={() => onSelectSite(sitesData[site.name.toLowerCase().replace(/[^a-z0-9]/g, '-')] || {
                ...site,
                colors: [],
                fonts: [],
                themeColor: '',
                isDark: false,
                title: site.name,
                screenshotUrl: `https://s.wordpress.com/mshots/v1/${encodeURIComponent(site.url)}?w=1280&h=800`,
                designMdPath: `${site.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}.md`,
              })}
            />
          ))}
        </div>
      ) : (
        <div className="top200-list">
          {visible.map(site => {
            const data = sitesData[site.name.toLowerCase().replace(/[^a-z0-9]/g, '-')];
            return (
              <div
                key={site.rank}
                className="top200-list-item"
                onClick={() => onSelectSite(data || {
                  ...site,
                  colors: [], fonts: [], themeColor: '', isDark: false, title: site.name,
                  screenshotUrl: `https://s.wordpress.com/mshots/v1/${encodeURIComponent(site.url)}?w=1280&h=800`,
                  designMdPath: `${site.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}.md`,
                })}
              >
                <span className="list-rank">#{site.rank}</span>
                <img
                  className="list-favicon"
                  src={`https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${encodeURIComponent(site.url)}&size=32`}
                  alt={site.name}
                  loading="lazy"
                />
                <span className="list-name">{site.name}</span>
                <span className="list-desc">{site.description}</span>
                <span className="list-category">{site.category}</span>
                {data && data.colors.length > 0 && (
                  <div className="list-swatches">
                    {data.colors.slice(0, 5).map((c, i) => (
                      <div key={i} className="list-swatch" style={{ background: c }} />
                    ))}
                  </div>
                )}
                <span className="list-arrow">→</span>
              </div>
            );
          })}
        </div>
      )}

      {/* Load More */}
      {hasMore && (
        <div className="explore-load-more">
          <button onClick={() => setVisibleCount(c => c + PAGE_SIZE)}>
            Load more ({filtered.length - visibleCount} remaining)
          </button>
        </div>
      )}
    </div>
  );
}

function SiteCard({ site, data, onClick }: { site: TopSite; data?: SiteData; onClick: () => void }) {
  const screenshotUrl = data?.screenshotUrl || `https://s.wordpress.com/mshots/v1/${encodeURIComponent(site.url)}?w=1280&h=800`;
  const colors = data?.colors || [];
  const isDark = data?.isDark || false;

  return (
    <div className="top200-card" onClick={onClick}>
      {/* Screenshot */}
      <div className="card-screenshot-wrapper">
        <img
          className="card-screenshot"
          src={screenshotUrl}
          alt={`${site.name} screenshot`}
          loading="lazy"
          onError={(e) => {
            (e.target as HTMLImageElement).style.opacity = '0.3';
          }}
        />
        <div className="card-rank-badge">#{site.rank}</div>
        {data?.error && <div className="card-error-badge">⚠️</div>}
      </div>

      {/* Info */}
      <div className="top200-card-info">
        <div className="top200-card-header">
          <img
            className="top200-card-favicon"
            src={`https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${encodeURIComponent(site.url)}&size=32`}
            alt=""
            loading="lazy"
          />
          <h3 className="top200-card-name">{site.name}</h3>
        </div>
        <p className="top200-card-desc">{site.description}</p>
        <div className="top200-card-meta">
          <span className="top200-card-cat">{site.category}</span>
          {isDark && <span className="top200-card-theme dark">🌙 Dark</span>}
          {colors.length > 0 && <span className="top200-card-colors">{colors.length} colors</span>}
          {data && data.fonts.length > 0 && <span className="top200-card-fonts">{data.fonts.length} fonts</span>}
        </div>
        {colors.length > 0 && (
          <div className="top200-card-swatches">
            {colors.slice(0, 8).map((c, i) => (
              <div key={i} className="top200-card-swatch" style={{ background: c }} title={c} />
            ))}
          </div>
        )}
        <div className="top200-card-cta">
          View DESIGN.md →
        </div>
      </div>
    </div>
  );
}
