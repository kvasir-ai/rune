"""JavaScript for the rune documentation site."""
from __future__ import annotations


def get_javascript() -> str:
    """Return the complete JavaScript block including <script> tags."""
    return """
<script>
// -- Mobile menu --
const sidebar = document.getElementById('sidebar');
const sidebarBackdrop = document.getElementById('sidebar-backdrop');
const menuOpenButton = document.getElementById('menu-open');
const menuCloseButton = document.getElementById('menu-close');
const mobileMenuQuery = window.matchMedia('(max-width: 900px)');

function setMobileMenuOpen(isOpen) {
  if (!sidebar) return;
  const shouldOpen = mobileMenuQuery.matches && isOpen;
  sidebar.classList.toggle('open', shouldOpen);
  sidebar.setAttribute('aria-hidden', mobileMenuQuery.matches ? String(!shouldOpen) : 'false');
  menuOpenButton?.setAttribute('aria-expanded', String(shouldOpen));
  sidebarBackdrop?.classList.toggle('open', shouldOpen);
  if (sidebarBackdrop) sidebarBackdrop.hidden = !shouldOpen;
  document.body.classList.toggle('mobile-menu-open', shouldOpen);
}

menuOpenButton?.addEventListener('click', () => setMobileMenuOpen(true));
menuCloseButton?.addEventListener('click', () => setMobileMenuOpen(false));
sidebarBackdrop?.addEventListener('click', () => setMobileMenuOpen(false));
mobileMenuQuery.addEventListener?.('change', () => setMobileMenuOpen(false));
setMobileMenuOpen(false);

// -- Collapsible sidebar sections --
document.querySelectorAll('.nav-section-title[data-toggle]').forEach(title => {
  title.addEventListener('click', () => {
    const section = document.getElementById(title.dataset.toggle);
    const expanded = title.getAttribute('aria-expanded') === 'true';
    title.setAttribute('aria-expanded', !expanded);
    if (section) section.classList.toggle('collapsed');
  });
});

// -- Collapsible sub-groups (3rd level) --
document.querySelectorAll('.nav-sub-group-title[data-subtoggle]').forEach(title => {
  title.addEventListener('click', () => {
    const group = document.getElementById(title.dataset.subtoggle);
    const expanded = title.getAttribute('aria-expanded') === 'true';
    title.setAttribute('aria-expanded', !expanded);
    if (group) group.classList.toggle('collapsed');
  });
});

// -- Navigation --
function showSection(id, pushState) {
  const target = document.getElementById(id);
  if (!target) return;
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  target.classList.add('active');
  document.querySelectorAll('.nav-item, .nav-sub-item').forEach(n => n.classList.remove('active'));
  const activeNav = document.querySelector('.nav-item[data-section="' + id + '"], .nav-sub-item[data-section="' + id + '"]');
  if (activeNav) {
    activeNav.classList.add('active');
    const parentSection = activeNav.closest('.nav-section');
    if (parentSection && parentSection.classList.contains('collapsed')) {
      parentSection.classList.remove('collapsed');
      parentSection.querySelector('.nav-section-title').setAttribute('aria-expanded', 'true');
    }
    const parentSubGroup = activeNav.closest('.nav-sub-group');
    if (parentSubGroup && parentSubGroup.classList.contains('collapsed')) {
      parentSubGroup.classList.remove('collapsed');
      parentSubGroup.querySelector('.nav-sub-group-title').setAttribute('aria-expanded', 'true');
    }
  }
  document.getElementById('content').scrollTop = 0;
  window.scrollTo(0, 0);
  setMobileMenuOpen(false);
  if (pushState !== false) {
    history.pushState({ section: id }, '', id === 'home' ? location.pathname : '#' + id);
  }
  applyTheme();
}

// -- In-section scroll anchors (glossary badges) --
document.querySelectorAll('[data-scroll-to]').forEach(el => {
  el.addEventListener('click', e => {
    e.preventDefault();
    const target = document.getElementById(el.dataset.scrollTo);
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

document.querySelectorAll('[data-section]').forEach(el => {
  if (el.classList.contains('nav-section-title')) return;
  el.addEventListener('click', e => {
    if (e.target.closest('code.copyable')) return;
    if (e.target.closest('a')) return;
    e.preventDefault();
    showSection(el.dataset.section);
  });
});

// -- Search --
const searchInput = document.getElementById('search');
const searchResults = document.getElementById('search-results');
let searchSelectionIndex = -1;

const searchIndex = [];
document.querySelectorAll('.section[id]').forEach(section => {
  const id = section.id;
  const title = section.querySelector('h1')?.textContent || id;
  const text = section.textContent || '';
  const bc = section.querySelector('.breadcrumb');
  const path = bc ? bc.textContent.replace(/\\s*>\\s*/g, ' > ').trim() : '';
  searchIndex.push({ id, title, text: text.toLowerCase(), path });
});

function getSnippet(text, query, contextLen) {
  contextLen = contextLen || 60;
  const lower = text.toLowerCase();
  const idx = lower.indexOf(query.toLowerCase());
  if (idx === -1) return '';
  const start = Math.max(0, idx - contextLen);
  const end = Math.min(text.length, idx + query.length + contextLen);
  let snippet = (start > 0 ? '...' : '') + text.slice(start, end).trim() + (end < text.length ? '...' : '');
  const re = new RegExp('(' + query.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi');
  snippet = snippet.replace(re, '<mark>$1</mark>');
  return snippet;
}

function getSearchResultItems() {
  return Array.from(searchResults.querySelectorAll('.search-result-item'));
}

function updateSearchSelection(index) {
  const items = getSearchResultItems();
  if (!items.length) {
    searchSelectionIndex = -1;
    return;
  }
  searchSelectionIndex = Math.max(0, Math.min(index, items.length - 1));
  items.forEach((item, itemIndex) => {
    const isSelected = itemIndex === searchSelectionIndex;
    item.classList.toggle('selected', isSelected);
    item.setAttribute('aria-selected', String(isSelected));
    if (isSelected) item.scrollIntoView?.({ block: 'nearest' });
  });
}

function clearSearchResults() {
  searchSelectionIndex = -1;
  searchResults.classList.remove('visible');
  searchResults.innerHTML = '';
}

function activateSearchSelection() {
  const items = getSearchResultItems();
  const item = items[searchSelectionIndex] || items[0];
  if (!item) return;
  showSection(item.dataset.section);
  clearSearchResults();
  searchInput.value = '';
}

searchInput.addEventListener('input', () => {
  const q = searchInput.value.trim();
  if (q.length < 2) {
    clearSearchResults();
    return;
  }

  const qLower = q.toLowerCase();
  const matches = searchIndex
    .filter(s => s.text.includes(qLower) || s.title.toLowerCase().includes(qLower))
    .slice(0, 12);

  if (matches.length === 0) {
    searchSelectionIndex = -1;
    searchResults.innerHTML = '<div class="no-results">No results for "' + q.replace(/</g, '&lt;') + '"</div>';
    searchResults.classList.add('visible');
    return;
  }

  searchResults.innerHTML = matches.map(m => {
    const section = document.getElementById(m.id);
    const rawText = section ? section.textContent : '';
    const snippet = getSnippet(rawText, q);
    const titleHighlighted = m.title.replace(
      new RegExp('(' + q.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi'),
      '<mark>$1</mark>'
    );
    return '<button class="search-result-item" data-section="' + m.id + '">'
      + (m.path ? '<div class="result-section">' + m.path.replace(/</g, '&lt;') + '</div>' : '')
      + '<div class="result-title">' + titleHighlighted + '</div>'
      + (snippet ? '<div class="result-snippet">' + snippet + '</div>' : '')
      + '</button>';
  }).join('');

  searchResults.classList.add('visible');

  searchResults.querySelectorAll('.search-result-item').forEach(item => {
    item.addEventListener('click', () => {
      searchSelectionIndex = getSearchResultItems().indexOf(item);
      activateSearchSelection();
    });
  });

  updateSearchSelection(0);
});

searchInput.addEventListener('keydown', (e) => {
  const items = getSearchResultItems();
  if (!searchResults.classList.contains('visible') || !items.length) {
    if (e.key === 'Escape') {
      clearSearchResults();
      searchInput.value = '';
    }
    return;
  }

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    updateSearchSelection(searchSelectionIndex + 1);
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    updateSearchSelection(searchSelectionIndex - 1);
  } else if (e.key === 'Enter') {
    e.preventDefault();
    activateSearchSelection();
  } else if (e.key === 'Escape') {
    e.preventDefault();
    clearSearchResults();
    searchInput.value = '';
  }
});

document.addEventListener('click', (e) => {
  if (!e.target.closest('.search')) {
    clearSearchResults();
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    setMobileMenuOpen(false);
  }
});

// -- Theme Toggle --
const themeBtn = document.getElementById('theme-toggle');
const themeRoot = document.documentElement;
const sysDark = window.matchMedia('(prefers-color-scheme: dark)');

function getStoredTheme() {
  const stored = localStorage.getItem('theme');
  return stored === 'dark' || stored === 'light' ? stored : null;
}

function getEffectiveTheme() {
  const stored = getStoredTheme();
  return stored || (sysDark.matches ? 'dark' : 'light');
}

function applyTheme() {
  const theme = getEffectiveTheme();
  const hasStoredTheme = getStoredTheme() !== null;
  const isDark = theme === 'dark';

  themeRoot.classList.toggle('theme-set', hasStoredTheme);
  themeRoot.classList.toggle('theme-dark', hasStoredTheme && isDark);
  themeRoot.classList.toggle('theme-light', hasStoredTheme && !isDark);
  themeRoot.style.colorScheme = isDark ? 'dark' : 'light';

  if (themeBtn) {
    const nextTheme = isDark ? 'light' : 'dark';
    themeBtn.textContent = isDark ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
    themeBtn.setAttribute('aria-label', 'Switch to ' + nextTheme + ' theme');
    themeBtn.setAttribute('title', 'Switch to ' + nextTheme + ' theme');
    themeBtn.setAttribute('aria-pressed', String(isDark));
  }

  // Update dynamic nav colors
  const darkCol = { std: '#a7cca4', acc: '#f9dfa5', bg: 'rgba(255, 255, 255, 0.1)' };
  const lightCol = { std: '#424661', acc: '#7d4f16', bg: '#f5f2ea' };
  const c = isDark ? darkCol : lightCol;

  document.querySelectorAll('.nav-section-title').forEach(t => {
    t.style.color = t.classList.contains('gold') ? c.acc : c.std;
  });

  document.querySelectorAll('.nav-item, .nav-sub-item').forEach(i => {
    const isAccSec = i.closest('.nav-section')?.querySelector('.nav-section-title')?.classList.contains('gold');
    if (i.classList.contains('active')) {
      i.style.color = isAccSec ? c.acc : c.std;
      i.style.background = c.bg;
      i.style.borderLeftColor = isAccSec ? c.acc : c.std;
      i.classList.toggle('accent-active', isAccSec);
    } else {
      i.style.color = c.std;
      i.style.background = '';
      i.style.borderLeftColor = 'transparent';
      i.classList.remove('accent-active');
    }
  });

  document.querySelectorAll('.nav-sub-group-title').forEach(s => {
    s.style.color = c.std;
  });
}
applyTheme();
themeBtn?.addEventListener('click', () => {
  const nextTheme = getEffectiveTheme() === 'dark' ? 'light' : 'dark';
  localStorage.setItem('theme', nextTheme);
  applyTheme();
});
sysDark.addEventListener?.('change', () => {
  if (getStoredTheme() === null) applyTheme();
});

// Restore section from URL hash on load
const initialHash = location.hash.replace('#', '');
if (initialHash && document.getElementById(initialHash)) {
  showSection(initialHash, false);
}

// Handle browser back / forward
window.addEventListener('popstate', e => {
  const id = (e.state && e.state.section) || location.hash.replace('#', '') || 'home';
  showSection(id, false);
});

// -- Copy buttons on static <pre> blocks --
document.querySelectorAll('pre').forEach(pre => {
  const wrap = document.createElement('div');
  wrap.className = 'copy-wrap';
  pre.parentNode.insertBefore(wrap, pre);
  wrap.appendChild(pre);

  const btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.textContent = 'Copy';
  btn.setAttribute('aria-label', 'Copy code to clipboard');
  wrap.appendChild(btn);

  btn.addEventListener('click', () => {
    const code = pre.querySelector('code');
    const text = code ? code.textContent : pre.textContent;
    navigator.clipboard.writeText(text.trim()).then(() => {
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => {
        btn.textContent = 'Copy';
        btn.classList.remove('copied');
      }, 2000);
    });
  });
});

// -- Click-to-copy on inline .copyable code --
document.querySelectorAll('code.copyable').forEach(code => {
  code.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    navigator.clipboard.writeText(code.textContent.trim()).then(() => {
      code.classList.add('copied');
      setTimeout(() => code.classList.remove('copied'), 1200);
    });
  });
});

// -- Stage progress navigation --
document.querySelectorAll('.stage-progress-step[data-stage-nav]').forEach(step => {
  step.addEventListener('click', () => {
    const stage = parseInt(step.dataset.stageNav);
    const stageFirstSection = {
      1: 'home',
      2: 'quick-start',
      3: 'profiles',
      4: 'dag-dispatch'
    };
    const target = stageFirstSection[stage];
    if (target) showSection(target);
  });
});
</script>
"""
