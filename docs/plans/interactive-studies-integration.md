# Interactive Studies Integration

Align the study generation system's output with blog requirements, then integrate as Quarto posts.

---

## Strategy

**Two-phase approach:**

1. **Supra-Phase A**: Update `new_studies_format/VISUAL_GUIDE.md` — the upstream standard that governs how studies are generated. Make the output inherently compatible with the blog.

2. **Supra-Phase B**: Integrate studies as Quarto posts — minimal transformation needed since output is already blog-aligned.

This ensures future studies are born compatible, not retrofitted.

---

## Analysis Summary

### Current State

**Study System Output** (`new_studies_format/viz/`):
- Standalone HTML + CSS + JS (D3.js v7)
- IBM Plex Mono typography
- Blue accent color (#2563eb) for data emphasis
- White background (#ffffff)
- Rounded corners (2-4px) on bars, tooltips, sparklines, selects
- Shadows on tooltips
- Global CSS reset (`* { margin: 0 }`)
- `:root` variable definitions

**Blog Visual Identity** (`docs/VISUAL_IDENTITY.md`):
- Berkeley Mono typography
- Strictly monochrome (no color accents)
- Warm paper background (#FAFAF9 light, #1E1D1B dark)
- Dot grid background pattern
- Zero ornamentation: no shadows, no rounded corners
- Dark mode via system preference
- CSS variables defined in `styles.css`

### Gap Analysis

| Aspect | Current Studies | Blog Requirement | Change Needed |
|--------|-----------------|------------------|---------------|
| Font | IBM Plex Mono | Berkeley Mono | Update VISUAL_GUIDE |
| Colors | Blue accent #2563eb | Monochrome only | Update VISUAL_GUIDE |
| Background | Pure white | Warm paper (inherit) | Update VISUAL_GUIDE |
| Corners | Rounded (2-4px) | Sharp (0) | Update VISUAL_GUIDE |
| Shadows | Tooltip shadows | None | Update VISUAL_GUIDE |
| Dark mode | None | System preference | Update VISUAL_GUIDE |
| CSS structure | `:root`, global reset | Scoped, use blog vars | Update VISUAL_GUIDE |
| HTML structure | Full document | Fragment only | Update VISUAL_GUIDE |

### Detailed Violations in Current Viz

From `new_studies_format/viz/style.css`:

| Line | Violation | Fix |
|------|-----------|-----|
| 1-18 | `:root` variable definitions | Remove, use blog vars |
| 20-24 | Global reset `* { margin: 0 }` | Scope to `.viz-main *` |
| 110-111 | `.spark-bar { border-radius: 1px }` | Set to 0 |
| 151 | `.paper-row:hover { background: #f9fafb }` | Use `var(--code-bg)` |
| 179 | `.paper-bar-container { border-radius: 2px }` | Set to 0 |
| 186 | `.paper-bar { transition: width 0.3s }` | Reduce to 150ms max |
| 247 | `#sort-select { border-radius: 4px }` | Set to 0 |
| 267-276 | `@keyframes expand` 200ms animation | Reduce to 150ms |
| 316 | `.arxiv-link { color: var(--accent) }` | Use `var(--black)` |
| 330 | `#tooltip { box-shadow: ... }` | Remove |
| 330 | `#tooltip { border-radius implied }` | Set to 0 |

---

# SUPRA-PHASE A: Update VISUAL_GUIDE.md

Make the study generation system produce blog-compatible output by default.

## A1: Proposed VISUAL_GUIDE.md Rewrite

Replace `new_studies_format/VISUAL_GUIDE.md` with this content:

```markdown
# Visual Guide

Design principles for publication-ready visualizations that integrate with Linear Content blog.

> **Skills**: Use `/tufte-design` for design decisions and `/d3js-skill` for implementation patterns.

## Philosophy

Follow Tufte + Terminal-Minimalist aesthetic:

- Every pixel must earn its place
- Data speaks; decoration distracts
- Monochrome palette—no color accents
- Sharp edges—no rounded corners
- No shadows or gradients

## Integration Context

Visualizations are embedded in a Quarto blog with existing CSS variables. **Do not define your own variables**—inherit from the host page.

### Available Blog Variables

```css
/* Use these directly - they handle dark mode automatically */
var(--font-mono)      /* Berkeley Mono font stack */
var(--paper)          /* Background: #FAFAF9 light, #1E1D1B dark */
var(--black)          /* Primary: #000000 light, #E6E4DF dark */
var(--mid-gray)       /* Secondary text */
var(--border-color)   /* Structure, dividers, bar tracks */
var(--code-bg)        /* Hover backgrounds */
```

## Design Tokens

Use blog variables, with explicit sizing:

```css
/* Typography - inherit font, set sizes */
font-family: var(--font-mono);
font-size: 14px;           /* Base */
font-size: 12px;           /* Small/labels */
font-size: 1.5rem;         /* Headlines (match blog h1) */
line-height: 1.5;

/* Spacing */
--row-height: 32px;
--section-gap: 2rem;
--column-gap: 2rem;
```

## Output Structure

### HTML Fragment (Not Full Document)

Generate **fragments** that can be included in Quarto, not standalone pages:

```html
<!-- viz/app.html - NO doctype, html, head, or body -->
<main class="viz-main">
  <header class="viz-header">
    <h2>Study Title</h2>
    <p class="subtitle">Brief description</p>
  </header>

  <section id="content-section">
    <!-- Visualization content -->
  </section>
</main>

<div id="tooltip" class="viz-tooltip"></div>
```

**Rules:**
- Use `<h2>` for study title (Quarto provides `<h1>` via frontmatter)
- Prefix IDs with descriptive names to avoid conflicts
- Include tooltip div at end

### CSS Structure

```css
/* viz/style.css - scoped, no globals */

/* Container scope - reset only within viz */
.viz-main *,
.viz-main *::before,
.viz-main *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.viz-main {
  font-family: var(--font-mono);
  font-size: 14px;
  color: var(--black);
  line-height: 1.5;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Dark mode handled automatically via var() cascade */
```

**Forbidden in CSS:**
- `:root { }` definitions
- `* { margin: 0; padding: 0; }` global resets
- `body { }` selectors
- Hardcoded colors (use variables)
- `border-radius` > 0
- `box-shadow`

### JavaScript Structure

```javascript
// viz/main.js

// Determine data path relative to script location
const DATA_PATH = new URL('./viz_data.json', import.meta.url).href;
// Or use explicit path from page root:
// const DATA_PATH = './viz/viz_data.json';

// Wait for DOM
document.addEventListener('DOMContentLoaded', init);

async function init() {
  const data = await d3.json(DATA_PATH);
  // ... render
}
```

**Rules:**
- Data path must work from Quarto page context (`./viz/viz_data.json`)
- Use `DOMContentLoaded` or place script at end with `defer`
- Avoid ID conflicts with common names (use descriptive prefixes)
- If using ES modules, `import.meta.url` gives script location

## Component Patterns

### Bars

```css
.bar {
  background: var(--black);
  border-radius: 0;
  height: 8px;
}

.bar-track {
  background: var(--border-color);
  border-radius: 0;
}
```

### Sparklines

```css
.spark-bar {
  background: var(--black);
  opacity: 0.6;
  border-radius: 0;
}
```

### Tooltips

```css
.viz-tooltip {
  position: absolute;
  pointer-events: none;
  background: var(--paper);
  border: 1px solid var(--border-color);
  padding: 12px;
  max-width: 400px;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.15s;
  z-index: 1000;
  /* NO box-shadow, NO border-radius */
}
```

### Expandable Details

```css
.detail-panel {
  border-left: 3px solid var(--black);
  padding-left: 1rem;
  margin: 8px 0;
  background: var(--paper);
}
```

### Interactive Rows

```css
.data-row {
  padding: 8px 0;
  cursor: pointer;
}

.data-row:hover {
  background: var(--code-bg);
}
```

### Links

```css
a {
  color: var(--black);
  text-decoration: underline;
  text-underline-offset: 2px;
}

a:hover {
  text-decoration-thickness: 2px;
  /* NO color change */
}
```

### Form Controls

```css
select {
  font-family: var(--font-mono);
  font-size: 12px;
  padding: 4px 8px;
  border: 1px solid var(--border-color);
  border-radius: 0;
  background: var(--paper);
  color: var(--black);
  cursor: pointer;
}

select:focus {
  outline: none;
  border-color: var(--black);
}
```

## Data Emphasis Without Color

Since color accents are forbidden, use:

| Technique | Use Case |
|-----------|----------|
| **Opacity** (0.4-0.6) | Secondary/background data |
| **Bold weight** | Emphasis within text |
| **Border-left** (3px) | Panel/section emphasis |
| **Whitespace** | Group related items |
| **Direct labels** | Instead of legends |
| **Size variation** | Headline stats vs details |

## D3.js Patterns

### Standard Setup

```javascript
const ROW_HEIGHT = 32;
const SECTION_GAP = 32;

// Use CSS variables in JS when needed
const style = getComputedStyle(document.documentElement);
const black = style.getPropertyValue('--black').trim();
```

### Tooltip Pattern

```javascript
const tooltip = d3.select('.viz-tooltip');

selection
  .on('mouseenter', (e, d) => {
    tooltip.style('opacity', 1).html(formatTooltip(d));
  })
  .on('mousemove', (e) => {
    tooltip
      .style('left', (e.pageX + 12) + 'px')
      .style('top', (e.pageY - 12) + 'px');
  })
  .on('mouseleave', () => tooltip.style('opacity', 0));
```

### Transitions

```javascript
// Max 150ms, ease-out
selection.transition()
  .duration(150)
  .ease(d3.easeOut)
  .attr('transform', d => `translate(0, ${d.y})`);
```

## Checklist

Before generating output:

- [ ] HTML is a fragment (no doctype/html/head/body)
- [ ] CSS has no `:root` or global resets
- [ ] All colors use `var(--*)` blog variables
- [ ] No `border-radius` > 0 anywhere
- [ ] No `box-shadow` anywhere
- [ ] No color accents (monochrome only)
- [ ] Links use underline, not color
- [ ] Transitions ≤ 150ms
- [ ] Data labels direct (no legend lookup)
- [ ] IDs prefixed to avoid conflicts

## File Output Structure

Each study should produce:

```
viz/
├── app.html       # HTML fragment
├── style.css      # Scoped CSS (no :root, no global reset)
├── main.js        # D3 visualization
└── viz_data.json  # Data file
```
```

---

## A2: Implementation Phases for VISUAL_GUIDE Update

### Phase A.1: Update VISUAL_GUIDE.md
- [x] Replace `new_studies_format/VISUAL_GUIDE.md` with new content
- [x] **Checkpoint**: Document updated

### Phase A.2: Validate Against Current Viz
- [ ] Audit current `viz/style.css` against new rules
- [ ] List all violations (rounded corners, shadows, colors, etc.)
- [ ] **Checkpoint**: Gap list complete

### Phase A.3: Create Reference Implementation
- [ ] Update `viz/style.css` to comply with new VISUAL_GUIDE
- [ ] Update `viz/index.html` → `viz/app.html` (fragment only)
- [ ] Verify no `:root`, no global resets
- [ ] Replace all colors with blog variables
- [ ] Remove all border-radius
- [ ] Remove all box-shadow
- [ ] **Checkpoint**: Reference viz complies with guide

### Phase A.4: Dark Mode Verification
- [ ] Test reference viz with dark mode (will need blog context)
- [ ] Verify all elements adapt correctly
- [ ] **Checkpoint**: Dark mode works

---

# SUPRA-PHASE B: Quarto Integration

Integrate blog-aligned studies as posts.

## B1: Post Structure

Note: Existing posts use underscore separators (e.g., `20160825_sentiment_bukowski`).

```
posts/
├── [existing text posts...]
└── 20250103_paper_selection/
    ├── index.qmd           # Quarto wrapper
    └── viz/
        ├── app.html        # HTML fragment (from study system)
        ├── style.css       # Scoped CSS
        ├── main.js         # D3 code
        └── viz_data.json   # Data
```

## B2: Quarto Wrapper Template

```yaml
---
title: "LLM Paper Selection Experiment"
description: "Comparing single-shot vs multi-run consensus in paper selection."
date: "2025-01-03"
categories: [experiments, llm]
format:
  html:
    page-layout: full
    toc: false
---
```

```html
<div class="viz-container">
{{\< include viz/app.html \>}}
</div>

<link rel="stylesheet" href="viz/style.css">
<script src="https://d3js.org/d3.v7.min.js"></script>
<script type="module">
  // Load data relative to page, not script
  const DATA_PATH = './viz/viz_data.json';

  const { default: init } = await import('./viz/main.js');
  // Or if main.js self-initializes, just import it:
  // import './viz/main.js';
</script>
```

**Alternative (simpler, if main.js handles its own path):**

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
  // Set data path before main.js runs
  window.VIZ_DATA_PATH = './viz/viz_data.json';
</script>
<script src="viz/main.js" defer></script>
```

Then in `main.js`:
```javascript
const DATA_PATH = window.VIZ_DATA_PATH || './viz/viz_data.json';
```

## B3: Integration CSS (Optional)

If needed, add to `styles.css` for viz-specific tweaks:

```css
/* Viz container - ensure full width */
.viz-container {
  width: 100%;
  /* Inherits blog dot grid background */
}

/* Optional: solid background for dense viz */
.viz-container.solid-bg {
  background-color: var(--paper);
  background-image: none;
}
```

## B4: Implementation Phases for Integration

### Phase B.1: Create First Study Post
- [x] Create `posts/20260103_llm-resampling/` directory
- [x] Copy compliant viz files from Phase A.3
- [x] Update `main.js` to use configurable DATA_PATH
- [x] Write `index.qmd` wrapper with data path config and `resources` for viz_data.json
- [x] Run `quarto preview`
- [x] **Checkpoint**: Post renders without errors, data loads correctly

### Phase B.2: Verify Visual Alignment
- [x] Compare viz appearance to blog posts
- [x] Verify typography matches (Berkeley Mono)
- [x] Verify color palette (monochrome)
- [x] Verify no rounded corners visible
- [x] Verify no shadows visible
- [x] **Checkpoint**: Visually indistinguishable from blog aesthetic

### Phase B.3: Test Interactions
- [x] Tooltips position correctly
- [x] Hover states work
- [x] Expandable detail panels work
- [x] Sorting dropdown works
- [x] Data loading works (relative path)
- [x] **Checkpoint**: All interactions functional

### Phase B.4: Dark Mode
- [x] Toggle system dark mode
- [x] Verify all viz elements adapt
- [x] Check contrast ratios
- [x] **Checkpoint**: Dark mode fully functional

### Phase B.5: Mobile
- [x] Test at 750px (below 800px breakpoint)
- [x] Verify single-column stacking
- [x] **Checkpoint**: Mobile-ready

### Phase B.6: Document
- [x] Add "Viz Post" section to `docs/STRUCTURE.md`
- [x] Document post creation workflow
- [x] **Checkpoint**: Documentation complete

---

## File Changes Summary

### Supra-Phase A (Upstream)

| File | Action |
|------|--------|
| `new_studies_format/VISUAL_GUIDE.md` | Rewrite (new content) |
| `new_studies_format/viz/app.html` | Create (fragment from index.html) |
| `new_studies_format/viz/style.css` | Update (remove :root, radius, shadow) |
| `new_studies_format/viz/index.html` | Delete or keep as standalone demo |

### Supra-Phase B (Integration)

| File | Action |
|------|--------|
| `posts/20250103_paper_selection/index.qmd` | Create |
| `posts/20250103_paper_selection/viz/*` | Copy from updated new_studies_format |
| `docs/STRUCTURE.md` | Add viz post section |
| `styles.css` | Optional: add .viz-container rules |

---

## Backward Compatibility

**Old posts remain unchanged.** The new viz post type is additive:

- Text posts: `posts/YYYYMMDD_slug/index.qmd` or `index.ipynb`
- Viz posts: `posts/YYYYMMDD_slug/index.qmd` + `viz/` folder

Both work within the same Quarto build. The listing shows all posts sorted by date.

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Study system generates old format | VISUAL_GUIDE is authoritative; update skills that reference it |
| CSS variable cascade fails | Remove ALL `:root` from viz CSS |
| ID conflicts in Quarto | Prefix all IDs (e.g., `stats-headline` not `headline`) |
| Monochrome limits expressiveness | Use opacity, weight, borders, whitespace per Tufte |
| D3 bundle size | CDN with async; acceptable for interactive content |

---

## Decision Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Color accent | No | Blog identity is strictly monochrome |
| HTML output | Fragment | Enables Quarto include without conflicts |
| CSS structure | Scoped, no :root | Inherits blog dark mode automatically |
| Border radius | 0 everywhere | Blog forbids rounded corners |
| Shadows | None | Blog forbids decorative effects |
