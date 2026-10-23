# Framework-Specific Security Patterns

## React Security

### XSS prevention

```jsx
// DEFAULT SAFE - React escapes by default
<div>{userInput}</div>

// DANGEROUS - bypasses escaping
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// If HTML is required, sanitize first
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

### URL handling

```jsx
// DANGEROUS - javascript: URLs in href
<a href={userInput}>Link</a>

// SAFE - validate URL protocol
function SafeLink({ href, children }) {
  const safeHref = useMemo(() => {
    try {
      const url = new URL(href, window.location.origin);
      if (['http:', 'https:', 'mailto:'].includes(url.protocol)) return href;
    } catch {}
    return '#';
  }, [href]);

  return <a href={safeHref}>{children}</a>;
}
```

### State and props

```jsx
// DANGEROUS - spreading user-controlled props
<Component {...userControlledObject} />

// SAFE - explicitly pass allowed props
<Component
  title={userControlledObject.title}
  description={userControlledObject.description}
/>
```

### Server-side rendering (SSR)

```jsx
// DANGEROUS - injecting user data into SSR without escaping
<script>
  window.__INITIAL_STATE__ = {JSON.stringify(userControlledData)}
</script>

// SAFE - serialize with escaping
import serialize from 'serialize-javascript';
<script
  dangerouslySetInnerHTML={{
    __html: `window.__INITIAL_STATE__ = ${serialize(data, { isJSON: true })}`
  }}
/>
```

## Astro Security

### Content escaping

```astro
---
const userInput = Astro.props.userInput;
---

<!-- SAFE - auto-escaped -->
<div>{userInput}</div>

<!-- DANGEROUS - bypasses escaping -->
<div set:html={userInput} />

<!-- If HTML required, sanitize -->
---
import DOMPurify from 'dompurify';
const sanitized = DOMPurify.sanitize(userInput);
---
<div set:html={sanitized} />
```

### Dynamic imports

```astro
---
// DANGEROUS - user-controlled import path
const component = await import(userInput);

// SAFE - allowlist approach
const allowedComponents = {
  'card': () => import('./Card.astro'),
  'button': () => import('./Button.astro')
};

const loadComponent = allowedComponents[userInput];
if (!loadComponent) throw new Error('Invalid component');
const Component = await loadComponent();
---
```

### API endpoints

```javascript
// src/pages/api/data.js
export async function POST({ request }) {
  const contentType = request.headers.get('content-type');
  if (!contentType?.includes('application/json')) {
    return new Response('Invalid content type', { status: 415 });
  }

  const body = await request.json();
  if (!validateInput(body)) {
    return new Response('Invalid input', { status: 400 });
  }

  return new Response(JSON.stringify(result), {
    headers: { 'Content-Type': 'application/json' }
  });
}
```

## Twig Security

### Output escaping

```twig
{# SAFE - auto-escaped for HTML context #}
{{ userInput }}

{# DANGEROUS - raw bypasses escaping #}
{{ userInput|raw }}

{# DANGEROUS - autoescape disabled #}
{% autoescape false %}
  {{ userInput }}
{% endautoescape %}

{# Context-specific escaping #}
{{ userInput|e('html') }}
{{ userInput|e('js') }}
{{ userInput|e('css') }}
{{ userInput|e('url') }}
{{ userInput|e('html_attr') }}
```

### Template inclusion

```twig
{# DANGEROUS - user-controlled template path #}
{% include userInput %}

{# SAFE - use allowlist #}
{% if templateName in ['header', 'footer', 'sidebar'] %}
  {% include templateName ~ '.html.twig' %}
{% endif %}
```

### Sandbox mode (Symfony)

```yaml
# config/packages/twig.yaml
twig:
  sandbox:
    policy:
      tags: ['if', 'for', 'set']
      filters: ['escape', 'upper', 'lower']
      methods:
        Symfony\Component\Routing\Generator\UrlGeneratorInterface: ['generate']
      properties: []
      functions: ['path', 'url']
```

### CSRF in forms

```twig
{# Symfony CSRF protection #}
<form method="post">
  <input type="hidden" name="_csrf_token" value="{{ csrf_token('form_name') }}">
  {# form fields #}
</form>
```

## Bun Security

### Request handling

```javascript
Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);
    const origin = req.headers.get('origin');
    if (origin && !isAllowedOrigin(origin)) {
      return new Response('Forbidden', { status: 403 });
    }
    if (isRateLimited(req)) {
      return new Response('Too Many Requests', { status: 429 });
    }
    return handleRequest(req);
  }
});
```

### File handling

```javascript
function safeReadFile(userPath) {
  const baseDir = '/app/public';
  const resolved = Bun.resolveSync(userPath, baseDir);
  if (!resolved.startsWith(baseDir)) throw new Error('Path traversal detected');
  return Bun.file(resolved).text();
}
```

## HTML5 APIs Security

### Web storage

```javascript
// NEVER store sensitive data in localStorage
localStorage.setItem('token', jwt);  // DANGEROUS

// Use httpOnly cookies for tokens instead, or memory with short expiration.
// If localStorage is necessary, encrypt:
import { encrypt, decrypt } from './crypto';
localStorage.setItem('data', encrypt(sensitiveData, key));
```

### postMessage

```javascript
window.addEventListener('message', (event) => {
  const allowedOrigins = ['https://trusted.com'];
  if (!allowedOrigins.includes(event.origin)) return;
  if (typeof event.data !== 'object') return;
  if (!['action1', 'action2'].includes(event.data.type)) return;
  handleMessage(event.data);
});

// Always specify target origin when sending
iframe.contentWindow.postMessage(data, 'https://specific-origin.com');
// NEVER use '*' for sensitive data
```

### WebSockets

```javascript
const wss = new WebSocket.Server({
  server,
  verifyClient: ({ origin, req }, callback) => {
    const allowed = ['https://myapp.com'];
    callback(allowed.includes(origin));
  }
});

wss.on('connection', (ws) => {
  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data);
      if (!isValidMessage(msg)) { ws.close(1008, 'Invalid message'); return; }
      handleMessage(msg);
    } catch {
      ws.close(1008, 'Invalid JSON');
    }
  });
});
```

OWASP Reference: https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html
