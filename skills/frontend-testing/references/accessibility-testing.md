# Accessibility Testing

Automated accessibility testing catches common issues early. Combine with manual testing and assistive-technology validation for comprehensive coverage.

## Limitations of Automated Testing

Automated tools detect approximately 30-40% of accessibility issues. They catch: missing labels and alt text, color-contrast violations, invalid ARIA attributes, duplicate IDs, missing landmark regions.

They cannot catch: logical reading order, meaningful link text in context, appropriate focus management, keyboard-trap issues in complex flows, whether content is actually understandable.

**Always combine automated testing with manual review and user testing.**

## Playwright + axe-core Integration

### Setup

```bash
npm install @axe-core/playwright --save-dev
```

### Basic page scan

```javascript
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test.describe("Homepage", () => {
  test("has no automatically detectable accessibility violations", async ({ page }) => {
    await page.goto("/");
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });
});
```

### Wait for page state

Always ensure the page is in the expected state before scanning:

```javascript
test("navigation menu is accessible when open", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /menu/i }).click();
  await page.getByRole("navigation", { name: /main/i }).waitFor();

  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

### Scan specific regions

```javascript
test("checkout form is accessible", async ({ page }) => {
  await page.goto("/checkout");
  const results = await new AxeBuilder({ page })
    .include("#checkout-form")
    .analyze();
  expect(results.violations).toEqual([]);
});
```

### Exclude known issues

```javascript
const results = await new AxeBuilder({ page })
  .exclude("#third-party-widget")  // can't control this
  .exclude("[data-ad-unit]")       // ads managed externally
  .analyze();
```

**Document why exclusions exist. Remove them when fixed.**

## WCAG Targeting

```javascript
// WCAG 2.1 Level AA (most common compliance target)
const results = await new AxeBuilder({ page })
  .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
  .analyze();

// WCAG 2.2 (latest standard)
const results = await new AxeBuilder({ page })
  .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
  .analyze();

// Best practices (not WCAG requirements but recommended)
const results = await new AxeBuilder({ page }).withTags(["best-practice"]).analyze();
```

| Target | Tags |
|--------|------|
| WCAG 2.1 AA | `["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]` |
| WCAG 2.2 AA | Add `"wcag22aa"` |
| Section 508 | `["section508"]` |
| Best practices | `["best-practice"]` |

## Creating Reusable Fixtures

```javascript
// fixtures/axe.js
import { test as base } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

export const test = base.extend({
  makeAxeBuilder: async ({ page }, use) => {
    const makeAxeBuilder = () => new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .exclude("#cookie-banner")          // known third-party issue
      .exclude("[data-testid='ad-unit']");
    await use(makeAxeBuilder);
  },
});

export { expect } from "@playwright/test";
```

```javascript
import { test, expect } from "./fixtures/axe";

test("product page is accessible", async ({ page, makeAxeBuilder }) => {
  await page.goto("/products/123");
  const results = await makeAxeBuilder().analyze();
  expect(results.violations).toEqual([]);
});
```

## Handling Violations

### Understanding results

```javascript
const results = await new AxeBuilder({ page }).analyze();

results.violations.forEach(violation => {
  console.log(`Rule: ${violation.id}`);
  console.log(`Impact: ${violation.impact}`);  // minor, moderate, serious, critical
  console.log(`Description: ${violation.description}`);
  console.log(`Help: ${violation.helpUrl}`);

  violation.nodes.forEach(node => {
    console.log(`  Element: ${node.html}`);
    console.log(`  Fix: ${node.failureSummary}`);
  });
});
```

### Impact levels

| Level | Description | Priority |
|-------|-------------|----------|
| Critical | Blocks access for some users | Fix immediately |
| Serious | Major barriers | Fix soon |
| Moderate | Inconsistencies | Plan to fix |
| Minor | Annoyances | Improve when possible |

### Progressive enforcement

Start permissive, tighten over time:

```javascript
// Phase 1: only critical issues fail
const criticalViolations = results.violations.filter(v => v.impact === "critical");
expect(criticalViolations).toEqual([]);

// Phase 2: critical and serious
const seriousViolations = results.violations.filter(v => ["critical", "serious"].includes(v.impact));
expect(seriousViolations).toEqual([]);

// Phase 3: all violations (goal state)
expect(results.violations).toEqual([]);
```

### Disable specific rules

```javascript
const results = await new AxeBuilder({ page })
  .disableRules(["color-contrast"])  // tracked in JIRA-123
  .analyze();
```

**Document why rules are disabled. Remove when fixed.**

## Integration Patterns

### Per-component tests

```javascript
test.describe("Button component", () => {
  test("default button is accessible", async ({ page }) => {
    await page.goto("/storybook/button--default");
    const results = await new AxeBuilder({ page }).include("#storybook-root").analyze();
    expect(results.violations).toEqual([]);
  });

  test("disabled button is accessible", async ({ page }) => {
    await page.goto("/storybook/button--disabled");
    const results = await new AxeBuilder({ page }).include("#storybook-root").analyze();
    expect(results.violations).toEqual([]);
  });
});
```

### Critical user flows

Scan at each step of important journeys:

```javascript
test("checkout flow is accessible at each step", async ({ page }) => {
  await page.goto("/cart");
  let results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);

  await page.getByRole("link", { name: /checkout/i }).click();
  await page.getByRole("heading", { name: /shipping/i }).waitFor();
  results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);

  await page.getByRole("button", { name: /continue/i }).click();
  await page.getByRole("heading", { name: /payment/i }).waitFor();
  results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

### After dynamic content

Always re-scan after content changes:

```javascript
test("modal is accessible when opened", async ({ page }) => {
  await page.goto("/");
  let results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);

  await page.getByRole("button", { name: /settings/i }).click();
  await page.getByRole("dialog").waitFor();

  results = await new AxeBuilder({ page }).include("[role='dialog']").analyze();
  expect(results.violations).toEqual([]);
});
```

## Common Issues and Fixes

### Missing form labels

```html
<!-- BAD -->
<input type="email" placeholder="Email">

<!-- GOOD -->
<label for="email">Email address</label>
<input id="email" type="email">

<!-- ALSO GOOD (visually hidden label) -->
<label for="search" class="visually-hidden">Search products</label>
<input id="search" type="search" placeholder="Search...">
```

### Color contrast

```css
/* BAD: 2.61:1 ratio */
.muted-text { color: #a0a0a0; background: #ffffff; }

/* GOOD: 4.5:1+ ratio for normal text */
.muted-text { color: #6b6b6b; background: #ffffff; }
```

### Missing button names

```html
<!-- BAD -->
<button><svg>...</svg></button>

<!-- GOOD -->
<button aria-label="Close dialog"><svg>...</svg></button>

<!-- ALSO GOOD -->
<button>
  <svg aria-hidden="true">...</svg>
  <span class="visually-hidden">Close dialog</span>
</button>
```

### Duplicate IDs

```html
<!-- BAD -->
<input id="email" />
<input id="email" />  <!-- Duplicate! -->

<!-- GOOD -->
<input id="billing-email" />
<input id="shipping-email" />
```

## References

- [axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [Playwright Accessibility Testing](https://playwright.dev/docs/accessibility-testing)
- [WCAG Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [Deque University](https://dequeuniversity.com/) — free accessibility training
