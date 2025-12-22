# Visual Identity

Linear Content follows a **terminal-minimalist aesthetic with industrial plotting paper undertones**.

## Philosophy

- **Less is more** - every visual element must earn its place
- **Technical honesty** - the design should feel like it was made by engineers, for engineers
- **Subtle warmth** - avoid sterile coldness without becoming decorative
- **Zero ornamentation** - no gradients, shadows, rounded corners, or color accents

## Color Palette

```
Paper (background)    #FAFAF9   warm off-white, suggests aged paper
Black (primary)       #000000   text, borders, emphasis
Dark Gray             #1A1A1A   secondary emphasis
Mid Gray              #666666   descriptions, secondary text
Light Gray            #E5E5E5   subtle backgrounds
Border Gray           #CCCCCC   dividers, rules
Grid Color            #E8E8E6   dot pattern (barely visible)
```

The palette is strictly monochrome. Color accents are forbidden.

### Dark Mode Palette

Dark mode inverts the monochrome palette while preserving warmth:

```
Dark Paper (bg)       #161615   warm dark, avoids blue-black
Light Text            #E8E8E6   primary text
Light Gray            #D4D4D4   secondary emphasis
Mid Gray              #999999   secondary text
Subtle Dark           #2A2A29   backgrounds
Dark Border           #404040   dividers, rules
Dark Grid             #252524   dot pattern
```

Theme toggle cycles: system (◐) → light (○) → dark (●)

## Typography

**Berkeley Mono** throughout - headings, body, code. No font mixing.

```
Body:      1rem / 1.7 line-height
Headings:  700 weight, lowercase preferred
Code:      0.8-0.85rem
```

## Visual Elements

### Dot Grid Background
Faint radial dots at 20px intervals. Should be felt, not seen.

```css
background-image: radial-gradient(circle, #E8E8E6 1px, transparent 1px);
background-size: 20px 20px;
```

### Left Margin Tick Marks
Subtle dashed vertical line on content area, evoking plotting axes.

```css
background-image: repeating-linear-gradient(
  to bottom,
  #CCCCCC 0px, #CCCCCC 4px,
  transparent 4px, transparent 20px
);
opacity: 0.5;
```

### Borders
- Navbar: 2px solid black (the heaviest element)
- H2 headings: 1px bottom border
- Code blocks: 3px left border (black)
- Dividers: 1px border-color

### Links
Underlined, black. Hover thickens underline to 2px. No color change.

## Do's

- Use flat, sharp edges
- Maintain high contrast (black on paper)
- Let whitespace breathe
- Keep interactions subtle (underline thickness, not color)
- Use lowercase for titles/brand

## Don'ts

- Add color accents
- Use rounded corners
- Add shadows or gradients
- Use multiple typefaces
- Add decorative elements
- Over-engineer hover states

## File Reference

| File | Purpose |
|------|---------|
| `_brand.yml` | Quarto brand config (colors, typography) |
| `styles.css` | All custom styles (incl. dark mode variables) |
| `scripts/theme.js` | Theme toggle controller |
| `fonts/` | Berkeley Mono woff2 files |

## Influences

- Engineering graph paper / lab notebooks
- Terminal interfaces
- Brutalist web design
- Rhodia dot pads
