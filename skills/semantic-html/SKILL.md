---
name: semantic-html
description: "Write semantic HTML that serves all users — native elements over ARIA, proper landmarks, heading hierarchy, and accessible forms/tables. Use when creating components, page structures, or reviewing markup."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Frontend, HTML, Accessibility, Semantics, Web]
    category: frontend
    related_skills: [accessibility-frontend, css-coder, frontend-testing]
---

# Semantic HTML

Write HTML that conveys meaning, serves all users, and respects the web platform.

## When to Use

Creating components/page sections; reviewing markup for accessibility/semantics; choosing between native elements and ARIA; structuring heading hierarchy; making interactive elements accessible; building labeled forms with error handling; creating responsive tables.

## Core Principles

**Content realism** — design content is idealized, real content isn't. Account for long sentences/words, images with varying aspect ratios, multi-language support (browsers can translate even if you didn't plan for it), and dynamic content that changes length/structure. Build for real-world content, not just what looks good in a mockup.

**Landmarks-first planning** — plan the full page's landmarks and heading hierarchy before building individual components. This surfaces the right element choices early and avoids overusing landmarks (which dilutes their usefulness).

**Native over ARIA** — first rule of ARIA: if a native element already has the semantics/behavior you need, use it instead of patching a generic element with ARIA. Red flag: high div count + high ARIA count on a non-complex component signals patches instead of foundations.

- *Redundant ARIA* adds noise and can confuse assistive tech: `<ul role="list">` (ul already has list semantics), `<img src="avatar.png" alt="" role="presentation">` (empty alt already suppresses the name), `<span aria-label="Most Popular">Most Popular</span>` (duplicates visible text).
- *Don't override native semantics with `role`* — role changes what AT announces, but native keyboard behavior/states/events stay the same, creating a mismatch. `<input type="checkbox" role="switch">` is wrong (still behaves like a checkbox); use a real checkbox or build a proper switch widget. Only add `role` when you deliberately need different semantics *and* the behavior genuinely matches it.

**Visual vs. semantic hierarchy** — related but not coupled. Pick heading level by document structure; control visual appearance with CSS classes (e.g. a `.u-Heading-XXL` utility) independent of the semantic level.

## Document Structure

**Skip links** — required on any page with nav or other repeated content before the main content. Place as the first focusable element in `<body>`, visually hidden until focused:

```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <a href="#search" class="skip-link">Skip to search</a>
  <header>...</header>
  <nav>...</nav>
  <main id="main-content" tabindex="-1">...</main>
</body>
```
```css
.skip-link { position: absolute; transform: translateY(-100%); }
.skip-link:focus { transform: translateY(0); }
```

- `tabindex="-1"` on `<main>`: `<main>` isn't natively focusable. Without it, activating the skip link scrolls there but doesn't always move keyboard focus — the attribute makes `<main>` programmatically focusable without entering the normal tab order.
- Add more skip links when a page has a prominent search bar, sidebar, or long secondary nav — the goal is cutting Tab presses to reach primary content.
- If a sidebar `<nav>` sits late in the DOM (e.g. after `<main>`), add a "skip to navigation" link so keyboard users don't have to tab through all of main first.
- The primary skip link always targets `<main id="main-content">`; additional ones can target other meaningful landmarks (`<search>`, a sidebar `<nav>`, a prominent form).
- Why it matters: without skip links, a 12-item nav costs keyboard users 12 extra keystrokes on *every* page load.

**Landmark elements:**

| Element | Use When | Notes |
|---|---|---|
| `header` | Page or section header | Can appear multiple times in different contexts |
| `footer` | Page or section footer | Contact info, copyright, related links |
| `nav` | Navigation sections | Must be labelled; don't put "navigation" in the label (screen readers already announce it) |
| `main` | Primary content | Only one per page; must contain the primary `<h1>` |
| `aside` | Tangentially related content | Removable without changing the page's main story (sidebars, ads) |
| `search` | Search functionality | Contains the search form, not the results |
| `form` | User input | Only a landmark when labelled via `aria-labelledby`/`aria-label` |
| `article` | Self-contained content | Would make sense syndicated or standalone |
| `section` | Thematic grouping | Only a landmark when labelled |

