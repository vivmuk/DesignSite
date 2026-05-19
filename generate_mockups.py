#!/usr/bin/env python3
"""Generate rich, detailed HTML mockups for all Design Skills."""

import os

SKILLS = [
    {'id':'8-bit-orbit-video-template','name':'8-Bit Orbit Video','category':'media','description':'Retro 8-bit orbital animation video template'},
    {'id':'ad-creative','name':'Ad Creative','category':'design','description':'Generate advertising creatives for digital campaigns'},
    {'id':'after-hours-editorial-template','name':'After Hours Editorial','category':'design','description':'Dark editorial template with nightlife aesthetics'},
    {'id':'agent-browser','name':'Agent Browser','category':'development','description':'Browser automation for agents'},
    {'id':'ai-music-album','name':'AI Music Album','category':'media','description':'AI-generated music album covers and content'},
    {'id':'algorithmic-art','name':'Algorithmic Art','category':'design','description':'Generative and algorithmic art creation'},
    {'id':'apple-hig','name':'Apple HIG','category':'design','description':'Apple Human Interface Guidelines implementation'},
    {'id':'article-magazine','name':'Magazine Article','category':'content','description':'Long-form magazine-style article layout'},
    {'id':'artifacts-builder','name':'Artifacts Builder','category':'development','description':'Web artifact builder with live preview'},
    {'id':'brainstorming','name':'Brainstorming','category':'utility','description':'Creative brainstorming assistance'},
    {'id':'brand-guidelines','name':'Brand Guidelines','category':'design','description':'Brand guideline document creation'},
    {'id':'canvas-design','name':'Canvas Design','category':'design','description':'HTML5 canvas-based visual design'},
    {'id':'card-twitter','name':'Twitter Card','category':'design','description':'Twitter/X share card with Open Graph previews'},
    {'id':'card-xiaohongshu','name':'Xiaohongshu Card','category':'design','description':'Little Red Book social card design'},
    {'id':'color-expert','name':'Color Expert','category':'design','description':'Color theory, palette generation, and accessibility'},
    {'id':'competitive-ads-extractor','name':'Competitive Ads Extractor','category':'utility','description':'Extract and analyze competitor ad creatives'},
    {'id':'copywriting','name':'Copywriting','category':'content','description':'Professional copywriting for marketing'},
    {'id':'creative-director','name':'Creative Director','category':'design','description':'Creative direction and art direction skills'},
    {'id':'d3-visualization','name':'D3 Visualization','category':'development','description':'Data visualization with D3.js'},
    {'id':'data-report','name':'Data Report','category':'content','description':'Data-driven report generation'},
    {'id':'deck-guizang-editorial','name':'Guizang Deck','category':'content','description':'Magazine-style presentation deck with WebGL hero'},
    {'id':'deck-open-slide-canvas','name':'Open Slide Canvas','category':'content','description':'Open canvas slide presentation format'},
    {'id':'deck-swiss-international','name':'Swiss International Deck','category':'content','description':'Swiss International Style presentation template'},
    {'id':'design-brief','name':'Design Brief','category':'design','description':'Structured design brief creation'},
    {'id':'design-consultation','name':'Design Consultation','category':'design','description':'Expert design consultation and advice'},
    {'id':'design-md','name':'Design MD','category':'design','description':'Markdown-based design documentation'},
    {'id':'design-review','name':'Design Review','category':'design','description':'5-dimensional design critique and review'},
    {'id':'digits-fintech-swiss-template','name':'Digits Fintech Swiss','category':'design','description':'Swiss-style fintech dashboard template'},
    {'id':'doc','name':'Document','category':'content','description':'Document creation and formatting'},
    {'id':'doc-kami-parchment','name':'Kami Parchment Doc','category':'content','description':'Parchment-style document with Japanese aesthetics'},
    {'id':'docx','name':'DOCX','category':'content','description':'Word document generation'},
    {'id':'domain-name-brainstormer','name':'Domain Brainstormer','category':'utility','description':'Domain name ideation and brainstorming'},
    {'id':'editorial-burgundy-principles-template','name':'Burgundy Editorial','category':'design','description':'Burgundy editorial principles template'},
    {'id':'enhance-prompt','name':'Enhance Prompt','category':'ai','description':'AI prompt enhancement and optimization'},
    {'id':'fal-3d','name':'FAL 3D','category':'ai','description':'3D asset generation via FAL'},
    {'id':'fal-generate','name':'FAL Generate','category':'ai','description':'AI generation via FAL platform'},
    {'id':'fal-image-edit','name':'FAL Image Edit','category':'ai','description':'Image editing via FAL'},
    {'id':'fal-kling-o3','name':'FAL Kling O3','category':'media','description':'Kling O3 video generation via FAL'},
    {'id':'fal-lip-sync','name':'FAL Lip Sync','category':'media','description':'AI lip-sync animation via FAL'},
    {'id':'fal-realtime','name':'FAL Realtime','category':'ai','description':'Real-time AI generation via FAL'},
    {'id':'fal-restore','name':'FAL Restore','category':'ai','description':'Image restoration and enhancement via FAL'},
    {'id':'fal-train','name':'FAL Train','category':'ai','description':'Custom model training via FAL'},
    {'id':'fal-tryon','name':'FAL TryOn','category':'ai','description':'Virtual try-on via FAL'},
    {'id':'fal-upscale','name':'FAL Upscale','category':'ai','description':'AI image upscaling via FAL'},
    {'id':'fal-video-edit','name':'FAL Video Edit','category':'media','description':'Video editing via FAL'},
    {'id':'fal-vision','name':'FAL Vision','category':'ai','description':'Computer vision via FAL'},
    {'id':'faq-page','name':'FAQ Page','category':'design','description':'Searchable FAQ page with accordion layout'},
    {'id':'field-notes-editorial-template','name':'Field Notes Editorial','category':'design','description':'Field notes style editorial template'},
    {'id':'figma-code-connect-components','name':'Figma Code Connect','category':'development','description':'Figma component-to-code connection tool'},
    {'id':'figma-create-design-system-rules','name':'Figma Design System Rules','category':'design','description':'Generate design system rules from Figma files'},
    {'id':'figma-create-new-file','name':'Figma New File','category':'design','description':'Create new Figma design files programmatically'},
    {'id':'figma-generate-design','name':'Figma Generate Design','category':'ai','description':'AI-powered design generation in Figma'},
    {'id':'figma-generate-library','name':'Figma Generate Library','category':'design','description':'Auto-generate design library components'},
    {'id':'figma-implement-design','name':'Figma Implement Design','category':'development','description':'Implement Figma designs as production code'},
    {'id':'figma-use','name':'Figma Use','category':'design','description':'Figma integration and usage utilities'},
    {'id':'flutter-animating-apps','name':'Flutter Animating Apps','category':'development','description':'Animated Flutter mobile app interfaces'},
    {'id':'frame-data-chart-nyt','name':'NYT Data Chart','category':'design','description':'New York Times-style data visualization frames'},
    {'id':'frame-flowchart-sticky','name':'Sticky Flowchart','category':'design','description':'Interactive sticky note flowchart frames'},
    {'id':'frame-glitch-title','name':'Glitch Title','category':'design','description':'Glitch-effect title frame animations'},
    {'id':'frame-light-leak-cinema','name':'Light Leak Cinema','category':'media','description':'Cinematic light leak frame effects'},
    {'id':'frame-liquid-bg-hero','name':'Liquid BG Hero','category':'design','description':'Liquid background hero frame animations'},
    {'id':'frame-logo-outro','name':'Logo Outro','category':'media','description':'Animated logo outro frame templates'},
    {'id':'frame-macos-notification','name':'macOS Notification','category':'design','description':'macOS-style notification frame mockups'},
    {'id':'frontend-design','name':'Frontend Design','category':'design','description':'Complete frontend design implementation'},
    {'id':'frontend-dev','name':'Frontend Dev','category':'development','description':'Frontend development with best practices'},
    {'id':'frontend-skill','name':'Frontend Skill','category':'development','description':'General frontend skill toolkit'},
    {'id':'frontend-slides','name':'Frontend Slides','category':'content','description':'Slide presentations with frontend code examples'},
    {'id':'full-page-screenshot','name':'Full Page Screenshot','category':'utility','description':'Capture full-page screenshots of websites'},
    {'id':'gif-sticker-maker','name':'GIF Sticker Maker','category':'media','description':'Create animated GIF stickers'},
    {'id':'gsap-core','name':'GSAP Core','category':'development','description':'GreenSock animation platform core'},
    {'id':'gsap-react','name':'GSAP React','category':'development','description':'GSAP animations for React components'},
    {'id':'gsap-scrolltrigger','name':'GSAP ScrollTrigger','category':'development','description':'Scroll-triggered GSAP animations'},
    {'id':'gsap-timeline','name':'GSAP Timeline','category':'development','description':'GSAP timeline-based animation sequences'},
    {'id':'hand-drawn-diagrams','name':'Hand-Drawn Diagrams','category':'design','description':'Excalidraw-style hand-drawn diagrams'},
    {'id':'hatch-pet','name':'Hatch Pet','category':'design','description':'Interactive virtual pet character designs'},
    {'id':'html-ppt-retro-quarterly-review','name':'Retro Quarterly Review','category':'content','description':'Retro-style quarterly business review presentation'},
    {'id':'image-enhancer','name':'Image Enhancer','category':'ai','description':'AI-powered image enhancement and upscaling'},
    {'id':'imagegen','name':'Image Generation','category':'ai','description':'AI image generation from text prompts'},
    {'id':'imagen','name':'Imagen','category':'ai','description':'Google Imagen-style image creation'},
    {'id':'login-flow','name':'Login Flow','category':'design','description':'Complete login/authentication flow design'},
    {'id':'marketing-psychology','name':'Marketing Psychology','category':'content','description':'Psychology-driven marketing content design'},
    {'id':'minimax-docx','name':'MiniMax Docx','category':'content','description':'Document generation in DOCX format'},
    {'id':'minimax-pdf','name':'MiniMax PDF','category':'content','description':'PDF document generation and formatting'},
    {'id':'mockup-device-3d','name':'3D Device Mockup','category':'design','description':'3D device mockup presentations'},
    {'id':'nanobanana-ppt','name':'NanoBanana PPT','category':'content','description':'Presentation slide generation with NanoBanana'},
    {'id':'paywall-upgrade-cro','name':'Paywall Upgrade CRO','category':'design','description':'Conversion-optimized paywall and upgrade designs'},
    {'id':'pdf','name':'PDF Generation','category':'content','description':'PDF document creation and formatting'},
    {'id':'pixelbin-media','name':'PixelBin Media','category':'media','description':'Media processing and transformation'},
    {'id':'plan-design-review','name':'Plan Design Review','category':'design','description':'Planned design review and iteration workflow'},
    {'id':'platform-design','name':'Platform Design','category':'design','description':'Platform-level design system creation'},
    {'id':'poster-hero','name':'Marketing Poster','category':'design','description':'Vertical poster/hero image for social sharing'},
    {'id':'ppt-keynote','name':'PPT Keynote','category':'content','description':'Keynote-style presentation generation'},
    {'id':'pptx','name':'PPTX Generation','category':'content','description':'PowerPoint presentation file generation'},
    {'id':'pptx-generator','name':'PPTX Generator','category':'content','description':'Advanced PPTX slide generation engine'},
    {'id':'pptx-html-fidelity-audit','name':'PPTX HTML Audit','category':'utility','description':'Audit HTML-to-PPTX conversion fidelity'},
    {'id':'release-notes-one-pager','name':'Release Notes One-Pager','category':'content','description':'Single-page release notes summary design'},
    {'id':'remotion','name':'Remotion','category':'media','description':'Programmatic video creation with React'},
    {'id':'replicate','name':'Replicate','category':'ai','description':'AI model inference via Replicate API'},
    {'id':'resume-modern','name':'Modern Resume','category':'content','description':'Modern resume/CV design template'},
    {'id':'screenshot','name':'Screenshot','category':'utility','description':'Website screenshot capture tool'},
    {'id':'screenshots-marketing','name':'Marketing Screenshots','category':'design','description':'Marketing-ready screenshot compositions'},
    {'id':'shadcn-ui','name':'shadcn/ui','category':'development','description':'shadcn/ui component implementation'},
    {'id':'shader-dev','name':'Shader Development','category':'development','description':'GLSL/WebGL shader programming'},
    {'id':'slack-gif-creator','name':'Slack GIF Creator','category':'media','description':'Create animated GIFs for Slack'},
    {'id':'slides','name':'Slides','category':'content','description':'Presentation slide creation tool'},
    {'id':'social-reddit-card','name':'Reddit Card','category':'design','description':'Reddit-optimized social card design'},
    {'id':'social-spotify-card','name':'Spotify Card','category':'design','description':'Spotify-style social sharing card'},
    {'id':'social-x-post-card','name':'X Post Card','category':'design','description':'Twitter/X post card design'},
    {'id':'sora','name':'Sora Video','category':'media','description':'AI video generation with Sora'},
    {'id':'speech','name':'Speech/TTS','category':'media','description':'Text-to-speech and audio generation'},
    {'id':'stitch-loop','name':'Stitch Loop','category':'media','description':'Seamless looping animation creation'},
    {'id':'swiftui-design','name':'SwiftUI Design','category':'development','description':'SwiftUI interface design and code generation'},
    {'id':'swiss-creative-mode-template','name':'Swiss Creative Mode','category':'design','description':'Creative mode Swiss design template'},
    {'id':'swiss-user-research-video-template','name':'Swiss User Research Video','category':'media','description':'Swiss-style user research video template'},
    {'id':'taste-skill','name':'Taste Skill','category':'design','description':'Design taste and aesthetic judgment system'},
    {'id':'theme-factory','name':'Theme Factory','category':'development','description':'Dynamic theme generation engine'},
    {'id':'threejs','name':'Three.js','category':'development','description':'3D web graphics with Three.js'},
    {'id':'ui-skills','name':'UI Skills','category':'design','description':'Comprehensive UI component design skills'},
    {'id':'ui-ux-pro-max','name':'UI/UX Pro Max','category':'design','description':'Advanced UI/UX design and prototyping'},
    {'id':'venice-audio-music','name':'Venice Music','category':'media','description':'AI music generation via Venice'},
    {'id':'venice-audio-speech','name':'Venice Speech','category':'media','description':'AI text-to-speech via Venice'},
    {'id':'venice-image-edit','name':'Venice Image Edit','category':'ai','description':'AI image editing via Venice API'},
    {'id':'venice-image-generate','name':'Venice Image Generate','category':'ai','description':'AI image generation via Venice'},
    {'id':'venice-video','name':'Venice Video','category':'media','description':'AI video generation via Venice'},
    {'id':'vfx-text-cursor','name':'VFX Text Cursor','category':'design','description':'Visual effects for text cursor animations'},
    {'id':'video-downloader','name':'Video Downloader','category':'utility','description':'Download videos from URLs'},
    {'id':'video-hyperframes','name':'HyperFrames','category':'media','description':'HTML-to-video motion graphics generation'},
    {'id':'web-artifacts-builder','name':'Web Artifacts Builder','category':'development','description':'Build web artifacts with live preview'},
    {'id':'web-design-guidelines','name':'Web Design Guidelines','category':'design','description':'Web design best practices and guidelines'},
    {'id':'wpds','name':'WPDS','category':'development','description':'Washington Post Design System implementation'},
    {'id':'youtube-clipper','name':'YouTube Clipper','category':'media','description':'Clip and caption YouTube videos'},
]

