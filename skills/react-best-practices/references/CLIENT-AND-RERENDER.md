# Client-side fetching and re-render optimization (MEDIUM–HIGH impact)

Read this reference when reviewing client components, hooks, or anything involving `useState`/`useEffect`/`useMemo`/`useCallback` and unnecessary re-renders.

## Client-side data fetching

**Use SWR for automatic deduplication.** Manual `fetch` + `useState`/`useEffect` in each component instance means every instance fetches independently. SWR (https://swr.vercel.app) dedupes, caches, and revalidates across instances: `useSWR('/api/users', fetcher)`. Use `useSWRMutation` for writes.

**Deduplicate global event listeners.** A hook that calls `addEventListener` inside its own `useEffect` registers a new listener per component instance using it. Use `useSWRSubscription` with a shared module-level registry so N instances share 1 listener (register callbacks in a `Map` keyed by event, with one actual `addEventListener` behind the subscription).

**Use passive event listeners for scrolling.** Touch/wheel listeners without `{ passive: true }` force the browser to wait for the listener to finish before it can start scrolling, in case `preventDefault()` is called — causing visible scroll delay.
```typescript
document.addEventListener('touchstart', handler, { passive: true })
```
Use passive for tracking/analytics/logging listeners. Don't use it for custom swipe/zoom gestures that actually call `preventDefault()`.

**Version and minimize localStorage data.** Prefix keys with a version and store only the fields the UI needs — not the full server object.
```typescript
const VERSION = 'v2'
localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify({ theme, language })) // not the full user object
```
Always wrap `getItem`/`setItem` in try/catch — both throw in private browsing (Safari/Firefox) or when quota is exceeded. Versioning lets you migrate schemas cleanly later.

## Re-render optimization

**Don't define components inside components.** (HIGH impact) Defining a component inline creates a new component *type* every render — React unmounts and remounts it, losing state, re-running effects, recreating DOM. Symptoms: inputs losing focus per keystroke, animations restarting, effect cleanup/setup firing every render.
```tsx
// Bad: Avatar is a new type every UserProfile render
function UserProfile({ user, theme }) {
  const Avatar = () => <img src={user.avatarUrl} className={theme} />
  return <Avatar />
}
// Good: pass props instead of closing over parent scope
function Avatar({ src, theme }) { return <img src={src} className={theme} /> }
function UserProfile({ user, theme }) { return <Avatar src={user.avatarUrl} theme={theme} /> }
```

**Calculate derived state during render, not in an effect.** If a value can be computed from current props/state, don't store it in its own state + sync it with `useEffect` — derive it inline during render.
```tsx
// Bad: redundant state + effect, causes an extra render and state drift
const [fullName, setFullName] = useState('')
useEffect(() => setFullName(firstName + ' ' + lastName), [firstName, lastName])
// Good
const fullName = firstName + ' ' + lastName
```

**Subscribe to derived state, not continuous values.** Subscribing to a continuously-changing value (e.g. window width) re-renders on every change even if only a derived boolean matters.
```tsx
// Bad: re-renders on every pixel
const width = useWindowWidth(); const isMobile = width < 768
// Good: re-renders only when the boolean flips
const isMobile = useMediaQuery('(max-width: 767px)')
```

**Defer state reads to the point of use.** Don't subscribe to dynamic state (`useSearchParams`, localStorage) if it's only read inside a callback — read it on demand instead so the component doesn't re-render on every change.
```tsx
// Bad: subscribes to all searchParams changes just to read one value on click
const searchParams = useSearchParams()
const handleShare = () => shareChat(chatId, { ref: searchParams.get('ref') })
// Good: read directly from window at call time
const handleShare = () => shareChat(chatId, { ref: new URLSearchParams(window.location.search).get('ref') })
```

**Put interaction logic in event handlers, not state+effect.** If a side effect is triggered by one specific user action, run it in that handler directly — modeling it as state + effect makes the effect re-run on unrelated dependency changes and risks duplicate firing.
```tsx
// Bad
const [submitted, setSubmitted] = useState(false)
useEffect(() => { if (submitted) { post('/api/register'); showToast('Registered', theme) } }, [submitted, theme])
// Good
function handleSubmit() { post('/api/register'); showToast('Registered', theme) }
```

**Use functional setState updates.** When new state depends on the current value, use the updater-function form — otherwise the callback must list state as a dependency (recreated every change) or risks a stale closure.
```tsx
// Bad: recreated every items change, or stale if dependency forgotten
const addItems = useCallback(n => setItems([...items, ...n]), [items])
// Good: stable reference, always current
const addItems = useCallback(n => setItems(curr => [...curr, ...n]), [])
```

**Use lazy state initialization.** Passing a computed value directly to `useState(expensiveCall())` re-runs that computation on *every* render even though it's only used once — pass a function instead.
```tsx
// Bad: buildSearchIndex() runs every render
const [searchIndex] = useState(buildSearchIndex(items))
// Good: runs once
const [searchIndex] = useState(() => buildSearchIndex(items))
```
Skip this for cheap literals or simple primitives — the function wrapper itself has no benefit there.

**Narrow effect dependencies to primitives.** Depending on a whole object re-runs the effect on any field change, not just the one used.
```tsx
// Bad: re-runs on any user field change
useEffect(() => console.log(user.id), [user])
// Good
useEffect(() => console.log(user.id), [user.id])
```
For threshold-style derived state, compute the boolean outside the effect so it only re-runs on the transition, not every intermediate value (e.g. derive `isMobile = width < 768` first, then depend on `isMobile`).

**Split combined hook computations.** A `useMemo`/`useEffect` that bundles multiple independent steps re-runs all of them when any one dependency changes, even ones unrelated to that dependency.
```tsx
// Bad: changing sortOrder recomputes the filter too
const sorted = useMemo(() => filter(products, category).toSorted(sortOrder), [products, category, sortOrder])
// Good: split so each recomputes only for its own inputs
const filtered = useMemo(() => filter(products, category), [products, category])
const sorted = useMemo(() => filtered.toSorted(sortOrder), [filtered, sortOrder])
```

**Extract expensive work into memoized components.** Wrapping expensive work in `useMemo` inside a component that might early-return (e.g. on `loading`) still runs the computation before the return. Extracting it into its own `memo()`'d component lets the early return skip it entirely.

**Extract a memoized component's non-primitive default parameter to a constant.** A default value like `onClick = () => {}` creates a new function every render, breaking `memo()`'s equality check even when the prop isn't passed.
```tsx
// Bad: new function identity every render
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }) { ... })
// Good
const NOOP = () => {}
const UserAvatar = memo(function UserAvatar({ onClick = NOOP }) { ... })
```

**Don't wrap simple primitive expressions in `useMemo`.** For a cheap boolean/number/string expression, the dependency-comparison overhead of `useMemo` can cost more than just recomputing it.
```tsx
// Bad: unnecessary memo overhead
const isLoading = useMemo(() => user.isLoading || notifications.isLoading, [user.isLoading, notifications.isLoading])
// Good
const isLoading = user.isLoading || notifications.isLoading
```

**Use `useRef` for transient high-frequency values.** Values that change often but don't need to trigger a re-render (mouse position, interval ticks) belong in a ref, updated via direct DOM manipulation if needed — not `useState`.

**Use `startTransition` for non-urgent frequent updates** (e.g. scroll position tracking) so they don't block more urgent UI work.

**Use `useDeferredValue` for expensive derived renders.** When typing triggers an expensive filter/render, defer the *derived* computation so the input itself stays responsive; wrap the expensive part in `useMemo` keyed on the deferred value, or it still recomputes every render.
```tsx
const deferredQuery = useDeferredValue(query)
const filtered = useMemo(() => items.filter(i => fuzzyMatch(i, deferredQuery)), [items, deferredQuery])
```

Note throughout: React Compiler, where enabled, automatically handles many of these memoization cases (`memo`, `useMemo`, static JSX hoisting, dependency tracking) — manual memoization is still correct but may be redundant on a compiled codebase.

## Advanced hook patterns (lower frequency, still worth flagging)

**Don't put `useEffectEvent` results in effect dependency arrays.** An Effect Event's identity intentionally changes every render — including it as a dependency defeats the point and re-runs the effect constantly. Depend on the actual reactive values (e.g. `roomId`), call the Effect Event from inside the effect body.

**Store event handlers in refs for stable subscriptions.** A `useEffect` that re-subscribes whenever a passed-in callback changes identity causes unnecessary unsubscribe/resubscribe churn. Store the handler in a ref (updated via its own effect), or use `useEffectEvent` where available, so the subscription effect itself only depends on stable values like the event name.

**Initialize app-wide state once, not per mount.** `useEffect(() => { initOnce() }, [])` inside a component re-runs if that component remounts (and double-fires in React dev strict mode). Use a module-level guard (`let didInit = false`) or a top-level init in the app's entry module for anything that must truly run once per app load, not once per component mount.

## Sources
* https://swr.vercel.app
* https://react.dev/learn/you-might-not-need-an-effect
* https://react.dev/reference/react/useDeferredValue
* https://react.dev/reference/react/useEffectEvent
