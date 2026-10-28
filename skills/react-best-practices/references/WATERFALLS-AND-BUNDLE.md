# Waterfalls and bundle size (CRITICAL impact)

Read this reference when reviewing async data-fetching code or anything affecting initial JS bundle size. These are the two highest-impact categories — sequential awaits and oversized bundles are usually the biggest wins available.

## Eliminating waterfalls

**Promise.all() for independent operations.** Sequential `await`s that don't depend on each other cost a full round trip each.
```typescript
// Bad: 3 round trips
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
// Good: 1 round trip
const [user, posts, comments] = await Promise.all([fetchUser(), fetchPosts(), fetchComments()])
```

**Dependency-based parallelization.** When some calls depend on others, don't force everything into one `Promise.all()` that waits on the slowest unrelated dependency — start independent work immediately and only chain what truly depends on it.
```typescript
// Bad: profile waits for config unnecessarily
const [user, config] = await Promise.all([fetchUser(), fetchConfig()])
const profile = await fetchProfile(user.id)
// Good: create all promises first, resolve what's needed when needed
const userPromise = fetchUser()
const profilePromise = userPromise.then(u => fetchProfile(u.id))
const [user, config, profile] = await Promise.all([userPromise, fetchConfig(), profilePromise])
```
For complex dependency graphs, `better-all` (https://github.com/shuding/better-all) auto-maximizes parallelism.

**Prevent waterfall chains in API routes / Server Actions.** Start independent operations immediately even if you await them later.
```typescript
// Bad: config waits for auth, data waits for both
const session = await auth(); const config = await fetchConfig(); const data = await fetchData(session.user.id)
// Good: start immediately, await when needed
const sessionPromise = auth(); const configPromise = fetchConfig()
const session = await sessionPromise
const [config, data] = await Promise.all([configPromise, fetchData(session.user.id)])
```

**Defer await until needed.** Move `await` into the branch that actually uses the result, so skipped branches don't pay for it.
```typescript
// Bad: always awaits userData even if skipProcessing is true
async function handleRequest(userId, skip) {
  const userData = await fetchUserData(userId)
  if (skip) return { skipped: true }
  return processUserData(userData)
}
// Good
async function handleRequest(userId, skip) {
  if (skip) return { skipped: true }
  const userData = await fetchUserData(userId)
  return processUserData(userData)
}
```
Also order independent checks so cheap/likely-to-fail ones run before expensive fetches (e.g. check resource existence before fetching permissions, if a missing resource should short-circuit first).

**Check cheap conditions before async flags.** If a branch needs both `await getFlag()` and a cheap sync condition, check the sync condition first — don't pay for the network/flag call when the sync check already fails.
```typescript
// Bad
const flag = await getFlag(); if (flag && cheapCondition) { /* ... */ }
// Good
if (cheapCondition) { const flag = await getFlag(); if (flag) { /* ... */ } }
```
Keep original order if the sync condition is itself expensive or depends on the flag.

**Strategic Suspense boundaries.** Don't await data in an async component before returning JSX if only part of the layout needs it — wrap just that part in `<Suspense>` so the rest renders immediately.
```tsx
// Bad: whole page blocks on data
async function Page() { const data = await fetchData(); return <div><Sidebar/><Header/><DataDisplay data={data}/><Footer/></div> }
// Good: only DataDisplay blocks
function Page() { return <div><Sidebar/><Header/><Suspense fallback={<Skeleton/>}><DataDisplay/></Suspense><Footer/></div> }
async function DataDisplay() { const data = await fetchData(); return <div>{data.content}</div> }
```
Share one promise across siblings with `use(promise)` to avoid duplicate fetches. Skip this pattern when the data affects layout/positioning, is SEO-critical above the fold, is cheap/fast, or when avoiding a loading→content layout shift matters more than initial paint speed.

## Bundle size optimization

**Avoid barrel file imports.** Popular icon/component libraries can have thousands of re-exports in their entry file — importing from the barrel can cost 200–800ms per cold start even if you only use a few exports.
```tsx
// Bad: loads the whole library's module graph
import { Check, X, Menu } from 'lucide-react'
```
Prefer Next.js's `experimental.optimizePackageImports: ['lucide-react', ...]` in `next.config.js` (keeps normal import syntax, transforms at build time, preserves types) over manual deep imports (`import Button from '@mui/material/Button'`), since some libraries' deep paths lack type declarations. Commonly affected: `lucide-react`, `@mui/material`, `@tabler/icons-react`, `react-icons`, `@radix-ui/react-*`, `lodash`, `date-fns`, `rxjs`.

**Dynamic imports for heavy components.** Lazy-load large components not needed on initial render.
```tsx
// Bad: bundles with main chunk
import { MonacoEditor } from './monaco-editor'
// Good
const MonacoEditor = dynamic(() => import('./monaco-editor').then(m => m.MonacoEditor), { ssr: false })
```

**Defer non-critical third-party libraries.** Analytics/logging/error-tracking don't block interaction — load after hydration with `dynamic(..., { ssr: false })`, same pattern as above.

**Conditional module loading.** Load large data/modules only when a feature is actually activated (e.g. inside `useEffect` gated on a flag, with a `typeof window !== 'undefined'` guard so it doesn't bloat the SSR bundle).

**Preload based on user intent.** Preload a heavy bundle on hover/focus before the user clicks, to hide the import cost.
```tsx
<button onMouseEnter={() => { if (typeof window !== 'undefined') void import('./monaco-editor') }} onClick={onClick}>Open Editor</button>
```

**Prefer statically analyzable import/file paths.** If a path is composed from a variable too dynamically, bundlers either include a broad set of possible files, can't analyze the import, or (in Next.js) widen file tracing — larger server bundles, slower builds, worse cold starts.
```ts
// Bad: bundler can't tell what's importable
const Page = await import(PAGE_MODULES[pageName])
// Good: explicit map of allowed modules
const PAGE_MODULES = { home: () => import('./pages/home'), settings: () => import('./pages/settings') } as const
const Page = await PAGE_MODULES[pageName]()
```
Same principle applies to file-system paths built with `path.join(cwd, someVar)` in server code — prefer literal paths at each callsite over composed ones.

## Sources
* https://nextjs.org/docs/app/api-reference/config/next-config-js/output
* https://vercel.com/blog/how-we-optimized-package-imports-in-next-js
* https://github.com/shuding/better-all