# Category themes
THEMES = {
    'design':      {'primary':'#8b5cf6','bg':'#0f0b1a','accent':'#c4b5fd','label':'Design & Visual','icon':'🎨'},
    'content':     {'primary':'#06b6d4','bg':'#0a1419','accent':'#67e8f9','label':'Content & Documents','icon':'📝'},
    'media':       {'primary':'#f43f5e','bg':'#1a0a0d','accent':'#fda4af','label':'Media & Video','icon':'🎬'},
    'development': {'primary':'#22c55e','bg':'#0a1a0f','accent':'#86efac','label':'Development & Code','icon':'💻'},
    'ai':          {'primary':'#f472b6','bg':'#1a0a14','accent':'#f9a8d4','label':'AI & Generation','icon':'🤖'},
    'utility':     {'primary':'#f59e0b','bg':'#1a140a','accent':'#fcd34d','label':'Utility & Tools','icon':'🛠️'},
}

def hex_to_rgb(h):
    h = h.lstrip('#')
    return f'{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}'

def cat_for(sid):
    for s in SKILLS:
        if s['id'] == sid: return s['category']
    return 'design'

def feature_list(sid):
    F = {
        '8-bit-orbit-video-template': [('Retro Animation','Pixel-perfect 8-bit orbital animations with customizable palettes'),('Video Export','Export to MP4, GIF, or WebM at any resolution'),('Loop Engine','Seamless looping with zero frame jumps'),('Layer System','Background, orbit, foreground layers with parallax'),('Palette Editor','8-bit color palette generator with dithering options')],
        'ad-creative': [('Multi-Platform Export','Generate ad sizes for Facebook, Instagram, TikTok, Google Ads'),('A/B Variants','Auto-generate color, copy, and layout variants'),('Brand Kit','Lock in brand colors, fonts, and logos for consistency'),('Smart Resize','Intelligent content-aware resizing across placements'),('CTR Predict','Score creative variants for predicted click-through rate')],
        'after-hours-editorial': [('Dark Mode First','Optimized for dark backgrounds with proper contrast ratios'),('Nightlife Palette','Curated color sets from neon to deep noir'),('Typography Drama','High-contrast type scales for editorial impact'),('Grid Overlay','Asymmetric editorial grids with subtle guides'),('Print Export','CMYK-safe export for magazine-ready output')],
        'agent-browser': [('Headless Automation','Control browsers with AI agents — click, scroll, extract'),('Multi-Tab','Manage multiple tabs and windows simultaneously'),('Session Memory','Persist cookies, localStorage, and auth across runs'),('Screenshot & DOM','Capture page state and parse DOM structure'),('Error Recovery','Auto-retry on timeouts, CAPTCHAs, and rate limits')],
        'ai-music-album': [('Album Art','Generate cohesive album covers matching music style'),('Track Listing','Auto-format track lists with duration and credits'),('Vinyl Mockup','Preview album art on vinyl, CD, and cassette formats'),('Liner Notes','Generate AI-written liner notes and credits'),('Streaming Cards','Create Spotify and Apple Music ready card designs')],
        'algorithmic-art': [('Generative Systems','Build L-systems, cellular automata, and reaction-diffusion'),('Noise Fields','Perlin, Simplex, and Worley noise for organic forms'),('Particle Systems','Millions of particles with GPU-accelerated rendering'),('Parametric Control','Real-time sliders for every generation parameter'),('High-Res Export','Export at 8K+ for print and large-format display')],
        'apple-hig': [('SF Symbols','Complete SF Symbols library with weight and scale variants'),('UIKit Components','Pixel-perfect iOS component implementations'),('Dark/Light Mode','Seamless dual-appearance with semantic colors'),('Haptics Guide','Taptic engine patterns and feedback specifications'),('Dynamic Type','Full Dynamic Type scaling from accessibility to compact')],
        'article-magazine': [('Drop Caps','Elegant drop cap styles with configurable typography'),('Pull Quotes','Magazine-style pull quotes with ornamental borders'),('Multi-Column','Automatic multi-column layout with balanced text'),('Image Galleries','Full-bleed, inline, and carousel image placements'),('Print-Ready','Export to PDF with CMYK separation and bleed marks')],
        'artifacts-builder': [('Live Preview','Real-time preview of HTML, CSS, and JavaScript artifacts'),('Component Library','Shadcn-style component snippets for rapid assembly'),('Hot Reload','Instant updates on every keystroke'),('Export Options','Download as HTML, React component, or deploy instantly'),('Version History','Track changes with built-in diff and rollback')],
        'brainstorming': [('Mind Mapping','Visual mind maps that grow with your ideas'),('Random Prompts','Curated prompts for lateral thinking and ideation'),('Clustering','Auto-group related ideas into thematic clusters'),('Timer Mode','Time-boxed brainstorming sprints with Pomodoro'),('Vote & Rank','Team voting on best ideas with weighted rankings')],
        'brand-guidelines': [('Color System','Primary, secondary, and accent palette with accessibility ratios'),('Typography Scale','Font hierarchy, sizing, and weight specifications'),('Logo Usage','Clear space, minimum size, and misusage examples'),('Icon Library','Consistent icon style with size and stroke guidelines'),('Voice & Tone','Brand voice attributes with before/after examples')],
        'canvas-design': [('Infinite Canvas','Zoom and pan across unlimited design space'),('Vector Tools','Pen, shape, and path tools for precision illustration'),('Layer Management','Group, lock, and reorder layers with blend modes'),('Export Engine','SVG, PNG, PDF, and WebP export at any resolution'),('Plugin API','Extend canvas tools with custom plugins and scripts')],
        'card-twitter': [('OG Preview','Real-time Open Graph meta tag preview and optimization'),('Aspect Ratios','1:1, 16:9, and 1.91:1 Twitter card formats'),('Gradient Builder','Custom gradient backgrounds with brand palette support'),('Text Overlay','Bold headline and subtitle with shadow for readability'),('Analytics','Embedded UTM tracking and engagement scoring')],
        'card-xiaohongshu': [('Vertical First','Optimized for Xiaohongshu 3:4 vertical card format'),('Mandarin Types','Beautiful Chinese typography with proper line height'),('Sticker Decor','Trendy sticker and emoji overlay decoration system'),('Product Tags','Inline product mention tags with price badges'),('Mood Filters','Warm, cool, vintage, and K-pop mood filter presets')],
        'color-expert': [('Palette Generator','AI-powered palette generation from images, themes, or moods'),('Contrast Checker','WCAG AA and AAA compliance scoring in real-time'),('Colorblind Sim','Protanopia, deuteranopia, and tritanopia previews'),('Harmony Engine','Complementary, analogous, triadic, and tetradic harmonies'),('Export Formats','ASE, CSS variables, Tailwind, and JSON palette export')],
        'competitive-ads-extractor': [('Ad Discovery','Scrape competitor ad libraries from Meta, Google, TikTok'),('Visual Analysis','AI-powered creative analysis — colors, layout, copy patterns'),('Spend Estimator','Estimated ad spend and frequency metrics'),('Trend Tracking','Temporal trend analysis of competitor creative strategies'),('Export Library','Download competitor creatives organized by brand and date')],
        'copywriting': [('AIDA Framework','Attention, Interest, Desire, Action structured copy'),('Tone Controls','Formal, casual, playful, authoritative, empathetic'),('Multi-Variant','Generate 5-10 headline and body copy variants'),('SEO Optimized','Keyword-aware copy with density scoring'),('Brand Voice','Lock in brand voice attributes for consistent output')],
        'creative-director': [('Mood Boards','Collaborative mood boards with drag-and-drop assets'),('Art Direction','Set visual direction — style, tone, era, references'),('Feedback Loops','Annotated visual feedback with drawing tools'),('Asset Curation','AI-curated visual references from design history'),('Pitch Decks','Director vision pitch presentation templates')],
        'd3-visualization': [('Chart Library','55+ chart types — bar, line, area, scatter, treemap, force'),('Responsive SVG','Fluid SVGs that scale perfectly to any viewport'),('Interaction','Tooltip, zoom, brush, and click-through interactions'),('Data Binding','Enter-update-exit pattern for live data streams'),('Transitions','Buttery-smooth D3 transitions with custom easing')],
        'data-report': [('Live Data','Connect to APIs, databases, and spreadsheets for live data'),('Chart Builder','Drag-and-drop chart creation with 30+ visualization types'),('Auto Insights','AI-generated insights and trend annotations'),('Branding','Apply brand colors, fonts, and logos to all reports'),('Scheduled Export','Automated PDF/HTML delivery on any schedule')],
        'deck-guizang-editorial': [('WebGL Hero','Stunning 3D hero sections with shader-based effects'),('Editorial Grid','Magazine-style asymmetric grid layouts for each slide'),('Typography Master','Full control over type hierarchy, spacing, and rhythm'),('Slide Transitions','Smooth editorial transitions — push, reveal, dissolve'),('Interactive Elements','Embedded data visualizations and live demos')],
        'deck-open-slide-canvas': [('Freeform Canvas','Infinite canvas for non-linear slide layouts'),('Zoom Levels','Zoom from overview to detail with smooth transitions'),('Connector Lines','Smart connectors between elements with auto-routing'),('Multimedia','Embed video, audio, 3D, and live code blocks'),('Collaboration','Real-time multiplayer editing with cursors')],
        'deck-swiss-international': [('Grid System','Rigorous Swiss grid with modular column spaces'),('Typography Focus','Helvetica, Univers — classic Swiss type at every scale'),('White Space','Generous margins and breathing room per Muller-Brockmann'),('Numbering','Clear slide numbering and progress indicators'),('Minimal Color','Restrained color — one accent on neutral fields')],
        'design-brief': [('Structured Template','Comprehensive brief sections — goals, audience, constraints'),('Stakeholder Input','Collaborative fields for team and client input'),('Mood References','Embedded reference images with annotation capabilities'),('Timeline','Built-in Gantt chart for design milestones'),('Success Metrics','Measurable KPI fields with target definitions')],
        'design-consultation': [('Expert Matching','AI matches your project to relevant design expertise'),('Live Review','Scheduled design review sessions with annotations'),('Priority Queue','Urgent projects get fast-tracked consultation'),('Recommendations','Actionable design improvements with before/after'),('Knowledge Base','Access curated design principles and case studies')],
        'design-md': [('Markdown Native','Write design specs in Markdown with live preview'),('Interactive','Embedded Figma frames, code blocks, and color swatches'),('Diff Tracking','Visual diff between design specification versions'),('Multi-Format','Export to PDF, HTML, or design token JSON'),('Template Library','Pre-built spec templates for web, mobile, and brand')],
        'design-review': [('5D Framework','Hierarchy, contrast, rhythm, consistency, emotion dimensions'),('Score Cards','Quantitative scores per dimension with benchmarks'),('Action Items','Specific, implementable improvement suggestions'),('Version Compare','Side-by-side comparison of design iterations'),('Team Review','Multi-reviewer aggregation and consensus scoring')],
        'digits-fintech-swiss-template': [('Dashboard Grid','Swiss-grid dashboard layout optimized for fintech data'),('Financial Charts','Area, candlestick, and donut charts for financial KPIs'),('Number Hierarchy','Smart number formatting with K, M, B suffixes'),('Dark/Light','Bento-card based theme with smooth dark/light toggle'),('Compliance Ready','SOC2 and GDPR-ready with audit trail display')],
        'doc': [('Rich Formatter','Headings, lists, tables, code blocks, and callouts'),('Table of Contents','Auto-generated TOC with anchor links'),('Collaboration','Real-time co-editing with comment threads'),('Version Control','Full revision history with change highlighting'),('Multi-Export','PDF, DOCX, HTML, and Markdown export options')],
        'doc-kami-parchment': [('Washi Textures','Japanese paper texture backgrounds and overlays'),('Ink Typography','Sumi-e inspired heading and body text styles'),('Vertical Mode','Traditional tategaki vertical text layout option'),('Stamp Seals','Hanko seal placement system for authentication marks'),('Kanji Art','Decorative kanji headings with brush stroke effects')],
        'docx': [('Template Library','Professional DOCX templates — letters, reports, proposals'),('Styles Engine','Consistent heading, body, and caption styles throughout'),('Table Magic','Smart tables with auto-formatting and conditional styling'),('Header/Footer','Custom headers, footers, and page numbering systems'),('Track Changes','Accept/reject interface for collaborative editing')],
        'domain-name-brainstormer': [('AI Variations','Generate 50+ domain name variations from any seed word'),('Availability Check','Real-time domain availability lookup across TLDs'),('Trend Scoring','Domain trendiness and brandability scoring'),('Categorization','Auto-organize by style — techy, brandable, keyword, acronym'),('Purchase Links','Direct links to registrars with best pricing')],
    }
    if sid in F:
        return F[sid]
    cat = cat_for(sid)
    defaults = {
        'design':      [('Visual Systems','Build cohesive design systems with tokens, components, and patterns'),('Pixel Perfect','Every specification matches production — no handoff drift'),('Rapid Prototyping','Go from concept to interactive prototype in minutes'),('Accessibility First','Built-in WCAG compliance checks and suggestions'),('Export Anywhere','SVG, PNG, PDF, CSS, and code export for every asset')],
        'content':     [('Smart Templates','Professional templates for documents, slides, and reports'),('Auto Formatting','Intelligent layout engine that adapts to content length'),('Multi-Format','One source document exports to PDF, DOCX, HTML, and more'),('Collaboration','Real-time editing with comments, annotations, and versioning'),('Brand Lock','Enforce brand guidelines across every document automatically')],
        'media':       [('Timeline Editor','Visual timeline for frame-precise editing and sequencing'),('Effects Library','200+ transitions, filters, and animated overlays'),('Audio Sync','Auto-sync audio tracks with visual timeline markers'),('Multi-Export','MP4, WebM, GIF, and MOV at any resolution up to 4K'),('Batch Processing','Render multiple variants simultaneously')],
        'development': [('Type-Safe Code','Generated code with full TypeScript types and documentation'),('Framework Ready','Output for React, Vue, Svelte, and vanilla JS'),('Hot Reload','Live preview updates as you modify generated code'),('Testing Built-in','Generated unit tests and integration test stubs'),('Deploy Ready','One-click deploy to Vercel, Netlify, or custom servers')],
        'ai':          [('Multi-Model','Access leading AI models — GPT-4, Claude, Stable Diffusion, and more'),('Batch Generation','Generate hundreds of variants from a single prompt'),('Quality Scoring','AI rates output quality and suggests improvements'),('Style Control','Fine-tune style, tone, and mood for consistent output'),('Prompt Library','Curated prompt templates for every use case')],
        'utility':     [('Automation','Configure once, run forever — batch, schedule, or webhook'),('Integration','Works with 40+ tools — Figma, Notion, Slack, and more'),('Logging','Full audit trail of every operation and transformation'),('Error Recovery','Automatic retry and fallback on temporary failures'),('Speed','Sub-second processing for most operations')],
    }
    return defaults.get(cat, defaults['design'])


