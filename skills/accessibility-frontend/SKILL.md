---
name: accessibility-frontend
description: "Audit and fix web accessibility against WCAG 2.2."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Frontend, Accessibility, A11y, WCAG, Web]
    category: frontend
    related_skills: [web-quality-audit, performance-frontend, core-web-vitals, seo, best-practices-frontend]
---

# Accessibility (a11y)

WCAG 2.2-based guidelines for making content usable by everyone, including people with disabilities. Pairs with Lighthouse accessibility audits for evidence.

## Evidence-led workflow

On a rendered page:

1. Run an accessibility audit (Lighthouse, axe, or equivalent tooling) to get failing nodes.
2. Use the failed nodes to localize the component — don't scan the whole repo for generic patterns.
3. Inspect the accessibility tree (names, roles, states, landmarks, heading structure) and walk the flow with keyboard only.
4. Fix the source, then re-run the same audit + manual check.

If live tooling isn't available, fall back to Lighthouse CLI or axe plus the same manual checks. Automated tools only catch a subset of real barriers — a 100 score isn't WCAG conformance, and a low score isn't the full picture either.

## WCAG principles: POUR

| Principle | Description |
|---|---|
| **P**erceivable | Content reaches users through more than one sense |
| **O**perable | Interface works for everyone, keyboard included |
| **U**nderstandable | Content and interaction are predictable |
| **R**obust | Works with assistive technology |

## Conformance levels

| Level | Requirement | Target |
|---|---|---|
| **A** | Minimum | Must pass |
| **AA** | Standard | Should pass — legal requirement in many places |
| **AAA** | Enhanced | Nice to have |

---

## Perceivable

### Text alternatives (1.1)

Every image needs alt text — descriptive for meaningful images, empty (`alt=""`) for decorative ones, with `aria-describedby` for complex ones needing a longer description:
```html
<img src="chart.png" alt="Bar chart showing 40% increase in Q3 sales">
<img src="decorative-border.png" alt="" role="presentation">
<figure>
  <img src="infographic.png" alt="2024 market trends infographic" aria-describedby="infographic-desc">
  <figcaption id="infographic-desc"><!-- detailed description --></figcaption>
</figure>
```

Icon-only buttons need an accessible name — via `aria-label` or visually-hidden text:
```html
<button aria-label="Open menu"><svg aria-hidden="true"><!-- icon --></svg></button>
<button><svg aria-hidden="true"><!-- icon --></svg><span class="visually-hidden">Open menu</span></button>
```
```css
.visually-hidden {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;
}
```

### Color contrast (1.4.3, 1.4.6)

| Text size | AA minimum | AAA enhanced |
|---|---|---|
| Normal (< 18px / < 14px bold) | 4.5:1 | 7:1 |
| Large (≥ 18px / ≥ 14px bold) | 3:1 | 4.5:1 |
| UI components & graphics | 3:1 | 3:1 |

```css
.high-contrast { color: #333; background: #fff; } /* ~7:1 */
:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; } /* 1.4.11: focus needs ≥3:1 too */
```

Never signal state with color alone — pair it with an icon and text:
```html
<div class="field-error">
  <input aria-invalid="true" aria-describedby="email-error">
  <span id="email-error" class="error-message"><svg aria-hidden="true"></svg>Please enter a valid email address</span>
</div>
```

### Media alternatives (1.2)
```html
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="en" label="English" default>
  <track kind="descriptions" src="descriptions.vtt" srclang="en" label="Descriptions">
</video>
<audio controls><source src="podcast.mp3" type="audio/mp3"></audio>
<details><summary>Transcript</summary><p>Full transcript text...</p></details>
```

---

## Operable

### Keyboard accessible (2.1)

