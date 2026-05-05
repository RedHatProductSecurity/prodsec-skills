---
name: discovery-mechanisms
description: Enforce support for OAuth 2.0 and OIDC discovery mechanisms in MCP clients. Use when building, configuring, or reviewing MCP client authentication and authorization server discovery.
category: "secure_development"
subcategory: "mcp-client"
---

# Discovery Mechanisms for MCP Clients

## Security Requirement

MCP clients MUST support both of the following discovery mechanisms for locating authorization servers:

1. **OAuth 2.0 Authorization Server Metadata** (RFC 8414)
2. **OpenID Connect Discovery 1.0**

Supporting both mechanisms ensures interoperability with any authorization server an MCP server may designate.

## OAuth 2.0 Authorization Server Metadata (RFC 8414)

The client fetches metadata from `/.well-known/oauth-authorization-server`:

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "scopes_supported": ["tools:read", "tools:execute"],
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "client_credentials"],
  "code_challenge_methods_supported": ["S256"]
}
```

## OpenID Connect Discovery 1.0

The client fetches metadata from `/.well-known/openid-configuration`:

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "userinfo_endpoint": "https://auth.example.com/userinfo",
  "jwks_uri": "https://auth.example.com/.well-known/jwks.json",
  "scopes_supported": ["openid", "profile", "tools:read"],
  "response_types_supported": ["code"],
  "id_token_signing_alg_values_supported": ["RS256"]
}
```

## Discovery Flow

```
1. MCP client connects to MCP server
2. MCP client fetches Protected Resource Metadata from MCP server
3. Extract authorization_servers from the metadata
4. For each authorization server, attempt discovery:
   a. Try /.well-known/openid-configuration
   b. Try /.well-known/oauth-authorization-server
   c. Use whichever succeeds (prefer OIDC if both available)
5. Use discovered endpoints for authentication flows
```

## Implementation Checklist

- [ ] Implement fetching and parsing of `/.well-known/openid-configuration`
- [ ] Implement fetching and parsing of `/.well-known/oauth-authorization-server`
- [ ] Handle both metadata formats and extract required endpoints
- [ ] Cache discovery metadata with appropriate TTL
- [ ] Validate `issuer` in metadata matches the expected authorization server URL
- [ ] Handle network errors and fallback between discovery mechanisms