def make_html(skill):
    s = skill
    t = THEMES.get(s['category'], THEMES['design'])
    p = t['primary']
    bg = t['bg']
    accent = t['accent']
    label = t['label']
    icon = t['icon']
    sid = s['id']
    name = s['name']
    desc = s['description']
    rgb = hex_to_rgb(p)

    # Feature cards
    icons_list = ['⚡','🎯','🔄','📐','🧩','🛡️']
    features = feature_list(sid)
    feature_cards = []
    for i, (title, body) in enumerate(features[:6]):
        ic = icons_list[i % len(icons_list)]
        feature_cards.append(f'''<div class="card">
      <div class="card-icon">{ic}</div>
      <h3>{title}</h3>
      <p>{body}</p>
    </div>''')
    feature_cards_html = '\n'.join(feature_cards)

    # Stats
    stats_data = {
        'design': [('4.2M+','Designs Created'),('98%','Satisfaction Rate'),('340+','Templates Available'),('12s','Avg. Render Time')],
        'content': [('2.8M+','Documents Generated'),('99.2%','Format Accuracy'),('180+','Templates'),('8s','Avg. Generation')],
        'media': [('1.6M+','Videos Created'),('97%','Quality Score'),('95+','Effects Library'),('15s','Avg. Render')],
        'development': [('890K+','Components Built'),('99.8%','Code Quality'),('60+','Frameworks'),('2s','Avg. Build')],
        'ai': [('6.1M+','Generations'),('99.5%','Uptime'),('50+','Models Available'),('3s','Avg. Response')],
        'utility': [('3.4M+','Tasks Completed'),('100%','Automation Rate'),('40+','Integrations'),('1s','Avg. Processing')],
    }
    sdata = stats_data.get(s['category'], stats_data['design'])
    stats_html = ''.join(f'<div class="stat"><div class="stat-value">{v}</div><div class="stat-label">{l}</div></div>' for v,l in sdata)

    # Demo section based on category
    cat = s['category']
    if cat == 'design':
        demo = f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div style="background:rgba({rgb},0.08);border-radius:8px;padding:24px;display:flex;flex-direction:column;justify-content:space-between;min-height:200px">
        <div>
          <div style="font-size:11px;text-transform:uppercase;color:{p};letter-spacing:0.1em;font-weight:600;margin-bottom:8px">Design System</div>
          <div style="font-size:24px;font-weight:700;margin-bottom:8px">Component Library</div>
          <div style="font-size:13px;color:var(--text-muted)">Consistent, reusable components built for scale</div>
        </div>
        <div style="display:flex;gap:8px;margin-top:16px">
          <div style="background:{p};color:#000;padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600">Primary</div>
          <div style="background:transparent;border:1px solid {p};color:{p};padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600">Secondary</div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;gap:16px">
        <div style="background:var(--surface-2);border-radius:8px;padding:16px;display:flex;align-items:center;gap:12px">
          <div style="width:40px;height:40px;border-radius:8px;background:{p}"></div>
          <div><div style="font-size:13px;font-weight:600">Spacing Scale</div><div style="font-size:11px;color:var(--text-muted)">4 &middot; 8 &middot; 12 &middot; 16 &middot; 24 &middot; 32 &middot; 48</div></div>
        </div>
        <div style="background:var(--surface-2);border-radius:8px;padding:16px;display:flex;gap:6px;flex-wrap:wrap">
          <div style="width:28px;height:28px;border-radius:6px;background:{p}"></div>
          <div style="width:28px;height:28px;border-radius:6px;background:{accent}"></div>
          <div style="width:28px;height:28px;border-radius:6px;background:#1a1a2e"></div>
          <div style="width:28px;height:28px;border-radius:6px;background:#e8e8e8"></div>
          <div style="width:28px;height:28px;border-radius:6px;background:rgba(255,255,255,0.06)"></div>
        </div>
        <div style="background:var(--surface-2);border-radius:8px;padding:16px">
          <div style="font-size:13px;font-weight:600;margin-bottom:8px">Typography</div>
          <div style="font-size:28px;font-weight:800;letter-spacing:-0.02em">Aa</div>
          <div style="font-size:11px;color:var(--text-muted)">Inter &middot; 300/400/600/800</div>
        </div>
      </div>
    </div>'''
    elif cat == 'content':
        demo = f'''<div style="display:flex;gap:24px;align-items:stretch">
      <div style="flex:1;background:var(--surface-2);border-radius:8px;padding:24px">
        <div style="font-size:11px;text-transform:uppercase;color:{p};letter-spacing:0.1em;font-weight:600;margin-bottom:12px">Document Preview</div>
        <div style="font-size:22px;font-weight:700;margin-bottom:6px">Quarterly Report</div>
        <div style="font-size:12px;color:var(--text-muted);margin-bottom:16px">FY2026 Q1 &middot; Generated automatically</div>
        <div style="height:4px;background:rgba(255,255,255,0.06);border-radius:2px;margin-bottom:8px"><div style="height:4px;width:72%;background:{p};border-radius:2px"></div></div>
        <div style="display:flex;gap:12px;margin-top:16px">
          <div style="flex:1;background:rgba({rgb},0.12);border-radius:6px;padding:12px;text-align:center">
            <div style="font-size:20px;font-weight:700;color:{p}">$2.4M</div>
            <div style="font-size:10px;color:var(--text-muted)">Revenue</div>
          </div>
          <div style="flex:1;background:var(--surface);border-radius:6px;padding:12px;text-align:center">
            <div style="font-size:20px;font-weight:700">18.3%</div>
            <div style="font-size:10px;color:var(--text-muted)">Growth</div>
          </div>
        </div>
      </div>
      <div style="width:180px;display:flex;flex-direction:column;gap:12px">
        <div style="background:var(--surface-2);border-radius:8px;padding:16px;text-align:center">
          <div style="font-size:24px;font-weight:700;color:{p}">PDF</div>
          <div style="font-size:10px;color:var(--text-muted)">Export Ready</div>
        </div>
        <div style="background:var(--surface-2);border-radius:8px;padding:16px;text-align:center">
          <div style="font-size:24px;font-weight:700">DOCX</div>
          <div style="font-size:10px;color:var(--text-muted)">Word Format</div>
        </div>
        <div style="background:var(--surface-2);border-radius:8px;padding:16px;text-align:center">
          <div style="font-size:24px;font-weight:700;color:{p}">MD</div>
          <div style="font-size:10px;color:var(--text-muted)">Markdown</div>
        </div>
      </div>
    </div>'''
    elif cat == 'media':
        demo = f'''<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">
      <div style="background:rgba(255,255,255,0.03);border-radius:8px;overflow:hidden;aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;position:relative">
        <div style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.6);padding:2px 8px;border-radius:4px;font-size:10px">00:12</div>
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none"><circle cx="24" cy="24" r="22" fill="rgba(255,255,255,0.1)"/><polygon points="20,16 20,32 34,24" fill="{p}"/></svg>
      </div>
      <div style="background:rgba(255,255,255,0.03);border-radius:8px;overflow:hidden;aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;position:relative">
        <div style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.6);padding:2px 8px;border-radius:4px;font-size:10px">00:24</div>
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none"><circle cx="24" cy="24" r="22" fill="rgba(255,255,255,0.1)"/><polygon points="20,16 20,32 34,24" fill="{p}"/></svg>
      </div>
      <div style="background:rgba(255,255,255,0.03);border-radius:8px;overflow:hidden;aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;position:relative">
        <div style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.6);padding:2px 8px;border-radius:4px;font-size:10px">00:08</div>
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none"><circle cx="24" cy="24" r="22" fill="rgba(255,255,255,0.1)"/><polygon points="20,16 20,32 34,24" fill="{p}"/></svg>
      </div>
    </div>
    <div style="margin-top:16px;display:flex;align-items:center;gap:12px">
      <div style="flex:1;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;position:relative"><div style="position:absolute;left:0;top:0;width:35%;height:4px;background:{p};border-radius:2px"></div></div>
      <span style="font-size:11px;color:var(--text-muted)">0:14 / 0:44</span>
    </div>'''
    elif cat == 'development':
        demo = f'''<div style="display:flex;gap:16px;font-family:'SF Mono','Fira Code',monospace;font-size:12px">
      <div style="flex:1;background:rgba(0,0,0,0.4);border-radius:8px;padding:16px;overflow:hidden">
        <div style="color:var(--text-muted);margin-bottom:8px;display:flex;justify-content:space-between">
          <span>app.tsx</span><span style="color:{p}">&#9679; running</span>
        </div>
        <pre style="line-height:1.8;color:#a0a0a0;white-space:pre-wrap"><span style="color:#c678dd">import</span> {'{'} <span style="color:{p}">Component</span> {'}'} <span style="color:#c678dd">from</span> <span style="color:#98c379">'./skill'</span>;

