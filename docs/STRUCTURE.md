# Project Structure

Linear Content is a Quarto-based technical blog.

## Directory Layout

```
linear-content-v2/
├── _quarto.yml        # Site configuration
├── _brand.yml         # Brand colors, typography
├── theme-dark.scss    # Bootstrap dark mode overrides
├── styles.css         # Custom CSS
├── index.qmd          # Homepage with post listing
├── about.qmd          # About page
├── posts/             # Blog posts (one folder per post)
├── fonts/             # Berkeley Mono woff2 files
├── images/            # Site images
├── pending/           # Draft posts (not published)
├── scripts/           # Build/utility scripts
└── docs/              # Developer documentation
    ├── STRUCTURE.md   # This file
    ├── VISUAL_IDENTITY.md
    └── history/       # Archived implementation notes
```

## Key Files

| File | Purpose |
|------|---------|
| `_quarto.yml` | Site metadata, navbar, footer, format options |
| `_brand.yml` | Color palette, typography definitions |
| `theme-dark.scss` | Bootstrap Sass variable overrides for dark mode |
| `styles.css` | All visual styling (dot grid, tick marks, etc.) |
| `index.qmd` | Post listing configuration |
| `docs/history/` | Archived implementation notes and specs |

## Adding Posts

Create a folder in `posts/` with an `index.qmd`:

```
posts/
└── my-new-post/
    ├── index.qmd      # Post content
    └── images/        # Post-specific images (optional)
```

Post frontmatter:
```yaml
---
title: "Post Title"
description: "Brief description"
date: "2024-01-15"
categories: [nlp, data science]
---
```

## Building

```bash
quarto preview          # Local dev server
quarto render           # Build to _site/
```

## Design System

See [VISUAL_IDENTITY.md](./VISUAL_IDENTITY.md) for colors, typography, and styling guidelines.
