from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

generate = importlib.import_module("cli.site").generate
get_javascript = importlib.import_module("cli.site.javascript").get_javascript
get_styles = importlib.import_module("cli.site.styles").get_styles


def _generate_html(tmp_path: Path) -> tuple[Path, str]:
    site_dir = tmp_path / "site"
    index_path = generate(root_dir=ROOT, site_dir=site_dir)
    return index_path, index_path.read_text(encoding="utf-8")


def _run_node_harness(args: list[str], script: str) -> dict[str, object] | list[dict[str, object]]:
    result = subprocess.run(
        ["node", "-e", script, *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_all_data_section_targets_resolve_to_sections(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)
    markup = html.split("<script>", 1)[0]

    section_ids = set()
    for tag in re.findall(r"<section\b[^>]*>", markup):
        class_match = re.search(r'\bclass="([^"]+)"', tag)
        id_match = re.search(r'\bid="([^"]+)"', tag)
        if not class_match or not id_match:
            continue
        if "section" in class_match.group(1).split():
            section_ids.add(id_match.group(1))
    targets = set(re.findall(r'data-section="([^"]+)"', markup))

    assert targets <= section_ids


def test_manual_pages_use_man_page_structure_with_mastery_stage_progress(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    manual_section_ids = {
        "rune-cheatsheet",
        "rune-man-1",
        "rune-cli-top",
        "rune-cli-profile",
        "rune-cli-resource",
        "rune-cli-system",
        "rune-cli-mcp",
        "rune-man-env",
        "rune-man-profiles",
        "rune-man-tools",
    }

    for section_id in manual_section_ids:
        match = re.search(
            rf'<section class="section" id="{section_id}">(.*?)</section>',
            html,
            re.DOTALL,
        )
        assert match is not None, section_id
        section_html = match.group(1)
        assert 'class="stage-progress"' in section_html
        assert 'data-current-stage="4"' in section_html

    assert "RUNE(1)</button>" in html
    assert "RUNE-QUICKREF(7)" in html
    assert "RUNE(1) &mdash; Manual Page" not in html
    assert "COMMAND GROUPS" in html
    assert "rune mcp status" in html
    assert "Setup &amp; Reset" in html
    assert "System Checks" in html
    assert "rune reset [--global|--project]" in html
    assert "rune reset --project" in html
    assert "<tr><th>Task</th><th>Command</th><th>Purpose</th></tr>" not in html
    assert "WHAT IS A PROFILE?" not in html
    assert "REGISTRY SHAPE" not in html
    assert "RUNE(1) &mdash; MCP Commands" in html
    assert "RUNE(1) &mdash; Profiles Commands" not in html
    assert "RUNE(1) &mdash; Profile Commands" in html
    assert "rune mcp &lt;subcommand&gt; [name]" in html
    assert "&amp;#x1F527;" not in html
    assert "&amp;#x2699;&amp;#xFE0F;" not in html
    assert html.index('data-section="rune-cheatsheet"') < html.index('data-section="rune-man-1"')
    assert '<button data-section="rune-cheatsheet">Manual Pages</button>' in html


def test_sidebar_emphasizes_guided_start(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    assert "Start Here" in html
    assert "<h1>Start Here</h1>" in html
    assert 'class="sidebar-brand" data-section="home"' in html
    assert 'class="title mobile-brand" data-section="home"' in html
    assert 'class="nav-intro"' not in html
    assert '<button class="nav-item active" data-section="home"><span class="emoji" aria-hidden="true">&#x1F3E0;</span> Start Here</button>' in html


def test_hooks_and_reference_lanes_expose_overviews_and_link_back_to_them(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    assert 'data-section="hooks-overview"' in html
    assert 'data-section="reference-overview"' in html
    assert '<section class="section" id="hooks-overview">' in html
    assert '<section class="section" id="reference-overview">' in html
    assert '<button data-section="hooks-overview">Hooks</button>' in html
    assert '<button data-section="reference-overview">Reference</button>' in html
    assert "References &amp; Inspirations" not in html


def test_hooks_pages_render_breadcrumb_paths(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    expected_breadcrumbs = [
        '<nav class="breadcrumb" aria-label="Breadcrumb"><button data-section="home">Home</button> <span>&#x203A;</span> Hooks</nav>',
        '<nav class="breadcrumb" aria-label="Breadcrumb"><button data-section="home">Home</button> <span>&#x203A;</span> <button data-section="hooks-overview">Hooks</button> <span>&#x203A;</span> Safety Check</nav>',
        '<nav class="breadcrumb" aria-label="Breadcrumb"><button data-section="home">Home</button> <span>&#x203A;</span> <button data-section="hooks-overview">Hooks</button> <span>&#x203A;</span> Auto-Lint</nav>',
        '<nav class="breadcrumb" aria-label="Breadcrumb"><button data-section="home">Home</button> <span>&#x203A;</span> <button data-section="hooks-overview">Hooks</button> <span>&#x203A;</span> Stage Complete</nav>',
        '<nav class="breadcrumb" aria-label="Breadcrumb"><button data-section="home">Home</button> <span>&#x203A;</span> <button data-section="hooks-overview">Hooks</button> <span>&#x203A;</span> Context Awareness</nav>',
        '<nav class="breadcrumb" aria-label="Breadcrumb"><button data-section="home">Home</button> <span>&#x203A;</span> <button data-section="hooks-overview">Hooks</button> <span>&#x203A;</span> Done Criteria</nav>',
        '<nav class="breadcrumb" aria-label="Breadcrumb"><button data-section="home">Home</button> <span>&#x203A;</span> <button data-section="hooks-overview">Hooks</button> <span>&#x203A;</span> Plan Mode Rules</nav>',
        '<nav class="breadcrumb" aria-label="Breadcrumb"><button data-section="home">Home</button> <span>&#x203A;</span> <button data-section="hooks-overview">Hooks</button> <span>&#x203A;</span> Session Discipline</nav>',
    ]

    for breadcrumb in expected_breadcrumbs:
        assert breadcrumb in html


def test_hooks_and_operating_guides_use_mastery_stage_progress(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    stage_4_sections = {
        "hooks-overview",
        "hook-safety-check",
        "hook-auto-lint",
        "hook-stage-complete",
        "hook-context-awareness",
        "hook-done-criteria",
        "hook-plan-mode-rules",
        "hook-session-discipline",
        "operating-guides",
        "knowledge-pipeline",
        "prompting",
        "token-economics",
        "markdown-management",
        "project-management",
    }

    for section_id in stage_4_sections:
        match = re.search(
            rf'<section class="section" id="{section_id}">(.*?)</section>',
            html,
            re.DOTALL,
        )
        assert match is not None, section_id
        section_html = match.group(1)
        assert 'class="stage-progress"' in section_html
        assert 'data-current-stage="4"' in section_html


def test_site_generator_emits_valid_search_result_markup() -> None:
    javascript = get_javascript()
    styles = get_styles()

    assert '+ \'</button>\';' in javascript
    assert '+ </button>\';' not in javascript
    assert "searchInput.addEventListener('keydown'" in javascript
    assert "activateSearchSelection();" in javascript
    assert ".search-result-item.selected" in styles
    assert "--search-panel-bg:" in styles
    assert "background: var(--search-panel-bg);" in styles


def test_site_generator_uses_current_repo_urls(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    assert "https://github.com/kvasir-ai/rune.git" in html
    assert "https://github.com/kvasir-ai/rune/blob/main" in html


def test_site_generator_uses_decisions_not_adrs(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    assert "docs/decisions/" in html
    assert "docs/adrs/" not in html


def test_site_generator_includes_general_skill_contract(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    assert "phase-label phase-general" in html
    assert "/skill-contract" in html


def test_site_generator_uses_operating_guides_labels(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    assert 'id="operating-guides"' in html
    assert "Operating Guides" in html
    assert "Knowledge Distance" in html
    assert "Documentation Structure" in html
    assert "Planning for DAGs" in html
    assert "Deep Dives" not in html
    assert "Prompting &amp; Knowledge Distance" not in html
    assert "nav-operating-guides" in html
    assert "nav-deep-dives" not in html


def test_core_concept_phase_pages_drop_stage_chrome_and_legacy_agent_terms(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    phase_ids = {
        "phase-1-explore",
        "phase-2-plan",
        "phase-3-build",
        "phase-4-validate",
    }

    sections: dict[str, str] = {}
    for section_id in phase_ids:
        match = re.search(
            rf'<section class="section" id="{section_id}">(.*?)</section>',
            html,
            re.DOTALL,
        )
        assert match is not None, section_id
        sections[section_id] = match.group(1)
        assert 'class="stage-progress"' not in sections[section_id]

    combined = "\n".join(sections.values())
    assert "DEVELOPER" not in combined
    assert "SECURITY" not in combined
    assert "TESTER" not in combined
    assert "architect agent" not in combined
    assert "agent: developer" not in combined
    assert "agent: security" not in combined
    assert "Knowledge Manager" in combined
    assert "technical-writer" in combined
    assert "APPROVED WITH WARNINGS" in combined


def test_agency_section_splits_catalog_from_authoring(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    agents_match = re.search(
        r'<section class="section" id="agents">(.*?)</section>',
        html,
        re.DOTALL,
    )
    onboarding_match = re.search(
        r'<section class="section" id="agent-onboarding">(.*?)</section>',
        html,
        re.DOTALL,
    )

    assert agents_match is not None
    assert onboarding_match is not None

    agents_html = agents_match.group(1)
    onboarding_html = onboarding_match.group(1)

    assert "Frontmatter fields" not in agents_html
    assert "How to read the catalog" in agents_html
    assert "Use the Rune Agency pages this way" in agents_html
    assert "data-section=\"agent-onboarding\"" in agents_html
    assert "All frontmatter fields" in onboarding_html
    assert "data-section=\"agents\"" in onboarding_html
    assert html.index('id="agents"') < html.index('id="skills"')
    assert html.index('id="skills"') < html.index('id="rules-catalog"')
    assert html.index('id="rules-catalog"') < html.index('id="agent-onboarding"')


def test_getting_started_section_is_more_actionable_and_uses_live_skill_names(
    tmp_path: Path,
) -> None:
    _, html = _generate_html(tmp_path)

    home_match = re.search(
        r'<section class="section active" id="home">(.*?)</section>',
        html,
        re.DOTALL,
    )
    quick_start_match = re.search(
        r'<section class="section" id="quick-start">(.*?)</section>',
        html,
        re.DOTALL,
    )
    talk_match = re.search(
        r'<section class="section" id="talk">(.*?)</section>',
        html,
        re.DOTALL,
    )

    assert home_match is not None
    assert quick_start_match is not None
    assert talk_match is not None

    home_html = home_match.group(1)
    quick_start_html = quick_start_match.group(1)
    talk_html = talk_match.group(1)

    assert "<h1>Start Here</h1>" in home_html
    assert "Your first three stops" in home_html
    assert "Use the Getting Started pages this way" in home_html
    assert "After the basics" in home_html
    assert "Knowledge Pipeline" not in home_html

    assert "Choose your install scope" in quick_start_html
    assert "Pick one path. You do not need both." in quick_start_html
    assert "Verify the deployment" in quick_start_html
    assert "Machine-wide install" in quick_start_html
    assert "Project-local install" in quick_start_html
    assert "First five minutes" in quick_start_html
    assert "What setup changed" in quick_start_html
    assert "rune reset --global" in quick_start_html
    assert "rune reset --project" in quick_start_html

    assert "A good first conversation" in talk_html
    assert "You do not need perfect phrasing." in talk_html
    assert "Use both interaction styles" in talk_html
    assert "/km-audit" in talk_html
    assert "/km-doc-cleanup" not in talk_html
    assert "Keep the team current" in talk_html
    assert "Next steps" in talk_html


def test_site_generator_includes_hook_runtime_contract_and_hook_bundle_docs(tmp_path: Path) -> None:
    _, html = _generate_html(tmp_path)

    assert "hook-runtime-contract" in html
    assert "src/rune-agency/hooks-meta.yaml" in html
    assert "active project root" in html
    assert "No active workflow." in html
    assert 'Suggested next owner: judge for "RUNE-123".' in html
    assert '"status": "completed"' in html


def test_site_generator_wires_google_fonts_only(tmp_path: Path) -> None:
    site_dir = tmp_path / "site"
    index_path = generate(root_dir=ROOT, site_dir=site_dir)
    html = index_path.read_text(encoding="utf-8")
    styles = get_styles()

    assert "https://fonts.googleapis.com/css2?family=Germania+One&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" in html
    assert 'href="fonts/stylesheet.css"' not in html
    assert not (site_dir / "fonts").exists()
    assert 'src="assets/rune-docs.png"' in html
    assert (site_dir / "assets" / "rune-docs.png").exists()
    assert (site_dir / "assets" / "rune-banner.jpg").exists()
    assert not (site_dir / "docs").exists()
    assert 'font-family: "Inter", "Avenir Next", "Segoe UI", system-ui, sans-serif;' in styles
    assert 'font-family: "Germania One", system-ui;' in styles
    assert '.card h4 { font-size: 0.85rem; font-weight: 600; margin-bottom: 0.3rem; color: var(--accent); font-family: "Inter", "Avenir Next", "Segoe UI", system-ui, sans-serif; font-style: normal; }' in styles
    assert '.agent-info h4 { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.4rem; color: var(--accent); font-family: "Inter", "Avenir Next", "Segoe UI", system-ui, sans-serif; font-style: normal; }' in styles


def test_theme_styles_support_manual_override() -> None:
    styles = get_styles()
    javascript = get_javascript()

    assert ":root.theme-dark .phase-explore" in styles
    assert ":root:not(.theme-set) .phase-explore" in styles
    assert "themeRoot.classList.toggle('theme-set', hasStoredTheme);" in javascript
    assert "themeRoot.classList.toggle('theme-dark', hasStoredTheme && isDark);" in javascript
    assert "themeRoot.classList.toggle('theme-light', hasStoredTheme && !isDark);" in javascript


def test_theme_toggle_switches_in_both_directions(tmp_path: Path) -> None:
    index_path, _ = _generate_html(tmp_path)

    harness = r"""
const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync(process.argv[1], 'utf8');
const sysDark = process.argv[2] === 'true';
const stored = process.argv[3] === 'null' ? null : process.argv[3];
const match = html.match(/<script>([\s\S]*)<\/script>/);
if (!match) throw new Error('script not found');
const script = match[1];

function mkList() {
  const classes = new Set();
  return {
    add(name) { classes.add(name); },
    remove(name) { classes.delete(name); },
    toggle(name, force) {
      if (force === undefined) {
        if (classes.has(name)) {
          classes.delete(name);
          return false;
        }
        classes.add(name);
        return true;
      }
      if (force) classes.add(name);
      else classes.delete(name);
      return force;
    },
    contains(name) { return classes.has(name); },
    value() { return Array.from(classes).sort().join(' '); },
  };
}

const listeners = {};
const nodes = {
  sidebar: { classList: mkList(), querySelector: () => null },
  content: { scrollTop: 0 },
  'menu-open': { addEventListener: (_, cb) => { listeners.menuOpen = cb; } },
  'menu-close': { addEventListener: (_, cb) => { listeners.menuClose = cb; } },
  search: { addEventListener: () => {}, value: '' },
  'search-results': { classList: mkList(), innerHTML: '', querySelectorAll: () => [] },
  'theme-toggle': {
    textContent: '',
    attrs: {},
    classList: mkList(),
    addEventListener: (_, cb) => { listeners.themeClick = cb; },
    setAttribute: (name, value) => { nodes['theme-toggle'].attrs[name] = value; },
  },
};

const document = {
  body: { classList: mkList() },
  documentElement: { classList: mkList(), style: {} },
  getElementById(id) { return nodes[id] || null; },
  querySelectorAll() { return []; },
  querySelector() { return null; },
  addEventListener() {},
  createElement() {
    return {
      className: '',
      textContent: '',
      setAttribute() {},
      addEventListener() {},
      appendChild() {},
      classList: mkList(),
    };
  },
};

const storage = new Map(stored === null ? [] : [['theme', stored]]);
const context = {
  document,
  window: {
    matchMedia: () => ({ matches: sysDark, addEventListener: () => {} }),
    addEventListener: () => {},
    scrollTo: () => {},
  },
  history: { pushState: () => {} },
  location: { hash: '', pathname: '/index.html' },
  localStorage: {
    getItem(key) { return storage.has(key) ? storage.get(key) : null; },
    setItem(key, value) { storage.set(key, String(value)); },
  },
  navigator: { clipboard: { writeText: () => Promise.resolve() } },
  console,
  setTimeout: (cb) => cb(),
  clearTimeout: () => {},
};

vm.createContext(context);
vm.runInContext(script, context);

function snapshot(label) {
  return {
    label,
    root: document.documentElement.classList.value(),
    scheme: document.documentElement.style.colorScheme || '',
    stored: context.localStorage.getItem('theme'),
    icon: nodes['theme-toggle'].textContent,
    title: nodes['theme-toggle'].attrs.title,
  };
}

const states = [snapshot('initial')];
listeners.themeClick();
states.push(snapshot('after1'));
listeners.themeClick();
states.push(snapshot('after2'));
process.stdout.write(JSON.stringify(states));
"""

    dark_states = _run_node_harness([str(index_path), "true", "null"], harness)
    assert dark_states[0]["root"] == ""
    assert dark_states[0]["scheme"] == "dark"
    assert dark_states[0]["stored"] is None
    assert dark_states[1]["root"] == "theme-light theme-set"
    assert dark_states[1]["scheme"] == "light"
    assert dark_states[1]["stored"] == "light"
    assert dark_states[2]["root"] == "theme-dark theme-set"
    assert dark_states[2]["scheme"] == "dark"
    assert dark_states[2]["stored"] == "dark"

    light_states = _run_node_harness([str(index_path), "false", "null"], harness)
    assert light_states[0]["root"] == ""
    assert light_states[0]["scheme"] == "light"
    assert light_states[0]["stored"] is None
    assert light_states[1]["root"] == "theme-dark theme-set"
    assert light_states[1]["scheme"] == "dark"
    assert light_states[1]["stored"] == "dark"
    assert light_states[2]["root"] == "theme-light theme-set"
    assert light_states[2]["scheme"] == "light"
    assert light_states[2]["stored"] == "light"


def test_hard_refresh_with_hash_does_not_break_navigation(tmp_path: Path) -> None:
    index_path, _ = _generate_html(tmp_path)

    harness = r"""
const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync(process.argv[1], 'utf8');
const match = html.match(/<script>([\s\S]*)<\/script>/);
if (!match) throw new Error('script not found');
const script = match[1];

function mkList(init = []) {
  const classes = new Set(init);
  return {
    add(name) { classes.add(name); },
    remove(name) { classes.delete(name); },
    toggle(name, force) {
      if (force === undefined) {
        if (classes.has(name)) {
          classes.delete(name);
          return false;
        }
        classes.add(name);
        return true;
      }
      if (force) classes.add(name);
      else classes.delete(name);
      return force;
    },
    contains(name) { return classes.has(name); },
    value() { return Array.from(classes).sort().join(' '); },
  };
}

const listeners = {};
const sections = {
  home: { id: 'home', classList: mkList(['section']) },
  'quick-start': { id: 'quick-start', classList: mkList(['section']) },
  'knowledge-pipeline': { id: 'knowledge-pipeline', classList: mkList(['section']) },
  'dag-dispatch': { id: 'dag-dispatch', classList: mkList(['section']) },
};
const navLink = {
  dataset: { section: 'home' },
  classList: mkList(),
  addEventListener: (_, cb) => { listeners.navClick = cb; },
};
const themeBtn = {
  textContent: '',
  attrs: {},
  addEventListener: (_, cb) => { listeners.themeClick = cb; },
  setAttribute: (name, value) => { themeBtn.attrs[name] = value; },
};
const stageStep = {
  dataset: { stageNav: '2' },
  addEventListener: (_, cb) => { listeners.stageClick = cb; },
};
const sidebar = { classList: mkList(), querySelector: () => null };
const content = { scrollTop: 0 };

const document = {
  documentElement: { classList: mkList(), style: {} },
  body: { classList: mkList() },
  getElementById(id) {
    if (id === 'theme-toggle') return themeBtn;
    if (id === 'sidebar') return sidebar;
    if (id === 'content') return content;
    if (id === 'menu-open' || id === 'menu-close') return { addEventListener: () => {} };
    if (id === 'search') return { addEventListener: () => {}, value: '' };
    if (id === 'search-results') return { classList: mkList(), innerHTML: '', querySelectorAll: () => [] };
    return sections[id] || null;
  },
  querySelectorAll(selector) {
    if (selector === '.section') return Object.values(sections);
    if (selector === '.section[id]') {
      return Object.values(sections).map(section => ({
        ...section,
        querySelector: () => null,
        textContent: section.id,
      }));
    }
    if (selector === '[data-section]') return [navLink];
    if (selector === '[data-scroll-to]') return [];
    if (selector === '.nav-section-title[data-toggle]') return [];
    if (selector === '.nav-sub-group-title[data-subtoggle]') return [];
    if (selector === '.nav-item, .nav-sub-item') return [];
    if (selector === '.nav-section-title') return [];
    if (selector === '.nav-sub-group-title') return [];
    if (selector === 'pre') return [];
    if (selector === 'code.copyable') return [];
    if (selector === '.stage-progress-step[data-stage-nav]') return [stageStep];
    return [];
  },
  querySelector() { return null; },
  addEventListener() {},
  createElement() {
    return {
      className: '',
      textContent: '',
      setAttribute() {},
      addEventListener() {},
      appendChild() {},
      classList: mkList(),
    };
  },
};

const context = {
  document,
  window: {
    matchMedia: () => ({ matches: false, addEventListener: () => {} }),
    addEventListener: (_, cb) => { listeners.popstate = cb; },
    scrollTo: () => {},
  },
  history: { pushState: () => {} },
  location: { hash: '#quick-start', pathname: '/index.html' },
  localStorage: {
    getItem: () => null,
    setItem: () => {},
  },
  navigator: { clipboard: { writeText: () => Promise.resolve() } },
  console,
  setTimeout: (cb) => cb(),
  clearTimeout: () => {},
};

vm.createContext(context);
vm.runInContext(script, context);

process.stdout.write(JSON.stringify({
  quickStartActive: sections['quick-start'].classList.contains('active'),
  themeClickBound: typeof listeners.themeClick === 'function',
  navClickBound: typeof listeners.navClick === 'function',
  stageClickBound: typeof listeners.stageClick === 'function',
  popstateBound: typeof listeners.popstate === 'function',
}));
"""

    state = _run_node_harness([str(index_path)], harness)
    assert state["quickStartActive"] is True
    assert state["themeClickBound"] is True
    assert state["navClickBound"] is True
    assert state["stageClickBound"] is True
    assert state["popstateBound"] is True
