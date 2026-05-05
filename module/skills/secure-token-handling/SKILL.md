---
name: secure-token-handling
description: Enforce secure token validation and storage in MCP servers. Use when implementing or reviewing token handling, JWT validation, or token storage in MCP servers.
category: "secure_development"
subcategory: "mcp-server"
---

# Secure Token Handling for MCP Servers

## Security Requirement

MCP servers MUST implement best practices for token validation and secure token storage to prevent token-based attacks.

## Token Validation Requirements

Every incoming token MUST be validated for:

| Check | Details |
|---|---|
| **Signature** | Verify JWT signature against the IdP's JWKS; reject unsigned or weakly signed tokens |
| **Expiry (`exp`)** | Reject expired tokens; do not allow clock skew greater than 30 seconds |
| **Audience (`aud`)** | Must match the MCP server's audience identifier |
| **Issuer (`iss`)** | Must match the trusted IdP issuer URL |
| **Not-before (`nbf`)** | If present, reject tokens used before this time |
| **Token ID (`jti`)** | Check against revocation list if token revocation is supported |

## Secure Token Storage

If the MCP server needs to store tokens (e.g., cached access tokens or refresh tokens for downstream services):

| Requirement | Details |
|---|---|
| **Encrypt at rest** | Tokens stored on disk or in databases must be encrypted |
| **Memory-only when possible** | Prefer in-memory token storage; avoid persisting to disk |
| **Short-lived cache** | Cache tokens only for the duration of their validity |
| **No logging** | Never log token values; log token metadata (jti, sub, exp) instead |
| **Secure deletion** | Clear tokens from memory when no longer needed |

## Anti-Patterns

```python
# WRONG - logging the token
logger.info(f"Received token: {token}")

# WRONG - storing token in plaintext file
with open("tokens.txt", "a") as f:
    f.write(token)

# CORRECT - log metadata only
logger.info(f"Token validated: sub={claims['sub']}, exp={claims['exp']}")
```

## Implementation Checklist

- [ ] Validate JWT signature against IdP JWKS on every request
- [ ] Reject expired tokens with minimal clock skew tolerance (≤30s)
- [ ] Verify `aud` matches the MCP server's identifier
- [ ] Verify `iss` matches the trusted IdP
- [ ] Check `jti` against revocation list if available
- [ ] Never log token values; log only token metadata
- [ ] Encrypt any tokens stored at rest
- [ ] Prefer in-memory token caching over disk persistence
- [ ] Clear tokens from memory when no longer needed
- [ ] Reject tokens with `alg: none` or weak signing algorithms
