---
name: web-application-security
description: >
  Review web application security controls against OWASP-aligned risks. Use
  when building, auditing, or reviewing server-side web applications that
  handle user input, sessions, authentication, or access control.
category: "secure_development"
subcategory: "web-security"
---

# Web Application Security

## Vulnerability Classes

| Category | Threats |
|---|---|
| **Input validation** | Command injection, SQL injection, Cross-Site Scripting (XSS) |
| **Upload handling** | Local File Inclusion (LFI), Remote File Inclusion (RFI) |
| **Session management** | Man-in-the-Middle (MITM), session fixation, session hijacking |
| **Data exposure** | Cleartext data theft, insecure storage, cache leaks |
| **Authentication** | Credential stuffing, brute force, account enumeration |
| **Access control** | Privilege escalation, IDOR, missing function-level checks |

## Security Requirements

### Server-Side Controls

All security controls MUST be implemented server-side. Client-side validation is a UX convenience, not a security boundary. This applies to:

- Input validation and sanitization
- Upload type and size restrictions
- Authentication and session management
- Authorization decisions

### Network-Level Protections

- Deploy a Web Application Firewall (WAF) in front of public-facing applications where feasible
- Enable DDoS protection on Internet-facing endpoints
- Terminate TLS at the edge; enforce HTTPS end-to-end

### CORS

- Configure Cross-Origin Resource Sharing to allow only known, explicitly listed origins
- Never use wildcard (`*`) origins on endpoints that accept credentials
- Validate the `Origin` header server-side before reflecting it

### CSRF Protection

- Enable framework-provided CSRF token mechanisms (e.g., Django CSRF middleware, Spring CSRF, Rails `protect_from_forgery`)
- Use `SameSite` cookie attributes as a defense-in-depth layer
- Verify tokens on every state-changing request

### Session Management

- Generate a new session ID after successful authentication (prevent session fixation)
- Never expose session IDs in URLs
- Store session tokens in secure, HttpOnly, SameSite cookies
- Invalidate sessions on logout, idle timeout, and absolute timeout
- Bind sessions to client fingerprint where feasible (IP, User-Agent)

### Sensitive Data Handling

- Encrypt sensitive data in transit (TLS 1.2+) and at rest
- Do not store sensitive data longer than necessary
- Disable caching for responses containing sensitive data (`Cache-Control: no-store`)
- Never log passwords, tokens, or PII

### Authentication Hardening

- Implement multi-factor authentication for privileged or Internet-facing accounts
- Use uniform error responses for login, registration, and credential recovery to prevent account enumeration (e.g., "Invalid credentials" regardless of whether the username exists)
- Enforce account lockout or progressive delays after repeated authentication failures

### Access Control

- Adopt least-privilege and deny-by-default for every request
- Route all requests through a centralized access-control verification layer
- Enforce authorization on direct object references; never rely on obscurity of IDs
- Re-validate privileges on long-lived sessions

## Implementation Checklist

- [ ] All validation and authorization logic runs server-side
- [ ] WAF or equivalent network protection is in place for public endpoints
- [ ] CORS whitelist is explicit (no wildcard with credentials)
- [ ] CSRF tokens are validated on every state-changing request
- [ ] Session IDs rotate after authentication
- [ ] Sessions are invalidated on logout and timeout
- [ ] Sensitive data responses set `Cache-Control: no-store`
- [ ] MFA is available for Internet-facing authentication
- [ ] Login/registration/recovery responses are uniform (no enumeration)
- [ ] Every request passes through centralized access-control checks

## References

- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- [OWASP Proactive Controls: Protect Data Everywhere](https://owasp.org/www-project-proactive-controls/v3/en/c8-protect-data-everywhere)
- [OWASP Proactive Controls: Enforce Access Controls](https://owasp.org/www-project-proactive-controls/v3/en/c7-enforce-access-controls)
