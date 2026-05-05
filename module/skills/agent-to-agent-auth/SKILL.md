---
name: agent-to-agent-auth
description: Enforce SPIFFE/SPIRE plus mTLS for agent-to-agent communication. Use when designing, building, or reviewing authentication between AI agents or multi-agent systems.
category: "secure_development"
subcategory: "agent"
---

# Agent-to-Agent Authentication

## Security Requirement

Agent-to-agent communication MUST follow the service-to-service recommendation and implement SPIFFE/SPIRE+mTLS.

## Why SPIFFE/SPIRE for Agent-to-Agent

- Agents are software workloads, making SPIFFE the natural identity framework
- No credentials exchanged over the network (SPIRE handles attestation and certificate issuance)
- Mutual authentication ensures both agents verify each other's identity
- Short-lived X.509 certificates (SVIDs) are automatically rotated
- Each agent gets a unique SPIFFE ID that can be used for authorization decisions

## Architecture

```
Agent A                          Agent B
  │                                │
  ├── SPIFFE ID:                   ├── SPIFFE ID:
  │   spiffe://domain/agent/a      │   spiffe://domain/agent/b
  │                                │
  ├── Gets SVID from SPIRE Agent   ├── Gets SVID from SPIRE Agent
  │                                │
  └── mTLS connection ────────────→└── Validates Agent A's SVID
      (presents SVID)                  (presents own SVID)
```

## SPIFFE ID Convention for Agents

Use a consistent SPIFFE ID naming convention:

```
spiffe://<trust-domain>/agent/<agent-type>/<instance-id>
```

Examples:
- `spiffe://example.com/agent/data-analyst/prod-01`
- `spiffe://example.com/agent/code-reviewer/staging-02`

## Implementation Checklist

- [ ] Deploy SPIRE server and agents for the agent infrastructure
- [ ] Register each agent type as a SPIRE workload entry
- [ ] Configure agents to obtain SVIDs from the SPIRE agent
- [ ] Implement mTLS for all agent-to-agent communication
- [ ] Extract peer agent's SPIFFE ID from the TLS certificate for authorization
- [ ] Define authorization policies based on SPIFFE IDs (which agents can communicate)
- [ ] Monitor SVID rotation and certificate expiration