<span style="color:#c678dd">export const</span> <span style="color:{p}">{sid.replace("-","_")}</span> = () {'{'} {'{'}
  &lt;<span style="color:#e06c75">div</span> <span style="color:#d19a66">className</span>=<span style="color:#98c379">"container"</span>&gt;
    &lt;<span style="color:#e06c75">h1</span>&gt;{name}&lt;/<span style="color:#e06c75">h1</span>&gt;
    &lt;<span style="color:{p}">Component</span> /&gt;
  &lt;/<span style="color:#e06c75">div</span>&gt;
{'}'}{'}'}</pre>
      </div>
      <div style="flex:1;background:var(--surface-2);border-radius:8px;padding:16px;display:flex;flex-direction:column;gap:12px">
        <div style="font-size:12px;font-weight:600;margin-bottom:4px;font-family:Inter,sans-serif">Build Output</div>
        <div style="display:flex;align-items:center;gap:8px"><div style="width:8px;height:8px;border-radius:50%;background:#22c55e"></div><span style="font-size:12px;font-family:Inter,sans-serif">Compiled successfully</span></div>
        <div style="display:flex;align-items:center;gap:8px"><div style="width:8px;height:8px;border-radius:50%;background:#22c55e"></div><span style="font-size:12px;font-family:Inter,sans-serif">0 TypeScript errors</span></div>
        <div style="display:flex;align-items:center;gap:8px"><div style="width:8px;height:8px;border-radius:50%;background:#22c55e"></div><span style="font-size:12px;font-family:Inter,sans-serif">Bundle: 24.3 kB (gzipped)</span></div>
        <div style="display:flex;align-items:center;gap:8px"><div style="width:8px;height:8px;border-radius:50%;background:#f59e0b"></div><span style="font-size:12px;font-family:Inter,sans-serif">1 warning (unused import)</span></div>
        <div style="margin-top:auto;background:{p};color:#000;padding:8px 12px;border-radius:6px;font-size:12px;font-weight:600;text-align:center;font-family:Inter,sans-serif">Deploy &rarr;</div>
      </div>
    </div>'''
    elif cat == 'ai':
        demo = f'''<div style="display:flex;gap:16px">
      <div style="flex:1;background:rgba(0,0,0,0.3);border-radius:8px;padding:16px">
        <div style="font-size:11px;text-transform:uppercase;color:{p};letter-spacing:0.1em;font-weight:600;margin-bottom:12px">Input</div>
        <div style="background:rgba(255,255,255,0.03);border-radius:6px;padding:12px;font-size:13px;line-height:1.6;color:var(--text-muted)">
          Generate a {sid.replace("-"," ")} that demonstrates professional quality output with modern design principles...
        </div>
        <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
          <span class="tag">Quality: High</span>
          <span class="tag">Style: Modern</span>
          <span class="tag">Size: 1024px</span>
        </div>
      </div>
      <div style="display:flex;align-items:center"><svg width="24" height="24" viewBox="0 0 24 24" fill="{p}"><path d="M8 5l8 7-8 7V5z"/></svg></div>
      <div style="flex:1;background:var(--surface-2);border-radius:8px;padding:16px">
        <div style="font-size:11px;text-transform:uppercase;color:{p};letter-spacing:0.1em;font-weight:600;margin-bottom:12px">Output</div>
        <div style="background:rgba(0,0,0,0.2);border-radius:6px;height:140px;display:flex;align-items:center;justify-content:center;border:1px dashed rgba(255,255,255,0.1)">
          <div style="text-align:center">
            <div style="font-size:36px;margin-bottom:4px">&#10024;</div>
            <div style="font-size:12px;color:var(--text-muted)">AI Generated Result</div>
          </div>
        </div>
        <div style="margin-top:12px;font-size:11px;color:var(--text-muted)">Generated in 2.3s &middot; 1,024 tokens &middot; Model: OpenFlux v3</div>
      </div>
    </div>'''
    else:  # utility
        demo = f'''<div style="display:flex;gap:16px">
      <div style="flex:1;display:flex;flex-direction:column;gap:12px">
        <div style="background:var(--surface-2);border-radius:8px;padding:16px">
          <div style="font-size:11px;text-transform:uppercase;color:{p};letter-spacing:0.1em;font-weight:600;margin-bottom:8px">Configure</div>
          <div style="margin-bottom:8px">
            <div style="font-size:12px;color:var(--text-muted);margin-bottom:4px">Source URL</div>
            <div style="background:rgba(0,0,0,0.3);border-radius:6px;padding:8px 12px;font-size:13px;font-family:monospace;color:{accent}">https://example.com/page</div>
          </div>
          <div style="display:flex;gap:8px">
            <div style="background:{p};color:#000;padding:6px 16px;border-radius:6px;font-size:12px;font-weight:600;text-align:center;flex:1">Run Tool</div>
            <div style="background:var(--surface);border:1px solid var(--border);padding:6px 16px;border-radius:6px;font-size:12px;text-align:center">Reset</div>
          </div>
        </div>
        <div style="background:var(--surface-2);border-radius:8px;padding:16px;display:flex;align-items:center;gap:12px">
          <div style="width:36px;height:36px;border-radius:50%;background:rgba({rgb},0.15);display:flex;align-items:center;justify-content:center;font-size:16px">&#10003;</div>
          <div><div style="font-size:13px;font-weight:600">Completed</div><div style="font-size:11px;color:var(--text-muted)">Processed in 1.4s</div></div>
        </div>
      </div>
      <div style="flex:1;background:rgba(0,0,0,0.3);border-radius:8px;padding:16px">
        <div style="font-size:11px;text-transform:uppercase;color:{p};letter-spacing:0.1em;font-weight:600;margin-bottom:8px">Output</div>
        <div style="font-size:12px;font-family:monospace;line-height:1.7;color:var(--text-muted)">
          <span style="color:#22c55e">&#10003;</span> Analyzing source... <span style="color:var(--text-muted)">done</span><br>
          <span style="color:#22c55e">&#10003;</span> Processing data... <span style="color:var(--text-muted)">done</span><br>
          <span style="color:#22c55e">&#10003;</span> Generating output... <span style="color:var(--text-muted)">done</span><br>
          <span style="color:{p}">&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;</span><br>
          Result: 47 items processed<br>
          Output saved to /results/
        </div>
      </div>
    </div>'''

    # Feature row based on category
    if cat == 'design':
        feature_row = f'''<div class="feature-row">
  <div class="feature-text">
    <div class="tag" style="margin-bottom:16px">Design Tokens</div>
    <h2>Systematic Design at Scale</h2>
    <p>Every color, spacing unit, and typography rule becomes a design token. Build consistent interfaces that scale from prototype to production without drift.</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px">
      <div style="background:rgba(255,255,255,0.04);border:1px solid var(--border);border-radius:6px;padding:4px 12px;font-size:12px;font-family:monospace">--color-primary</div>
      <div style="background:rgba(255,255,255,0.04);border:1px solid var(--border);border-radius:6px;padding:4px 12px;font-size:12px;font-family:monospace">--spacing-4</div>
      <div style="background:rgba(255,255,255,0.04);border:1px solid var(--border);border-radius:6px;padding:4px 12px;font-size:12px;font-family:monospace">--radius-lg</div>
    </div>
  </div>
  <div class="feature-visual" style="background:linear-gradient(135deg, rgba({rgb},0.05), rgba({rgb},0.02));flex-direction:column;gap:12px;align-items:flex-start;padding:28px">
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <div style="width:32px;height:32px;border-radius:8px;background:{p}"></div>
      <div style="width:32px;height:32px;border-radius:8px;background:{accent}"></div>
      <div style="width:32px;height:32px;border-radius:8px;background:#1a1a2e;border:1px solid rgba(255,255,255,0.15)"></div>
      <div style="width:32px;height:32px;border-radius:8px;background:#e8e8e8"></div>
    </div>
    <div style="font-size:36px;font-weight:800;letter-spacing:-0.03em">Aa Bb Cc</div>
    <div style="font-size:13px;color:var(--text-muted)">Inter &middot; 800 / 400 / 300</div>
    <div style="display:flex;gap:4px;width:100%">
      <div style="flex:1;height:4px;border-radius:2px;background:{p}"></div>
      <div style="flex:1;height:4px;border-radius:2px;background:{accent}"></div>
      <div style="flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,0.1)"></div>
    </div>
  </div>
