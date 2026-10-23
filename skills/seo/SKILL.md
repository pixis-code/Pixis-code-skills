---
name: seo
description: "Optimize for search engine visibility: technical SEO, on-page SEO, and structured data."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Frontend, SEO, Search, Structured Data, Web]
    category: frontend
    related_skills: [web-quality-audit, accessibility-frontend, performance-frontend, core-web-vitals, best-practices-frontend]
---

# SEO optimization

Search engine optimization based on Lighthouse SEO audits and Google Search guidelines. Covers technical SEO, on-page optimization, and structured data.

## Evidence-led audit workflow

Check for a real audit tool before claiming anything was audited. **Never report a Lighthouse score, an indexing status, or a ranking claim as fact unless a real tool call or user-provided Search Console evidence produced it this session.**

With a live audit capability: run SEO + Agentic Browsing checks to localize rendered-page failures → inspect what the audit alone can't establish (response headers, redirects, `robots.txt`, sitemap coverage, canonical consistency across templates, structured-data eligibility, Search Console evidence if the user provides it) → keep technical crawl/index findings separate from content-quality and authority judgments, and never invent ranking-factor weights or promise ranking changes → fix the source, re-run, and report that indexation/ranking outcomes stay pending until the search engine actually re-crawls.

Without one: static source/config review only, using category-specific Lighthouse CLI output or direct HTML/HTTP inspection. A Lighthouse SEO score covers a useful technical subset — it is never a ranking prediction.

| Area | What this skill can verify |
|------|----------------------------|
| Crawl and index controls | Technical configuration and consistency |
| Rendered metadata and semantics | Presence, validity, and page-template issues |
| Structured data | Syntax and eligibility signals, not guaranteed rich results |
| Core Web Vitals | Link to measured field/lab evidence from `performance-frontend`/`core-web-vitals` |
| Content usefulness and authority | Review quality, but never assign synthetic ranking percentages |

---

## Technical SEO

### Crawlability

**robots.txt:**
```text
# /robots.txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /private/
# ❌ Don't block resources needed for rendering: Disallow: /static/
Sitemap: https://example.com/sitemap.xml
```

**Meta robots:**
```html
<meta name="robots" content="index, follow"> <!-- default -->
<meta name="robots" content="noindex, nofollow"> <!-- noindex a page -->
<meta name="robots" content="index, nofollow"> <!-- indexable, don't follow links -->
<meta name="robots" content="max-snippet:150, max-image-preview:large"> <!-- control snippets -->
```

**Canonical URLs:**
```html
<link rel="canonical" href="https://example.com/page"> <!-- prevents duplicate-content issues -->
<link rel="canonical" href="https://example.com/current-page"> <!-- self-referencing, recommended -->
<!-- For paginated content: self-referencing canonical per page, or rel="prev"/"next" -->
```

### XML sitemap
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```
Max 50,000 URLs or 50MB per sitemap (use a sitemap index for larger sites); include only canonical, indexable URLs; update `lastmod` when content changes; submit to Google Search Console.

### URL structure
```
✅ https://example.com/products/blue-widget
❌ https://example.com/p?id=12345
❌ https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```
Hyphens not underscores, lowercase only, keep under ~75 characters, keywords natural (not stuffed), avoid parameters where possible, HTTPS always.

### HTTPS & security
```html
<img src="https://example.com/image.jpg"> <!-- not http:// -->
```
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

---

## On-page SEO

### Title tags
```html
<!-- ❌ Missing or generic -->
<title>Page</title>
<!-- ✅ Descriptive, primary keyword near the start -->
<title>Blue Widgets for Sale | Premium Quality | Example Store</title>
```
50–60 characters is a rough linting proxy, not a hard pass/fail — Google truncates to fit rendered device width. Describe the topic naturally near the beginning, keep unique per page, add the brand when it helps users distinguish the result. Google may rewrite the visible title link from headings/anchor text/other sources even when `<title>` is short — investigate accuracy and consistency rather than auto-shortening. See [Google's title-link guidance](https://developers.google.com/search/docs/appearance/title-link).

### Meta descriptions
```html
<meta name="description" content="Shop premium blue widgets with free shipping. 30-day returns. Rated 4.9/5 by 10,000+ customers.">
```
Roughly 150–160 characters as a linting proxy only — snippets are query/device-dependent and Google may select page content instead. Natural topic coverage, compelling CTA, unique per page, matches page content.

### Heading structure
```html
<!-- ❌ Poor hierarchy -->
<h2>Welcome to Our Store</h2><h4>Products</h4><h1>Contact Us</h1>

<!-- ✅ Logical hierarchy -->
<h1>Blue Widgets - Premium Quality</h1>
  <h2>Product Features</h2>
    <h3>Durability</h3><h3>Design</h3>
  <h2>Customer Reviews</h2>
```
Primary heading should be descriptive and hierarchy unambiguous — don't fail a page just because valid HTML has more than one `<h1>`. Don't skip levels, include keywords naturally, avoid generic headings.

### Image SEO
```html
<!-- ❌ -->
<img src="IMG_12345.jpg">
<!-- ✅ -->
<img src="blue-widget-product-photo.webp"
     alt="Blue widget with chrome finish, side view showing control panel"
     width="800" height="600" loading="lazy">
