---
name: runtime-restrictions
description: Enforce timeouts and rate limiting in MCP servers to prevent abuse and DoS. Use when building, configuring, or reviewing MCP server runtime controls, resource limits, or abuse prevention.
category: "secure_development"
subcategory: "mcp-server"
---

# Runtime Restrictions for MCP Servers

## Security Requirement

MCP servers MUST implement strict timeouts and rate limiting to prevent abuse and Denial of Service (DoS) attacks.

## Timeouts

| Timeout Type | Purpose |
|---|---|
| **Request timeout** | Maximum time for an entire MCP request to complete |
| **Tool execution timeout** | Maximum time for a single tool invocation to run |
| **Connection timeout** | Maximum idle time before disconnecting a client |
| **Upstream timeout** | Maximum time waiting for downstream API responses |

Tool executions without timeouts can be exploited to exhaust server resources (CPU, memory, connections).

## Rate Limiting

| Strategy | Description |
|---|---|
| **Per-user rate limit** | Limit requests per authenticated user over a time window |
| **Per-tool rate limit** | Limit invocations of specific tools (sensitive tools get tighter limits) |
| **Global rate limit** | Overall request limit to protect server capacity |
| **Concurrent execution limit** | Maximum number of simultaneous tool executions |

## Implementation Checklist

- [ ] Set request timeout for all MCP requests (reject if exceeded)
- [ ] Set per-tool execution timeouts (kill long-running tools)
- [ ] Set connection idle timeout (disconnect idle clients)
- [ ] Implement per-user rate limiting
- [ ] Implement per-tool rate limiting for sensitive tools
- [ ] Set concurrent execution limits to prevent resource exhaustion
- [ ] Return standard error responses when limits are hit (429, timeout errors)
- [ ] Log rate limit violations and timeout events for security monitoring
- [ ] Make timeout and rate limit values configurable by deployers
