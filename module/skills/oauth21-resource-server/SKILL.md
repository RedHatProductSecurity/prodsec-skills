---
name: oauth21-resource-server
description: Enforce MCP servers to act as OAuth 2.1 resource servers by default. Use when building, configuring, or reviewing MCP server authentication and authorization defaults.
category: "secure_development"
subcategory: "mcp-server"
---

# OAuth 2.1 Resource Server for MCP Servers

## Security Requirement

MCP servers MUST be capable of acting as an OAuth 2.1 resource server, and this MUST be their default behavior. The server should not operate without authentication unless explicitly opted out by the deployer.

## What "Resource Server" Means

As an OAuth 2.1 resource server, the MCP server:

- Accepts and validates OAuth 2.1 access tokens on every request
- Rejects requests without a valid token (401 Unauthorized)
- Enforces scopes from the token against the requested operation
- Publishes its Protected Resource Metadata for client discovery (see `mcp_server/protected-resource-metadata`)

## Default Behavior

| Configuration | Acceptable |
|---|---|
| OAuth 2.1 token validation enabled by default | **Yes (required)** |
| No authentication by default, opt-in OAuth | **No** |
| API key only by default | **No** |
| Open access by default | **No** |

The principle is: **secure by default, opt-out only with explicit configuration**.

## Implementation Checklist

- [ ] Implement OAuth 2.1 resource server capabilities (token validation, scope enforcement)
- [ ] Enable OAuth 2.1 as the default authentication mechanism (not opt-in)
- [ ] Validate access tokens on every incoming request
- [ ] Return 401 Unauthorized for requests without valid tokens
- [ ] Enforce token scopes against the requested operation
- [ ] Publish Protected Resource Metadata (see `mcp_server/protected-resource-metadata`)
- [ ] Allow deployers to configure the authorization server, but not to disable authentication without explicit action
