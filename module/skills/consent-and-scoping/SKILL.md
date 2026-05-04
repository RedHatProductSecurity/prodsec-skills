---
name: consent-and-scoping
description: Enforce granular OAuth scopes and explicit user consent in MCP servers. Use when designing, building, or reviewing MCP server permission models, scope definitions, or consent flows.
category: "secure_development"
subcategory: "mcp-server"
---

# Consent and Granular Scoping for MCP Servers

## Security Requirement

MCP servers MUST implement granular OAuth scopes and ensure users explicitly consent to them. Scopes should map to specific tool capabilities, not broad "access everything" permissions.

## Granular Scope Design

Define scopes at the tool and action level:

| Scope | Permission |
|---|---|
| `email.send` | Send emails via the email tool |
| `email.read` | Read emails via the email tool |
| `files.read` | Read files via the filesystem tool |
| `files.write` | Write files via the filesystem tool |
| `database.query` | Execute read-only database queries |
| `database.modify` | Execute write database operations |

Avoid overly broad scopes like `tools.all` or `admin` that grant blanket access.

## Explicit Consent

Users MUST explicitly consent to the scopes being requested. The consent flow should:

1. Clearly describe what each scope allows
2. Let users see the specific tools and actions being authorized
3. Allow users to selectively grant or deny individual scopes
4. Record consent decisions for audit purposes

## Confused Deputy Prevention

Granular scoping prevents confused deputy attacks where an MCP server is tricked into performing unauthorized actions:

- A tool with `email.read` scope cannot be manipulated to send emails
- A tool with `files.read` scope cannot be used to write or delete files
- The scope boundary acts as a hard limit regardless of what the LLM requests

## Implementation Checklist

- [ ] Define granular scopes for each tool and action (e.g., `email.send`, `files.read`)
- [ ] Publish scopes in Protected Resource Metadata (`scopes_supported`)
- [ ] Enforce scope checks on every tool invocation
- [ ] Implement user consent flow that clearly describes each scope
- [ ] Allow users to selectively grant or deny scopes
- [ ] Log consent decisions for audit
- [ ] Reject tool invocations that exceed the granted scopes
- [ ] Review and update scopes when new tools are added
