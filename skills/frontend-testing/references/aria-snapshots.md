# ARIA Snapshot Testing

ARIA snapshots capture the accessibility tree structure in YAML format. A single snapshot assertion can replace multiple individual assertions while validating semantic structure.

## Why ARIA Snapshots

### Consolidation

Instead of multiple assertions:

```javascript
await expect(page.getByRole("heading", { level: 1 })).toHaveText("Welcome");
await expect(page.getByRole("textbox", { name: /email/i })).toBeVisible();
await expect(page.getByRole("textbox", { name: /password/i })).toBeVisible();
await expect(page.getByRole("button", { name: /sign in/i })).toBeEnabled();
await expect(page.getByRole("link", { name: /forgot/i })).toBeVisible();
```

One snapshot covers all:

```javascript
await expect(page.getByRole("main")).toMatchAriaSnapshot(`
  - heading "Welcome" [level=1]
  - textbox "Email"
  - textbox "Password"
  - button "Sign in"
  - link "Forgot password?"
`);
```

### Benefits over visual snapshots

| Aspect | ARIA Snapshot | Visual Screenshot |
|--------|---------------|-------------------|
| Styling changes | Unaffected | Fails |
| Font rendering | Unaffected | Varies by OS |
| Cross-browser | Consistent | Different per browser |
| What it validates | Semantic structure | Pixel appearance |
| Accessibility | Validates a11y tree | No a11y validation |
| File size | Tiny (YAML text) | Large (PNG images) |

### What it catches

Missing or changed accessible names, wrong heading levels, missing form labels, changed element roles, broken landmark structure, state changes (checked, disabled, expanded).

## YAML Syntax

```yaml
- role "accessible name" [attribute=value]
```

### Roles

```yaml
- heading "Page Title" [level=1]
- navigation
- main
- button "Submit"
- link "Learn more"
- textbox "Email"
- checkbox "Remember me" [checked=true]
- combobox "Country"
- list
- listitem "Item one"
- table
- row
- cell "Data"
- dialog "Confirm deletion"
- alert
- img "Product photo"
```

### Accessible names

```yaml
# Exact match
- button "Submit Order"
# Regex match
- heading /Welcome.*/ [level=1]
- link /\d+ items in cart/
```

### Attributes

```yaml
- heading "Title" [level=1]
- heading "Subtitle" [level=2]
- checkbox "Accept terms" [checked=true]
- checkbox "Newsletter" [checked=false]
- button "Submit" [disabled=true]
- button "Menu" [expanded=true]
- button "Details" [expanded=false]
- tab "Overview" [selected=true]
- option "English" [selected=true]
- button "Bold" [pressed=true]
- link "Documentation":
  - /url: "https://docs.example.com"
```

### Nesting

Indentation shows hierarchy:

```yaml
- navigation:
  - list:
    - listitem:
      - link "Home"
    - listitem:
      - link "Products"
    - listitem:
      - link "About"
- main:
  - heading "Products" [level=1]
  - list:
    - listitem "Product A"
    - listitem "Product B"
```

## Basic Usage

### Inline snapshot

```javascript
import { test, expect } from "@playwright/test";

test("login form structure", async ({ page }) => {
  await page.goto("/login");
  await expect(page.getByRole("main")).toMatchAriaSnapshot(`
    - heading "Sign In" [level=1]
    - textbox "Email"
    - textbox "Password"
    - button "Sign In"
    - link "Forgot password?"
    - link "Create account"
  `);
});
```

### External snapshot file

```javascript
test("dashboard structure", async ({ page }) => {
  await page.goto("/dashboard");
  await expect(page.getByRole("main")).toMatchAriaSnapshot({
    name: "dashboard-main.aria.yml",
  });
});
```

### Scoped snapshots

```javascript
// Just the header
await expect(page.getByRole("banner")).toMatchAriaSnapshot(`
  - link "Logo"
  - navigation:
    - link "Home"
    - link "Products"
    - link "About"
  - button "Menu"
`);

// Just a form
await expect(page.getByRole("form", { name: /checkout/i })).toMatchAriaSnapshot(`
  - textbox "Card number"
  - textbox "Expiry"
  - textbox "CVC"
  - button "Pay now"
`);

// Just a specific component
await expect(page.getByTestId("product-card")).toMatchAriaSnapshot(`
  - img "Product photo"
  - heading "Product Name" [level=3]
  - text "$29.99"
  - button "Add to cart"
`);
```

## Partial Matching

By default, snapshots perform subset matching — omit elements you don't care about.

### Omit names

```javascript
await expect(locator).toMatchAriaSnapshot(`
  - button
`);
await expect(locator).toMatchAriaSnapshot(`
  - heading [level=1]
`);
```

### Omit attributes

```javascript
await expect(locator).toMatchAriaSnapshot(`
  - checkbox "Remember me"
`);
```

### Omit children

```javascript
// Only verify Home and About links exist; other links in the nav are ignored
await expect(page.getByRole("navigation")).toMatchAriaSnapshot(`
  - link "Home"
  - link "About"
