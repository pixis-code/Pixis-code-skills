# Locator Strategies

Locators determine how tests find elements. Good locators are resilient to implementation changes while verifying accessibility.

## Priority Hierarchy

Both Playwright and Testing Library recommend this order. Each level provides accessibility verification as a byproduct.

### 1. Accessible Roles (first choice)

Query the accessibility tree. If this fails, the UI likely has accessibility issues.

```javascript
// Playwright
page.getByRole("button", { name: /submit/i })
page.getByRole("textbox", { name: /email/i })
page.getByRole("heading", { level: 1 })
page.getByRole("navigation")
page.getByRole("listitem")

// Testing Library
screen.getByRole("button", { name: /submit/i })
screen.getByRole("checkbox", { checked: true })
```

**Why first**: users and assistive technologies perceive the page through roles. Testing with roles validates both functionality and accessibility.

**Name option**: filters by accessible name (visible text, aria-label, or aria-labelledby).

```javascript
page.getByRole("button", { name: /save/i })
page.getByRole("button", { name: /cancel/i })
page.getByRole("button", { name: /delete/i })
```

**Common roles**: `button`, `link`, `textbox`, `checkbox`, `radio`, `combobox`, `listbox`, `option`, `heading`, `navigation`, `main`, `article`, `dialog`, `alert`, `alertdialog`, `list`, `listitem`, `table`, `row`, `cell`, `tab`, `tablist`, `tabpanel`.

### 2. Label Text (forms)

```javascript
// Playwright
page.getByLabel("Email address")
page.getByLabel(/password/i)

// Testing Library
screen.getByLabelText("Email address")
screen.getByLabelText(/confirm password/i)
```

**Why second**: form users navigate by labels. Tests using labels fail if labels are missing or improperly associated — catching real accessibility bugs.

### 3. Placeholder Text (fallback for forms)

Use only when labels aren't available — placeholder is not a label substitute.

```javascript
page.getByPlaceholder("Search products...")
screen.getByPlaceholderText("Enter your query")
```

### 4. Visible Text (non-interactive content)

```javascript
// Playwright
page.getByText("Welcome back, Sarah")
page.getByText(/order confirmed/i)

// Testing Library
screen.getByText("No results found")
screen.getByText(/loading/i)
```

Useful for assertions on content, but doesn't verify semantic structure.

### 5. Alt Text (images)

```javascript
page.getByAltText("Company logo")
screen.getByAltText(/product photo/i)
```

### 6. Title Attribute

Rarely used — most elements shouldn't rely on title for identification.

```javascript
page.getByTitle("Close dialog")
screen.getByTitle(/help/i)
```

### 7. Test IDs (last resort)

Escape hatch when semantic queries fail. Provides no accessibility verification.

```javascript
// Playwright
page.getByTestId("pricing-calculator")

// Testing Library
screen.getByTestId("data-grid")
```

**When appropriate**: complex dynamic components (data grids, charts), elements with no stable accessible name, third-party components you can't modify.

**When to avoid**: any element that has text, label, or semantic role; as a default choice to "make tests easier."

## Playwright-Specific Patterns

### Chaining and filtering

```javascript
// Find delete button in specific row
const userRow = page.getByRole("row").filter({ hasText: "john@example.com" });
await userRow.getByRole("button", { name: /delete/i }).click();

// Combine locators
const submitButton = page
  .getByRole("button", { name: /submit/i })
  .and(page.locator("[type=submit]"));
```

### Scoped queries with `within`

```javascript
// Playwright
const form = page.getByRole("form", { name: /checkout/i });
await form.getByLabel("Card number").fill("4111111111111111");

// Testing Library
import { within } from "@testing-library/react";
const form = screen.getByRole("form");
within(form).getByLabelText("Email");
```

### Handling multiple elements

```javascript
const buttons = await page.getByRole("button").all();
const deleteButtons = buttons.filter(b => b.textContent.includes("Delete"));

// Or be more specific
page.getByRole("button", { name: "Delete", exact: true });
```

## Testing Library Variants

### get vs query vs find

| Variant | No match | Multiple matches | Async |
|---------|----------|------------------|-------|
| `getBy` | Throws | Throws | No |
| `queryBy` | Returns null | Throws | No |
| `findBy` | Throws | Throws | Yes (waits) |

```javascript
screen.getByRole("button", { name: /submit/i });               // should exist now
expect(screen.queryByRole("alert")).not.toBeInTheDocument();    // testing absence
await screen.findByRole("alert");                               // appears after async action
```

### Regex vs string matching

```javascript
screen.getByText("Submit Order");    // exact match (case-sensitive)
screen.getByText(/submit order/i);   // flexible match (recommended for resilience)
screen.getByText(/submit/i);         // partial match
```

## Anti-Patterns

### CSS selectors as primary strategy

```javascript
// BAD: tied to implementation
page.locator(".btn-primary");
page.locator("#submit-form-btn");
page.locator("div.container > form > button");

// GOOD: tied to user experience
page.getByRole("button", { name: /submit/i });
```

### XPath

```javascript
// BAD: brittle, hard to read
page.locator("//div[@class='form']//button[text()='Submit']");

// GOOD: clear and semantic
page.getByRole("button", { name: /submit/i });
```

### Position-based selection

```javascript
// BAD: breaks when order changes
page.getByRole("button").nth(2);

// GOOD: explicit about which element
page.getByRole("button", { name: /delete account/i });
```

### Test IDs for everything

```javascript
// BAD: no accessibility verification
page.getByTestId("submit-button");
page.getByTestId("email-input");
page.getByTestId("error-message");

// GOOD: validates accessibility
page.getByRole("button", { name: /submit/i });
page.getByLabel("Email");
page.getByRole("alert");
```

## Debugging Locators

### Playwright

```javascript
// Log all accessible elements
await page.getByRole("button").evaluateAll(buttons => buttons.map(b => b.textContent));

// npx playwright test --debug
// npx playwright codegen example.com
```

### Testing Library

```javascript
screen.debug();                       // log the DOM
screen.debug(screen.getByRole("form")); // log specific element
// testing-playground.com or browser extension
```

## References

- [Playwright Locators](https://playwright.dev/docs/locators)
- [Testing Library Queries](https://testing-library.com/docs/queries/about/)
- [ARIA Roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)
- [Testing Library Priority Guide](https://testing-library.com/docs/queries/about/#priority)
