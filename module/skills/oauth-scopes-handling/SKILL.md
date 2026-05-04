---
name: oauth-scopes-handling
description: Handle OAuth scopes correctly in MCP clients. Use when building or reviewing MCP client authorization flows, scope negotiation, or permission handling.
category: "secure_development"
subcategory: "mcp-client"
---

# OAuth Scopes Handling in MCP Clients

## Security Requirement

MCP clients MUST correctly discover and use OAuth scopes when authenticating to MCP servers. Scopes define the permissions the client is requesting and MUST be handled as follows:

## Scope Discovery Priority

1. **WWW-Authenticate header**: If the MCP client receives a `scope` parameter in the `WWW-Authenticate` header of a 401 response, it MUST use those scopes.
2. **Protected Resource Metadata**: If no scope is provided in the 401 response, check `scopes_supported` in the Protected Resource Metadata (PRM) document.

## Flow

```
1. MCP client attempts to access MCP server resource
2. MCP server returns 401 Unauthorized with:
   WWW-Authenticate: Bearer realm="mcp", scope="tools:read tools:execute"
3. MCP client extracts scope from WWW-Authenticate header
   → If scope present: use those scopes for authorization request
   → If scope absent: fetch PRM and use scopes_supported
4. MCP client requests authorization with the discovered scopes
```

## Example: WWW-Authenticate with Scope

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="mcp-server",
  scope="tools:read tools:execute resources:read"
```

The client should request exactly these scopes (or a subset) from the authorization server.

## Implementation Checklist

- [ ] Parse `scope` parameter from `WWW-Authenticate` header on 401 responses
- [ ] Fall back to `scopes_supported` from Protected Resource Metadata if no scope in 401
- [ ] Request only the scopes needed for the intended operation (principle of least privilege)
- [ ] Handle scope downgrading gracefully (authorization server may grant fewer scopes)
- [ ] Re-request scopes if the server indicates insufficient permissions on subsequent requests
