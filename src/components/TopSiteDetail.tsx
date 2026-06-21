import { useState, useEffect } from 'react';
import type { SiteData } from './Top200Tab';

interface TopSiteDetailProps {
  site: SiteData;
  onBack: () => void;
}

export function TopSiteDetail({ site, onBack }: TopSiteDetailProps) {
  const [designMd, setDesignMd] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'screenshot' | 'design-md' | 'colors' | 'fonts'>('screenshot');
  const [copied, setCopied] = useState(false);
  const [copiedColor, setCopiedColor] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/top-sites/${site.designMdPath}`)
      .then(res => res.text())
      .then(setDesignMd)
      .catch(() => setDesignMd('DESIGN.md not available'));
  }, [site.designMdPath]);

  const handleCopyMd = () => {
    navigator.clipboard.writeText(designMd);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleCopyColor = (color: string) => {
    navigator.clipboard.writeText(color);
    setCopiedColor(color);
    setTimeout(() => setCopiedColor(null), 1500);
  };

  return (
    <div className="top200-detail">
      <button className="detail-back" onClick={onBack}>← Back to Top 200</button>

      {/* Header */}
      <header className="top200-detail-header">
        <img
          className="top200-detail-favicon"
          src={`https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${encodeURIComponent(site.url)}&size=64`}
          alt=""
        />
        <div>
          <h1>{site.name}</h1>
          <p className="top200-detail-url">{site.url}</p>
          <p className="top200-detail-desc">{site.description}</p>
        </div>
      </header>

      {/* Tabs */}
      <div className="top200-detail-tabs">
        <button className={`detail-tab ${activeTab === 'screenshot' ? 'active' : ''}`} onClick={() => setActiveTab('screenshot')}>
          📸 Screenshot
        </button>
        <button className={`detail-tab ${activeTab === 'design-md' ? 'active' : ''}`} onClick={() => setActiveTab('design-md')}>
          📄 DESIGN.md
        </button>
        <button className={`detail-tab ${activeTab === 'colors' ? 'active' : ''}`} onClick={() => setActiveTab('colors')}>
          🎨 Colors ({site.colors.length})
        </button>
        <button className={`detail-tab ${activeTab === 'fonts' ? 'active' : ''}`} onClick={() => setActiveTab('fonts')}>
          🔤 Fonts ({site.fonts.length})
        </button>
      </div>

      {/* Content */}
      <div className="top200-detail-content">
        {activeTab === 'screenshot' && (
          <div className="detail-screenshot-section">
            <img
              className="detail-screenshot-img"
              src={site.screenshotUrl}
              alt={`${site.name} full page screenshot`}
            />
            <div className="detail-screenshot-meta">
              <p><strong>Category:</strong> {site.category}</p>
              <p><strong>Theme:</strong> {site.isDark ? '🌙 Dark mode' : '☀️ Light mode'}</p>
              {site.themeColor && <p><strong>Theme color:</strong> <span className="theme-color-chip" style={{ background: site.themeColor }} /> {site.themeColor}</p>}
              <p><strong>Page title:</strong> {site.title}</p>
            </div>
          </div>
        )}

        {activeTab === 'design-md' && (
          <div className="detail-export">
            <div className="export-header">
              <span className="export-filename">{site.designMdPath}</span>
              <button className="export-copy-btn" onClick={handleCopyMd}>
                {copied ? '✓ Copied!' : '📋 Copy DESIGN.md'}
              </button>
            </div>
            <pre className="export-code"><code>{designMd}</code></pre>
          </div>
        )}

        {activeTab === 'colors' && (
          <div className="detail-colors-section">
            {site.colors.length > 0 ? (
              <div className="detail-color-grid">
                {site.colors.map((color: string, i: number) => (
                  <div key={i} className="detail-color-card" onClick={() => handleCopyColor(color)}>
                    <div className="detail-color-swatch" style={{ background: color }} />
                    <div className="detail-color-info">
                      <span className="detail-color-hex">{copiedColor === color ? '✓ Copied!' : color}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="detail-empty">No colors were extracted from this site's inline styles. This may be because the site uses external CSS files.</p>
            )}
          </div>
        )}

        {activeTab === 'fonts' && (
          <div className="detail-fonts-section">
            {site.fonts.length > 0 ? (
              site.fonts.map((font: string, i: number) => (
                <div key={i} className="detail-font-card">
                  <span className="detail-font-name">{font}</span>
                  <div className="detail-font-preview" style={{ fontFamily: `${font}, sans-serif` }}>
                    The quick brown fox jumps over the lazy dog
                  </div>
                </div>
              ))
            ) : (
              <p className="detail-empty">No custom fonts were detected. The site may use system fonts or load fonts via external CSS.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