Everything must work by keyboard. Prefer native elements (`<button>`, `<a href>`, form controls) — they get focus, Enter/Space activation, and assistive-tech semantics for free:
```html
<!-- ❌ not focusable, no keyboard activation -->
<div class="card" onclick="handleAction()">Open</div>
<!-- ✅ -->
<button type="button" onclick="handleAction()">Open</button>
```
Only hand-roll keyboard handling when a native element genuinely isn't an option — and never add it on top of a real `<button>`, since Enter/Space already fire its click:
```javascript
element.setAttribute('role', 'button');
element.setAttribute('tabindex', '0');
element.addEventListener('click', handleAction);
element.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleAction(); }
});
```
No keyboard traps — users must Tab into and out of every component. Native `<dialog>` handles this for free; see [modal focus trap](references/A11Y-PATTERNS.md#modal-focus-trap) otherwise.

### Focus visible (2.4.7)
```css
*:focus { outline: none; }               /* ❌ never do this alone */
:focus-visible {                          /* ✅ keyboard-only focus ring */
  outline: 2px solid currentColor; outline-offset: 2px;
}
button:focus-visible { box-shadow: 0 0 0 3px rgba(0, 95, 204, 0.5); } /* or a brand color, verified ≥3:1 */
```

### Focus not obscured (2.4.11) — new in 2.2

A focused element can't be fully hidden behind sticky headers/footers/overlays (AAA 2.4.12: no part hidden at all):
```css
:target { scroll-margin-top: 80px; }
:focus { scroll-margin-top: 80px; scroll-margin-bottom: 60px; }
```

### Skip links (2.4.1)
Let keyboard users bypass repeated nav. Full markup: [skip link pattern](references/A11Y-PATTERNS.md#skip-link).

### Target size (2.5.8) — new in 2.2
Interactive targets ≥ **24×24 CSS px** (AA); exceptions for inline links, browser-controlled sizing, and non-overlapping targets.
```css
button, [role="button"], input[type="checkbox"] + label, input[type="radio"] + label {
  min-width: 24px; min-height: 24px;
}
.touch-target { min-width: 44px; min-height: 44px; display: inline-flex; align-items: center; justify-content: center; } /* comfortable */
```

### Dragging movements (2.5.7) — new in 2.2
Any drag action needs a single-pointer alternative (buttons, inputs). See [dragging movements pattern](references/A11Y-PATTERNS.md#dragging-movements).

### Timing (2.2)
Let users extend time limits:
```javascript
function showSessionWarning() {
  const modal = createModal({
    title: 'Session Expiring', content: 'Your session will expire in 2 minutes.',
    actions: [{ label: 'Extend session', action: extendSession }, { label: 'Log out', action: logout }],
    timeout: 120000
  });
}
```

### Motion (2.3)
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important;
  }
}
```

---

## Understandable

### Page language (3.1.1)
```html
<html lang="en">
<p>The French word for hello is <span lang="fr">bonjour</span>.</p>
```

### Consistent navigation (3.2.3)
```html
<nav aria-label="Main">
  <ul><li><a href="/" aria-current="page">Home</a></li><li><a href="/products">Products</a></li></ul>
</nav>
```

### Consistent help (3.2.6) — new in 2.2
A repeated help mechanism (contact, chat widget, FAQ) must stay in the **same relative position** on every page — don't make users re-find it.

### Form labels (3.3.2)
Every input needs a programmatically associated label. Explicit/implicit/with-instructions examples: [form labels pattern](references/A11Y-PATTERNS.md#form-labels).

### Error handling (3.3.1, 3.3.3)
Announce errors via `role="alert"`/`aria-live`, set `aria-invalid="true"`, focus the first error on submit. Full markup: [error handling pattern](references/A11Y-PATTERNS.md#error-handling).

### Redundant entry (3.3.7) — new in 2.2
Don't make users re-type what they already gave you this session — auto-populate or let them pick a prior value. Exceptions: security re-confirmation, expired data.
```html
<fieldset>
  <legend>Shipping address</legend>
  <label><input type="checkbox" id="same-as-billing" checked> Same as billing address</label>
</fieldset>
```

### Accessible authentication (3.3.8) — new in 2.2
Login can't require a cognitive test (remembering a password, solving a puzzle) unless paste/autofill works, an alternative exists (passkey, SSO, email link), or it's object/personal-content recognition (AA only).
```html
<input type="password" id="password" autocomplete="current-password">
<button type="button">Sign in with passkey</button>
<button type="button">Email me a login link</button>
```

---

## Robust

### ARIA usage (4.1.2)
Prefer native elements over ARIA-on-a-div:
```html
<!-- ❌ --> <div role="button" tabindex="0">Click me</div>
<!-- ✅ --> <button>Click me</button>
```
When ARIA is genuinely needed, get the roles/states right — see [ARIA tabs pattern](references/A11Y-PATTERNS.md#aria-tabs).

### Live regions (4.1.3)
`aria-live` announces dynamic changes without stealing focus — see [live regions pattern](references/A11Y-PATTERNS.md#live-regions-and-notifications).

---

## Testing checklist

**Automated:**
```bash
npx lighthouse https://example.com --only-categories=accessibility
npm install @axe-core/cli -g && axe https://example.com
```

**Manual:**
- [ ] Keyboard: Tab through the whole page, Enter/Space activate
- [ ] Screen reader: VoiceOver (Mac), NVDA (Windows), TalkBack (Android)
- [ ] Zoom: usable at 200%
- [ ] High contrast mode
- [ ] `prefers-reduced-motion: reduce`
- [ ] Focus order matches visual order
- [ ] Targets ≥ 24×24px

Shortcuts: [screen reader commands](references/A11Y-PATTERNS.md#screen-reader-commands).

## Fix priority

**Critical:** missing form labels · missing alt text · insufficient contrast · keyboard traps · no focus indicator
**Serious:** missing page language · missing heading structure · vague link text · autoplay media · missing skip links
**Moderate:** missing icon ARIA labels · inconsistent nav · missing error ID · uncontrolled timing · missing landmarks

## References

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Deque axe Rules](https://dequeuniversity.com/rules/axe/)
- [WCAG criteria reference](references/WCAG.md)
- [Accessibility code patterns](references/A11Y-PATTERNS.md)
