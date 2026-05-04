---
name: agent-identity
description: Enforce that AI agents have their own identity separate from human users. Use when designing, building, or reviewing agent identity management, agent authentication, or agent permission models.
category: "secure_development"
subcategory: "agent"
---

# Agent Own Identity

## Security Recommendation

Agents SHOULD have their own identity and SHOULD NOT use the identity of a human user. Each agent must be a distinct, identifiable entity in the system.

## Rationale

Giving agents their own identity enables:

- **Specific permissions**: Assign permissions tailored to the agent's purpose, following least privilege
- **Audit trail**: Distinguish agent actions from human actions in logs and audit records
- **Runtime identification**: Identify which agent performed which action at runtime
- **Accountability**: Trace decisions and actions back to the specific agent
- **Blast radius control**: Limit the impact of a compromised agent to its own permissions

## Using Human Identity (Anti-Pattern)

When an agent acts under a human user's identity:
- All agent actions appear as user actions in audit logs
- The agent inherits all of the user's permissions (likely more than needed)
- It becomes impossible to distinguish human from agent activity
- Revoking agent access requires revoking the user's credentials

## Implementation Guidance

- Register each agent as a distinct service account or workload in the identity provider
- Use SPIFFE IDs or service account identifiers for agent identity
- Assign agent-specific scopes and permissions (not inherited from users)
- Include agent identity in all log entries and audit records
- When an agent acts on behalf of a user, use delegation mechanisms (e.g., Token Exchange with `act` claim) that preserve both identities

## Example: Agent vs. User in Audit Log

```json
{
  "action": "tool:execute",
  "tool": "database-query",
  "actor": {
    "type": "agent",
    "id": "agent:data-analyst-v2",
    "delegated_by": "user:jane.doe"
  },
  "timestamp": "2026-03-03T10:15:00Z"
}
```
