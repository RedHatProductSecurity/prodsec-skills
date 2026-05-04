---
name: mcp-client-dynamic-client-registration
description: Support OAuth 2.0 Dynamic Client Registration in MCP clients. Use when building or reviewing MCP client registration with authorization servers that support dynamic registration.
category: "secure_development"
subcategory: "mcp-client"
---

# Dynamic Client Registration for MCP Clients

## Security Recommendation

Authorization servers and MCP clients MAY support the OAuth 2.0 Dynamic Client Registration Protocol (RFC 7591). This allows MCP clients to register with authorization servers automatically without manual pre-registration.

## When to Use

Dynamic Client Registration is useful when:
- MCP clients connect to many different MCP servers with different authorization servers
- Manual client registration is impractical at scale
- The authorization server supports it (check the discovery metadata for `registration_endpoint`)

## Registration Flow

```
1. MCP client discovers authorization server via Protected Resource Metadata
2. MCP client fetches authorization server metadata
3. Check for registration_endpoint in the metadata
4. If available, POST client registration request:
   POST /register HTTP/1.1
   Content-Type: application/json
   {
     "client_name": "MCP Client App",
     "redirect_uris": ["https://client.example.com/callback"],
     "grant_types": ["authorization_code"],
     "response_types": ["code"],
     "token_endpoint_auth_method": "none"
   }
5. Authorization server returns client_id (and optionally client_secret)
6. Use returned credentials for subsequent OAuth flows
```

## Implementation Checklist

- [ ] Check authorization server metadata for `registration_endpoint`
- [ ] Implement RFC 7591 client registration request
- [ ] Store returned `client_id` and `client_secret` securely
- [ ] Handle registration errors gracefully
- [ ] Support re-registration if credentials are lost or expired
- [ ] Prefer Client ID Metadata Documents when both mechanisms are available