</div>'''
    elif cat == 'content':
        feature_row = f'''<div class="feature-row">
  <div class="feature-text">
    <div class="tag" style="margin-bottom:16px">Multi-Format Export</div>
    <h2>One Source, Every Format</h2>
    <p>Write once, export everywhere. Generate PDFs, DOCX, slides, and markdown from a single source of truth. No reformatting, no rework.</p>
    <div style="display:flex;gap:12px;margin-top:16px">
      <div style="background:{p};color:#000;padding:6px 16px;border-radius:6px;font-size:12px;font-weight:600">PDF</div>
      <div style="border:1px solid var(--border);padding:6px 16px;border-radius:6px;font-size:12px">DOCX</div>
      <div style="border:1px solid var(--border);padding:6px 16px;border-radius:6px;font-size:12px">HTML</div>
      <div style="border:1px solid var(--border);padding:6px 16px;border-radius:6px;font-size:12px">MD</div>
    </div>
  </div>
  <div class="feature-visual" style="flex-direction:column;gap:8px;align-items:flex-start;padding:24px">
    <div style="width:100%;background:rgba(255,255,255,0.06);border-radius:6px;padding:12px;font-family:monospace;font-size:11px;color:var(--text-muted)">
      <div style="color:{p}">## Section One</div>
      <div>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>
      <div style="margin-top:8px;color:{p}">## Section Two</div>
      <div>Sed do eiusmod tempor incididunt ut labore.</div>
    </div>
    <div style="display:flex;gap:8px;width:100%">
      <div style="flex:1;background:{p};border-radius:6px;padding:8px;text-align:center;font-size:11px;font-weight:600;color:#000">PDF &#10003;</div>
      <div style="flex:1;background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:8px;text-align:center;font-size:11px">DOCX &#10003;</div>
      <div style="flex:1;background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:8px;text-align:center;font-size:11px">HTML &#10003;</div>
    </div>
  </div>
