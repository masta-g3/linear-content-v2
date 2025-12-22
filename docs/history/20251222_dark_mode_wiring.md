# Dark Mode Wiring (Quarto + Bootstrap)

Proper dual-theme wiring so Bootstrap components respect dark mode.

## Problem

Single Bootstrap theme (`data-mode="light"`) caused listing titles/descriptions to render with light-mode colors even when system preference was dark. The `<a>` wrappers in listings picked up Bootstrap's link colors instead of our custom tokens.

## Solution

Quarto-native dual theme configuration:

1. **`_quarto.yml`**: Configure both light and dark themes
   ```yaml
   theme:
     light: [cosmo, _brand.yml]
     dark: [cosmo, _brand.yml, theme-dark.scss]
   ```

2. **`theme-dark.scss`**: Bootstrap Sass variable overrides for dark mode
   - `$body-bg`, `$body-color`, `$link-color`, `$text-muted`, `$border-color`

3. **`styles.css`**: Dual selector approach
   - `@media (prefers-color-scheme: dark)` for system preference fallback
   - `body.quarto-dark` for Quarto toggle compatibility
   - Listing anchor inheritance rules (`color: inherit`)

## Architecture

```
_quarto.yml → theme-dark.scss → Bootstrap dark CSS
                              ↓
styles.css → Custom tokens (--paper, --black, etc.)
                              ↓
           Listing/post styling consistency
```

## Known Issue

Quarto 1.7.29 has a JS bug: theme toggle errors on pages without code blocks (missing `quarto-text-highlighting-styles` element). Toggle is hidden via CSS; site follows system preference.

## Status: Complete

- [x] Dual theme configuration in _quarto.yml
- [x] Bootstrap dark overrides in theme-dark.scss
- [x] CSS token selectors updated
- [x] Listing description anchor inheritance
- [x] Toggle hidden (Quarto bug workaround)
