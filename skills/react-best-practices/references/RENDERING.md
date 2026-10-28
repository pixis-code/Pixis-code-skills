# Rendering performance (MEDIUM impact, some HIGH)

Read this reference when reviewing JSX output, hydration behavior, scripts, or long-list rendering.

**Use `defer` or `async` on script tags.** (HIGH) A script tag without either blocks HTML parsing while it downloads and executes, delaying FCP/TTI. Use `defer` for DOM-dependent scripts (preserves execution order), `async` for independent ones (e.g. analytics, no order guarantee). In Next.js prefer `next/script`'s `strategy` prop over raw tags.

**Use React DOM resource hints.** (HIGH) `prefetchDNS`/`preconnect`/`preload`/`preloadModule`/`preinit`/`preinitModule` from `react-dom` let a server component hint the browser to start DNS/connection/resource work before the client even gets the HTML.
```tsx
preconnect('https://api.example.com')
preload('/fonts/inter.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' })
preinit('/styles/critical.css', { as: 'style' })
```
Use `prefetchDNS` for third-party domains needed later, `preconnect` for APIs fetched immediately, `preload` for current-page critical resources, `preloadModule`/`preinitModule` for JS needed for the likely next navigation or that must execute early.

**`content-visibility: auto` for long lists.** (HIGH) Defers off-screen layout/paint work.
```css
.message-item { content-visibility: auto; contain-intrinsic-size: 0 80px; }
```
For 1000 list items, skips layout/paint for the ~990 currently off-screen — roughly 10x faster initial render. Always pair with `contain-intrinsic-size` matching the item's real size, or scrollbar/scroll-position behavior breaks.

**Prevent hydration mismatch without flicker.** Reading `localStorage`/cookies directly during render breaks SSR (undefined on server); reading it in `useEffect` after mount causes a visible flash of the default value before it updates. Instead, inject a synchronous inline script that sets the DOM attribute before React hydrates.
```tsx
<div id="theme-wrapper">{children}</div>
<script dangerouslySetInnerHTML={{ __html: `(function(){try{var t=localStorage.getItem('theme')||'light';var el=document.getElementById('theme-wrapper');if(el)el.className=t;}catch(e){}})();` }} />
```
Useful for theme toggles, user prefs, auth state, or any client-only value that should render correctly on first paint.

**Suppress only genuinely expected hydration mismatches.** Values that intentionally differ server vs. client (random IDs, `Date.now()`, locale/timezone formatting) trigger noisy hydration warnings. Wrap just that element in `suppressHydrationWarning` — never use it to silence a real bug, and don't apply it broadly.
```tsx
<span suppressHydrationWarning>{new Date().toLocaleString()}</span>
```

**Use `<Activity>` for frequently toggled, expensive content.** Preserves component state and DOM across show/hide instead of unmounting, avoiding both the remount cost and state loss.
```tsx
<Activity mode={isOpen ? 'visible' : 'hidden'}><ExpensiveMenu /></Activity>
```

**Prefer `useTransition` over manual loading state.** Manual `isLoading` state management duplicates what `useTransition`'s built-in `isPending` already gives you, with better error resilience (pending resets correctly even if the transition throws) and automatic cancellation of superseded transitions.

**Use explicit ternaries for conditional rendering, not `&&`.** `{count && <Badge/>}` renders the literal `0` when `count` is `0` (or `NaN`, etc.) because `&&` returns the falsy operand itself, and React renders that.
```tsx
// Bad: renders "0" when count is 0
{count && <span className="badge">{count}</span>}
// Good
{count > 0 ? <span className="badge">{count}</span> : null}
```

**Hoist static JSX elements outside the component.** An element with no dependency on props/state gets recreated every render for no reason — define it once at module scope (especially worth it for large static SVGs).

**Animate the SVG's wrapper `<div>`, not the SVG element itself.** Many browsers don't hardware-accelerate CSS transforms/transitions applied directly to SVG elements; wrapping in a div and animating the wrapper gets GPU acceleration.

**Reduce SVG coordinate precision.** Excess decimal precision (`M 10.293847 20.847362`) bloats file size for no visual difference; one decimal place is usually enough. Automate with `npx svgo --precision=1 --multipass icon.svg`.

## Sources
* https://react.dev/reference/react-dom#resource-preloading-apis
* https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#defer
* https://react.dev/reference/react/useTransition
