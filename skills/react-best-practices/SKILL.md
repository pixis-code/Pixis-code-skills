---
name: react-best-practices
description: "Review and refactor React/Next.js code for performance: waterfalls, bundle size, server-component patterns, re-renders, and rendering."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Frontend, React, Next.js, Performance, Rerenders, Server Components]
    category: frontend
    related_skills: [performance-frontend, core-web-vitals, best-practices-frontend]
---

# React / Next.js best practices

React- and Next.js-specific performance patterns, adapted from Vercel Engineering's rule set. This is the React-specific companion to `performance-frontend` and `core-web-vitals` — those cover general loading/runtime performance and the three Core Web Vitals; this one covers React/Next.js-specific causes: data-fetching waterfalls, bundle splitting, Server Component pitfalls, and re-render waste that those skills don't reach.

## How it works

This is almost entirely static code review — identify patterns against the rules below and explain the fix. **Don't state a specific performance number (ms saved, % faster, bundle size) as a measured fact about the user's code unless a real tool call (profiler, bundle analyzer, trace) produced it this session.** Some rules below cite general published figures (e.g. "barrel imports commonly cost 200–800ms") — these are documented, real benchmarks from the source material, safe to mention as general context, but never imply they're what *this* specific code will save without measuring it. Frame findings as hypotheses the pattern supports, not confirmed numbers.

If a profiler, bundle analyzer, or trace tool genuinely is available this session, use it to confirm before/after — then the measured-tier language applies, same as `performance-frontend` and `core-web-vitals`.

## Rule categories, by impact

| Priority | Category | Impact | Reference |
|---|---|---|---|
| 1 | Eliminating waterfalls | CRITICAL | [WATERFALLS-AND-BUNDLE.md](references/WATERFALLS-AND-BUNDLE.md) |
| 2 | Bundle size optimization | CRITICAL | [WATERFALLS-AND-BUNDLE.md](references/WATERFALLS-AND-BUNDLE.md) |
| 3 | Server-side performance & safety | HIGH | [SERVER.md](references/SERVER.md) |
| 4 | Client-side data fetching | MEDIUM-HIGH | [CLIENT-AND-RERENDER.md](references/CLIENT-AND-RERENDER.md) |
| 5 | Re-render optimization | MEDIUM | [CLIENT-AND-RERENDER.md](references/CLIENT-AND-RERENDER.md) |
| 6 | Rendering performance | MEDIUM (some HIGH) | [RENDERING.md](references/RENDERING.md) |
| 7 | Advanced hook patterns | LOW | [CLIENT-AND-RERENDER.md](references/CLIENT-AND-RERENDER.md) (bottom section) |

When reviewing code, start with whichever categories the code actually touches — a component doing data fetching should be checked against waterfalls/server first; a component with lots of state/effects against re-render second; bundle size only when imports or heavy dependencies are visible.

**Generic JavaScript micro-optimizations** (loop patterns, Map/Set lookups, caching property access, `requestIdleCallback`, etc.) are intentionally not included here — that ground is already covered by `performance-frontend` and `best-practices-frontend`, and isn't React-specific.

## Quick index

**Waterfalls & bundle (CRITICAL):** Promise.all for independent calls, dependency-based parallelization, don't block unrelated branches on one await, check cheap conditions before async flags, Suspense boundaries for partial-page blocking · barrel-import avoidance, dynamic imports for heavy components, defer third-party scripts, conditional module loading, hover/focus preload, statically analyzable import paths.

**Server (HIGH):** authenticate every Server Action internally, never store request data in module-level mutable variables, parallelize RSC tree fetches via composition, chain nested fetches per-item not globally, minimize what's serialized to the client, avoid duplicate-reference serialization, `React.cache()` for per-request dedup (primitive args only), LRU cache for cross-request reuse, hoist static I/O to module level, `after()` for non-blocking side effects.

**Client fetching & re-renders (MEDIUM-HIGH → LOW):** SWR for dedup, shared event listeners, passive scroll/touch listeners, versioned minimal localStorage · no components defined inside components, derive state during render not in effects, subscribe to derived booleans not raw values, defer reads to point of use, interaction logic in handlers not state+effect, functional setState, lazy `useState` init, primitive effect dependencies, split combined hooks, memoized component extraction, stable default values for memoized components, skip `useMemo` on cheap primitives, `useRef` for transient values, `startTransition`/`useDeferredValue` for non-urgent updates · effect-event dependency pitfalls, refs for stable handler subscriptions, once-per-app-load init guards.

**Rendering (MEDIUM, some HIGH):** `defer`/`async` on scripts, React DOM resource hints (preconnect/preload/preinit), `content-visibility` for long lists · hydration-safe client-only values (sync inline script, not post-hydration effect), `suppressHydrationWarning` only for genuinely expected mismatches · `<Activity>` for toggled expensive content, `useTransition` over manual loading state, ternaries over `&&` for conditionals, hoisted static JSX, animate SVG wrappers not SVG elements, reduced SVG precision.

## References
- [Waterfalls & bundle size](references/WATERFALLS-AND-BUNDLE.md) — read for async data-fetching review or anything touching initial JS bundle size
- [Server-side performance & safety](references/SERVER.md) — read for RSCs, Server Actions, route handlers
- [Client fetching & re-renders](references/CLIENT-AND-RERENDER.md) — read for client components, hooks, state/effect review
- [Rendering performance](references/RENDERING.md) — read for JSX output, hydration, scripts, long lists
- [Performance skill](../performance-frontend/SKILL.md) — general (non-React) loading/runtime performance
- [Core Web Vitals skill](../core-web-vitals/SKILL.md) — LCP/INP/CLS deep-dive
- https://react.dev
- https://nextjs.org
