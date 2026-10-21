---
name: best-practices-frontend
description: "Apply modern web development best practices for security, browser compatibility, and code quality."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Frontend, Security, Best Practices, Web Quality, Web]
    category: frontend
    related_skills: [web-quality-audit, accessibility-frontend, performance-frontend, core-web-vitals, seo]
---

# Best practices

Modern web development standards based on Lighthouse Best Practices audits. Covers security, browser compatibility, and code quality patterns.

## Evidence-led audit workflow

Check for a real audit/trace tool before claiming anything was audited. **Never report a Lighthouse score or audit result as proof of security unless a real tool call produced it this session.**

With a live audit capability: run a Best Practices audit (navigation mode for a normal load, snapshot mode to preserve current state) → inspect listed console/network failures, fetching details only when they support a finding → supplement with dependency, header, config, and source inspection (an audit alone isn't a full security assessment) → fix the implicated code, re-run, keep security findings separate from style preferences.

Without one: static code/config review only. Flag issues against the patterns below, explain why each matters, and label findings as hypotheses — verify with the Lighthouse CLI or a dependency/header check once that tooling exists.

## Security

Read [the security reference](references/SECURITY.md) when security is in scope or an audit surfaces a related failure. It covers HTTPS/HSTS, CSP and Trusted Types, Subresource Integrity, headers, dependencies, sanitization, and cookies.

At minimum:

* **Use HTTPS without mixed content.** Add HSTS only after confirming every relevant subdomain supports HTTPS.
* **Treat a strict CSP as defense in depth.** Prefer nonces or hashes and test with report-only before enforcement.
* **Sanitize untrusted HTML and protect DOM XSS sinks.** Prefer text APIs when markup is not required.
* **Pin and review third-party code.** Use SRI where the delivery model supports it and keep dependencies patched.
* **Verify response headers at runtime.** Source configuration alone does not prove what the deployed page sends.

## Browser compatibility

### Document setup: doctype, charset, viewport
```html
<!-- ❌ Invalid/missing doctype, late charset, no viewport -->
<HTML>
<head>
  <title>Page</title>
  <meta charset="UTF-8"> <!-- charset must be first element in head -->
</head>

<!-- ✅ Correct order: doctype → charset first → viewport → title -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page</title>
</head>
```
A pre-HTML5 doctype (e.g. `<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">`) or a missing one triggers quirks mode — always use the plain HTML5 doctype.

### Feature detection
```javascript
// ❌ Browser detection (brittle)
if (navigator.userAgent.includes('Chrome')) {
  // Chrome-specific code
}

// ✅ Feature detection
if ('IntersectionObserver' in window) {
  // Use IntersectionObserver
} else {
  // Fallback
}

// ✅ Using @supports in CSS
@supports (display: grid) {
  .container { display: grid; }
}
@supports not (display: grid) {
  .container { display: flex; }
}
```

### Polyfills (when needed)

Prefer **bundling at build time** (Babel/SWC + `core-js`, or `@vitejs/plugin-legacy`) targeted by your supported-browsers list — no runtime check, no polyfill bytes shipped to modern browsers.

If a runtime load is unavoidable, append a script element — never `document.write` (blocks the parser, broken in async/deferred contexts):
```html
<script>
  if (!('fetch' in window)) {
    const s = document.createElement('script');
    s.src = '/polyfills/fetch.js';
    s.defer = true;
    document.head.appendChild(s);
  }
</script>
```

**Never load polyfills from a third-party CDN you don't control** — `polyfill.io` was [compromised in mid-2024](https://sansec.io/research/polyfill-supply-chain-attack), serving malware to ~100k sites. Self-host or use a vetted mirror ([Cloudflare's `cdnjs` build](https://blog.cloudflare.com/polyfill-io-now-available-on-cdnjs-reduce-your-supply-chain-risk/)), and pin it with [SRI](references/SECURITY.md#subresource-integrity-sri-for-third-party-scripts).

---

## Deprecated APIs

### Avoid these
```javascript
// ❌ document.write (blocks parsing)
document.write('<script src="..."></script>');
// ✅ Dynamic script loading
const script = document.createElement('script');
script.src = '...';
document.head.appendChild(script);

// ❌ Synchronous XHR (blocks main thread)
const xhr = new XMLHttpRequest();
xhr.open('GET', url, false); // false = synchronous
// ✅ Async fetch
const response = await fetch(url);

// ❌ Application Cache (deprecated)
<html manifest="cache.manifest">
// ✅ Service Workers
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

### Event listener passive
```javascript
// ❌ Non-passive touch/wheel (may block scrolling)
element.addEventListener('touchstart', handler);
element.addEventListener('wheel', handler);
// ✅ Passive listeners (allows smooth scrolling)
element.addEventListener('touchstart', handler, { passive: true });
element.addEventListener('wheel', handler, { passive: true });
// ✅ If you need preventDefault, be explicit
element.addEventListener('touchstart', handler, { passive: false });
```

---

## Console & errors

### No console errors
```javascript
// ❌ Errors in production
console.log('Debug info'); // Remove in production
throw new Error('Unhandled'); // Catch all errors

// ✅ Proper error handling
try {
  riskyOperation();
} catch (error) {
  errorTracker.captureException(error); // Log to error tracking service
  showErrorMessage('Something went wrong. Please try again.'); // User-friendly message
}
```

### Error boundaries (React)
```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  static getDerivedStateFromError(error) { return { hasError: true }; }
  componentDidCatch(error, info) { errorTracker.captureException(error, { extra: info }); }
  render() {
    if (this.state.hasError) return <FallbackUI />;
    return this.props.children;
  }
}
// Usage
<ErrorBoundary><App /></ErrorBoundary>
```

### Global error handler
```javascript
window.addEventListener('error', (event) => {
  errorTracker.captureException(event.error);
});
window.addEventListener('unhandledrejection', (event) => {
  errorTracker.captureException(event.reason);
});
```

---

## Source maps

### Production configuration
```javascript
// ❌ Source maps exposed in production
module.exports = { devtool: 'source-map' }; // Exposes source code

