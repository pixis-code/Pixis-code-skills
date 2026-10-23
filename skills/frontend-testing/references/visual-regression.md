# Visual Regression Testing

Visual regression testing (VRT) catches unintended visual changes by comparing screenshots against approved baselines.

## When to Use VRT

**Good candidates:** design-system components, critical landing pages, complex layouts (grids, dashboards), components with CSS that changes frequently, cross-browser visual consistency.

**Poor candidates:** pages with frequently changing dynamic content, components with animations, time-dependent displays, pages with third-party content (ads, embeds).

## Playwright Visual Testing

### Basic screenshot comparison

```javascript
import { test, expect } from "@playwright/test";

test("homepage looks correct", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveScreenshot();
});
```

First run creates the baseline. Subsequent runs compare against it.

### Named screenshots

```javascript
test("hero section renders correctly", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveScreenshot("homepage-hero.png");
});
```

### Element screenshots

More stable than full-page screenshots:

```javascript
test("product card renders correctly", async ({ page }) => {
  await page.goto("/products/123");
  const productCard = page.getByTestId("product-card");
  await expect(productCard).toHaveScreenshot("product-card.png");
});
```

### Full page screenshots

```javascript
test("full page layout", async ({ page }) => {
  await page.goto("/about");
  await expect(page).toHaveScreenshot("about-page-full.png", { fullPage: true });
});
```

## Handling Instability

Visual tests fail due to timing, rendering, or environment differences. Stabilize tests before trusting results.

### Wait for network and fonts

```javascript
test("page renders after loading", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  await page.evaluate(() => document.fonts.ready);
  await expect(page).toHaveScreenshot();
});
```

### Disable animations

```javascript
// playwright.config.js
export default defineConfig({
  use: { contextOptions: { reducedMotion: "reduce" } },
});
```

```javascript
test("static screenshot", async ({ page }) => {
  await page.goto("/");
  await page.addStyleTag({
    content: `
      *, *::before, *::after {
        animation-duration: 0s !important;
        transition-duration: 0s !important;
      }
    `,
  });
  await expect(page).toHaveScreenshot();
});
```

### Mask dynamic content

```javascript
test("page with masked dynamic content", async ({ page }) => {
  await page.goto("/dashboard");
  await expect(page).toHaveScreenshot({
    mask: [
      page.locator("[data-testid='current-time']"),
      page.locator("[data-testid='user-avatar']"),
      page.locator(".ad-container"),
    ],
  });
});
```

### Fixed viewport

```javascript
// playwright.config.js
export default defineConfig({
  use: { viewport: { width: 1280, height: 720 } },
});
```

```javascript
test("mobile view", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto("/");
  await expect(page).toHaveScreenshot("homepage-mobile.png");
});
```

### Hide scrollbars

```javascript
await page.addStyleTag({
  content: `
    ::-webkit-scrollbar { display: none; }
    * { scrollbar-width: none; }
  `,
});
```

## Tolerance Settings

Allow minor pixel differences to reduce flakiness.

```javascript
// playwright.config.js — global
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,       // allow up to 100 different pixels
      maxDiffPixelRatio: 0.01,  // or 1% of total pixels
      threshold: 0.2,           // color difference threshold (0-1)
    },
  },
});
```

```javascript
// Per-screenshot
await expect(page).toHaveScreenshot({ maxDiffPixels: 50, threshold: 0.3 });
```

| Setting | Value | Use Case |
|---------|-------|----------|
| `threshold` | 0.1 | Strict pixel matching |
| `threshold` | 0.2 | Standard tolerance (default) |
| `threshold` | 0.3 | Generous for anti-aliasing |
| `maxDiffPixels` | 50 | Small components |
| `maxDiffPixels` | 200 | Full pages |
| `maxDiffPixelRatio` | 0.01 | 1% tolerance |

## Updating Baselines

Update when: intentional design changes, new features affecting layout, browser rendering-engine updates, after fixing visual bugs.

```bash
npx playwright test --update-snapshots
```

**Never update blindly.** Review changes first:

```bash
git diff --stat
open tests/screenshots/
```

Workflow: test fails on visual difference → review diff image → if intentional, update baseline and commit; if unintentional, fix the code and re-run.

## Cross-Browser Testing

Screenshots differ between browsers due to rendering differences. Playwright automatically creates separate baselines per browser:

```
example.spec.ts-snapshots/
├── homepage-chromium-linux.png
├── homepage-firefox-linux.png
└── homepage-webkit-linux.png
```

```javascript
// playwright.config.js
export default defineConfig({
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
  ],
});
```

### OS differences

Font rendering varies by OS. Options: run visual tests in CI only (consistent environment), use Docker with consistent fonts, generate baselines in CI rather than locally.

## CI/CD Configuration

```yaml
# GitHub Actions
- name: Run visual tests
  run: npx playwright test --project=chromium

- name: Upload diff artifacts on failure
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: visual-diff
    path: test-results/
```

```yaml
# Generate baselines in CI for consistency
- name: Update baselines
  run: npx playwright test --update-snapshots
- name: Commit baselines
  run: |
    git config user.name "CI Bot"
    git add "**/*.png"
    git commit -m "Update visual baselines"
    git push
```

## Organizing Screenshots

```
tests/
├── visual/
│   ├── homepage.spec.ts
│   └── components/
│       ├── button.spec.ts
│       └── card.spec.ts
└── visual.spec.ts-snapshots/
    ├── homepage-chromium.png
    └── button-default-chromium.png
```

```javascript
// Custom path template
export default defineConfig({
  snapshotPathTemplate: "{testDir}/__snapshots__/{projectName}/{testFilePath}/{arg}{ext}",
});
```

## Reporting and Review

```bash
npx playwright show-report
```

Shows expected (baseline), actual (current), and diff highlighting changed pixels.

```javascript
// Save all artifacts on failure
export default defineConfig({
  use: { trace: "on-first-retry", screenshot: "only-on-failure" },
  outputDir: "test-results/",
});
```

## Anti-Patterns

### Removing platform suffix

```javascript
// BAD: removes platform/browser suffix from snapshot names
test.beforeEach(async ({}, testInfo) => {
  testInfo.snapshotSuffix = "";
});
// Results in one baseline used across all platforms — constant false positives/negatives.
```

Font rendering, anti-aliasing, and subpixel rendering all differ by OS and browser. Keep the default naming:

```
button-chromium-darwin.png
button-chromium-linux.png
button-firefox-linux.png
```

### Too many full-page screenshots

```javascript
// BAD: full page with dynamic content
await expect(page).toHaveScreenshot({ fullPage: true });

// GOOD: target stable regions
const header = page.getByRole("banner");
await expect(header).toHaveScreenshot("header.png");
```

### No stabilization

```javascript
// BAD: screenshot immediately
await page.goto("/");
await expect(page).toHaveScreenshot();

// GOOD: wait for stable state
await page.goto("/");
await page.waitForLoadState("networkidle");
await page.evaluate(() => document.fonts.ready);
await expect(page).toHaveScreenshot();
```

### Overly strict tolerance

```javascript
// BAD: zero tolerance causes flaky tests
await expect(page).toHaveScreenshot({ maxDiffPixels: 0 });

// GOOD: allow minor rendering differences
await expect(page).toHaveScreenshot({ maxDiffPixels: 50 });
```

### Updating without review

```bash
# BAD: blindly update all baselines
npx playwright test --update-snapshots

# GOOD: review first
npx playwright test
npx playwright show-report
npx playwright test --update-snapshots
```

## References

- [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)
- [Pixelmatch](https://github.com/mapbox/pixelmatch) — image comparison library used by Playwright
