# JWT Security Reference

## Common Vulnerabilities

### "None" algorithm attack

Attacker changes algorithm to "none" to bypass signature verification.

```javascript
// VULNERABLE - accepts any algorithm
const decoded = jwt.verify(token, secret);

// SECURE - explicitly specify allowed algorithms
const decoded = jwt.verify(token, secret, {
  algorithms: ['HS256']
});
```

### Algorithm confusion attack

Switching from RS256 to HS256 using the public key as the secret.

```javascript
// VULNERABLE - auto-detects algorithm
const decoded = jwt.verify(token, publicKey);

// SECURE - specify expected algorithm
const decoded = jwt.verify(token, publicKey, {
  algorithms: ['RS256']
});
```

### Weak secret

```javascript
// VULNERABLE - weak secret, brute-forceable
const token = jwt.sign(payload, 'password123');

// SECURE - strong random secret (256+ bits)
const crypto = require('crypto');
const secret = crypto.randomBytes(32);
const token = jwt.sign(payload, secret);

// Or use RSA keys
const privateKey = fs.readFileSync('private.pem');
const token = jwt.sign(payload, privateKey, { algorithm: 'RS256' });
```

## Token Sidejacking Prevention

Add a fingerprint to prevent stolen-token reuse:

```javascript
const crypto = require('crypto');

function generateFingerprint() {
  return crypto.randomBytes(32).toString('hex');
}

function createToken(userId, fingerprint) {
  const fingerprintHash = crypto.createHash('sha256').update(fingerprint).digest('hex');
  return jwt.sign({ sub: userId, fph: fingerprintHash }, secret, { expiresIn: '15m' });
}

// Set fingerprint as httpOnly cookie
res.cookie('__Secure-Fgp', fingerprint, {
  httpOnly: true, secure: true, sameSite: 'Strict', maxAge: 15 * 60 * 1000
});

// Validate both token and fingerprint
function validateToken(token, fingerprintCookie) {
  const decoded = jwt.verify(token, secret, { algorithms: ['HS256'] });
  const fingerprintHash = crypto.createHash('sha256').update(fingerprintCookie).digest('hex');
  if (decoded.fph !== fingerprintHash) throw new Error('Invalid fingerprint');
  return decoded;
}
```

## Token Storage (Client-Side)

### Recommended: sessionStorage + fingerprint cookie

```javascript
sessionStorage.setItem('token', jwt);
sessionStorage.removeItem('token'); // on logout

fetch('/api/data', {
  headers: { 'Authorization': `Bearer ${sessionStorage.getItem('token')}` }
});
```

### Alternative: httpOnly cookie

```javascript
res.cookie('token', jwt, {
  httpOnly: true, secure: true, sameSite: 'Strict', maxAge: 15 * 60 * 1000
});
// Needs CSRF protection alongside cookie-based auth.
```

### Avoid: localStorage

```javascript
// VULNERABLE - persists after browser close, accessible to XSS
localStorage.setItem('token', jwt);
```

## Token Expiration

```javascript
// Short-lived access tokens (15-60 minutes)
const accessToken = jwt.sign(payload, secret, { expiresIn: '15m' });

// Longer refresh tokens (days/weeks)
const refreshToken = jwt.sign({ sub: userId, type: 'refresh' }, refreshSecret, { expiresIn: '7d' });

app.post('/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  try {
    const decoded = jwt.verify(refreshToken, refreshSecret, { algorithms: ['HS256'] });
    if (decoded.type !== 'refresh') throw new Error('Invalid token type');
    if (await isTokenRevoked(refreshToken)) throw new Error('Token revoked');
    const newAccessToken = jwt.sign({ sub: decoded.sub }, secret, { expiresIn: '15m' });
    res.json({ accessToken: newAccessToken });
  } catch (error) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});
```

## Token Revocation

JWTs are stateless, so revocation needs an additional mechanism:

```javascript
// Denylist approach (use Redis in production, not an in-memory Map)
const revokedTokens = new Map();

function revokeToken(token) {
  const decoded = jwt.decode(token);
  const tokenId = decoded.jti;
  const expiry = decoded.exp * 1000;
  revokedTokens.set(tokenId, expiry);
  setTimeout(() => revokedTokens.delete(tokenId), expiry - Date.now());
}

function isTokenRevoked(token) {
  const decoded = jwt.decode(token);
  return revokedTokens.has(decoded.jti);
}

// Include jti (JWT ID) in tokens
const token = jwt.sign({ sub: userId, jti: crypto.randomUUID() }, secret, { expiresIn: '15m' });
```

## Token Information Disclosure

JWTs are base64-encoded, not encrypted — payload data is visible to anyone who has the token.

```javascript
// VULNERABLE - sensitive data in payload
const token = jwt.sign({ sub: userId, ssn: '123-45-6789', salary: 100000 }, secret);

// SECURE - minimal claims
const token = jwt.sign({ sub: userId, role: 'user' }, secret);

// If sensitive data is required, encrypt the token itself
const encryptedToken = encrypt(token, encryptionKey);
```

## Validation Middleware

```javascript
function authenticateToken(req, res, next) {
  const authHeader = req.headers.authorization;
  const token = authHeader?.split(' ')[1]; // "Bearer TOKEN"
  if (!token) return res.status(401).json({ error: 'Token required' });

  try {
    const decoded = jwt.verify(token, secret, {
      algorithms: ['HS256'], issuer: 'myapp', audience: 'myapp-users'
    });

    const fingerprint = req.cookies['__Secure-Fgp'];
    if (!validateFingerprint(decoded, fingerprint)) throw new Error('Invalid fingerprint');
    if (isTokenRevoked(token)) throw new Error('Token revoked');

    req.user = decoded;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    return res.status(403).json({ error: 'Invalid token' });
  }
}
```

## Security Checklist

- [ ] Explicit algorithm specification (never auto-detect)
- [ ] Strong secret (256+ bits) or RSA keys
- [ ] Short expiration times (15-60 minutes for access tokens)
- [ ] Token fingerprint with httpOnly cookie
- [ ] Validate issuer (`iss`) and audience (`aud`) claims
- [ ] Implement token revocation mechanism
- [ ] No sensitive data in payload
- [ ] Store in sessionStorage (not localStorage)
- [ ] Send via Authorization header
- [ ] HTTPS only

OWASP Reference: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
