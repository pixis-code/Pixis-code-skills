---
name: core-web-vitals
description: "Diagnose and fix Core Web Vitals (LCP, INP, CLS) using field and lab evidence."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Frontend, Core Web Vitals, LCP, INP, CLS, Performance, Web]
    category: frontend
    related_skills: [web-quality-audit, performance-frontend, accessibility-frontend, seo, best-practices-frontend]
---

# Core Web Vitals optimization

Targeted diagnosis and fixes for the three Core Web Vitals, using field data to identify real user impact and browser traces to find the cause. This is the deep-dive companion to `performance-frontend` — that skill covers general loading/runtime performance; this one covers only LCP, INP, and CLS, in much more diagnostic depth (per-phase causes, framework-specific fixes, exact scoring formulas).

## Measure before optimizing

Check for a real tool before claiming anything is measured. **Never state that LCP, INP, or CLS is failing (or has improved) without runtime evidence from a real tool call this session; identify likely causes from code instead, explicitly as hypotheses.**

With a live tool, prefer this sequence: check page-level CrUX p75 data (clearly label an origin-level fallback when page data isn't available) → record a browser performance trace under stated conditions → analyze only the insights tied to the failing metric → inspect the implicated code → re-run the same lab measurement after the fix, and don't claim an immediate field improvement — CrUX and first-party RUM both need new user visits to reflect a change.

Without one: static source review only. Flag likely causes against the patterns below, but do not claim a metric is actually failing — that requires runtime evidence.

## The three metrics

| Metric | Measures | Good | Needs work | Poor |
|--------|----------|------|------------|------|
| **LCP** | Loading | ≤ 2.5s | 2.5s – 4s | > 4s |
| **INP** | Interactivity | ≤ 200ms | 200ms – 500ms | > 500ms |
| **CLS** | Visual Stability | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |

Google measures at the **75th percentile** — 75% of page visits must meet "Good" thresholds for the page/origin to pass.

---

## LCP: Largest Contentful Paint

LCP measures when the largest visible content element renders — usually a hero image/video, a large text block, a background image, or an `<svg>` element.

### Common LCP issues

**1. Slow server response (TTFB > 800ms)** — fix with CDN, caching, optimized backend, edge rendering.

**2. Render-blocking resources:**
```html
<!-- ❌ Blocks rendering -->
<link rel="stylesheet" href="/all-styles.css">
<!-- ✅ Critical CSS inlined, rest deferred -->
<style>/* Critical above-fold CSS */</style>
<link rel="preload" href="/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

**3. Slow resource load / late discovery:**
```html
<!-- ❌ LCP image discoverable only after a stylesheet loads -->
<div class="hero"></div>
<!-- ✅ Discoverable in initial HTML and prioritized -->
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">
<img src="/hero.webp" alt="Hero" fetchpriority="high">
```
Prefer a discoverable `<img>` with `fetchpriority="high"`. Add the preload only when a trace shows the resource is otherwise discovered late — duplicate/speculative preloads compete for bandwidth.

**4. Client-side rendering delays:**
```javascript
// ❌ Content loads after JavaScript
useEffect(() => {
  fetch('/api/hero-text').then(r => r.json()).then(setHeroText);
}, []);
// ✅ Server-side or static rendering
export async function getServerSideProps() {
  const heroText = await fetchHeroText();
  return { props: { heroText } };
}
```

**5. Make navigations instant with the Speculation Rules API**

For sites with predictable same-origin journeys, prerendering a likely next page speeds up the *subsequent* navigation — treat this as a navigation optimization, never a substitute for fixing the current page's LCP.
```html
<script type="speculationrules">
{ "prerender": [{ "where": { "href_matches": "/*" }, "eagerness": "moderate" }] }
</script>
```
Current Chrome `eagerness` behavior:

| `eagerness` | Trigger |
|-------------|---------|
| `conservative` | Pointer or touch down |
| `moderate` | Desktop: 200ms hover, or earlier pointer down; mobile: viewport heuristics |
| `eager` | Chrome 143+: desktop 10ms hover; mobile 50ms after the anchor enters the viewport |
| `immediate` | As soon as the rules are observed |

Start conservatively; measure prediction hit rate, transferred bytes, server load, and navigation improvement before expanding. Recheck [Chrome's eagerness docs](https://developer.chrome.com/docs/web-platform/prerender-pages#eagerness) before hardcoding timing-sensitive behavior.

Caveats: each prerender is roughly a full page load — scope `where` carefully (exclude logout/checkout) and avoid `immediate` outside small sites. Side effects (analytics, ads) fire when the prerender starts, not when the user navigates — gate them on the [`prerenderingchange` event](https://developer.chrome.com/docs/web-platform/prerender-pages#detect_when_a_page_is_prerendered_or_used_for_a_full_navigation) or `document.prerendering`. Chromium-only — Safari/Firefox ignore it, so it's a progressive enhancement, never a regression.

### LCP optimization checklist
```markdown
- [ ] TTFB < 800ms (CDN, edge caching)
- [ ] LCP resource discoverable in initial HTML and prioritized; preload only if a trace shows late discovery
- [ ] LCP image optimized (WebP/AVIF, correct size)
- [ ] Critical CSS inlined (< 14KB)
- [ ] No render-blocking JavaScript in <head>
- [ ] Fonts don't block text rendering (font-display: swap)
- [ ] LCP element in initial HTML (not JS-rendered)
- [ ] Speculation Rules added for likely-next navigations (moderate eagerness)
```

### LCP element identification
This snippet diagnoses the *current page session only* — it is not field data.
```javascript
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP element:', lastEntry.element);
  console.log('LCP time:', lastEntry.startTime);
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

Read [the detailed LCP reference](references/LCP.md) for framework-specific fixes (Next.js/Nuxt/Astro), the TTFB→load→render breakdown, and the common-issues-to-evidence table.

---

## INP: Interaction to Next Paint

INP measures responsiveness across clicks, taps, and key presses during a visit. Diagnose its three phases separately — input delay, processing time, presentation delay — before touching the handler; a slow interaction may be main-thread contention *before* the handler runs, expensive work *inside* it, or delayed rendering *after* it.

When field INP is poor or a trace identifies a slow interaction, read [the INP reference](references/INP.md) for trace interpretation, yielding patterns, third-party/rendering causes, a single-session observer, and production attribution.

---

## CLS: Cumulative Layout Shift

CLS measures unexpected layout shifts across a page visit (score = impact fraction × distance fraction). Use field attribution or a trace to find the shifted node and its trigger — don't assume the visible "victim" element is the actual cause; it may just be what got pushed by content inserted above it.

When field CLS is poor or a trace reports shifts, read [the CLS reference](references/CLS.md) for reserved-space patterns, dynamic-content handling, font/animation fixes, a debugging observer, and a verification checklist.

---

## Measurement sources

| Source | Use |
|--------|-----|
| A browser performance trace (when such a capability is available) | Observe one load/interaction and diagnose focused insights; use included CrUX context when available |
| CrUX or Search Console | Prioritize aggregated real-user outcomes at p75 |
| Lighthouse CLI or PageSpeed Insights | Controlled lab fallback when no live trace tool is available |
| First-party RUM | Segment current production experience by route, device, release, attribution |
| Raw `PerformanceObserver` | Inspect one page session during debugging, not field data |

Don't route performance diagnosis through a general Lighthouse "audit" call — that covers non-performance categories. Don't compare a single lab value directly against a field p75 as if they were equivalent samples.

When adding or reviewing production collection, read [the first-party RUM reference](../performance-frontend/references/RUM.md). Prefer the `web-vitals` library — raw browser APIs don't by themselves implement every Core Web Vital's full lifecycle and reporting rules.

---

## Framework quick fixes

### Next.js
```jsx
// LCP: next/image with priority
import Image from 'next/image';
<Image src="/hero.jpg" priority fill alt="Hero" />
// INP: dynamic imports
const HeavyComponent = dynamic(() => import('./Heavy'), { ssr: false });
// CLS: Image component handles dimensions automatically
```

### React
```jsx
// LCP: preload in head
<link rel="preload" href="/hero.jpg" as="image" fetchpriority="high" />
// INP: memoize + useTransition
const [isPending, startTransition] = useTransition();
startTransition(() => setExpensiveState(newValue));
// CLS: always specify dimensions in img tags
```

### Vue/Nuxt
```vue
<!-- LCP: nuxt/image with preload -->
<NuxtImg src="/hero.jpg" preload loading="eager" />
<!-- INP: async components -->
<component :is="() => import('./Heavy.vue')" />
<!-- CLS: aspect-ratio CSS -->
<img :style="{ aspectRatio: '16/9' }" />
```

## References

- [Detailed LCP optimization](references/LCP.md) — read when an LCP trace points to discovery, loading, or render delay
- [Detailed INP optimization](references/INP.md) — read when a trace or field attribution identifies a slow interaction
- [Detailed CLS optimization](references/CLS.md) — read when a trace or field attribution identifies unexpected shifts
- [web.dev LCP](https://web.dev/articles/lcp)
- [web.dev INP](https://web.dev/articles/inp)
- [web.dev CLS](https://web.dev/articles/cls)
- [Performance skill](../performance-frontend/SKILL.md)
