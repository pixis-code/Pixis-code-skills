---
name: frontend-security
description: "Audit frontend codebases for security vulnerabilities: XSS, CSRF, DOM vulnerabilities, CSP, input validation, file-upload security, JWT implementation, and Node.js/NPM dependency audits. Targets web platform (vanilla HTML/CSS/JS), React, Astro, Twig, Node.js, and Bun. Based on OWASP security guidelines."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Frontend, Security, XSS, CSRF, OWASP, Web]
    category: frontend
    related_skills: [react-best-practices, best-practices-frontend, core-web-vitals]
---

# Frontend Security Audit

Perform comprehensive security audits of frontend codebases: identify vulnerabilities, bad practices, and missing protections, and report with remediation guidance.

## Hallucination Guard

Every finding below is a pattern match against the code — not a confirmed exploit. State clearly when something is a *structural risk* (the pattern exists, exploitability depends on unverified factors like whether the endpoint is reachable or the data is attacker-controlled) versus a *confirmed vulnerability* (traced end-to-end: untrusted input reaches the dangerous sink with no sanitization in between). Don't claim a finding is "exploited" or "actively dangerous" without tracing the actual data flow in the code — a `grep` hit is a lead, not a verdict. OWASP-published general risk descriptions are safe to cite as-is; claims about *this specific codebase's* exposure require reading the code.

## Audit Process

