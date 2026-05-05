---
name: oauth21-implementation
description: Enforce OAuth 2.1 implementation in authorization servers for MCP ecosystems. Use when building, configuring, or reviewing authorization servers that serve MCP clients and servers.
category: "secure_development"
subcategory: "authorization-server"
---

# OAuth 2.1 Implementation for Authorization Servers

## Security Requirement

Authorization servers MUST implement OAuth 2.1 for both confidential and public clients. OAuth 2.1 consolidates security best practices from OAuth 2.0 and its extensions into a single specification.

## Key OAuth 2.1 Requirements

| Requirement | Details |
|---|---|
| **PKCE required** | All authorization code grants MUST use PKCE (RFC 7636), even for confidential clients |
| **Redirect URI exact matching** | Redirect URIs MUST be compared using exact string matching |
| **No implicit grant** | The implicit grant type is removed |
| **No resource owner password grant** | The ROPC grant type is removed |
| **Refresh token rotation** | Refresh tokens MUST be sender-constrained or one-time use |
| **Bearer token usage** | Per RFC 6750 with additional security requirements |

## Required Grants for MCP Ecosystem

The authorization server MUST support:

- **`authorization_code` + PKCE**: For human users via MCP clients (public clients)
- **`client_credentials`**: For service-to-service MCP communication (confidential clients)
- **`device_code`**: For CLI tools and headless MCP clients
- **Token Exchange** (RFC 8693): For MCP servers accessing downstream tools

## Implementation Checklist

- [ ] Implement OAuth 2.1 compliant authorization code flow with mandatory PKCE
- [ ] Enforce exact redirect URI matching
- [ ] Remove or disable implicit and ROPC grant types
- [ ] Implement refresh token rotation (one-time use or sender-constrained)
- [ ] Support `client_credentials` grant for confidential clients
- [ ] Support `device_code` grant for CLI/headless clients
- [ ] Implement Token Exchange (RFC 8693)
- [ ] Issue short-lived access tokens (TTL ≤15min recommended)
- [ ] Support resource indicators (RFC 8707) for multi-resource environments
