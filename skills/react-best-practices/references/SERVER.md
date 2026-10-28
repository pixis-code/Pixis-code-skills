# Server-side performance and safety (HIGH impact)

Read this reference when reviewing React Server Components, Server Actions, or Next.js route handlers.

**Authenticate Server Actions like API routes.** A `"use server"` function is a public endpoint — it can be invoked directly, bypassing middleware or page-level guards. Verify auth/authorization *inside every action*, not just upstream.
```typescript
// Bad: no check at all
'use server'
export async function deleteUser(userId: string) { await db.user.delete({ where: { id: userId } }) }
// Good
'use server'
export async function deleteUser(userId: string) {
  const session = await verifySession()
  if (!session) throw unauthorized('Must be logged in')
  if (session.user.role !== 'admin' && session.user.id !== userId) throw unauthorized('Cannot delete other users')
  await db.user.delete({ where: { id: userId } })
}
```
Validate input → authenticate → authorize → mutate, in that order, when combining with schema validation (e.g. zod).

**Avoid shared module state for request data.** Server renders can run concurrently in the same process. A mutable module-level variable storing request/user data can leak across concurrent requests — real race condition, real security bug (user A's data in user B's response).
```tsx
// Bad: race condition between concurrent requests
let currentUser = null
export default async function Page() { currentUser = await auth(); return <Dashboard/> }
// Good: keep request data in the render tree, not module scope
export default async function Page() { const user = await auth(); return <Dashboard user={user}/> }
```
Safe exceptions: immutable static config loaded once, caches intentionally designed and keyed for cross-request reuse, process-wide singletons with no request-specific mutable data.

**Parallel data fetching with component composition.** RSCs execute sequentially within a tree — a parent's `await` blocks siblings defined after it in the same function, even if their data has no dependency. Restructure via composition so independent fetches start together.
```tsx
// Bad: Sidebar waits for Page's own await to finish
export default async function Page() { const header = await fetchHeader(); return <div>{header}<Sidebar/></div> }
// Good: both fetch simultaneously, each in its own async component
async function Header() { const data = await fetchHeader(); return <div>{data}</div> }
async function Sidebar() { const items = await fetchSidebarItems(); return <nav>{items.map(renderItem)}</nav> }
export default function Page() { return <div><Header/><Sidebar/></div> }
```

**Parallel nested data fetching.** When fetching nested data in parallel, chain the dependent fetch *within* each item's own promise so one slow item doesn't block the rest.
```tsx
// Bad: ALL authors wait until EVERY chat has loaded
const chats = await Promise.all(chatIds.map(id => getChat(id)))
const chatAuthors = await Promise.all(chats.map(chat => getUser(chat.author)))
// Good: each item independently chains getChat -> getUser
const chatAuthors = await Promise.all(chatIds.map(id => getChat(id).then(chat => getUser(chat.author))))
```

**Minimize serialization at RSC boundaries.** Everything passed from a Server Component to a Client Component is serialized into the HTML/RSC payload — size matters. Pass only the fields the client actually uses, not the whole object.
```tsx
// Bad: serializes all 50 fields of user
return <Profile user={user} />  // client only reads user.name
// Good
return <Profile name={user.name} />
```

**Avoid duplicate serialization in RSC props.** Serialization dedupes by object *reference*, not value — passing both an array and a transformed copy (`.toSorted()`, `.filter()`, `.map()`, spread) serializes both. Do transforms client-side instead.
```tsx
// Bad: sends 6 strings (2 arrays x 3 items each)
<ClientList usernames={usernames} usernamesOrdered={usernames.toSorted()} />
// Good: send once, transform in the client component with useMemo
<ClientList usernames={usernames} />
```
Impact is highest for primitive arrays (fully duplicated); object arrays duplicate only the array wrapper since nested objects still dedupe by reference.

**Per-request dedup with `React.cache()`.** Wraps a function so repeat calls within one request return the cached result — mainly for DB queries, auth checks, and other non-`fetch` async work (Next.js's `fetch` is already auto-deduped per request). Uses shallow equality (`Object.is`) on arguments, so inline object args defeat it.
```typescript
// Bad: new object every call -> always a cache miss
const getUser = cache(async (params: { uid: number }) => db.user.findUnique({ where: { id: params.uid } }))
getUser({ uid: 1 }); getUser({ uid: 1 })  // runs twice
// Good: primitive args use value equality
const getUser = cache(async (uid: number) => db.user.findUnique({ where: { id: uid } }))
getUser(1); getUser(1)  // second call hits cache
```

**Cross-request LRU caching.** `React.cache()` only lives for one request. For data reused across a user's sequential requests within seconds, use an LRU cache (e.g. `lru-cache`) instead. Especially effective with Vercel Fluid Compute, where concurrent requests can share the same function instance; in traditional serverless, each invocation is isolated, so consider Redis instead.

**Hoist static I/O to module level.** Reading the same font/logo/config file or template on every request wastes I/O. Module-level code runs once per module load, not per request.
```typescript
// Bad: re-fetches font/logo on every request
export async function GET() { const fontData = await fetch(...).then(r => r.arrayBuffer()); ... }
// Good: starts once at module init, awaited inside the handler
const fontData = fetch(...).then(r => r.arrayBuffer())
export async function GET() { const [font] = await Promise.all([fontData]); ... }
```
Use for assets that don't vary per request. Don't use for per-user/per-request data, files that change at runtime (use TTL caching instead), or very large files that would bloat memory.

**Use `after()` for non-blocking operations.** Next.js's `after()` schedules work (logging, analytics, cache invalidation) to run after the response is already sent, instead of blocking it.
```tsx
// Bad: response waits for logging
await updateDatabase(request); await logUserAction({ userAgent })
return Response.json({ status: 'success' })
// Good
await updateDatabase(request)
after(async () => { await logUserAction({ userAgent }) })
return Response.json({ status: 'success' })
```
Runs even if the response fails/redirects; works in Server Actions, Route Handlers, and Server Components.

## Sources
* https://nextjs.org/docs/app/guides/authentication
* https://react.dev/reference/react/cache
* https://github.com/isaacs/node-lru-cache
* https://nextjs.org/docs/app/api-reference/functions/after