1. **Scan for dangerous patterns** — run *every* applicable search below (skip only those for stacks the project doesn't use) and list every hit before ranking. Don't pick a few files to read and stop; triage each hit as confirmed (untrusted data reaches the sink) or structural (pattern only), and say which hits you did not trace.
2. **Review framework-specific risks** — check for framework security-bypass patterns (see `references/framework-patterns.md`).
3. **Validate defensive measures** — verify CSP, CSRF tokens, input validation are actually present and correctly configured, not just assumed. For CSP and security headers, search *every* place they can be set before concluding anything (see "Locating CSP and Security Headers" below).
4. **Check dependencies** — run the audit command for the project's package manager (`npm audit`, `yarn npm audit`, `pnpm audit`, `bun audit`, per its lockfile). Report totals for the full tree and, separately, for production-only (`--omit=dev` / `--prod`), and name every critical and high package with its advisory — don't summarize them as a count. Quote installed versions from the lockfile or `npm ls`, not from version ranges in `package.json`.
5. **Report findings** — categorize by severity with concrete remediation guidance.

## Critical Vulnerability Patterns to Search

### XSS indicators (search priority: HIGH)

```bash
# React dangerous patterns
grep -rn "dangerouslySetInnerHTML" --include="*.jsx" --include="*.tsx" --include="*.js"

# Direct DOM manipulation
grep -rn "\.innerHTML\s*=" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx"
grep -rn "\.outerHTML\s*=" --include="*.js" --include="*.ts"
grep -rn "document\.write" --include="*.js" --include="*.ts"

# URL-based injection
grep -rn "location\.href\s*=" --include="*.js" --include="*.ts"
grep -rn "location\.replace" --include="*.js" --include="*.ts"
grep -rn "window\.open" --include="*.js" --include="*.ts"

# Eval and code execution
grep -rn "eval\s*(" --include="*.js" --include="*.ts"
grep -rn "new Function\s*(" --include="*.js" --include="*.ts"
grep -rn "setTimeout\s*(\s*['\"]" --include="*.js" --include="*.ts"
grep -rn "setInterval\s*(\s*['\"]" --include="*.js" --include="*.ts"

# Twig unescaped output
grep -rn "|raw" --include="*.twig" --include="*.html.twig"
grep -rn "{% autoescape false %}" --include="*.twig"
```

### Library-specific sinks (search only if the dependency is present in package.json)

```bash
# react-markdown: identity urlTransform disables URL protocol filtering; rehype-raw renders raw HTML
grep -rnE "urlTransform|transformLinkUri|rehype-raw|rehypeRaw" src
# mermaid: securityLevel "loose" allows HTML labels and click handlers
grep -rn "securityLevel" src
# Any HTML sanitizer in use (absence next to raw-HTML sinks is itself a finding)
grep -rnEi "dompurify|sanitize-html|isomorphic-dompurify" src package.json
# Variable URLs assigned to links/navigation
grep -rnE "href=\{[^}]*\}|window\.location|location\.assign" src
```

### CSRF indicators

```bash
# Forms without CSRF tokens
grep -rn "<form" --include="*.html" --include="*.jsx" --include="*.tsx" --include="*.twig"

# State-changing requests without protection
grep -rn "fetch\s*(" --include="*.js" --include="*.ts" | grep -E "(POST|PUT|DELETE|PATCH)"
grep -rn "axios\.(post|put|delete|patch)" --include="*.js" --include="*.ts"
```

### Sensitive data exposure

```bash
# localStorage/sessionStorage with sensitive data
grep -rn "localStorage\." --include="*.js" --include="*.ts"
grep -rn "sessionStorage\." --include="*.js" --include="*.ts"

# Hardcoded secrets
grep -rn "api[_-]?key\s*[:=]" --include="*.js" --include="*.ts" --include="*.env"
grep -rn "secret\s*[:=]" --include="*.js" --include="*.ts"
grep -rn "password\s*[:=]" --include="*.js" --include="*.ts"
```

### Unauthenticated server endpoints

Also grep for every exported Server Action / API route handler, not just the ones reached by tracing what's currently rendered — an unreferenced `'use server'` export or API route is still a live, callable endpoint whether or not any component imports it today. "Nothing calls this yet" is not a reason to skip the auth check.

```bash
grep -rn "'use server'" --include="*.ts" --include="*.tsx"
grep -rln "export async function (GET|POST|PUT|DELETE|PATCH)" --include="route.ts" --include="route.tsx"
```

## Locating CSP and Security Headers

A CSP or security header is often set outside `index.html`, at the CDN/host or server. Before reporting one as missing, search all of these:

```bash
grep -rniE "content-security-policy|x-frame-options|strict-transport-security" . \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist
ls public/_headers _headers public/_redirects vercel.json netlify.toml wrangler.toml \
  firebase.json staticwebapp.config.json nginx.conf .htaccess 2>/dev/null
```

- Static hosts: `public/_headers` or `_headers` (Cloudflare Pages, Netlify), `vercel.json`, `netlify.toml`, `firebase.json`, `staticwebapp.config.json`.
- Servers: nginx/Apache configs, `.htaccess`, Express/Helmet or other middleware, Vite/Next config `headers()`.
- Markup: `<meta http-equiv="Content-Security-Policy">` in `index.html`.

Reporting rules:
- **Found** → evaluate it, don't just note it exists: is it `Report-Only` (not enforced)? Does `script-src` allow `'unsafe-inline'`, `'unsafe-eval'`, or wildcards/`https:`? Is `frame-ancestors`/`object-src` set?
- **Not found in the repo** → say "not found in the repo; it may be set at the CDN/edge or hosting dashboard" and recommend verifying the deployed response headers (`curl -I <url>`). Never state "no CSP exists" from a repo search alone — absence in code is not absence in production.

## Reference Documentation

Load these based on what the scan turns up:

- **XSS vulnerabilities found** → `references/xss-prevention.md`
- **CSRF concerns** → `references/csrf-protection.md`
- **DOM manipulation issues** → `references/dom-security.md`
- **CSP review needed** → `references/csp-configuration.md`
- **Input handling issues** → `references/input-validation.md`
- **Node.js/NPM audit** → `references/nodejs-npm-security.md`
- **Framework-specific patterns** → `references/framework-patterns.md`
- **File upload handling** → `references/file-upload-security.md`
- **JWT implementation** → `references/jwt-security.md`

## Severity Classification

- **CRITICAL** — exploitable XSS, authentication bypass, secrets exposure
- **HIGH** — missing CSRF protection, unsafe DOM manipulation, injection vectors
- **MEDIUM** — weak CSP, missing security headers, improper input validation
- **LOW** — informational disclosure, deprecated functions, suboptimal practices

## Report Format

```markdown
## Security Audit Report

### Summary
- Critical: X findings
- High: X findings
- Medium: X findings
- Low: X findings

### Critical Findings

#### [CRITICAL-001] Title
- **Location**: file:line
- **Pattern**: code snippet
- **Risk**: description of the vulnerability
- **Remediation**: how to fix
- **Reference**: OWASP link

### High Findings
[...]
```

Also include a sink table so coverage gaps are visible. Every `.innerHTML =`, `.outerHTML =`, `insertAdjacentHTML`, `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]` or `|raw` hit whose assigned value is not a constant string must get a row, even if it looks low risk. Hits that only clear content (`innerHTML = ""`) may be skipped. Before finishing, compare the row count to the grep hit count and list any hits you left out and why:

| Sink / pattern | File:line | Data source | Status (confirmed / structural / not traced) |
|---|---|---|---|

## OWASP Reference Links

- [XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [DOM XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
- [CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [CSP](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)
- [DOM Clobbering](https://cheatsheetseries.owasp.org/cheatsheets/DOM_Clobbering_Prevention_Cheat_Sheet.html)
- [Node.js Security](https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html)
- [NPM Security](https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html)
- [AJAX Security](https://cheatsheetseries.owasp.org/cheatsheets/AJAX_Security_Cheat_Sheet.html)
- [File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [Error Handling](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)
- [JWT Security](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [User Privacy](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html)
