---
name: protected-resource-metadata
description: Enforce OAuth 2.0 Protected Resource Metadata implementation in MCP servers. Use when building, configuring, or reviewing MCP server authentication and authorization discovery.
category: "secure_development"
subcategory: "mcp-server"
---

# Protected Resource Metadata for MCP Servers

## Security Requirement

MCP servers MUST implement OAuth 2.0 Protected Resource Metadata (RFC 9728). MCP clients MUST use this metadata to discover the authorized authorization servers for a given MCP server.

## What It Provides

Protected Resource Metadata allows MCP clients to discover:
- Which authorization servers are trusted by the MCP server
- What scopes are available (`scopes_supported`)
- What token formats and mechanisms are required

## Implementation Checklist

- [ ] Expose a `/.well-known/oauth-protected-resource` endpoint
- [ ] Include `resource` identifier matching the MCP server's URL
- [ ] List all trusted authorization servers in `authorization_servers`
- [ ] Publish `scopes_supported` for available permissions
- [ ] Ensure metadata is served over HTTPS
- [ ] Keep metadata up to date when authorization configuration changes

## Example: Protected Resource Metadata Response

```json
{
  "resource": "https://mcp-server.example.com",
  "authorization_servers": [
    "https://auth.example.com"
  ],
  "scopes_supported": [
    "tools:read",
    "tools:execute",
    "resources:read"
  ],
  "bearer_methods_supported": ["header"],
  "resource_documentation": "https://docs.example.com/mcp-api"
}
```
