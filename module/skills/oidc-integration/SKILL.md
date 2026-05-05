---
name: oidc-integration
description: Enforce OIDC IdP integration for inference engines. Use when designing, building, or reviewing authentication for inference engines, LLM APIs, or AI model serving endpoints.
category: "secure_development"
subcategory: "inference-engine"
---

# OIDC Integration for Inference Engines

## Security Requirement

Inference engines MUST integrate with external OIDC Identity Providers (e.g., Keycloak) for authentication. They MUST consume tokens issued by the IdP directly and support discovery via `/.well-known/openid-configuration`.

Raw API key authentication alone is not acceptable for production inference engines.

## Required Grant Types

The inference engine MUST support these OAuth 2.0/OIDC grants from the IdP:

| Grant Type | Use Case |
|---|---|
| `authorization_code` + PKCE | Human users via interactive browser flows |
| `client_credentials` | Service accounts and automated workloads |
| `device_code` | CLI tools and headless environments |
| OIDC-A extensions | LLM agents chaining calls across services |

## Implementation Checklist

- [ ] Configure inference engine to discover IdP via `/.well-known/openid-configuration`
- [ ] Implement `authorization_code` + PKCE flow for human users
- [ ] Implement `client_credentials` flow for service accounts
- [ ] Implement `device_code` flow for CLI/tools
- [ ] Support OIDC-A extensions for agent-chained calls
- [ ] Validate all incoming tokens against the IdP's JWKS endpoint
- [ ] Reject requests without valid IdP-issued tokens

## Example: IdP Discovery Configuration

```yaml
auth:
  idp:
    issuer: "https://your-idp.com"
    discovery_url: "https://your-idp.com/.well-known/openid-configuration"
    jwks_uri: "https://your-idp.com/.well-known/jwks.json"
    supported_grants:
      - authorization_code
      - client_credentials
      - device_code
    pkce_required: true
```