// ✅ Hidden source maps (uploaded to error tracker)
module.exports = { devtool: 'hidden-source-map' };

// ✅ Or no source maps in production
module.exports = { devtool: process.env.NODE_ENV === 'production' ? false : 'source-map' };
```

**Strip `sourcesContent` from production maps** when uploading to your error tracker — bundlers embed the full original source in the `.map` file by default, so anyone who obtains it (including via a misconfigured upload step) gets your unminified code. Omit it in your bundler config, or use a Sentry/Bugsnag CLI flag that strips it on upload. For Vite, prefer `sourcemap: 'hidden'` over `'true'` so the `//# sourceMappingURL=` comment isn't emitted into the bundle.

---

## Performance best practices

### Avoid blocking patterns
```javascript
// ❌ Blocking script
<script src="heavy-library.js"></script>
// ✅ Deferred script
<script defer src="heavy-library.js"></script>

// ❌ Blocking CSS import
@import url('other-styles.css');
// ✅ Link tags (parallel loading)
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="other-styles.css">
```

### Efficient event handlers
```javascript
// ❌ Handler on every element
items.forEach(item => { item.addEventListener('click', handleClick); });

// ✅ Event delegation
container.addEventListener('click', (e) => {
  if (e.target.matches('.item')) handleClick(e);
});
```

### Memory management
```javascript
// ❌ Memory leak (never removed)
const handler = () => { /* ... */ };
window.addEventListener('resize', handler);

// ✅ Cleanup when done (e.g. on component unmount)
window.removeEventListener('resize', handler);

// ✅ Using AbortController
const controller = new AbortController();
window.addEventListener('resize', handler, { signal: controller.signal });
controller.abort(); // cleanup
```

---

## Code quality

### Valid HTML
```html
<!-- ❌ Invalid HTML -->
<div id="header">
<div id="header"> <!-- Duplicate ID -->
<ul><div>Item</div></ul> <!-- Invalid child -->
<a href="/"><button>Click</button></a> <!-- Invalid nesting -->

<!-- ✅ Valid HTML -->
<header id="site-header"></header>
<ul><li>Item</li></ul>
<a href="/" class="button">Click</a>
```

### Semantic HTML
```html
<!-- ❌ Non-semantic -->
<div class="header"><div class="nav"><div class="nav-item">Home</div></div></div>
<div class="main"><div class="article"><div class="title">Headline</div></div></div>

<!-- ✅ Semantic HTML5 -->
<header><nav><a href="/">Home</a></nav></header>
<main><article><h1>Headline</h1></article></main>
```

### Image aspect ratios
```html
<!-- ❌ Distorted images -->
<img src="photo.jpg" width="300" height="100"> <!-- actual ratio 4:3, squishes the image -->

<!-- ✅ Preserve aspect ratio -->
<img src="photo.jpg" width="300" height="225"> <!-- actual 4:3 dimensions -->

<!-- ✅ CSS object-fit for flexibility -->
<img src="photo.jpg" style="width: 300px; height: 200px; object-fit: cover;">
```

---

## Permissions & privacy

### Request permissions properly
```javascript
// ❌ Request on page load (bad UX, often denied)
navigator.geolocation.getCurrentPosition(success, error);

// ✅ Request in context, after user action
findNearbyButton.addEventListener('click', async () => {
  if (await showPermissionExplanation()) { // Explain why you need it
    navigator.geolocation.getCurrentPosition(success, error);
  }
});
```

### Permissions policy
```html
<!-- Restrict powerful features -->
<meta http-equiv="Permissions-Policy" content="geolocation=(), camera=(), microphone=()">
<!-- Or allow for specific origins -->
<meta http-equiv="Permissions-Policy" content="geolocation=(self 'https://maps.example.com')">
```

---

## Audit checklist

### Security (critical)
- [ ] HTTPS enabled, no mixed content
- [ ] No vulnerable dependencies (`npm audit`)
- [ ] CSP headers configured (with `frame-ancestors`, `base-uri`, `form-action`)
- [ ] `require-trusted-types-for 'script'` enforced (or report-only during rollout)
- [ ] Third-party `<script>`/`<link rel="stylesheet">` pinned with SRI hashes
- [ ] Security headers present (HSTS, X-Content-Type-Options, Referrer-Policy)
- [ ] No exposed source maps (and `sourcesContent` stripped from uploaded ones)

### Compatibility
- [ ] Valid HTML5 doctype
- [ ] Charset declared first in head
- [ ] Viewport meta tag present
- [ ] No deprecated APIs used
- [ ] Passive event listeners for scroll/touch

### Code quality
- [ ] No console errors
- [ ] Valid HTML (no duplicate IDs)
- [ ] Semantic HTML elements used
- [ ] Proper error handling
- [ ] Memory cleanup in components

### UX
- [ ] No intrusive interstitials
- [ ] Permission requests in context
- [ ] Clear error messages
- [ ] Appropriate image aspect ratios

## Tools

| Tool | Purpose |
|------|---------|
| `npm audit` | Dependency vulnerabilities |
| [SecurityHeaders.com](https://securityheaders.com) | Header analysis |
| [W3C Validator](https://validator.w3.org) | HTML validation |
| A live Best Practices audit (when such a capability is available) | Rendered best-practices checks |
| Lighthouse CLI | Best Practices audit fallback, no live tool needed |
| [Observatory](https://observatory.mozilla.org) | Security scan |

## References

- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Security reference](references/SECURITY.md)
