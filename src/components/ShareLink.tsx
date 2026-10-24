import { useCallback, useState, type MouseEvent } from 'react';

export type ShareSection = 'styles' | 'stylesdb' | 'addons' | 'interactive' | 'techniques' | 'top200';

export function slugify(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

/** Canonical, agent-shareable URL for one component. */
export function componentUrl(section: ShareSection, id: string): string {
  return `${window.location.origin}${window.location.pathname}#/${section}/${encodeURIComponent(id)}`;
}

export async function copyComponentLink(section: ShareSection, id: string): Promise<boolean> {
  const url = componentUrl(section, id);
  try {
    await navigator.clipboard.writeText(url);
    return true;
  } catch {
    try {
      const ta = document.createElement('textarea');
      ta.value = url;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand('copy');
      document.body.removeChild(ta);
      return ok;
    } catch {
      return false;
    }
  }
}

interface ShareLinkProps {
  section: ShareSection;
  id: string;
  label?: string;
  compact?: boolean;
  className?: string;
}

/** One-click copy of this component's permanent link. Never navigates the card. */
export function ShareLink({ section, id, label, compact = false, className = '' }: ShareLinkProps) {
  const [state, setState] = useState<'idle' | 'copied' | 'failed'>('idle');

  const onClick = useCallback((e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    copyComponentLink(section, id).then(ok => {
      setState(ok ? 'copied' : 'failed');
      window.setTimeout(() => setState('idle'), 1400);
    });
  }, [section, id]);

  return (
    <button
      type="button"
      className={`share-link ${compact ? 'compact' : ''} ${state} ${className}`}
      onClick={onClick}
      onPointerDown={e => e.stopPropagation()}
      aria-label={`Copy link to ${label || id}`}
      title="Copy a permanent link to this component"
    >
      <span aria-hidden="true">{state === 'copied' ? '✓' : state === 'failed' ? '!' : '🔗'}</span>
      {!compact && <span>{state === 'copied' ? 'Link copied' : 'Copy link'}</span>}
    </button>
  );
}
