---
name: file-handling-uploads
description: >
  Apply when reviewing or writing code that accepts file uploads,
  processes user-supplied files, or serves stored files. Covers
  extension validation, content verification, filename security,
  storage isolation, and scanning.
license: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
origin: Adapted from CoSAI Project CodeGuard (https://github.com/cosai-oasis/project-codeguard)
category: "secure_development"
subcategory: "web-security"
---

# File Upload Security

Implement defense-in-depth for file uploads through multi-layered validation, secure storage, proper access controls, and monitoring. Never rely on a single validation method.

## Extension Validation

- Allow-list extensions only for business-critical functionality.
- Apply input validation before validating extensions.
- Avoid double extensions (e.g., `.jpg.php`) and null byte injection (e.g., `.php%00.jpg`).
- Use allow-list approach rather than deny-list for file extensions.
- Validate extensions after decoding the filename to prevent bypass attempts.

## Content Type and File Signature Validation

- Never trust client-supplied Content-Type headers -- they can be spoofed.
- Validate file signatures (magic numbers) in conjunction with Content-Type checking.
- Implement allow-list approach for MIME types as a quick protection layer.
- Use file signature validation but not as a standalone security measure.

## Filename Security

- Generate random filenames (UUID/GUID) instead of using user-supplied names.
- If user filenames are required, implement maximum length limits.
- Restrict characters to alphanumeric, hyphens, spaces, and periods only.
- Prevent leading periods (hidden files) and sequential periods (directory traversal).
- Avoid leading hyphens or spaces for safer shell script processing.

## File Content Validation

- For images, apply image rewriting techniques to destroy malicious content.
- For Microsoft documents, use Apache POI for validation.
- Avoid ZIP files due to numerous attack vectors.
- Implement manual file review in sandboxed environments when resources allow.
- Integrate antivirus scanning and Content Disarm and Reconstruct (CDR) for applicable file types.

## Storage Security

- Store files on different servers for complete segregation when possible.
- Store files outside webroot with administrative access only.
- If storing in webroot, set write-only permissions with proper access controls.
- Use application handlers that map IDs to filenames for public access.
- Consider database storage for specific use cases with DBA expertise.

## Access Control and Authentication

- Require user authentication before allowing file uploads.
- Implement proper authorization levels for file access and modification.
- Set filesystem permissions on the principle of least privilege.
- Scan files before execution if execution permission is required.

## Upload and Download Limits

- Set proper file size limits for upload protection.
- Consider post-decompression size limits for compressed files.
- Implement request limits for download services to prevent DoS attacks.
- Use secure methods to calculate ZIP file sizes safely.

## Additional Security Measures

- Protect file upload endpoints from CSRF attacks.
- Keep all file processing libraries securely configured and updated.
- Implement logging and monitoring for upload activities.
- Provide user reporting mechanisms for illegal content.
- Use secure extraction methods for compressed files.

## Implementation Checklist

- [ ] Extension allow-list enforced; double extension and null byte attacks blocked
- [ ] Magic number validation in addition to Content-Type checking
- [ ] Random filenames generated; user-supplied names sanitized or rejected
- [ ] Image rewriting and/or CDR applied to uploaded content
- [ ] Files stored outside webroot with least-privilege permissions
- [ ] Authentication required for uploads; authorization for access
- [ ] Size limits enforced for uploads and decompressed content
- [ ] CSRF protection on upload endpoints; logging enabled
