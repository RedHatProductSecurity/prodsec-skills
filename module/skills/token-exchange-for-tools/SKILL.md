---
name: token-exchange-for-tools
description: Implement OAuth Token Exchange in MCP servers for secure downstream API access. Use when designing or reviewing how MCP servers authenticate to third-party APIs or web tools.
category: "secure_development"
subcategory: "mcp-server"
---

# Token Exchange for MCP Server Tools

## Security Recommendation

When an MCP server needs to access third-party APIs on behalf of a user, the preferred approach is to use SPIFFE/SPIRE+mTLS. When that is not feasible, the MCP server SHOULD perform an OAuth 2.0 Token Exchange (RFC 8693) to swap the user's original token for a scoped, short-lived token.

## Why Token Exchange

Token Exchange provides:
- **User identity preserved** (`sub` claim carries the original user's identity as the subject)
- **MCP server identity included** (`act` claim identifies the MCP server as the actor)
- **Scoped access** (exchanged token is limited to the permissions needed for the specific tool)
- **Short-lived** (exchanged token has a reduced TTL)
- **No token passthrough** (original user token is never sent to downstream services)
- **Audit trail** (both user and server identity are captured in the exchanged token)

## Token Exchange Flow

```
1. User authenticates to MCP server (user gets token A)
2. MCP server needs to call third-party API
3. MCP server sends Token Exchange request to authorization server:
   - subject_token: user's token A
   - subject_token_type: urn:ietf:params:oauth:token-type:access_token
   - requested_token_type: urn:ietf:params:oauth:token-type:access_token
   - scope: only the scopes needed for the third-party API
   - actor_token: MCP server's own credential (optional)
4. Authorization server returns token B with:
   - sub: original user identity
   - act: { sub: MCP server identity }
   - scope: reduced scopes
   - exp: short TTL
5. MCP server calls third-party API with token B
```

## Resulting Token Structure

```json
{
  "sub": "user-123",
  "act": {
    "sub": "mcp-server-tools-xyz"
  },
  "scope": "read:specific-resource",
  "exp": 1700000000,
  "iss": "https://auth.example.com"
}
```

## Implementation Checklist

- [ ] Register MCP server as a Token Exchange client at the authorization server
- [ ] Implement Token Exchange request per RFC 8693
- [ ] Request only the minimum scopes needed for each downstream tool
- [ ] Set short TTL on exchanged tokens
- [ ] Never forward the original user token to any downstream service
- [ ] Log token exchange events for audit purposes