</div>'''
    elif cat == 'media':
        feature_row = f'''<div class="feature-row">
  <div class="feature-text">
    <div class="tag" style="margin-bottom:16px">Timeline Editor</div>
    <h2>Frame-Perfect Control</h2>
    <p>Visual timeline editor with keyframe animation, transition curves, and real-time preview. What you see is exactly what ships.</p>
    <div style="margin-top:16px;font-size:13px;color:var(--text-muted)">Supports MP4, WebM, GIF, and MOV export at up to 4K resolution.</div>
  </div>
  <div class="feature-visual" style="flex-direction:column;gap:12px;padding:24px">
    <div style="display:flex;gap:8px;width:100%;align-items:center">
      <div style="width:60px;height:40px;border-radius:6px;background:rgba({rgb},0.15);display:flex;align-items:center;justify-content:center;font-size:10px;color:{p}">00:00</div>
      <div style="flex:1;height:40px;background:rgba(255,255,255,0.05);border-radius:6px;position:relative;overflow:hidden"><div style="position:absolute;left:0;top:0;width:30%;height:100%;background:{p};opacity:0.3;border-radius:6px"></div><div style="position:absolute;left:30%;top:8px;bottom:8px;width:2px;background:{p}"></div></div>
      <div style="width:60px;height:40px;border-radius:6px;background:rgba(255,255,255,0.05);display:flex;align-items:center;justify-content:center;font-size:10px;color:var(--text-muted)">00:12</div>
    </div>
    <div style="display:flex;gap:6px">
      <div style="padding:4px 12px;background:{p};color:#000;border-radius:4px;font-size:10px;font-weight:600">Scene 1</div>
      <div style="padding:4px 12px;background:var(--surface-2);border-radius:4px;font-size:10px">Scene 2</div>
      <div style="padding:4px 12px;background:var(--surface-2);border-radius:4px;font-size:10px">Scene 3</div>
    </div>
  </div>
