# File Upload Security Reference

## Core Protection Checklist

- [ ] Validate file extension (allowlist only)
- [ ] Validate Content-Type header
- [ ] Validate file signature (magic bytes)
- [ ] Generate new random filename
- [ ] Enforce file size limits
- [ ] Store outside webroot
- [ ] Scan for malware
- [ ] Require authentication
- [ ] Implement CSRF protection

## Extension Validation

### Allowlist approach

```javascript
const ALLOWED_EXTENSIONS = {
  images: ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
  documents: ['.pdf', '.docx', '.xlsx'],
  data: ['.csv', '.json']
};

function validateExtension(filename, category) {
  const ext = path.extname(filename).toLowerCase();
  return ALLOWED_EXTENSIONS[category]?.includes(ext) ?? false;
}
```

### Dangerous extensions to block

```javascript
const DANGEROUS_EXTENSIONS = [
  '.php', '.php3', '.php4', '.php5', '.phtml',       // server-side execution
  '.asp', '.aspx', '.ascx', '.ashx',
  '.jsp', '.jspx', '.jspa',
  '.cgi', '.pl', '.py', '.rb',
  '.exe', '.dll', '.bat', '.cmd', '.com', '.msi', '.ps1', // Windows executable
  '.js', '.vbs', '.wsf', '.hta',                     // script files
  '.htaccess', '.htpasswd', '.config', '.ini',       // config files
  '.zip', '.tar', '.gz', '.rar', '.7z'               // archives (can hide malicious files)
];
```

### Double-extension prevention

```javascript
function sanitizeFilename(filename) {
  const parts = filename.split('.');
  if (parts.length > 2) {
    return `${parts[0]}.${parts[parts.length - 1]}`;
  }
  // Or generate a completely new filename
  const ext = path.extname(filename).toLowerCase();
  const uuid = crypto.randomUUID();
  return `${uuid}${ext}`;
}
```

## Content-Type Validation

```javascript
const ALLOWED_MIME_TYPES = {
  '.jpg': ['image/jpeg'], '.jpeg': ['image/jpeg'],
  '.png': ['image/png'], '.gif': ['image/gif'], '.webp': ['image/webp'],
  '.pdf': ['application/pdf'],
  '.docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']
};

function validateMimeType(file) {
  const ext = path.extname(file.originalname).toLowerCase();
  const allowedMimes = ALLOWED_MIME_TYPES[ext];
  if (!allowedMimes) return false;
  return allowedMimes.includes(file.mimetype);
}
```

## File Signature (Magic Bytes) Validation

```javascript
const FILE_SIGNATURES = {
  jpg: Buffer.from([0xFF, 0xD8, 0xFF]),
  png: Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
  gif: Buffer.from([0x47, 0x49, 0x46, 0x38]),
  pdf: Buffer.from([0x25, 0x50, 0x44, 0x46]),
  zip: Buffer.from([0x50, 0x4B, 0x03, 0x04])
};

async function validateFileSignature(filePath, expectedType) {
  const buffer = Buffer.alloc(8);
  const fd = await fs.open(filePath, 'r');
  await fd.read(buffer, 0, 8, 0);
  await fd.close();
  const signature = FILE_SIGNATURES[expectedType];
  if (!signature) return false;
  return buffer.slice(0, signature.length).equals(signature);
}
```

## Safe Storage

```javascript
const multer = require('multer');
const path = require('path');
const crypto = require('crypto');

// Store OUTSIDE webroot
const UPLOAD_DIR = '/var/app/uploads';  // Not in /public/

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const date = new Date().toISOString().split('T')[0];
    const dir = path.join(UPLOAD_DIR, date);
    fs.mkdirSync(dir, { recursive: true });
    cb(null, dir);
  },
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    const name = crypto.randomBytes(16).toString('hex');
    cb(null, `${name}${ext}`);
  }
});

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024, files: 1 },
  fileFilter: (req, file, cb) => {
    if (!validateMimeType(file)) { cb(new Error('Invalid file type')); return; }
    cb(null, true);
  }
});
```

## Secure File Serving

```javascript
// Serve files through application, not directly
app.get('/files/:id', async (req, res) => {
  if (!req.user || !canAccessFile(req.user, req.params.id)) {
    return res.status(403).send('Forbidden');
  }
  const fileRecord = await db.getFile(req.params.id); // from DB, not user input
  if (!fileRecord) return res.status(404).send('Not found');

  res.setHeader('Content-Type', fileRecord.mimeType);
  res.setHeader('Content-Disposition', `attachment; filename="${fileRecord.safeName}"`);
  res.setHeader('X-Content-Type-Options', 'nosniff');

  const stream = fs.createReadStream(fileRecord.path);
  stream.pipe(res);
});
```

## Image Rewriting

Destroy potential malicious content by re-encoding images:

```javascript
const sharp = require('sharp');

async function sanitizeImage(inputPath, outputPath) {
  await sharp(inputPath).rotate().toFormat('jpeg', { quality: 90 }).toFile(outputPath);
}
```

## ZIP File Handling

```javascript
const AdmZip = require('adm-zip');
const path = require('path');

function safeExtractZip(zipPath, destDir, maxSize = 100 * 1024 * 1024) {
  const zip = new AdmZip(zipPath);
  const entries = zip.getEntries();
  let totalSize = 0;

  for (const entry of entries) {
    const entryPath = path.join(destDir, entry.entryName);
    if (!entryPath.startsWith(path.resolve(destDir))) {
      throw new Error('Path traversal detected');
    }
    totalSize += entry.header.size;
    if (totalSize > maxSize) throw new Error('Extracted size exceeds limit');

    const ratio = entry.header.size / entry.header.compressedSize;
    if (ratio > 100) throw new Error('Suspicious compression ratio'); // zip bomb indicator
  }

  zip.extractAllTo(destDir, true);
}
```

## Express.js Complete Example

```javascript
const express = require('express');
const multer = require('multer');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs').promises;

const app = express();

const UPLOAD_DIR = '/var/app/uploads';
const MAX_FILE_SIZE = 5 * 1024 * 1024;
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif'];

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: MAX_FILE_SIZE },
  fileFilter: (req, file, cb) => {
    if (!ALLOWED_TYPES.includes(file.mimetype)) {
      cb(new multer.MulterError('LIMIT_UNEXPECTED_FILE'));
      return;
    }
    cb(null, true);
  }
});

app.post('/upload',
  requireAuth,
  csrfProtection,
  upload.single('file'),
  async (req, res) => {
    try {
      const file = req.file;
      if (!file) return res.status(400).json({ error: 'No file' });

      if (!validateMagicBytes(file.buffer, file.mimetype)) {
        return res.status(400).json({ error: 'Invalid file' });
      }

      const ext = path.extname(file.originalname).toLowerCase();
      const filename = `${crypto.randomUUID()}${ext}`;
      const filepath = path.join(UPLOAD_DIR, filename);

      await fs.writeFile(filepath, file.buffer);

      const fileRecord = await db.createFile({
        userId: req.user.id, filename,
        originalName: file.originalname, mimeType: file.mimetype, size: file.size
      });

      res.json({ id: fileRecord.id });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Upload failed' });
    }
  }
);
```

OWASP Reference: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
