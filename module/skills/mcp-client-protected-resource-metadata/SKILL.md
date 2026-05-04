---
name: mcp-client-protected-resource-metadata
description: Enforce use of OAuth 2.0 Protected Resource Metadata in MCP clients for discovering authorization servers. Use when building or reviewing MCP client authentication flows and authorization server discovery.
category: "secure_development"
subcategory: "mcp-client"
---

# Protected Resource Metadata Usage in MCP Clients

## Security Requirement

MCP clients MUST use OAuth 2.0 Protected Resource Metadata (RFC 9728) to discover the authorized authorization servers for any MCP server they connect to. Clients MUST NOT hardcode or manually configure authorization server URLs when the MCP server provides Protected Resource Metadata.

## Discovery Flow

```
1. MCP client attempts to access MCP server resource
2. MCP server returns 401 with WWW-Authenticate header
3. MCP client fetches /.well-known/oauth-protected-resource from MCP server
4. Extract authorization_servers list from the metadata
5. Use the authorization server(s) listed for token acquisition
6. Authenticate with the authorization server and obtain token
7. Retry the original request with the obtained token
```

## Metadata Fields to Consume

| Field | Usage |
|---|---|
| `authorization_servers` | List of trusted authorization server URLs to use |
| `scopes_supported` | Available scopes to request during authorization |
| `bearer_methods_supported` | How to present the bearer token (e.g., `header`) |

## Implementation Checklist

- [ ] On 401 response, fetch `/.well-known/oauth-protected-resource` from the MCP server
- [ ] Parse the `authorization_servers` field and select appropriate server
- [ ] Use `scopes_supported` to inform scope requests
- [ ] Respect `bearer_methods_supported` when presenting tokens
- [ ] Cache the metadata with appropriate TTL to avoid repeated lookups
- [ ] Re-fetch metadata when authorization fails after token refresh