```
Descriptive filenames, alt text describing content, compressed + properly sized, WebP/AVIF with fallbacks, lazy-load below-fold.

### Internal linking
```html
<!-- ❌ --> <a href="/products">Click here</a>
<!-- ✅ --> <a href="/products/blue-widgets">Browse our blue widget collection</a>
```
Descriptive anchor text with keywords, link to relevant internal pages, reasonable link count per page, fix broken links promptly, use breadcrumbs for hierarchy.

---

## Structured data (JSON-LD)

Read [the structured data reference](references/STRUCTURED-DATA.md) when the user requests schema markup or an audit surfaces a structured-data issue. Covers Organization, Article, Product, FAQ, and Breadcrumb examples plus validation links.

* **Describe visible, accurate content.** Don't add a type or claim solely to chase a rich result.
* **Use the most specific applicable type.** Keep identifiers and absolute URLs stable across renders.
* **Validate rendered output.** Passing syntax doesn't guarantee search-engine eligibility or display.

## Agentic browsing and AI discoverability

Keep these concepts separate:

* **Lighthouse Agentic Browsing** measures technical signals that help an assistant understand/interact with a rendered page (agent-facing accessibility tree, optional `llms.txt`, WebMCP registrations/schemas/form coverage).
* **Search indexing and ranking** depend on search-engine systems and can't be inferred from the Agentic Browsing score.
* **AI ingestion or citation** is product-specific — a technically browsable page or valid `llms.txt` doesn't prove any AI product will ingest, rank, or cite it.

Prioritize semantic HTML, descriptive labels, crawlable content, accurate metadata, clear structure — these help people, search engines, and agents alike. Add WebMCP tools only when the app has useful actions to expose and the user wants that integration; validate names/descriptions/schemas/form annotations with Lighthouse.

### Crawler controls are product-specific

Audit each documented user agent separately — don't apply a blanket "AI bot" rule:

| Control | Documented purpose | Effect of blocking |
|---------|--------------------|--------------------|
| `OAI-SearchBot` | ChatGPT search discovery | Prevents inclusion in ChatGPT summaries/snippets; a link/title may still surface via third-party discovery |
| `PerplexityBot` | Perplexity search indexing | Prevents that crawler indexing the blocked content |
| `Claude-SearchBot` / `Claude-User` | Claude search indexing / user-directed retrieval | May reduce search visibility / prevents retrieval for user-directed requests |
| `Google-Extended` | Controls certain Gemini training/grounding uses of Google-crawled content | Doesn't affect Google Search inclusion or ranking |

Training controls (`GPTBot`, `ClaudeBot`) are distinct from search/user-fetch controls. `GoogleOther` is a generic crawler, not an AI-search visibility switch. Verify current names and consequences in vendor docs: [OpenAI](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq), [Perplexity](https://docs.perplexity.ai/docs/resources/perplexity-crawlers), [Anthropic](https://privacy.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), [Google](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers).

### `llms.txt` is optional

An experimental proposal, not a cross-vendor discovery standard. Lighthouse can validate `/llms.txt`'s availability/shape, but that doesn't show any target product actually reads it. Add one only when the user requests it or a documented consumer supports it — never ahead of crawlability, semantic HTML, accurate metadata, and useful content, and never treat it as a ranking/citation factor.

---

## Mobile SEO

```html
<!-- ❌ --> <meta name="viewport" content="width=1024">
<!-- ✅ --> <meta name="viewport" content="width=device-width, initial-scale=1">
```
```css
/* ❌ Too small for mobile */
.small-link { padding: 4px; font-size: 12px; }
/* ✅ Adequate tap target */
.mobile-friendly-link { padding: 12px; font-size: 16px; min-height: 48px; min-width: 48px; }

/* ❌ Too small */
body { font-size: 10px; }
/* ✅ Readable without zooming */
body { font-size: 16px; line-height: 1.5; }
```

---

## International SEO

```html
<link rel="alternate" hreflang="en" href="https://example.com/page">
<link rel="alternate" hreflang="es" href="https://example.com/es/page">
<link rel="alternate" hreflang="x-default" href="https://example.com/page">
```
```html
<html lang="en"> <!-- or lang="es-MX" -->
```

---

## SEO audit checklist

**Critical:** HTTPS enabled · robots.txt allows crawling · no `noindex` on important pages · title tags present and unique · primary heading descriptive with logical hierarchy

**High priority:** meta descriptions present · sitemap submitted · canonical URLs set · mobile-responsive · Core Web Vitals passing

**Medium priority:** structured data implemented · internal linking strategy · image alt text · descriptive URLs · breadcrumb navigation · Agentic Browsing failures reviewed when agent access matters

**Ongoing:** fix crawl errors in Search Console · update sitemap on content changes · monitor ranking changes · check broken links · review Search Console insights

## Tools

| Tool | Use |
|------|-----|
| Google Search Console | Monitor indexing, fix issues |
| Google PageSpeed Insights | Performance + Core Web Vitals |
| Rich Results Test | Validate structured data |
| A live SEO/Agentic Browsing audit (when such a capability is available) | Rendered SEO checks |
| Lighthouse CLI | SEO audit fallback, no live tool needed |
| Screaming Frog | Crawl analysis |

## References

- [Google Search Central](https://developers.google.com/search)
- [Schema.org](https://schema.org/)
- [Structured data reference](references/STRUCTURED-DATA.md)
