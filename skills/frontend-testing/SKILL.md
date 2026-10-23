---
name: frontend-testing
description: Write tests that start with acceptance criteria, then add implementation tests for robustness. Use for unit tests (Vitest), end-to-end tests (Playwright), visual regression tests, or accessibility tests. Emphasizes user-centric testing, semantic locators, accessibility validation, and the balance between acceptance and implementation testing.
author: Pixis
license: MIT
related_skills: [accessibility-frontend, react-best-practices, frontend-security]
---

# Frontend Testing

Start by writing tests that validate acceptance criteria. Then add implementation tests where they provide value.

## Hallucination Guard

A test passing or failing is a real, verifiable fact once it's actually been run — state it as a fact only after running it, never from reading the code and predicting the outcome. When proposing new tests, be explicit about which are drawn from stated acceptance criteria (verifiable against the ticket/requirements) versus which are implementation tests you inferred from reading the code (verifiable only by running them). Don't claim coverage percentages or "this is now fully tested" without actually running a coverage tool — state what was added, not an unverified completeness claim.

## Core Principle

> "The more your tests resemble the way your software is used, the more confidence they can give you." — Kent C. Dodds

This guides testing decisions, but isn't the whole picture:

- **Acceptance criteria tests** verify the system does what users/stakeholders need. These should be stable across refactors.
- **Implementation tests** verify the pieces are robust — edge cases, error handling, complex logic. These may change when you refactor.

Both have value. The anti-pattern to avoid is tests that *only* mirror implementation without validating meaningful behavior.

## When to Load References

- **Unit tests with DOM** → `references/locator-strategies.md`
- **E2E tests** → `references/locator-strategies.md`, `references/aria-snapshots.md`
- **Visual regression tests** → `references/visual-regression.md`
- **Accessibility audits** → `references/accessibility-testing.md`
- **Structure validation** → `references/aria-snapshots.md` (consolidate multiple assertions into one)

## Workflow

### Step 1 — Start with Acceptance Criteria

Before writing any test, identify what the code should do from the user's perspective: ticket description, user story, Figma annotations, functional requirements, or product-owner clarification. Document criteria as a checklist — these become your first tests.

**Write acceptance tests before reading implementation.** This prevents circular validation where tests just confirm "code does what code does."

### Step 2 — Map Criteria to Test Cases

For each criterion, identify the happy path, edge cases, and error cases:

```
Criterion: "User can filter products by category"
├─ Happy path: Select category, products filter correctly
├─ Edge case: No products match filter, show empty state
├─ Edge case: Clear filter, all products show again
├─ Error case: Filter API fails, show error message
└─ Accessibility: Filter controls are keyboard accessible
```

### Step 3 — Add Implementation Tests (Unit Tests)

After acceptance tests pass, add unit tests for implementation robustness — edge cases the criteria don't cover (null, undefined, empty arrays, boundary values), algorithm correctness, error-handling paths, complex branching, performance-sensitive code:

```
Function: filterProducts(products, category)
├─ Acceptance: Returns matching products (from criteria)
├─ Implementation: Returns empty array when products is null
├─ Implementation: Returns all products when category is empty string
├─ Implementation: Handles case-insensitive category matching
└─ Implementation: Does not mutate original array
```

Acceptance tests should rarely change on refactor; implementation tests may need updates when internals change.

### Step 4 — Choose Test Type

| Scenario | Test Type | Tool |
|----------|-----------|------|
| Pure logic (no DOM) | Unit test | Vitest |
| Component behavior | Unit test with DOM | Vitest + Testing Library |
| User flows, real browser | E2E test | Playwright |
| Semantic structure validation | ARIA snapshot | Playwright `toMatchAriaSnapshot` |
| Visual appearance | VRT | Playwright screenshots |
| Accessibility compliance | A11y test | Playwright + axe-core |

**ARIA snapshots** are particularly valuable for E2E tests — a single snapshot can replace multiple individual assertions while validating the accessibility-tree structure.

**DOM environment for unit tests:** prefer `happy-dom` over `jsdom` — it's faster, and its API limitations are a useful signal: if happy-dom doesn't support what you're testing, consider whether it belongs in an E2E test instead.

### Step 5 — Write Tests Before/Alongside Code

- **Ideal**: test first, then implementation (TDD)
- **Acceptable**: test immediately after implementing each criterion
- **Avoid**: writing all tests after implementation is "done"

## Test Structure

### Unit tests (Vitest)

```javascript
describe("calculateDiscount", () => {
  describe("when customer has premium membership", () => {
    it("applies 20% discount to order total", () => {
      // Arrange
      const order = { total: 100, membership: "premium" };
      // Act
      const result = calculateDiscount(order);
      // Assert
      expect(result).toBe(80);
    });
  });
});
```

### Component tests (Vitest + Testing Library)

```javascript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

describe("LoginForm", () => {
  describe("when credentials are invalid", () => {
    it("displays error message to user", async () => {
      const user = userEvent.setup();
      render(<LoginForm />);

      await user.type(screen.getByLabelText(/email/i), "invalid@test.com");
      await user.type(screen.getByLabelText(/password/i), "wrong");
      await user.click(screen.getByRole("button", { name: /sign in/i }));

      expect(await screen.findByRole("alert")).toHaveTextContent(/invalid credentials/i);
    });
  });
});
```

### E2E tests (Playwright)

