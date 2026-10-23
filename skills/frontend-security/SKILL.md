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

1. **Scan for dangerous patterns** — search the codebase for known vulnerability indicators (below).
2. **Review framework-specific risks** — check for framework security-bypass patterns (see `references/framework-patterns.md`).
3. **Validate defensive measures** — verify CSP, CSRF tokens, input validation are actually present and correctly configured, not just assumed.
4. **Check dependencies** — review npm/Node dependencies for known vulnerabilities.
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
