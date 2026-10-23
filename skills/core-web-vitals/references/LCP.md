# LCP optimization reference

## What is LCP?

Largest Contentful Paint measures when the largest content element in the viewport becomes visible — typically an `<img>`, an `<image>` inside `<svg>`, a `<video>` with poster image, an element with a background `url()` image, or a block-level element containing text nodes.

## LCP timeline
```
[  Server Response  ][  Resource Load  ][  Render  ]
       TTFB              Download         Paint
       └─────────────────────────────────────┘
                         LCP Time
```

## Detailed optimizations

### 1. Server response time (TTFB)
Target: < 800ms. Causes: slow server/DB queries, no CDN/edge caching, inefficient backend, serverless cold starts.
```javascript
// Edge functions for dynamic content (Vercel example)
export const config = { runtime: 'edge' };
// stale-while-revalidate caching
res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=300');
```

### 2. Resource load time
**Images:**
```html
<!-- Preload only when a trace shows the LCP image is discovered late -->
<link rel="preload" as="image" href="/hero.webp"
      imagesrcset="/hero-400.webp 400w, /hero-800.webp 800w"
      imagesizes="100vw" fetchpriority="high">

<!-- Modern format with fallback -->
<picture>
  <source srcset="/hero.avif" type="image/avif">
  <source srcset="/hero.webp" type="image/webp">
  <img src="/hero.jpg" width="1200" height="600" fetchpriority="high" alt="Hero">
</picture>
```
**Text/web fonts:**
```css
@font-face {
  font-family: 'Heading';
  src: url('/fonts/heading.woff2') format('woff2');
  font-display: swap; /* show fallback immediately */
}
```

### 3. Render-blocking resources
**Critical CSS:**
```html
<head>
  <style>/* Only above-fold styles, < 14KB */</style>
  <link rel="preload" href="/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
</head>
```
**Defer JavaScript:**
```html
<!-- ❌ Blocks parsing -->
<script src="/app.js"></script>
<!-- ✅ Deferred -->
<script defer src="/app.js"></script>
<!-- ✅ Module (deferred by default) -->
<script type="module" src="/app.mjs"></script>
```

### 4. Client-side rendering
**Problem:** content not in initial HTML. Solutions:
```javascript
// SSR (Next.js)
export async function getServerSideProps() {
  const data = await fetchHeroContent();
  return { props: { hero: data } };
}
// SSG (Next.js)
export async function getStaticProps() {
  const data = await fetchHeroContent();
  return { props: { hero: data }, revalidate: 3600 };
}
```
```jsx
// Streaming SSR (React 18+)
import { Suspense } from 'react';
function Page() {
  return <Suspense fallback={<HeroSkeleton />}><Hero /></Suspense>;
}
```

## Framework-specific tips

**Next.js:**
```jsx
import Image from 'next/image';
<Image src="/hero.jpg" priority fill sizes="100vw" alt="Hero" />
```
**Nuxt:**
```vue
<NuxtImg src="/hero.jpg" preload loading="eager" sizes="100vw" />
```
**Astro:**
```astro
---
import { Image } from 'astro:assets';
import hero from '../assets/hero.jpg';
---
<Image src={hero} loading="eager" decoding="sync" alt="Hero" />
```

## Debugging LCP
```javascript
// Identifies the LCP element for the current session only
new PerformanceObserver((entryList) => {
  const entries = entryList.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP:', {
    element: lastEntry.element,
    time: lastEntry.startTime,
    size: lastEntry.size,
    url: lastEntry.url,
    renderTime: lastEntry.renderTime,
    loadTime: lastEntry.loadTime
  });
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

## Common issues

| Issue | Evidence to confirm | Typical fix |
|-------|---------------------|-------------|
| LCP resource discovered late | Large resource load delay in an LCP-discovery/breakdown insight | Put it in initial HTML, add priority, preload only when still necessary |
| Large image transfer | Resource load duration and response bytes dominate | Resize/compress, choose an appropriate format |
| Render-blocking CSS | A render-blocking insight and long render delay | Remove unused rules, split non-critical CSS, inline only proven critical CSS |
| Slow TTFB | A document-latency insight or LCP TTFB subpart dominates | Cache, reduce redirects, optimize server work |
| Client-rendered LCP | LCP element absent from initial HTML, render delay dominates | SSR, static rendering, or earlier rendering |

Don't attach generic millisecond-savings claims to these fixes. Measure the relevant LCP subpart before and after under equivalent conditions.
