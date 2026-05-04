---
name: mcp-client-client-metadata-support
description: Support OAuth Client ID Metadata Documents in MCP clients. Use when building or reviewing MCP client registration and identity presentation to authorization servers.
category: "secure_development"
subcategory: "mcp-client"
---

# OAuth Client ID Metadata Document Support in MCP Clients

## Security Recommendation

Authorization servers and MCP clients SHOULD support OAuth Client ID Metadata Documents. This mechanism allows MCP clients to present their identity and configuration to authorization servers without requiring pre-registration.

## What It Provides

Client ID Metadata Documents allow:
- Clients to self-describe their configuration (redirect URIs, grant types, etc.)
- Authorization servers to validate client properties without prior registration
- A standardized way for clients to present their identity

## How It Works

The MCP client hosts a metadata document at a URL that serves as its `client_id`. The authorization server fetches this document to learn about the client's configuration.

```json
{
  "client_id": "https://mcp-client.example.com/client-metadata",
  "client_name": "MCP Client App",
  "redirect_uris": ["https://mcp-client.example.com/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none",
  "scope": "tools:read tools:execute"
}
```

## Implementation Checklist

- [ ] Host a client metadata document at a stable, HTTPS URL
- [ ] Use the metadata document URL as the `client_id`
- [ ] Include all required fields: `client_id`, `redirect_uris`, `grant_types`, `response_types`
- [ ] Set `token_endpoint_auth_method` to `none` for public clients
- [ ] Serve the metadata document with correct `Content-Type: application/json`
- [ ] Ensure the metadata document is accessible to authorization servers
