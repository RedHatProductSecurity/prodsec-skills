---
name: agent-to-mcp-server-auth
description: Enforce authentication for agents connecting to MCP servers via MCP clients. Use when designing or reviewing how AI agents authenticate to MCP servers.
category: "secure_development"
subcategory: "agent"
---

# Agent-to-MCP-Server Authentication

## Security Requirement

When an agent connects through an MCP client to an MCP server, authentication SHOULD use SPIFFE/SPIRE+mTLS (the service-to-service recommendation).

## Preferred Approach: SPIFFE/SPIRE+mTLS

The agent (running as a workload) obtains a SVID from SPIRE and establishes an mTLS connection to the MCP server. Both parties authenticate each other via their SPIFFE IDs.

```
Agent (workload)
  → Obtains SVID from SPIRE Agent
  → MCP Client establishes mTLS to MCP Server
  → MCP Server validates agent's SPIFFE ID
  → MCP Server authorizes based on SPIFFE ID
```

## Fallback Approach: OAuth with User Delegation

If SPIFFE/SPIRE is not feasible, the agent and MCP client MAY act as an OAuth client and obtain permission from the user to access the MCP server (the resource server).

### Trade-offs of OAuth Fallback

| Aspect | Impact |
|---|---|
| **Audit trail** | Actions are logged as performed by the user, not the agent |
| **Permissions** | Agent operates with the user's permission scope |
| **Acceptability** | Similar to regular applications running with user permissions |
| **Recommendation** | Acceptable but not ideal; prefer SPIFFE/SPIRE when possible |

### OAuth Fallback Flow

```
1. Agent needs to access MCP server resource
2. MCP client initiates OAuth flow on behalf of the user
3. User grants permission (consent) for the agent to access the MCP server
4. MCP client obtains access token scoped to the MCP server
5. Agent uses the token through MCP client to access MCP server
6. All actions are logged under the user's identity
```

## Implementation Checklist

- [ ] Evaluate SPIFFE/SPIRE feasibility for the deployment environment
- [ ] If feasible: deploy SPIRE and register agent workloads, use mTLS
- [ ] If not feasible: implement OAuth client flow in the MCP client
- [ ] For OAuth fallback: implement user consent flow
- [ ] For OAuth fallback: request minimum scopes needed for agent operations
- [ ] Document which authentication method is in use and plan migration to SPIFFE/SPIRE
