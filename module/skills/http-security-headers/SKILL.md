---
name: http-security-headers
description: >
  Verify and configure HTTP response security headers. Use when reviewing web
  server configuration, reverse proxy setup, or application middleware that
  sets response headers.
category: "secure_development"
subcategory: "web-security"
---

# HTTP Security Headers

## Strict-Transport-Security (HSTS)

Forces HTTPS connections for a specified period, preventing protocol downgrade and MITM attacks.

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- Set `max-age` to at least one year (31536000 seconds)
- Include `includeSubDomains` to protect all subdomains
- Add `preload` only after verifying all subdomains support HTTPS, then submit to the [HSTS preload list](https://hstspreload.org/)

## X-Frame-Options

Controls whether a page can be rendered in a frame or iframe, mitigating clickjacking.

```
X-Frame-Options: DENY
```

- Use `DENY` to prevent framing entirely
- Use `SAMEORIGIN` only when the application legitimately embeds its own pages
- Prefer the `frame-ancestors` CSP directive for more granular control

## X-Content-Type-Options

Prevents MIME sniffing, forcing the browser to use the declared `Content-Type`.

```
X-Content-Type-Options: nosniff
```

- Always include this header; there is no reason to omit it

## X-XSS-Protection

Instructs older browsers to activate built-in XSS filtering.

```
X-XSS-Protection: 1; mode=block
```

- Use `mode=block` to block the entire page rather than attempting to sanitize
- Test thoroughly; the filter can cause false positives on some pages
- Modern browsers rely on CSP instead; this header is defense-in-depth for legacy clients

## Content-Security-Policy (CSP)

Defines trusted sources for scripts, styles, images, and other resources. The most powerful header for preventing XSS and code injection.

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; frame-ancestors 'none'
```

- Start with a restrictive policy and relax only as needed
- Use `Content-Security-Policy-Report-Only` first to monitor violations without breaking functionality
- Avoid `unsafe-inline` and `unsafe-eval` for `script-src`; use nonces or hashes instead
- Set `object-src 'none'` to block plugins (Flash, Java)
- Set `frame-ancestors 'none'` to replace `X-Frame-Options`

## Referrer-Policy

Controls how much referrer information is sent with requests, protecting user privacy.

```
Referrer-Policy: strict-origin-when-cross-origin
```

- Use `no-referrer` when maximum privacy is required
- Use `same-origin` to send referrer only on same-origin requests
- Use `strict-origin-when-cross-origin` as a balanced default

## Cache-Control

Controls caching behavior for responses. Misconfigured caching of sensitive data is a common vulnerability.

**Sensitive responses (authentication, personal data, tokens):**

```
Cache-Control: no-store, no-cache, must-revalidate, max-age=0
```

**Static assets (images, fonts, versioned bundles):**

```
Cache-Control: public, max-age=31536000, immutable
```

- Use `no-store` for any response containing user-specific or sensitive data
- Never cache authentication responses or pages containing tokens
- Use `private` when content is user-specific but cacheable by the browser

## Implementation Checklist

- [ ] HSTS is set with `max-age` >= 31536000 and `includeSubDomains`
- [ ] `X-Frame-Options: DENY` or CSP `frame-ancestors 'none'` is set
- [ ] `X-Content-Type-Options: nosniff` is present on all responses
- [ ] CSP is configured and does not use `unsafe-inline` or `unsafe-eval` for scripts
- [ ] `Referrer-Policy` is set to `strict-origin-when-cross-origin` or stricter
- [ ] Sensitive responses set `Cache-Control: no-store`
- [ ] Static assets use long-lived `Cache-Control` with versioned filenames
- [ ] Headers are verified with a scanner (e.g., [securityheaders.com](https://securityheaders.com/))