- `<main>` must contain the primary `<h1>` — screen reader users often jump straight to `<main>`; an `<h1>` sitting in a `<div>` before it strands them after the title with no context.
```html
<!-- Wrong -->
<header>...</header>
<div class="page-header"><h1>FAQ</h1></div>
<main>...</main>

<!-- Right -->
<header>...</header>
<main id="main-content" tabindex="-1">
  <h1>FAQ</h1>
  ...
</main>
```

- `<section>` without an accessible name behaves like a `<div>` — give it one via `aria-labelledby` to make it a real landmark; if you can't give it a meaningful label, question whether `section` is the right element.
- `<article>` — think beyond blog posts: comments, product cards, social posts, forum posts all qualify. Test: would this content still make sense extracted and dropped elsewhere with no surrounding context?
- `<address>` — per spec, represents contact info for its nearest `article`/`body` ancestor. Use for author/owner contact info, not generic postal addresses (use `<p>` or structured markup for those).
- `<aside>` vs `<section>` — test: would the page still be complete with this content removed? An ad, a related-article link, an author bio → `<aside>`. A "Still need help?" CTA, a key-findings summary, a signup prompt central to the page → `<section>`. When unsure: if it serves the page's primary purpose, it's a labelled `<section>`, not `<aside>`.
- `<aside>` for pull quotes is fine, but don't use `<blockquote>` for a pull quote drawn from the page's own content — `<blockquote>` signals an external/distinct quotation. Use `<p>` inside `<aside>` instead; save `<blockquote>` for genuine external quotes.

## Headings

