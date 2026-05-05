---
name: discovery-mechanism
description: Enforce authorization server metadata discovery for MCP ecosystems. Use when configuring or reviewing authorization server endpoint publication and discovery metadata.
category: "secure_development"
subcategory: "authorization-server"
---

# Discovery Mechanism for Authorization Servers

## Security Requirement

Authorization servers MUST provide at least one of the following discovery mechanisms:

1. **OAuth 2.0 Authorization Server Metadata** (RFC 8414)
2. **OpenID Connect Discovery 1.0**

MCP clients are required to support both, so the authorization server MUST implement at least one to ensure interoperability.

## Option 1: OAuth 2.0 Authorization Server Metadata (RFC 8414)

Expose metadata at `/.well-known/oauth-authorization-server`:

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "registration_endpoint": "https://auth.example.com/register",
  "revocation_endpoint": "https://auth.example.com/oauth/revoke",
  "scopes_supported": ["openid", "tools:read", "tools:execute"],
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "client_credentials", "urn:ietf:params:oauth:grant-type:device_code"],
  "code_challenge_methods_supported": ["S256"],
  "token_endpoint_auth_methods_supported": ["client_secret_basic", "none"]
}
```

## Option 2: OpenID Connect Discovery 1.0

Expose metadata at `/.well-known/openid-configuration`:

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "userinfo_endpoint": "https://auth.example.com/userinfo",
  "jwks_uri": "https://auth.example.com/.well-known/jwks.json",
  "registration_endpoint": "https://auth.example.com/register",
  "scopes_supported": ["openid", "profile", "tools:read", "tools:execute"],
  "response_types_supported": ["code"],
  "id_token_signing_alg_values_supported": ["RS256"]
}
```

## Implementation Checklist

- [ ] Implement at least one discovery endpoint (RFC 8414 or OIDC Discovery)
- [ ] Ensure `issuer` field matches the authorization server's canonical URL
- [ ] List all supported grant types, scopes, and response types
- [ ] Include `registration_endpoint` if Dynamic Client Registration is supported
- [ ] Include `revocation_endpoint` for token revocation
- [ ] Serve metadata over HTTPS
- [ ] Keep metadata up to date when server configuration changes
