---
name: sampling-controls
description: Control and restrict MCP server use of sampling. Use when building or reviewing MCP servers that might use sampling to request LLM completions from clients.
category: "secure_development"
subcategory: "mcp-server"
---

# Sampling Controls for MCP Servers

## Security Requirements

### Avoid Sampling

MCP servers SHOULD avoid using sampling. Sampling is the mechanism where the server asks the client's LLM to perform a task. This creates a bidirectional trust relationship that introduces security risks.

### If Sampling Is Used

If the MCP server must use sampling (asking the client's LLM to perform a task), apply these constraints:

| Constraint | Details |
|---|---|
| **Use sparingly** | Only use sampling when absolutely necessary; prefer direct computation |
| **Be predictable** | Sampling requests should be deterministic and expected by the user |
| **Expect rejection** | Be prepared for the user to reject the sampling request; handle gracefully |
| **Limit scope** | Keep sampling requests narrow and specific |
| **No sensitive data** | Never include sensitive data in sampling requests sent to the client's LLM |

## Risks of Sampling

| Risk | Description |
|---|---|
| **Prompt injection amplification** | Sampling can be exploited to inject prompts into the client's LLM |
| **Data leakage** | Sampling requests may inadvertently expose server-side data to the client's LLM |
| **Trust boundary violation** | The server is effectively executing code (LLM reasoning) on the client side |
| **Unpredictable behavior** | LLM responses to sampling requests are non-deterministic |
| **User confusion** | Users may not understand why the server is making LLM requests |

## Implementation Checklist

- [ ] Avoid using sampling unless absolutely necessary
- [ ] Document why sampling is needed for each use case
- [ ] Handle user rejection of sampling requests gracefully
- [ ] Keep sampling requests narrow, specific, and predictable
- [ ] Never include sensitive server-side data in sampling requests
- [ ] Log all sampling requests and responses for audit
- [ ] Provide users with visibility into when and why sampling occurs