```javascript
import { test, expect } from "@playwright/test";

test.describe("Product Catalog", () => {
  test.describe("filtering by category", () => {
    test("shows only matching products", async ({ page }) => {
      await page.goto("/products");
      await page.getByRole("combobox", { name: /category/i }).selectOption("Electronics");

      const products = page.getByRole("article");
      await expect(products).toHaveCount(5);
      await expect(products.first()).toContainText(/electronics/i);
      await expect(products.last()).toContainText(/electronics/i);
    });
  });
});
```

When verifying all items, use `Promise.all` for parallel assertions rather than sequential await in a loop:

```javascript
test("all products match filter", async ({ page }) => {
  await page.goto("/products");
  await page.getByRole("combobox", { name: /category/i }).selectOption("Electronics");

  const products = await page.getByRole("article").all();
  await Promise.all(
    products.map(product => expect(product.getByText(/electronics/i)).toBeVisible())
  );
});
```

### E2E tests with ARIA snapshots

Consolidates multiple assertions into one, validating semantic structure:

```javascript
test.describe("Login Page", () => {
  test("has correct form structure", async ({ page }) => {
    await page.goto("/login");
    // One snapshot replaces 5+ individual assertions
    await expect(page.getByRole("main")).toMatchAriaSnapshot(`
      - heading "Sign In" [level=1]
      - textbox "Email"
      - textbox "Password"
      - button "Sign In"
      - link "Forgot password?"
    `);
  });

  test("shows validation errors on empty submit", async ({ page }) => {
    await page.goto("/login");
    await page.getByRole("button", { name: /sign in/i }).click();
    await expect(page.getByRole("form")).toMatchAriaSnapshot(`
      - textbox "Email"
      - text "Email is required"
      - textbox "Password"
      - text "Password is required"
      - button "Sign In"
    `);
  });
});
```

## Locator Priority

1. **`getByRole`** — first choice, queries the accessibility tree
2. **`getByLabelText`** — best for form fields
3. **`getByPlaceholderText`** — when no label exists (not ideal)
4. **`getByText`** — for non-interactive elements
5. **`getByAltText`** — for images
6. **`getByTestId`** — last resort escape hatch

If you can't find an element with semantic queries, the UI may have accessibility issues.

## Anti-Patterns

### Testing only implementation details

```javascript
// BAD: tests internal method exists, provides no behavior guarantee
it("has a validateFields method", () => {
  expect(form.#validateFields).toBeDefined();
});

// BAD: asserts implementation without verifying outcome
it("calls the validator", () => {
  expect(mockValidator).toHaveBeenCalledWith(data);
});

// GOOD: tests observable behavior (acceptance)
it("prevents submission with invalid email", async () => {
  await user.type(emailInput, "not-an-email");
  await user.click(submitButton);
  expect(screen.getByRole("alert")).toHaveTextContent(/valid email/i);
});

// ALSO GOOD: tests implementation robustness (unit)
it("returns validation errors for malformed email", () => {
  const result = validateEmail("not-an-email");
  expect(result.valid).toBe(false);
  expect(result.error).toBe("Invalid email format");
});
```

The distinction: implementation tests should verify *meaningful* behavior of units, not just that code paths execute.

### Circular validation

```javascript
// BAD: expected value derived from implementation
const expected = formatPrice(100); // Don't compute expected from code!
expect(formatPrice(100)).toBe(expected);

// GOOD: expected value from requirements
expect(formatPrice(100)).toBe("$100.00");
```

### Over-mocking

```javascript
// BAD: mock everything, test nothing real
jest.mock("./api");
jest.mock("./utils");
jest.mock("./formatter");

// GOOD: mock only external boundaries (APIs, databases, time, file system)
// Keep business logic, components, formatters real.
```

### Brittle selectors

```javascript
// BAD: implementation-dependent
page.locator(".btn-primary.submit-form");
page.locator("#root > div > form > button:nth-child(3)");

// GOOD: semantic
page.getByRole("button", { name: /submit order/i });
```

## Failing Tests Mean Bugs (Usually)

**Acceptance test fails:**
1. Check the code under test first — likely a real bug.
2. Verify the test still matches current requirements — requirements may have changed.
3. Only update the test after confirming the new behavior is correct.

**Implementation test fails:**
1. If you're refactoring, the test may legitimately need updating.
2. If you're not refactoring, check the code — likely a bug.
3. Consider whether the test is too tightly coupled to implementation.

Don't reflexively update tests to pass. Investigate why they fail.

## Checklist Before Submitting Tests

- [ ] Each acceptance criterion has at least one test
- [ ] Edge cases from criteria are covered
- [ ] Implementation tests added for complex logic, error handling, boundary conditions
- [ ] Tests are named descriptively (criteria-based or behavior-based)
- [ ] Using semantic locators (`getByRole`, `getByLabelText`)
- [ ] No tests that only verify "code runs" without validating meaningful behavior
- [ ] Failing tests investigated appropriately (acceptance vs implementation)
- [ ] Accessibility checks included for interactive components
- [ ] Consider ARIA snapshots for structure validation

## References

- `references/locator-strategies.md` — complete locator hierarchy with examples
- `references/aria-snapshots.md` — structure validation, consolidating assertions
- `references/accessibility-testing.md` — axe-core integration, WCAG targeting
- `references/visual-regression.md` — screenshot testing, baseline management
