"""CSS styles for the rune documentation site."""
from __future__ import annotations


def get_styles() -> str:
    """Return the complete CSS block including <style> tags."""
    return """
<style>
/* -- Theme ------------------------------------------------- */
:root {
  --bg: #f5f2ea; --fg: #2b3044; --fg2: #424661; --accent: #7d4f16;
  --accent2: #ae6e1f; --card: #dfeae6; --border: rgba(43, 48, 68, 0.1);
  --nav-bg: #dfeae6; --nav-active: rgba(255, 255, 255, 0.6); --search-bg: rgba(255, 255, 255, 0.3);
  --search-panel-bg: #f8f5ef; --search-panel-border: rgba(43, 48, 68, 0.16); --search-panel-active: rgba(125, 79, 22, 0.12);
  --code-bg: #dfeae6; --tag: #424661; --tag-fg: #f5f2ea;
  --green: #a7cca4; --red: #b04a29; --yellow: #e1b64d;
  --gloss-ai: #424661; --gloss-ai-bg: rgba(66, 70, 97, 0.08);
  --gloss-kit: #7d4f16; --gloss-kit-bg: rgba(125, 79, 22, 0.08);
  --gloss-exec: #424661; --gloss-exec-bg: rgba(66, 70, 97, 0.08);
  --gloss-know: #b04a29; --gloss-know-bg: rgba(176, 74, 41, 0.08);
  --mobile-nav-height: 4rem;
  --content-max: clamp(20rem, 74vw, 78ch);
  --content-max-mobile: clamp(18rem, 100vw, 72ch);
  --content-pad-x: clamp(1rem, 4vw, 3rem);
  --content-pad-y: clamp(1.5rem, 1vw + 1.2rem, 2rem);
  --content-pad-bottom: clamp(3rem, 3vw + 2.2rem, 4rem);
}

/* Dark mode overrides */
:root.theme-dark {
  --bg: #1e1b18; --fg: #c9ddd8; --fg2: #a7cca4; --accent: #f9dfa5;
  --accent2: #ae6e1f; --card: rgba(0, 0, 0, 0.25); --border: rgba(201, 221, 216, 0.1);
  --nav-bg: #151311; --nav-active: rgba(255, 255, 255, 0.05); --search-bg: rgba(0, 0, 0, 0.2);
  --search-panel-bg: #1a1714; --search-panel-border: rgba(201, 221, 216, 0.18); --search-panel-active: rgba(249, 223, 165, 0.14);
  --code-bg: #110f0e; --tag: #72a9bf; --tag-fg: #1e1b18;
  --green: #a7cca4; --red: #ae6e1f; --yellow: #e1b64d;
  --gloss-ai: #c9ddd8; --gloss-ai-bg: rgba(201, 221, 216, 0.1);
  --gloss-kit: #f9dfa5; --gloss-kit-bg: rgba(249, 223, 165, 0.15);
  --gloss-exec: #e1b64d; --gloss-exec-bg: rgba(225, 182, 77, 0.15);
  --gloss-know: #ae6e1f; --gloss-know-bg: rgba(174, 110, 31, 0.15);
}

@media (prefers-color-scheme: dark) {
  :root:not(.theme-set) {
    --bg: #1e1b18; --fg: #c9ddd8; --fg2: #a7cca4; --accent: #f9dfa5;
    --accent2: #ae6e1f; --card: rgba(0, 0, 0, 0.25); --border: rgba(201, 221, 216, 0.1);
    --nav-bg: #151311; --nav-active: rgba(255, 255, 255, 0.05); --search-bg: rgba(0, 0, 0, 0.2);
    --search-panel-bg: #1a1714; --search-panel-border: rgba(201, 221, 216, 0.18); --search-panel-active: rgba(249, 223, 165, 0.14);
    --code-bg: #110f0e; --tag: #72a9bf; --tag-fg: #1e1b18;
    --green: #a7cca4; --red: #ae6e1f; --yellow: #e1b64d;
    --gloss-ai: #c9ddd8; --gloss-ai-bg: rgba(201, 221, 216, 0.1);
    --gloss-kit: #f9dfa5; --gloss-kit-bg: rgba(249, 223, 165, 0.15);
    --gloss-exec: #e1b64d; --gloss-exec-bg: rgba(225, 182, 77, 0.15);
    --gloss-know: #ae6e1f; --gloss-know-bg: rgba(174, 110, 31, 0.15);
  }
}

/* Base reset */
* { margin: 0; padding: 0; box-sizing: border-box; }
html { background: var(--bg); }
body {
  min-height: 100vh;
  background: var(--bg);
  color: var(--fg);
  font-family: "Inter", "Avenir Next", "Segoe UI", system-ui, sans-serif;
  font-size: clamp(0.96rem, 0.12vw + 0.93rem, 1.02rem);
  font-optical-sizing: auto;
  line-height: 1.7;
  overflow-x: hidden;
}
body.mobile-menu-open { overflow: hidden; }
a { color: var(--accent2); text-decoration: none; }
a:hover { color: var(--accent2); text-decoration: underline; }
button:focus-visible,
input:focus-visible,
a:focus-visible {
  outline: 2px solid var(--accent2);
  outline-offset: 2px;
}
button {
  appearance: none;
  -webkit-appearance: none;
  background: transparent;
  color: inherit;
  border: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
  text-align: inherit;
}

.layout { display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }

/* -- Mobile ------------------------------------------------ */
.mobile-nav { display: none; position: fixed; top: 0; left: 0; right: 0; background: var(--nav-bg); border-bottom: 1px solid var(--border); padding: 0.75rem 1rem; z-index: 200; min-height: var(--mobile-nav-height); }
.hamburger { background: none; border: 1px solid var(--border); border-radius: 6px; color: var(--fg); font-size: 1.3rem; padding: 0.3rem 0.6rem; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; width: auto; }
.mobile-nav .title { font-weight: 700; color: var(--accent); margin-left: 0.75rem; font-size: 1rem; }
.sidebar-backdrop { display: none; }
.sidebar .close-btn { display: none; text-align: right; padding: 0.75rem 1rem; }
.close-btn button { background: none; border: 1px solid var(--border); border-radius: 6px; color: var(--fg); font-size: 1.2rem; padding: 0.3rem 0.6rem; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; width: auto; }

/* -- Sidebar ----------------------------------------------- */
.sidebar { background: var(--nav-bg); border-right: 1px solid var(--border); padding: 1.5rem 0; position: sticky; top: 0; height: 100vh; overflow-y: auto; display: flex; flex-direction: column; }
.sidebar-brand,
.mobile-brand {
  display: inline-flex;
  align-items: center;
  color: var(--accent);
  font-family: "Germania One", system-ui;
  font-weight: 400;
  font-style: normal;
  letter-spacing: 0.02em;
  width: auto;
}
.sidebar-brand {
  font-size: clamp(1.28rem, 0.9rem + 0.8vw, 1.45rem);
  padding: 0 1.25rem;
  margin: 0 0 1rem;
}
.brand-logo { width: 22px; height: 22px; border-radius: 4px; object-fit: contain; flex-shrink: 0; }
.mobile-nav .title { display: flex; align-items: center; gap: 0.4rem; }
.mobile-brand {
  margin-left: 0.75rem;
  font-size: 1.25rem;
}
.sidebar-brand:hover,
.mobile-brand:hover {
  color: var(--accent2);
  text-decoration: none;
}
.sidebar .search { margin: 0 1rem 1rem; position: relative; }
.sidebar input { width: 100%; padding: 0.5rem 0.75rem 0.5rem 2rem; border: 1px solid var(--border); border-radius: 6px; background: var(--search-bg); color: var(--fg); font-size: 0.85rem; }
.sidebar input:focus { outline: 2px solid var(--accent2); border-color: transparent; }
.search-icon { position: absolute; left: 0.6rem; top: 50%; transform: translateY(-50%); color: var(--fg2); font-size: 0.8rem; pointer-events: none; }
.nav-intro { margin: 0 1rem 1rem; padding: 0.8rem 0.9rem; border: 1px solid var(--border); border-radius: 8px; background: var(--search-bg); }
.nav-intro-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--accent); margin-bottom: 0.45rem; }
.nav-intro-link { display: block; width: 100%; padding: 0.25rem 0; font-size: 0.88rem; color: var(--fg2); text-align: left; }
.nav-intro-link:hover { color: var(--fg); text-decoration: underline; }
.nav-section { margin-bottom: 0.25rem; }
.nav-section-title { display: flex; width: 100%; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--fg2); padding: 0.5rem 1.25rem 0.25rem; font-weight: 600; cursor: pointer; align-items: center; justify-content: space-between; user-select: none; font-family: inherit; }
.nav-section-title:hover { color: var(--fg); }
.nav-section-title.gold { color: var(--accent); }
.nav-section-title.gold:hover { filter: brightness(1.1); }
.nav-section-title .chevron { font-size: 0.7rem; transition: transform 0.2s; }
.nav-section.collapsed .nav-section-title .chevron { transform: rotate(-90deg); }
.nav-section.collapsed .nav-items { display: none; }
.nav-items { }
.nav-item { display: block; width: 100%; padding: 0.35rem 1.25rem 0.35rem 1.5rem; font-size: 0.95rem; color: var(--fg2); cursor: pointer; border-left: 3px solid transparent; transition: all 0.15s; text-align: left; font-family: inherit; }
.nav-item:hover { background: var(--nav-active); color: var(--fg); text-decoration: none; }
.nav-item.active { background: var(--bg); color: var(--fg2); border-left: 3px solid var(--fg2); font-weight: 700; }
.nav-item.active.accent-active { color: var(--accent); border-left-color: var(--accent); }
.nav-item .emoji { margin-right: 0.4rem; }
.nav-sub-group { margin: 0; }
.nav-sub-group-title { display: block; width: 100%; padding: 0.35rem 1.25rem 0.35rem 1.5rem; font-size: 0.95rem; color: var(--fg2); cursor: pointer; border-left: 3px solid transparent; user-select: none; font-weight: 600; text-align: left; font-family: inherit; }
.nav-sub-group-title:hover { background: var(--nav-active); color: var(--fg); text-decoration: none; }
.nav-sub-group-title .emoji { margin-right: 0.4rem; }
.nav-sub-group-title .chevron { font-size: 0.65rem; transition: transform 0.2s; opacity: 0.5; margin-left: 0.3rem; }
.nav-sub-group.collapsed .nav-sub-group-title .chevron { transform: rotate(-90deg); }
.nav-sub-group.collapsed .nav-sub-items { display: none; }
.nav-sub-items { }
.nav-sub-item { display: block; width: 100%; padding: 0.3rem 1.25rem 0.3rem 2.5rem; font-size: 0.9rem; color: var(--fg2); cursor: pointer; border-left: 3px solid transparent; transition: all 0.15s; text-align: left; font-family: inherit; }
.nav-sub-item:hover { background: var(--nav-active); color: var(--fg); text-decoration: none; }
.nav-sub-item.active { background: var(--bg); color: var(--fg2); border-left: 3px solid var(--fg2); font-weight: 700; }
.nav-sub-item.active.accent-active { color: var(--accent); border-left-color: var(--accent); }
.nav-sub-item .emoji { margin-right: 0.4rem; }

@media (prefers-color-scheme: dark) {
  :root:not(.theme-set) .nav-item.active, :root:not(.theme-set) .nav-sub-item.active { background: rgba(255, 255, 255, 0.1); }
}
:root.theme-dark .nav-item.active, :root.theme-dark .nav-sub-item.active { background: rgba(255, 255, 255, 0.1); }

.sidebar-footer { padding: 1rem 1.25rem; font-size: 0.7rem; color: var(--fg2); border-top: 1px solid var(--border); margin-top: auto; text-align: center; }

/* -- Content ----------------------------------------------- */
.content { width: min(100%, var(--content-max)); max-width: none; min-width: 0; margin-inline: auto; padding: var(--content-pad-y) var(--content-pad-x) var(--content-pad-bottom); }
.breadcrumb { font-size: 0.8rem; color: var(--fg2); margin-bottom: 1.5rem; }
.breadcrumb button { display: inline; color: var(--fg2); cursor: pointer; background: none; border: none; padding: 0; font-size: inherit; font-family: inherit; width: auto; }
.breadcrumb button:hover { color: var(--accent); text-decoration: underline; }
.breadcrumb span { margin: 0 0.4rem; }
h1, h2, h3, h4 {
  text-wrap: balance;
  font-family: "Germania One", system-ui;
  font-weight: 400;
  font-style: normal;
}
h1 { font-size: clamp(1.85rem, 2vw + 1.15rem, 2.6rem); line-height: 1.06; margin-bottom: 0.5rem; letter-spacing: 0.01em; }
h2 { font-size: clamp(1.32rem, 1vw + 1rem, 1.82rem); margin: clamp(2rem, 2vw + 1.5rem, 2.5rem) 0 0.75rem; padding-bottom: 0.4rem; border-bottom: 1px solid var(--border); letter-spacing: 0.01em; }
h3 { font-size: clamp(1.04rem, 0.45vw + 0.95rem, 1.22rem); margin: clamp(1.45rem, 1vw + 1.15rem, 1.75rem) 0 0.5rem; letter-spacing: 0.01em; }
h4 { font-size: clamp(0.98rem, 0.2vw + 0.93rem, 1.05rem); margin: 1.25rem 0 0.4rem; letter-spacing: 0.01em; }
p { margin-bottom: 1rem; color: var(--fg); max-width: 68ch; text-wrap: pretty; }
.subtitle { font-size: clamp(1rem, 0.35vw + 0.95rem, 1.12rem); color: var(--fg2); margin-bottom: 2rem; max-width: 62ch; }
ul, ol { margin-bottom: 1rem; padding-left: 1.5rem; }
li { margin-bottom: 0.3rem; color: var(--fg); max-width: 66ch; }
img, svg, video { max-width: 100%; height: auto; }

@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  .mobile-nav { display: flex; align-items: center; }
  .sidebar {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: min(22rem, calc(100vw - 2.5rem));
    max-width: 100%;
    height: 100vh;
    z-index: 300;
    overflow-y: auto;
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.18);
  }
  .sidebar.open {
    display: flex;
  }
  .sidebar-backdrop.open {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 250;
    background: rgba(24, 20, 16, 0.42);
    backdrop-filter: blur(2px);
  }
  .sidebar.open .close-btn { display: block; }
  .content { width: min(100%, var(--content-max-mobile)); padding: calc(var(--mobile-nav-height) + 1rem) clamp(1rem, 3.5vw, 1.25rem) 3rem; }
  .nav-item { display: block; width: 100%; padding: 0.6rem 1.25rem 0.6rem 1.5rem; }
  .copy-btn { opacity: 1; }
  table { font-size: 0.78rem; display: block; overflow-x: auto; white-space: nowrap; }
  td, th { padding: 0.4rem 0.5rem; }
  pre { max-width: calc(100vw - 2.5rem); }
  code { overflow-wrap: anywhere; word-break: normal; }
  .card-grid { grid-template-columns: 1fr; }
  .agent-grid { grid-template-columns: 1fr !important; }
  .theme-toggle { bottom: 1rem; right: 1rem; width: 36px; height: 36px; }
}

@media (max-width: 480px) {
  :root { --mobile-nav-height: 3.5rem; }
  .mobile-nav { padding: 0.6rem 0.85rem; }
  .hamburger,
  .close-btn button { font-size: 1.05rem; padding: 0.25rem 0.55rem; }
  .mobile-brand { margin-left: 0.6rem; font-size: 1.1rem; }
  .content { width: 100%; max-width: none; padding: calc(var(--mobile-nav-height) + 0.85rem) 0.95rem 2.5rem; }
  .stage-progress {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    border-radius: 10px;
    overflow: hidden;
  }
  .stage-progress-step {
    min-width: 0;
    padding: 0.55rem 0.3rem;
    font-size: 0.62rem;
    line-height: 1.25;
    white-space: normal;
  }
  .stage-progress-step:nth-child(2n) { border-right: none; }
  .stage-progress-step:nth-child(-n+2) { border-bottom: 1px solid var(--border); }
  .card-grid,
  .agent-grid,
  .stat-grid { grid-template-columns: 1fr !important; }
  .stat-grid { gap: 0.6rem; }
  .stat-card { padding: 0.9rem; }
  table { font-size: 0.74rem; }
  th, td { padding: 0.38rem 0.45rem; }
  pre { padding: 0.85rem 0.9rem; max-width: calc(100vw - 1.9rem); }
  .gloss-legend { gap: 0.4rem; }
  .gloss-badge { font-size: 0.72rem; padding: 0.25rem 0.7rem; }
  .theme-toggle { bottom: 0.85rem; right: 0.85rem; width: 34px; height: 34px; }
}

/* -- Cards ------------------------------------------------- */
.card-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin: 1.5rem 0; }
@media (max-width: 768px) { .card-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .card-grid { grid-template-columns: 1fr; } }
.card { display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; height: 100%; background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1rem; cursor: pointer; transition: all 0.2s; text-align: center; }
.card:hover { border-color: var(--accent2); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(140,88,47,0.1); }
.card .emoji { font-size: 1.8rem; margin-bottom: 0.5rem; display: block; }
.card h4 { font-size: 0.85rem; font-weight: 600; margin-bottom: 0.3rem; color: var(--accent); font-family: "Inter", "Avenir Next", "Segoe UI", system-ui, sans-serif; font-style: normal; }
.card p { font-size: 0.75rem; color: var(--fg2); margin: 0; line-height: 1.4; display: block; }

/* -- Agent grid -------------------------------------------- */
.agent-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin: 1rem 0 1.5rem; }
@media (max-width: 1024px) { .agent-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .agent-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .agent-grid { grid-template-columns: 1fr; } }

.agent-card { background: var(--card); border: 1px solid var(--border); border-top-width: 3px; border-radius: 10px; padding: 1.25rem 1rem; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; transition: all 0.2s; height: 100%; cursor: pointer; }
.agent-card:hover { border-color: var(--accent2); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(140,88,47,0.1); }
.agent-emoji { font-size: 2rem; margin-bottom: 0.75rem; display: block; }
.agent-info { width: 100%; }
.agent-info h4 { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.4rem; color: var(--accent); font-family: "Inter", "Avenir Next", "Segoe UI", system-ui, sans-serif; font-style: normal; }
.agent-info p { font-size: 0.78rem; color: var(--fg2); margin: 0 0 0.5rem; line-height: 1.4; }
.agent-info .tag { margin-top: 0.5rem; }
.agent-tools { font-size: 0.68rem !important; color: var(--fg2); margin: 0.4rem 0 0 !important; font-family: monospace; opacity: 0.7; border-top: 1px solid var(--border); padding-top: 0.4rem; }
.tag-version { opacity: 0.6; }

/* -- Phase groups ------------------------------------------ */
.phase-group { margin-bottom: 1.25rem; }
.phase-label { display: inline-block; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; padding: 0.2rem 0.65rem; border-radius: 99px; margin-bottom: 0.6rem; }
.phase-explore { background: #dfeae6; color: #2b3044; }
.phase-plan    { background: #c9ddd8; color: #2b3044; }
.phase-build   { background: #7d4f16; color: #f5f2ea; }
.phase-validate { background: #f9dfa5; color: #1e1b18; }

@media (prefers-color-scheme: dark) {
  :root:not(.theme-set) .phase-explore { background: rgba(167, 204, 164, 0.2); color: #a7cca4; }
  :root:not(.theme-set) .phase-plan { background: rgba(114, 169, 191, 0.2); color: #72a9bf; }
  :root:not(.theme-set) .phase-build { background: rgba(174, 110, 31, 0.2); color: #ae6e1f; }
  :root:not(.theme-set) .phase-validate { background: rgba(249, 223, 165, 0.2); color: #f9dfa5; }
}
:root.theme-dark .phase-explore { background: rgba(167, 204, 164, 0.2); color: #a7cca4; }
:root.theme-dark .phase-plan { background: rgba(114, 169, 191, 0.2); color: #72a9bf; }
:root.theme-dark .phase-build { background: rgba(174, 110, 31, 0.2); color: #ae6e1f; }
:root.theme-dark .phase-validate { background: rgba(249, 223, 165, 0.2); color: #f9dfa5; }

/* -- Tags -------------------------------------------------- */
.tag { display: inline-block; background: var(--tag); color: var(--tag-fg); font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 99px; margin-right: 0.3rem; font-weight: 500; }

/* -- Stage badges ------------------------------------------ */
.stage-badge { display: inline-block; font-size: 0.6rem; font-weight: 700; width: 1.2rem; height: 1.2rem; line-height: 1.2rem; text-align: center; border-radius: 50%; margin-right: 0.35rem; vertical-align: middle; flex-shrink: 0; }
.stage-1 { background: #382816; color: #c9ddd8; }
.stage-2 { background: #72a9bf; color: #1e1b18; }
.stage-3 { background: #ae6e1f; color: #1e1b18; }
.stage-4 { background: #e1b64d; color: #382816; }
.stage-optional { display: inline-block; font-size: 0.58rem; font-weight: 500; color: var(--fg2); margin-left: 0.2rem; opacity: 0.7; vertical-align: middle; }

/* -- Stage progress bar ------------------------------------ */
.stage-progress { display: flex; gap: 0; margin: 0 0 2rem; border-radius: 8px; overflow: hidden; border: 1px solid var(--border); }
.stage-progress-step { display: flex; align-items: center; justify-content: center; flex: 1; padding: 0.5rem 0.25rem; text-align: center; font-size: 0.68rem; font-weight: 600; color: var(--fg2); background: var(--card); border-right: 1px solid var(--border); cursor: pointer; transition: all 0.15s; text-transform: uppercase; letter-spacing: 0.04em; border-top: none; border-bottom: none; border-left: none; border-radius: 0; width: auto; }
.stage-progress-step:last-child { border-right: none; }
.stage-progress-step:hover { background: var(--nav-active); color: var(--fg); }
.stage-progress-step.active { color: white !important; }
.stage-progress-step.stage-1.active { background: #382816; }
.stage-progress-step.stage-2.active { background: #72a9bf; color: #1e1b18 !important; }
.stage-progress-step.stage-3.active { background: #ae6e1f; }
.stage-progress-step.stage-4.active { background: #e1b64d; color: #382816 !important; }

/* -- Tables ------------------------------------------------ */
table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.88rem; }
th { background: var(--card); color: var(--accent); text-align: left; padding: 0.6rem 0.75rem; border: 1px solid var(--border); font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }
td { padding: 0.5rem 0.75rem; border: 1px solid var(--border); }
tr:nth-child(even) td { background: var(--card); }
.cli-table td:first-child { white-space: nowrap; width: 1%; }

/* -- Man Page Styles --------------------------------------- */
.man-section { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin: 2rem 0 0.75rem; padding: 0.2rem 0.6rem; color: var(--accent); background: var(--card); border: 1px solid var(--border); border-radius: 4px; display: inline-block; }

/* -- CLI table enhancements -------------------------------- */
.cli-table tr:hover td { background: var(--nav-active); }
.cli-table tr:nth-child(even):hover td { background: var(--nav-active); }
.cli-table td:first-child code { color: var(--accent); font-weight: 600; background: var(--card); border: 1px solid var(--border); }
.cli-table td:first-child code.copyable:hover { background: var(--accent); color: #fff; border-color: var(--accent); }

/* -- Code -------------------------------------------------- */
code { background: var(--code-bg); padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.85em; font-family: 'JetBrains Mono', 'Fira Code', monospace; }
pre { background: var(--code-bg); padding: 1rem 1.25rem; border-radius: 8px; overflow-x: auto; border: 1px solid var(--border); margin: 1rem 0; line-height: 1.5; }
pre code { background: none; padding: 0; }

/* -- Rules listing ----------------------------------------- */
.rule-list { margin: 0.5rem 0 1.5rem; }
.rule-item { padding: 0.3rem 0; font-size: 0.88rem; }
.rule-item code { font-weight: 600; }

/* -- Resource links (GitHub source) ------------------------ */
a.resource-link { text-decoration: none; color: inherit; display: block; width: 100%; height: 100%; }
a.resource-link:hover { color: var(--accent); }
a.resource-link:hover code { color: var(--accent); }
.agent-grid a.resource-link { display: block; }
.rule-item a.resource-link { display: block; transition: color 0.15s; }
.rule-item a.resource-link:hover { color: var(--accent); }

/* -- Stat cards -------------------------------------------- */
.stat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.75rem; margin: 1.5rem 0; }
.stat-card { display: block; width: 100%; background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1rem; text-align: center; cursor: pointer; transition: all 0.2s; }
.stat-card:hover { border-color: var(--accent2); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(140,88,47,0.1); }
.stat-card .number { font-size: 2rem; font-weight: 800; color: var(--accent); pointer-events: none; }
.stat-card .label { font-size: 0.78rem; color: var(--fg2); margin-top: 0.2rem; pointer-events: none; }

/* -- Sections ---------------------------------------------- */
.section { display: none; }
.section.active { display: block; }

/* -- Copy button ------------------------------------------- */
.copy-wrap { position: relative; }
.copy-btn { position: absolute; top: 0.5rem; right: 0.5rem; background: var(--border); border: none; color: var(--fg2); font-size: 0.75rem; padding: 0.25rem 0.5rem; border-radius: 4px; cursor: pointer; opacity: 0; transition: opacity 0.15s; width: auto; display: inline-flex; align-items: center; justify-content: center; }
.copy-wrap:hover .copy-btn { opacity: 1; }
.copy-btn.copied { background: var(--green); color: #fff; }

/* -- Copyable inline code ---------------------------------- */
code.copyable { cursor: pointer; position: relative; transition: background 0.15s; }
code.copyable:hover { background: var(--accent); color: #fff; }
code.copyable::after { content: '\\1F4CB'; font-size: 0.65em; margin-left: 0.3em; opacity: 0.5; }
code.copyable:hover::after { opacity: 1; }
code.copyable.copied { background: var(--green); color: #fff; }
code.copyable.copied::after { content: '\\2713'; opacity: 1; }

/* -- Search highlight -------------------------------------- */
mark { background: var(--tag); color: var(--tag-fg); padding: 0.1rem 0.2rem; border-radius: 3px; }

/* -- Theme toggle ------------------------------------------ */
.theme-toggle { position: fixed; bottom: 1.5rem; right: 1.5rem; width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--border); background: var(--card); cursor: pointer; font-size: 1.1rem; z-index: 100; padding: 0; display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 10px 24px rgba(66, 70, 97, 0.16); }

/* -- Search results overlay -------------------------------- */
.search-results { display: none; position: absolute; top: 100%; left: 0; right: 0; background: var(--search-panel-bg); border: 1px solid var(--search-panel-border); border-radius: 10px; margin-top: 0.35rem; max-height: 400px; overflow-y: auto; z-index: 50; box-shadow: 0 14px 32px rgba(0,0,0,0.18); backdrop-filter: blur(10px); }
.search-results.visible { display: block; }
.search-result-item { padding: 0.6rem 0.75rem; cursor: pointer; border-bottom: 1px solid var(--border); font-size: 0.82rem; width: 100%; text-align: left; background: none; border-top: none; border-left: none; border-right: none; }
.search-result-item:last-child { border-bottom: none; }
.search-result-item:hover { background: var(--search-panel-active); }
.search-result-item.selected { background: var(--search-panel-active); }
.search-result-item:focus-visible { background: var(--search-panel-active); }
.search-result-item .result-section { font-size: 0.7rem; color: var(--fg2); margin-bottom: 0.15rem; }
.search-result-item .result-title { font-weight: 600; color: var(--fg); }
.search-result-item .result-snippet { font-size: 0.75rem; color: var(--fg2); margin-top: 0.15rem; }
.search-result-item mark { font-size: inherit; }
.no-results { padding: 0.75rem; color: var(--fg2); font-size: 0.82rem; text-align: center; }

/* -- DAG scenario table ------------------------------------ */
.dag-table { margin: 1.5rem 0; }
.dag-table td.num { text-align: right; font-variant-numeric: tabular-nums; }
.highlight-row td { background: var(--nav-active) !important; font-weight: 600; }

/* -- Glossary -------------------------------------------- */
.gloss-legend { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.75rem; }
.gloss-badge { display: inline-flex; align-items: center; gap: 0.45rem; padding: 0.3rem 0.85rem; border-radius: 9999px; font-size: 0.78rem; font-weight: 600; border: 1px solid currentColor; text-decoration: none; transition: filter 0.15s; width: auto; background: none; font-family: inherit; }
.gloss-badge:hover { filter: brightness(0.88); }
.gloss-section-heading { margin: 2.25rem 0 0.6rem; font-size: 1rem; font-weight: 700; scroll-margin-top: 1rem; }
.gloss-badge::before { content: ''; width: 8px; height: 8px; border-radius: 50%; background: currentColor; flex-shrink: 0; }
.gloss-badge.gloss-ai { color: var(--gloss-ai); background: var(--gloss-ai-bg); }
.gloss-badge.gloss-kit { color: var(--gloss-kit); background: var(--gloss-kit-bg); }
.gloss-badge.gloss-exec { color: var(--gloss-exec); background: var(--gloss-exec-bg); }
.gloss-badge.gloss-know { color: var(--gloss-know); background: var(--gloss-know-bg); }
.gloss-cat-header td { background: var(--card); font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.09em; padding: 0.55rem 1rem !important; }
.gloss-cat-header.gloss-ai td { color: var(--gloss-ai); border-left: 3px solid var(--gloss-ai); }
.gloss-cat-header.gloss-kit td { color: var(--gloss-kit); border-left: 3px solid var(--gloss-kit); }
.gloss-cat-header.gloss-exec td { color: var(--gloss-exec); border-left: 3px solid var(--gloss-exec); }
.gloss-cat-header.gloss-know td { color: var(--gloss-know); border-left: 3px solid var(--gloss-know); }
.gloss-row { transition: background 0.1s; }
.gloss-row.gloss-ai { background: var(--gloss-ai-bg); } .gloss-row.gloss-ai td:first-child { border-left: 3px solid var(--gloss-ai); }
.gloss-row.gloss-kit { background: var(--gloss-kit-bg); } .gloss-row.gloss-kit td:first-child { border-left: 3px solid var(--gloss-kit); }
.gloss-row.gloss-exec { background: var(--gloss-exec-bg); } .gloss-row.gloss-exec td:first-child { border-left: 3px solid var(--gloss-exec); }
.gloss-row.gloss-know { background: var(--gloss-know-bg); } .gloss-row.gloss-know td:first-child { border-left: 3px solid var(--gloss-know); }
.gloss-row:hover { filter: brightness(0.96); }
</style>
"""
