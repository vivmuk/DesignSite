import { useState } from 'react';

type GuideId = 'design-md' | 'resources' | 'prompts';

const GUIDES: { id: GuideId; title: string; emoji: string }[] = [
  { id: 'design-md', title: 'DESIGN.md Examples', emoji: '📄' },
  { id: 'resources', title: 'AI Design Resources', emoji: '🧰' },
  { id: 'prompts', title: 'Design Prompts', emoji: '✏️' },
];

export function GuidesTab() {
  const [active, setActive] = useState<GuideId>('design-md');

  return (
    <div className="guides-tab">
      <div className="guides-sidebar">
        <h2 className="guides-title">Guides</h2>
        <nav className="guides-nav">
          {GUIDES.map(g => (
            <button
              key={g.id}
              className={`guide-nav-btn ${active === g.id ? 'active' : ''}`}
              onClick={() => setActive(g.id)}
            >
              <span className="guide-emoji">{g.emoji}</span>
              <span>{g.title}</span>
            </button>
          ))}
        </nav>
      </div>

      <div className="guides-content">
        {active === 'design-md' && <DesignMdGuide />}
        {active === 'resources' && <ResourcesGuide />}
        {active === 'prompts' && <PromptsGuide />}
      </div>
    </div>
  );
}

function DesignMdGuide() {
  return (
    <article className="guide-article">
      <h1>How to Use DESIGN.md With AI Agents</h1>
      <p className="guide-intro">
        A strong reference changes the first draft. Instead of asking an AI agent to invent taste from scratch,
        give it a real visual system before it starts working.
      </p>

      <h2>What this is</h2>
      <p>
        AI agents do better design work when the brief includes a visual system, not just taste words. Prompts like
        "make it premium" leave too much room for default layouts, weak spacing, and generic color choices.
      </p>
      <p>
        Each style in our Explore tab includes a DESIGN.md you can copy and paste into Cursor, Claude Code, Codex, v0,
        or Lovable. It gives the agent concrete context: palette, type scale, spacing rhythm, component patterns,
        and the overall feel of the style.
      </p>

      <h2>How to use it</h2>
      <h3>1. Choose a style with the right job</h3>
      <p>
        Start with the product you are building: landing page, dashboard, pricing page, onboarding, or docs. Pick a
        reference that matches the density, tone, and audience instead of choosing by name alone.
      </p>

      <h3>2. Paste the DESIGN.md into the agent context</h3>
      <p>
        Add the copied reference before your design request. Tell the agent which parts matter most: palette,
        typography, spacing, component weight, or the full system.
      </p>

      <h3>3. Ask for a specific screen or component</h3>
      <p>
        Give the agent a concrete task, such as "design a pricing section" or "build a settings page." The DESIGN.md
        narrows the visual direction while your prompt defines the product problem.
      </p>

      <h2>What to copy</h2>
      <p>
        The useful part of a DESIGN.md is the system behind the preview: how color is used, how type scales, how dense
        the layout feels, how components are framed, and how much visual noise the interface allows.
      </p>
      <p>
        You should not ask the agent to recreate any style exactly. Use the reference to set taste and constraints,
        then describe your own product, audience, content, and feature requirements.
      </p>

      <h2>When to use it</h2>
      <p>
        DESIGN.md is most useful at the start of a design task: landing pages, dashboards, pricing sections,
        onboarding flows, documentation, settings pages, and feature screens.
      </p>
      <p>
        They also help when a page already works but feels generic. Paste a reference into the agent context and ask
        for a focused pass on typography, spacing, hierarchy, component weight, or visual consistency.
      </p>

      <h2>Why it works</h2>
      <p>
        AI builders understand concrete instructions better than vague style direction. A prompt like "make this clean
        and premium" can produce almost anything. A reference with colors, font choices, spacing rhythm, and component
        notes gives the agent a smaller, sharper target.
      </p>

      <div className="guide-callout">
        <h3>Ready to try it?</h3>
        <p>Open the Explore tab, choose a style, click "View details", then copy the DESIGN.md export.</p>
      </div>
    </article>
  );
}