`);
```

### Strict child matching

```javascript
// Require exactly these children, in this order
await expect(page.getByRole("list")).toMatchAriaSnapshot(`
  - list:
    - /children: equal
    - listitem "Step 1"
    - listitem "Step 2"
    - listitem "Step 3"
`);
```

## Generating Snapshots

```bash
npx playwright codegen example.com
# In the recorder: click "Assert snapshot", select the element — snapshot is generated
```

```javascript
test("generate snapshot for review", async ({ page }) => {
  await page.goto("/products");
  const snapshot = await page.getByRole("main").ariaSnapshot();
  console.log(snapshot);
});
```

Updating snapshots when structure intentionally changes:

```bash
npx playwright test --update-snapshots
git diff   # review before committing
```

## Testing Patterns

### Component states

```javascript
test.describe("Accordion", () => {
  test("collapsed state", async ({ page }) => {
    await page.goto("/accordion");
    await expect(page.getByRole("region", { name: /details/i })).toMatchAriaSnapshot(`
      - button "Details" [expanded=false]
    `);
  });

  test("expanded state", async ({ page }) => {
    await page.goto("/accordion");
    await page.getByRole("button", { name: /details/i }).click();
    await expect(page.getByRole("region", { name: /details/i })).toMatchAriaSnapshot(`
      - button "Details" [expanded=true]
      - text "Additional information here"
    `);
  });
});
```

### Form validation states

```javascript
test("shows validation errors", async ({ page }) => {
  await page.goto("/signup");
  await page.getByRole("button", { name: /submit/i }).click();
  await expect(page.getByRole("form")).toMatchAriaSnapshot(`
    - textbox "Email"
    - text "Email is required"
    - textbox "Password"
    - text "Password is required"
    - button "Submit"
  `);
});
```

### Dynamic content with regex

```javascript
test("cart shows item count", async ({ page }) => {
  await page.goto("/cart");
  await expect(page.getByRole("banner")).toMatchAriaSnapshot(`
    - link "Home"
    - link /\\d+ items?/
  `);
});
```

### Before/after interaction

```javascript
test("dialog opens and closes", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("main")).toMatchAriaSnapshot(`
    - button "Open Settings"
  `);

  await page.getByRole("button", { name: /settings/i }).click();

  await expect(page.getByRole("dialog")).toMatchAriaSnapshot(`
    - dialog "Settings":
      - heading "Settings" [level=2]
      - checkbox "Dark mode"
      - checkbox "Notifications"
      - button "Save"
      - button "Cancel"
  `);
});
```

## Combining with Other Assertions

ARIA snapshots validate structure — combine with other assertions for complete coverage:

```javascript
test("product page", async ({ page }) => {
  await page.goto("/products/123");

  // Structure validation
  await expect(page.getByRole("main")).toMatchAriaSnapshot(`
    - img "Product photo"
    - heading "Widget Pro" [level=1]
    - text "$49.99"
    - button "Add to cart"
  `);

  // Functional validation
  await page.getByRole("button", { name: /add to cart/i }).click();
  await expect(page.getByRole("alert")).toContainText("Added to cart");

  // Accessibility validation (axe-core)
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

## Debugging

```javascript
const snapshot = await page.getByRole("main").ariaSnapshot();
console.log(snapshot);
```

Chrome DevTools: Elements panel → Accessibility tab → inspect the accessibility tree.

When a snapshot fails, the error shows expected vs actual:

```
Expected:
- heading "Welcome" [level=1]
- button "Sign In"

Actual:
- heading "Welcome Back" [level=1]
- button "Log In"
```

## Best Practices

### Scope appropriately

```javascript
// BAD: entire page - too broad, fragile
await expect(page.locator("body")).toMatchAriaSnapshot(`...`);

// GOOD: specific region - focused, stable
await expect(page.getByRole("form", { name: /login/i })).toMatchAriaSnapshot(`...`);
```

### Use for structure, not content

```javascript
// BAD: testing dynamic data
await expect(locator).toMatchAriaSnapshot(`
  - text "Order #12345"
  - text "Total: $127.50"
`);

// GOOD: testing structure with flexible matching
await expect(locator).toMatchAriaSnapshot(`
  - text /Order #\d+/
  - text /Total: \$[\d.]+/
`);
```

### Keep snapshots readable

```javascript
// BAD: too detailed, hard to review
await expect(locator).toMatchAriaSnapshot(`
  - main:
    - article:
      - header:
        - div:
          - span:
            - heading "Title" [level=1]
`);

// GOOD: focus on meaningful structure
await expect(locator).toMatchAriaSnapshot(`
  - heading "Title" [level=1]
  - text "Description"
  - button "Action"
`);
```

### Review before committing

```bash
git diff **/*.aria.yml   # verify changes are intentional before committing
```

## References

- [Playwright ARIA Snapshots](https://playwright.dev/docs/aria-snapshots)
- [ARIA Roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)
- [Accessible Name Computation](https://www.w3.org/TR/accname-1.1/)