</div>'''
    elif cat == 'development':
        feature_row = f'''<div class="feature-row">
  <div class="feature-text">
    <div class="tag" style="margin-bottom:16px">Type-Safe Output</div>
    <h2>Production-Grade Code Generation</h2>
    <p>Generate clean, type-safe code that integrates directly into your codebase. No boilerplate, no cleanup.</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px">
      <span class="tag">TypeScript</span>
      <span class="tag">React</span>
      <span class="tag">CSS Modules</span>
    </div>
  </div>
  <div class="feature-visual" style="background:rgba(0,0,0,0.5);padding:24px;align-items:flex-start;font-family:'SF Mono','Fira Code',monospace;font-size:12px">
    <div style="color:#c678dd">interface</div>
    <div style="color:{p};margin-left:16px">Props {'{'}</div>
    <div style="margin-left:32px">variant: <span style="color:#56b6c2">'primary' | 'secondary'</span>;</div>
    <div style="margin-left:32px">size: <span style="color:#56b6c2">'sm' | 'md' | 'lg'</span>;</div>
    <div style="margin-left:16px">{'}'}</div>
    <br>
    <div style="color:#c678dd">export const</div>
    <div style="color:{p};margin-left:16px">Component</div>
    <div style="color:var(--text-muted);margin-left:8px">= (props) =&gt; {'{'}</div>
    <div style="color:#c678dd;margin-left:32px">return</div>
    <div style="margin-left:48px">&lt;<span style="color:#e06c75">button</span> /&gt;</div>
    <div style="margin-left:16px">{'}'}</div>
  </div>
</div>'''
    elif cat == 'ai':
        feature_row = f'''<div class="feature-row">
  <div class="feature-text">
    <div class="tag" style="margin-bottom:16px">AI-Powered</div>
    <h2>Intelligent Generation Pipeline</h2>
    <p>Multi-model AI pipeline that understands context, maintains consistency, and iterates on feedback. From prompt to production in seconds.</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px">
      <span class="tag">Multi-Model</span>
      <span class="tag">Context-Aware</span>
      <span class="tag">Iterative</span>
    </div>
  </div>
  <div class="feature-visual" style="flex-direction:column;gap:16px;padding:24px">
    <div style="display:flex;align-items:center;gap:12px;width:100%">
      <div style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;font-size:16px">&#128221;</div>
      <div style="flex:1;height:3px;background:rgba(255,255,255,0.06);border-radius:2px;position:relative"><div style="position:absolute;left:0;top:0;width:100%;height:3px;background:{p};border-radius:2px"></div></div>
      <div style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;font-size:16px">&#129302;</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;width:100%">
      <div style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;font-size:16px">&#129302;</div>
      <div style="flex:1;height:3px;background:rgba(255,255,255,0.06);border-radius:2px;position:relative"><div style="position:absolute;left:0;top:0;width:100%;height:3px;background:{p};border-radius:2px"></div></div>
      <div style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;font-size:16px">&#10024;</div>
    </div>
    <div style="text-align:center;font-size:12px;color:var(--text-muted)">Prompt &rarr; Model &rarr; Refined Output</div>
  </div>
</div>'''
    else:  # utility
        feature_row = f'''<div class="feature-row">
  <div class="feature-text">
    <div class="tag" style="margin-bottom:16px">Automation</div>
    <h2>Set It and Forget It</h2>
    <p>Configure once, run forever. Batch processing, scheduled runs, and webhook triggers for automated workflows.</p>
    <div style="margin-top:16px;font-size:13px;color:var(--text-muted)">Webhook support &middot; Cron scheduling &middot; Batch API &middot; Event-driven</div>
  </div>
  <div class="feature-visual" style="flex-direction:column;gap:12px;padding:24px;align-items:flex-start">
    <div style="display:flex;gap:8px;width:100%">
      <div style="flex:1;background:var(--surface-2);border-radius:6px;padding:12px;text-align:center"><div style="font-size:20px;margin-bottom:4px">&#128229;</div><div style="font-size:11px">Input</div></div>
      <div style="flex:1;background:rgba({rgb},0.1);border-radius:6px;padding:12px;text-align:center"><div style="font-size:20px;margin-bottom:4px">&#9881;</div><div style="font-size:11px;color:{p}">Process</div></div>
      <div style="flex:1;background:var(--surface-2);border-radius:6px;padding:12px;text-align:center"><div style="font-size:20px;margin-bottom:4px">&#128228;</div><div style="font-size:11px">Output</div></div>
    </div>
    <div style="width:100%;height:3px;background:rgba(255,255,255,0.06);border-radius:2px;position:relative"><div style="position:absolute;left:0;top:0;width:65%;height:3px;background:{p};border-radius:2px"></div></div>
    <div style="font-size:12px;color:var(--text-muted)">Processing 847 of 1,200 items...</div>
  </div>
