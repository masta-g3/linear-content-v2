# Social Media Sharing Configuration

OpenGraph and Twitter Card metadata for link previews on social platforms.

## Configuration

```yaml
# _quarto.yml
website:
  site-url: https://blog.mg3.dev
  open-graph: true
  twitter-card: true
  image: /images/site-preview.png
```

## Files

| File | Purpose |
|------|---------|
| `images/site-preview.png` | Default social preview (1376×768, vector field typography) |
| `_quarto.yml` | Site-level OG/Twitter config |

## Generated Meta Tags

```html
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="https://blog.mg3.dev/images/site-preview.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://blog.mg3.dev/images/site-preview.png">
```

## Post-Level Images

Posts without an `image:` field use `site-preview.png` as fallback. To add post-specific previews:

```yaml
# posts/*/index.qmd
---
image: preview.png
---
```

## Validation Tools

- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)

## Completed

- [x] Site preview image created (Gemini 3 Pro generated)
- [x] Quarto config updated
- [x] Meta tags verified working
