# Node.js and NPM Security Reference

## NPM Dependency Security

### Audit commands

```bash
npm audit                          # Check for vulnerabilities
npm audit fix                      # Fix automatically where possible
npm audit fix --force              # Force fix (may have breaking changes)
npm audit --json > audit-report.json
```

### Lockfile enforcement

```bash
npm ci                   # Always use lockfile in CI/CD, instead of npm install
npm ci --ignore-scripts  # Safer for first run
```

### package.json security

```json
{
  "scripts": {
    "postinstall": "npm audit"
  },
  "overrides": {
    "vulnerable-package": "^2.0.0"
  }
}
```

## Dangerous Functions

### Code execution

```javascript
// DANGEROUS - never use with user input
eval(userInput);
new Function(userInput);
vm.runInThisContext(userInput);
require(userInput);
setTimeout(userInput, 1000);  // Executes as code if string

// SAFE - pass functions instead
setTimeout(() => { /* code */ }, 1000);
```

### Child process injection

```javascript
// DANGEROUS - command injection
const { exec } = require('child_process');
exec(`ls ${userInput}`);  // Shell injection

// SAFER - execFile with arguments array
const { execFile } = require('child_process');
execFile('ls', [userInput], callback);  // Arguments not interpreted by shell

// SAFEST - spawn with shell: false
const { spawn } = require('child_process');
spawn('ls', [userInput], { shell: false });
```

### File system

```javascript
const path = require('path');
const fs = require('fs');

// DANGEROUS - path traversal
const filePath = `/uploads/${userInput}`;

// SAFE - validate and resolve path
function safeReadFile(userInput, baseDir) {
  const safePath = path.resolve(baseDir, path.basename(userInput));
  if (!safePath.startsWith(path.resolve(baseDir))) {
    throw new Error('Invalid file path');
  }
  return fs.readFileSync(safePath);
}
```

## Request Handling

### Rate limiting

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, max: 100,
  message: 'Too many requests', standardHeaders: true, legacyHeaders: false
});
app.use(limiter);

// Stricter limits for auth endpoints
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, max: 5, message: 'Too many login attempts'
});
app.use('/api/login', authLimiter);
```

### Request size limits

```javascript
app.use(express.json({ limit: '100kb' }));
app.use(express.urlencoded({ extended: true, limit: '100kb' }));

const upload = multer({ limits: { fileSize: 5 * 1024 * 1024 } });
```

### Timeout configuration

```javascript
const server = app.listen(3000);
server.setTimeout(30000);
server.keepAliveTimeout = 65000;
server.headersTimeout = 66000;
```

## Secure Headers

```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"], scriptSrc: ["'self'"], styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"], objectSrc: ["'none'"], upgradeInsecureRequests: []
    }
  },
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  frameguard: { action: 'deny' }
}));
```

## Error Handling

```javascript
// Global error handler - don't expose internals to the client
app.use((err, req, res, next) => {
  console.error(err); // Log full error internally
  res.status(500).json({ error: 'An unexpected error occurred' });
});

// Async error wrapper
const asyncHandler = fn => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/data', asyncHandler(async (req, res) => {
  const data = await fetchData();
  res.json(data);
}));
```

## Environment Variables

```javascript
// NEVER commit secrets to code - use environment variables
const apiKey = process.env.API_KEY;

// Validate required env vars at startup
const required = ['API_KEY', 'DB_URL', 'SESSION_SECRET'];
required.forEach(varName => {
  if (!process.env[varName]) {
    console.error(`Missing required env var: ${varName}`);
    process.exit(1);
  }
});
```

## Regex DoS Prevention

```javascript
// DANGEROUS - evil regex (catastrophic backtracking)
const evilRegex = /^(a+)+$/;
evilRegex.test('aaaaaaaaaaaaaaaaaaaaaaaaaaa!'); // Hangs

// Use safe-regex to check patterns
const safe = require('safe-regex');
if (!safe(userProvidedRegex)) throw new Error('Unsafe regex pattern');

// Or use re2 for guaranteed linear time
const RE2 = require('re2');
const pattern = new RE2('^[a-z]+$');
```

## NPM Security Checklist

- [ ] Run `npm audit` regularly and in CI/CD
- [ ] Use `npm ci` instead of `npm install` in CI
- [ ] Enable 2FA on npm account
- [ ] Use lockfiles and commit them
- [ ] Review new dependencies before installation
- [ ] Use `--ignore-scripts` for untrusted packages
- [ ] Set up automated vulnerability scanning (Snyk, Dependabot)
- [ ] Keep dependencies updated
- [ ] Avoid typosquatting by double-checking package names

OWASP References:
- https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html