</div>'''

    hero_desc_map = {
        'ad-creative': 'Generate scroll-stopping ad creatives for every platform. From Facebook to TikTok, produce variants that convert — branded, formatted, and ready to ship.',
        'color-expert': 'Master color theory with AI-powered palettes, contrast checkers, and accessibility scores. Build harmonious systems that look stunning and pass WCAG.',
        'algorithmic-art': 'Create generative art through code. Explore mathematical beauty with L-systems, fractals, noise fields, and particle systems.',
    }

    hero_desc = hero_desc_map.get(sid, f'{desc}. Build, iterate, and ship with Open Design\'s {name.lower()} skill — professional tools for modern creators.')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} &mdash; {label} Skill</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root {{
  --primary: {p};
  --primary-rgb: {rgb};
  --bg: {bg};
  --accent: {accent};
  --surface: rgba(255,255,255,0.04);
  --surface-2: rgba(255,255,255,0.07);
  --border: rgba(255,255,255,0.1);
  --text: #e8e8e8;
  --text-muted: rgba(255,255,255,0.5);
  --radius: 10px;
}}
*,*::before,*::after {{ box-sizing:border-box; margin:0; padding:0; }}
html {{ scroll-behavior:smooth; }}
body {{ font-family:'Inter',system-ui,sans-serif; background:var(--bg); color:var(--text); line-height:1.6; -webkit-font-smoothing:antialiased; }}
a {{ color:var(--primary); text-decoration:none; }}
a:hover {{ opacity:0.85; }}
.container {{ max-width:1200px; margin:0 auto; padding:0 24px; }}
.nav {{ position:sticky; top:0; z-index:100; background:rgba(0,0,0,0.55); backdrop-filter:blur(24px); border-bottom:1px solid var(--border); padding:0 24px; }}
.nav-inner {{ max-width:1200px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; height:60px; }}
.nav-logo {{ display:flex; align-items:center; gap:10px; }}
.nav-logo span.icon {{ font-size:22px; }}
.nav-logo span.name {{ font-weight:700; font-size:15px; color:var(--text); }}
.nav-links {{ display:flex; gap:24px; align-items:center; }}
.nav-links a {{ color:var(--text); font-size:13px; opacity:0.65; transition:opacity 0.2s; }}
.nav-links a:hover {{ opacity:1; }}
.nav-cta {{ background:var(--primary); color:#000; padding:7px 18px; border-radius:7px; font-size:13px; font-weight:600; }}
.hero {{ padding:100px 24px 80px; text-align:center; position:relative; overflow:hidden; }}
.hero-glow {{ position:absolute; top:-250px; left:50%; transform:translateX(-50%); width:700px; height:700px; background:radial-gradient(circle, rgba(var(--primary-rgb),0.08) 0%, transparent 70%); pointer-events:none; }}
.hero-inner {{ max-width:800px; margin:0 auto; position:relative; }}
.hero-emoji {{ font-size:60px; margin-bottom:18px; }}
.hero-badge {{ display:inline-flex; align-items:center; gap:6px; background:var(--surface); border:1px solid var(--border); padding:6px 16px; border-radius:20px; font-size:12px; color:var(--primary); margin-bottom:24px; text-transform:uppercase; letter-spacing:0.05em; font-weight:600; }}
.hero h1 {{ font-size:clamp(32px,5vw,52px); font-weight:800; line-height:1.1; margin:0 0 16px; letter-spacing:-0.03em; }}
.hero p {{ font-size:17px; color:var(--text-muted); line-height:1.7; max-width:560px; margin:0 auto 36px; }}
.hero-actions {{ display:flex; gap:12px; justify-content:center; flex-wrap:wrap; }}
.btn-primary {{ background:var(--primary); color:#000; padding:13px 30px; border-radius:8px; font-size:14px; font-weight:700; border:none; cursor:pointer; box-shadow:0 0 30px rgba(var(--primary-rgb),0.25); transition:transform 0.15s,box-shadow 0.15s; }}
.btn-primary:hover {{ transform:translateY(-1px); box-shadow:0 0 40px rgba(var(--primary-rgb),0.35); }}
.btn-secondary {{ background:var(--surface); color:var(--text); padding:13px 30px; border-radius:8px; font-size:14px; font-weight:500; border:1px solid var(--border); cursor:pointer; transition:border-color 0.2s; }}
.btn-secondary:hover {{ border-color:var(--primary); }}
.section {{ padding:60px 24px; }}
.section-title {{ font-size:28px; font-weight:700; margin:0 0 12px; text-align:center; letter-spacing:-0.02em; }}
.section-sub {{ text-align:center; color:var(--text-muted); font-size:15px; margin:0 0 40px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:20px; }}
.card {{ background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:28px; transition:border-color 0.25s, transform 0.2s; cursor:default; }}
.card:hover {{ border-color:var(--primary); transform:translateY(-2px); }}
.card-icon {{ font-size:28px; margin-bottom:14px; }}
.card h3 {{ font-size:16px; font-weight:600; margin:0 0 8px; }}
.card p {{ font-size:14px; color:var(--text-muted); line-height:1.55; margin:0; }}
.stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:20px; padding:40px 24px; }}
.stat {{ text-align:center; padding:24px; background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); }}
.stat-value {{ font-size:36px; font-weight:800; color:var(--primary); margin-bottom:4px; }}
.stat-label {{ font-size:13px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.06em; }}
.feature-row {{ display:grid; grid-template-columns:1fr 1fr; gap:40px; align-items:center; padding:60px 24px; }}
.feature-text h2 {{ font-size:28px; font-weight:700; margin:0 0 12px; letter-spacing:-0.02em; }}
.feature-text p {{ color:var(--text-muted); margin:0 0 20px; line-height:1.65; }}
.feature-visual {{ background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:32px; min-height:260px; display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden; }}
.tag {{ display:inline-block; background:rgba(var(--primary-rgb),0.12); color:var(--primary); padding:3px 10px; border-radius:12px; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; }}
.footer {{ padding:32px 24px; text-align:center; opacity:0.4; font-size:12px; }}
@media(max-width:768px) {{
  .stats {{ grid-template-columns:repeat(2,1fr); }}
  .feature-row {{ grid-template-columns:1fr; }}
}}
</style>
</head>
<body>
<nav class="nav">
  <div class="nav-inner">
    <div class="nav-logo">
      <span class="icon">{icon}</span>
      <span class="name">{name}</span>
    </div>
    <div class="nav-links">
      <a href="#features">Features</a>
      <a href="#demo">Demo</a>
      <a href="#api">API</a>
      <a class="nav-cta" href="#">Try Free</a>
    </div>
  </div>
</nav>

<section class="hero">
  <div class="hero-glow"></div>
  <div class="hero-inner">
    <div class="hero-emoji">{icon}</div>
    <div class="hero-badge">{label} &middot; Open Design</div>
    <h1>{name}</h1>
    <p>{hero_desc}</p>
    <div class="hero-actions">
      <button class="btn-primary">Get Started</button>
      <button class="btn-secondary">View Examples</button>
    </div>
  </div>
</section>

<div class="container">
  <div class="stats">{stats_html}</div>
</div>

<section class="section" id="features">
  <h2 class="section-title">Key Features</h2>
  <p class="section-sub">Everything you need to create professional-quality output with {sid.replace("-"," ")}.</p>
  <div class="grid">
    {feature_cards_html}
  </div>
</section>

<section class="section" id="demo">
  <h2 class="section-title">Live Demo</h2>
  <p class="section-sub">See {sid.replace("-"," ").title()} in action</p>
  <div style="max-width:900px;margin:0 auto;background:var(--surface);border:1px solid var(--border);border-radius:12px;overflow:hidden">
    <div style="padding:12px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px">
      <div style="width:12px;height:12px;border-radius:50%;background:#ef4444"></div>
      <div style="width:12px;height:12px;border-radius:50%;background:#f59e0b"></div>
      <div style="width:12px;height:12px;border-radius:50%;background:#22c55e"></div>
      <span style="margin-left:auto;font-size:12px;color:var(--text-muted)">opendesign.studio/{sid}</span>
    </div>
    <div style="padding:32px;min-height:320px">
      {demo}
    </div>
  </div>
</section>

{feature_row}

<section class="section" style="border-top:1px solid var(--border)">
  <h2 class="section-title">How It Works</h2>
  <p class="section-sub">Three steps to {desc.lower()}</p>
  <div class="grid" style="grid-template-columns:repeat(3,1fr)">
    <div class="card" style="text-align:center">
      <div style="width:48px;height:48px;border-radius:50%;background:rgba(var(--primary-rgb),0.12);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;font-weight:800;color:var(--primary);font-size:20px">1</div>
      <h3>Configure</h3>
      <p>Set your parameters, choose your style, and define your creative direction.</p>
    </div>
    <div class="card" style="text-align:center">
      <div style="width:48px;height:48px;border-radius:50%;background:rgba(var(--primary-rgb),0.12);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;font-weight:800;color:var(--primary);font-size:20px">2</div>
      <h3>Generate</h3>
      <p>AI processes your input and generates professional-quality output instantly.</p>
    </div>
    <div class="card" style="text-align:center">
      <div style="width:48px;height:48px;border-radius:50%;background:rgba(var(--primary-rgb),0.12);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;font-weight:800;color:var(--primary);font-size:20px">3</div>
      <h3>Refine &amp; Export</h3>
      <p>Fine-tune the result, iterate on variations, and export in your preferred format.</p>
    </div>
  </div>
</section>

<section class="cta" style="text-align:center;padding:80px 24px;background:var(--surface);border-top:1px solid var(--border)">
  <h2 style="font-size:36px;font-weight:700;margin:0 0 16px;letter-spacing:-0.02em">Start Using {name}</h2>
  <p style="color:var(--text-muted);margin:0 0 28px">{label} skill &mdash; free to explore, powerful in production.</p>
  <button class="btn-primary" style="font-size:16px;padding:16px 36px">Get Started Free &rarr;</button>
</section>

<footer class="footer">&copy; 2026 Open Design Studio &middot; {name}</footer>
</body>
</html>'''


if __name__ == '__main__':
    out_dir = '/home/vivgates/.openclaw/workspace/DesignSite/public/showcase/skills'
    count = 0
    for skill in SKILLS:
        html = make_html(skill)
        path = os.path.join(out_dir, f"{skill['id']}.html")
        with open(path, 'w') as f:
            f.write(html)
        size = os.path.getsize(path)
        print(f"  ✓ {skill['id']}.html ({size:,} bytes)")
        count += 1
    print(f"\nGenerated {count} mockups")