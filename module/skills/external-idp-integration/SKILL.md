---
name: external-idp-integration
description: Enforce MCP server integration with external centralized identity providers. Use when building, configuring, or reviewing MCP server authentication against external IdPs like Keycloak.
category: "secure_development"
subcategory: "mcp-server"
---

# External IdP Integration for MCP Servers

## Security Requirement

MCP servers MUST be capable of integrating with centralized identity providers (e.g., Keycloak) for authentication and authorization. The MCP server should not implement its own user store but delegate identity management to an external IdP.

## Why External IdP

| Benefit | Description |
|---|---|
| **Centralized identity** | Single source of truth for user and service identities |
| **Standard protocols** | OIDC/OAuth 2.1 compliance out of the box |
| **Enterprise features** | MFA, federation, session management handled by IdP |
| **Reduced attack surface** | MCP server does not store credentials |
| **Consistent policy** | Same authentication policies across all services |

## Integration Requirements

The MCP server must:

1. Discover the IdP via standard metadata endpoints (`/.well-known/openid-configuration` or `/.well-known/oauth-authorization-server`)
2. Validate tokens issued by the IdP (JWT signature verification against JWKS)
3. Accept tokens from the configured IdP(s) only
4. Allow configuration of the trusted IdP issuer URL

## Example Configuration

```yaml
auth:
  idp:
    issuer: "https://keycloak.example.com/realms/mcp"
    jwks_uri: "https://keycloak.example.com/realms/mcp/protocol/openid-connect/certs"
    audience: "mcp-server"
  require_auth: true
```

## Implementation Checklist

- [ ] Support configuring one or more external IdP issuer URLs
- [ ] Discover IdP endpoints via standard metadata (OIDC Discovery or RFC 8414)
- [ ] Validate JWT tokens against the IdP's JWKS endpoint
- [ ] Verify `iss`, `aud`, `exp`, and `scope` claims on every request
- [ ] Reject tokens from untrusted issuers
- [ ] Support Keycloak and other standard OIDC-compliant IdPs
- [ ] Do not implement a built-in user store; delegate to the external IdP