- One `<h1>` per page; don't skip levels (h1 → h3); the sequence of headings should read as a sensible outline.
- Components with headings: make the level configurable with a sensible default (not every content author understands heading hierarchy), and let the config flow through generic → specific components (e.g. a generic `Card` defaults to `h3`; a `ProductCard` built on it inherits that, set explicitly per the section it's used in).
- Text that looks like a heading but isn't one semantically: style it with a CSS class (e.g. `<p class="u-Heading-L">`) instead of a real heading tag, so it doesn't corrupt the document outline.

## Lists

Use a list when **knowing the item count helps the user** — nav menus, search results, image galleries, process steps. Ask: are these genuinely peers? Would removing one make the rest feel incomplete? Is there an implicit "here are N things"?

| Type | Use When | Example |
|---|---|---|
| `ul` | Unordered collection where count matters | Nav items, search results |
| `ol` | Sequential steps or ranked items | Recipes, instructions, top-10 lists |
| `dl` | Term–description pairs | Glossaries, metadata, key–value pairs |
| `menu` | Toolbar commands | Action buttons, not navigation |

- `ol` takes `reversed` (countdown lists) and `start` (begin at a specific number) — both native, no JS needed.
- `dl` is often overlooked/confused with `details`/`summary` — use it for glossary definitions, metadata display, any term with one or more descriptions. A single `dt` can have multiple `dd`s.
- Decorative separators via CSS `::before`/`::after` (e.g. a breadcrumb `›`) are automatically excluded from the accessibility tree — no extra markup needed, and `aria-hidden` as a *CSS property* is invalid and does nothing. If injecting a separator via HTML instead, use `<span aria-hidden="true">`.

## Interactive Elements

**Buttons vs. links** — traditional rule: buttons do things, links go places. Progressive-enhancement lens: if a URL gives a meaningful fallback when JS fails, a link is valid even for action-like interactions.

| Interaction | Default | Consider a link when |
|---|---|---|
| Show more content | `button` | URL params could load it server-side |
| Toggle view (grid/list) | `button` | URL could preserve the view preference |
| Copy to clipboard | `button` | Copied content is a shareable URL |
| Tab selection | `button` | URL could load the specific tab's content |

Key question: what happens if JS fails? If a URL degrades gracefully, prefer the link.

**Unique accessible names for repeated buttons** — when the same action repeats (e.g. "Add to cart" on every product card), each instance needs a unique accessible name so screen reader users know which item it targets. Keep the *visible* label generic ("Add to cart" — sighted users get context from position); make the *accessible* name specific:

```html
<!-- aria-label with full context -->
<button aria-label="Add Nike Pegasus 41 to cart">Add to cart</button>

<!-- visually hidden text -->
<button>Add to cart <span class="visually-hidden">Nike Pegasus 41</span></button>

<!-- aria-describedby pointing at the product heading -->
<article>
  <h3 id="product-42">Nike Pegasus 41</h3>
  <button aria-describedby="product-42">Add to cart</button>
</article>
```

**Disabling controls** — `aria-disabled="true"` communicates state but doesn't prevent interaction. `disabled` on a `<button>` does both. For links, `aria-disabled="true"` alone is insufficient (still focusable/activatable) — use `<button disabled>` instead when truly unavailable, remove `href` to kill activation, or handle `keydown`/`click` explicitly if it must stay focusable.

**Popover API for lightweight overlays** — for dropdowns, action menus, and non-modal overlays, prefer the `popover` attribute over hand-rolled ARIA widget patterns:

```html
<button popovertarget="user-menu">
  <img src="avatar.png" alt="" />
  <span>Alice</span>
</button>
<ul id="user-menu" popover>
  <li><a href="/profile">Profile</a></li>
  <li><a href="/settings">Settings</a></li>
  <li><button>Sign out</button></li>
</ul>
```
The browser handles `aria-expanded` on the trigger, light-dismiss, focus, and keyboard interaction — no `role="menu"`/`role="menuitem"`/`role="none"` needed; the list stays a plain `<ul>` of links/buttons. Reach for true ARIA menu patterns only when building an actual application menu (menubar/menuitem/submenu) mirroring desktop behavior — most site nav and dropdowns should use Popover or a simple disclosure instead, since ARIA menu patterns have strict keyboard requirements (Home/End/character nav) that are easy to get wrong.

**Details/summary** — good for progressive disclosure (FAQs, expandable sections, collapsible nav). Not a substitute for a `<button>`-controlled widget needing real ARIA roles (`role="menu"`, `role="dialog"`) — dropdowns/menus/modal triggers need `<button>` so the correct pattern can be applied; `<details>/<summary>` has its own implicit semantics and can't meaningfully carry `aria-expanded` or menu roles.

## Forms

**Fieldset/legend for thematic grouping** (not layout) — address fields, personal-info sections, consent checkboxes, payment details, settings sections. Use `<fieldset>/<legend>` instead of `<section>/<h2>` whenever a region groups *inputs* — screen readers announce the legend before each field in the group, giving persistent context that `<section>/<h2>` doesn't. Benefits: enables progressive disclosure, reduces "wall of form fields" overwhelm, gives screen reader users context. Legends can be visually hidden while remaining in the accessible name.

**Grouping search/filter controls** — `<search>` wraps the *whole* search/filter interface, not just the text input:

```html
<!-- Correct -->
<search aria-label="Filter employees">
  <label for="q">Search</label>
  <input type="search" id="q" name="q" />
  <label for="dept">Department</label>
  <select id="dept" name="dept">...</select>
  <button type="submit">Apply filters</button>
</search>

<!-- Wrong: filter select left orphaned outside the landmark -->
<search><input type="search" /></search>
<select>...</select>
```

**Labels** — always use a real `<label>` element, no exceptions. Visually hidden labels are fine when design calls for it. Never use placeholder text as a label substitute (disappears on input — bad for cognitive load/stress/distraction — and usually has poor contrast and no persistent identification), and never reach for `aria-label` when a `<label>` would work.

**Required fields** — `required` tells assistive tech the field is required, but sighted users need a visual cue too. Pair it with a visible indicator and explain the convention:

```html
<fieldset>
  <legend>Contact details <span aria-hidden="true">*</span> required fields</legend>
  <label for="name">Full name <span aria-hidden="true">*</span></label>
  <input type="text" id="name" required />
</fieldset>
```
`aria-hidden` on the asterisk stops screen readers announcing "asterisk" (they already get required state from the attribute); the legend/page note explains the convention visually.

**Hint text** — associate via `aria-describedby` so screen readers announce the hint right after the label:
```html
<label for="email">Email address</label>
<p id="email-hint" class="hint">We'll only use this to send your receipt.</p>
<input type="email" id="email" aria-describedby="email-hint" />
```
Multiple associations are fine — space-separated IDs cover both hint and error: `aria-describedby="email-hint email-error"`.

**Error messages** (current best practice, given `aria-errormessage` browser-support gaps): set `aria-invalid="true"` on the invalid input, associate the message via `aria-describedby`, make the message actionable (state the problem *and* the fix), and consider `aria-live` on the error container for dynamically-shown (on-blur) errors.
```html
<label for="email">Email</label>
<input type="email" id="email" aria-invalid="true" aria-describedby="email-error" />
<p id="email-error" class="error">Enter a valid email address, like name@example.com</p>
```

## Tables

Use a table when data has **meaningful relationships in both dimensions** — rows and columns both matter, headers map clearly to data, every row has the same columns, each column holds one data type. Don't use one for a simple one-dimensional list, key–value pairs (use `dl`), form layout, or hierarchical data (use nested lists).

Baseline semantics every table needs: `caption` (purpose), `thead`/`tbody`/`tfoot` (structure), `th` with `scope` (header direction).

Responsive tables, in order of preference: (1) hide non-essential columns with a "show full table" option — keeps the main takeaways visible; (2) horizontal scroll — preserves semantics but can be hard for users with motor difficulties; (3) duplicate as cards on mobile — last resort, maintain accessibility in both versions. Note: modern browsers (Safari included) no longer strip table semantics under `display: grid`/`display: flex`, which opens up more responsive layout options without losing structure.

## Code Review Checklist

**Good signs:** skip link(s) as the first focusable element(s); landmarks used appropriately; logical heading hierarchy; native interactive elements used correctly; repeated action buttons have unique accessible names; forms have proper labels/fieldsets/hint associations; required fields visually indicated with an explained convention; tables have full semantic structure; ARIA used sparingly and correctly.

**Warning signs:** no skip link before a `<nav>`/repeated header content; high div count in a non-complex component; ARIA compensating for missing native semantics; redundant ARIA roles (`role="list"` on `<ul>`, `role="presentation"` on `<img alt="">`); a `role` changing semantics without matching behavior; `aria-label` duplicating visible text; an ARIA menu pattern used for a simple dropdown (use Popover instead); placeholders used as labels; heading levels chosen for visual size, not structure; generic elements with click handlers instead of buttons/links; tables used for layout; missing form labels; repeated buttons with identical accessible names ("Add to cart" × 6); `aria-disabled` on `<a>` without actually preventing keyboard activation; filter/search controls scattered outside a `<search>`/`<form>`; settings sections using `<section>/<h2>` instead of `<fieldset>/<legend>`.

## References

- `references/element-decision-trees.md` — quick decision frameworks for element selection
- `references/heading-patterns.md` — component heading patterns and configuration strategies

## Further Reading

[HTML Living Standard: Sections](https://html.spec.whatwg.org/dev/sections.html) · [Grouping Content](https://html.spec.whatwg.org/dev/grouping-content.html) · [Forms](https://html.spec.whatwg.org/dev/forms.html) · [Tables](https://html.spec.whatwg.org/dev/tables.html) · [MDN: ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)
