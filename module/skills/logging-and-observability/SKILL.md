---
name: logging-and-observability
description: Enforce centralized structured logging and audit trails in MCP servers. Use when building, configuring, or reviewing MCP server logging, observability, or audit capabilities.
category: "secure_development"
subcategory: "mcp-server"
---

# Logging and Observability for MCP Servers

## Security Requirement

MCP servers MUST implement comprehensive, centralized, structured logging. This is vital for auditing, troubleshooting, and detecting security incidents.

## Centralized and Structured Logging

| Requirement | Details |
|---|---|
| **Format** | JSON or other structured format (not unstructured text) |
| **Destination** | MCP servers must be capable of sending logs to a central system (e.g., OpenShift logging stack, ELK, Splunk) |
| **Protocol** | Standard log shipping (syslog, OTLP, Fluentd, or equivalent) |
| **Configurable** | Deployers must be able to configure the log destination |

## Audit Trail Requirements

Logs MUST capture enough detail to reconstruct a security incident:

| Field | Purpose |
|---|---|
| **User identity** | Who performed the action (from token `sub` claim) |
| **Tool name** | Which tool was invoked |
| **Parameters** | What parameters were passed (with sensitive data scrubbed) |
| **Timestamp** | When the action occurred (ISO 8601, UTC) |
| **Result** | Success or failure, including error details |
| **Source** | Client IP, request ID, session ID |

## Sensitive Data Scrubbing

Logs MUST scrub sensitive data before recording:

- Redact tokens and credentials (log metadata like `jti` and `sub` instead)
- Mask PII in parameters (email addresses, names, etc.)
- Truncate or hash large prompt content
- Never log passwords, API keys, or secret values

## Example Audit Log Entry

```json
{
  "timestamp": "2026-03-03T14:30:00Z",
  "event": "tool.invocation",
  "user": "user-123",
  "tool": "email.send",
  "parameters": {
    "to": "j***@example.com",
    "subject": "Meeting update"
  },
  "result": "success",
  "request_id": "req-abc-123",
  "source_ip": "10.0.1.42"
}
```

## Implementation Checklist

- [ ] Use structured logging format (JSON) for all log entries
- [ ] Configure centralized log destination (OpenShift logging, ELK, Splunk)
- [ ] Log every tool invocation with user, tool, parameters, and result
- [ ] Scrub sensitive data (tokens, PII, secrets) from all log entries
- [ ] Include enough detail to reconstruct security incidents
- [ ] Include request ID for correlating related log entries
- [ ] Make log destination configurable by deployers
- [ ] Log authentication and authorization events (successes and failures)
- [ ] Set log retention per organizational and regulatory requirements
