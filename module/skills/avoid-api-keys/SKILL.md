---
name: avoid-api-keys
description: Avoid using API keys in production AI systems. Use when reviewing authentication mechanisms, designing production deployments, or auditing credential management in AI and agentic systems.
category: "secure_development"
subcategory: "api-keys"
---

# Avoid API Keys in Production

## Security Recommendation

API keys SHOULD NOT be used in production environments. Short-lived, scoped bearer tokens issued by an identity provider are preferable.

## Why API Keys Are Problematic

| Issue | Impact |
|---|---|
| **Long-lived** | Extended exposure window if compromised |
| **Difficult to rotate** | Rotation requires coordination across all consumers |
| **Lack fine-grained scoping** | Cannot limit permissions per request or context |
| **No sender binding** | Any holder of the key can use it from anywhere |
| **No standard revocation** | No instant revocation mechanism across distributed systems |
| **Poor audit trail** | API keys don't carry identity claims about the caller |

## Preferred Alternative

Use short-lived, scoped bearer tokens from an OIDC Identity Provider:

| Property | API Key | IdP-Issued Token |
|---|---|---|
| Lifetime | Long-lived (months/years) | Short-lived (≤15 minutes) |
| Scoping | Broad or none | Per-request scopes |
| Revocation | Manual, slow | Instant via IdP + local blacklist |
| Identity | Opaque | Rich claims (sub, iss, aud, scope) |
| Rotation | Manual | Automatic via refresh tokens |
| Sender binding | None | DPoP or mTLS certificate binding |

## Migration Path

For systems currently using API keys:

1. Deploy an API gateway that accepts API keys from legacy clients
2. Gateway exchanges API keys for short-lived IdP tokens
3. Backend services only accept IdP tokens (never raw API keys)
4. Set deprecation timeline for API key consumers
5. Migrate consumers to OIDC flows
6. Retire API key support

## Credential Storage

Credentials (API keys, tokens, secrets) MUST NEVER be stored in source code. This applies to all credentials including those used to connect to third-party model endpoints. Credentials must be managed and stored securely using:

- Secret management systems (e.g., HashiCorp Vault, Kubernetes Secrets, AWS Secrets Manager)
- Environment variables injected at runtime (not baked into images)
- Encrypted configuration files with access controls

## Implementation Checklist

- [ ] Inventory all API keys in use across AI systems
- [ ] Classify each by use case (human user, service, agent, CI/CD)
- [ ] Deploy an OIDC Identity Provider if not already available
- [ ] For each use case, implement the appropriate OAuth 2.1 grant type
- [ ] Deploy API gateway for legacy API key conversion (if needed during migration)
- [ ] Set and communicate a deprecation timeline for API keys
- [ ] Monitor API key usage and track migration progress
- [ ] Remove API key support after migration is complete
- [ ] Scan source code repositories for hardcoded credentials
- [ ] Migrate any discovered hardcoded credentials to a secret management system