function ResourcesGuide() {
  return (
    <article className="guide-article">
      <h1>A Practical Design Library for AI-Built Products</h1>
      <p className="guide-intro">
        AI builders do not need another gallery of pretty screenshots. They need reusable context that makes a coding
        agent choose better type, spacing, colors, components, and page structure.
      </p>

      <h2>What this resource hub is for</h2>
      <p>
        OpenDesignStudio is built for people who use AI agents to ship product UI. The problem is rarely whether the
        agent can write React, Tailwind, or CSS. The problem is that it starts from weak visual assumptions.
      </p>
      <p>
        Each style in our library targets a specific design job: prompting an agent, choosing a website style, improving
        dashboards, shaping landing pages, or giving Cursor, Claude Code, Codex, v0, and Lovable a better visual brief.
      </p>

      <h2>How to use this hub</h2>
      <h3>1. Choose the design job</h3>
      <p>
        Decide whether you need a landing page, dashboard, product screen, prompt pattern, or full website style. The
        tighter the job, the better the reference will work.
      </p>

      <h3>2. Open the closest style</h3>
      <p>
        Use the Explore tab to compare styles by category, tags, and popularity. Compare them by density, tone, color,
        type, and component weight.
      </p>

      <h3>3. Give the agent a reference and a task</h3>
      <p>
        Paste the DESIGN.md into the agent context, explain your product, and ask for the exact screen or component
        you need.
      </p>

      <h2>Build a reusable library</h2>
      <p>
        The fastest teams keep a shortlist of references for common jobs: clean SaaS, dense dashboard, dark devtool,
        editorial storytelling, fintech trust, ecommerce conversion, and agency portfolio.
      </p>
      <p>
        When a new UI task appears, they do not start from a blank prompt. They start from a known visual system, then
        adapt it to the product in front of them.
      </p>

      <div className="guide-callout">
        <h3>Quick Start</h3>
        <p>Browse the Explore tab → Filter by category → Copy DESIGN.md → Paste into your AI agent</p>
      </div>
    </article>
  );
}

function PromptsGuide() {
  return (
    <article className="guide-article">
      <h1>How to Write Design Prompts That Produce Better UI</h1>
      <p className="guide-intro">
        The best prompt is not longer. It is more specific about the job, the audience, and the visual system the
        agent should work inside.
      </p>

      <h2>Why design prompts need reference material</h2>
      <p>
        AI agents often default to the same shapes: oversized hero copy, generic gradients, soft cards, and arbitrary
        spacing. A prompt that includes a real reference makes those defaults less likely.
      </p>
      <p>
        A good design prompt separates three things: the product problem, the interface you need, and the visual
        system the agent should follow.
      </p>

      <h2>The prompt structure</h2>
      <h3>1. Name the screen and audience</h3>
      <p>
        Start with the exact surface: pricing page, onboarding step, dashboard, settings screen, docs page, or
        marketing section. Add who it is for.
      </p>
      <pre className="guide-code">Pricing page for a B2B SaaS analytics tool. Audience: data-driven product managers.</pre>

      <h3>2. Attach a real visual reference</h3>
      <p>
        Paste the DESIGN.md before the task. Tell the agent which parts to preserve: density, type, color, spacing,
        component style, or overall restraint.
      </p>
      <pre className="guide-code">Use this DESIGN.md as the visual system. Preserve the type scale, color palette, and border radius values exactly.</pre>

      <h3>3. Define the acceptance criteria</h3>
      <p>
        Ask for responsive layout, clear states, accessible contrast, realistic content, and no decorative elements
        unless they serve the interface.
      </p>
      <pre className="guide-code">Must be responsive (mobile + desktop). Include hover, active, and disabled states. Use realistic content — no Lorem Ipsum. Accessible contrast (WCAG AA). No decorative gradients or glow effects.</pre>

      <h2>Common mistake: asking for style and structure at the same time</h2>
      <p>
        When a prompt mixes product strategy, layout, visual style, copy, and implementation details in one vague
        paragraph, the model fills the gaps with generic patterns.
      </p>
      <p>
        Split the work. First give it the reference and the user problem. Then ask for the screen. Then do a focused
        pass on typography, spacing, density, and interaction details.
      </p>

      <h2>Reusable prompt pattern</h2>
      <pre className="guide-code-block">{`## Visual System
[Paste DESIGN.md here]

## Screen
[Pricing page for a B2B SaaS tool]

## Audience
[Product managers at mid-market companies]

## Requirements
- Responsive (mobile + desktop)
- Include 3 tiers: Free, Pro ($29/mo), Enterprise (custom)
- Annual/monthly toggle
- Feature comparison table
- Clear CTA for each tier
- Use the exact color palette and type scale from the DESIGN.md
- No decorative elements that aren't in the reference

## Output
Single-page React component with Tailwind CSS.`}</pre>

      <div className="guide-callout">
        <h3>Pro tip</h3>
        <p>Keep a prompt pattern and a few trusted references for each repeated job: landing page, pricing, dashboard, table, settings, docs, onboarding, and empty states.</p>
      </div>
    </article>
  );
}
