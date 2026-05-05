---
name: logging
description: Enforce logging of access to sensitive external data sources in AI systems. Use when designing, building, or reviewing audit and logging capabilities for AI systems accessing external databases or data services.
category: "secure_development"
subcategory: "external-data-source"
---

# Logging for External Data Source Access

## Security Requirement

If the data contained and served by external data sources is sensitive, accesses to them MUST be logged. The product SHOULD have the functionality to send these events to an external logging facility using industry standards.

## What to Log

| Event | Details to Capture |
|---|---|
| **Data access** | Who accessed what data, when, from where |
| **Data modification** | Who modified what data, what changed |
| **Access denial** | Failed access attempts (authentication or authorization failures) |
| **Bulk operations** | Large data exports or queries |
| **Connection events** | Connection establishment and teardown |
| **Schema changes** | Structural changes to data sources |

## Logging Requirements

| Requirement | Details |
|---|---|
| **External logging facility** | Logs must be sendable to an external SIEM or logging platform |
| **Industry standard protocols** | Use syslog, OTLP, Fluentd, or equivalent |
| **Structured format** | JSON with consistent field names |
| **Principal identity** | Every log entry includes the authenticated principal |
| **Configurable** | Customers must be able to configure the external log destination |
| **Non-repudiation** | Logs should not be modifiable by the application |

## Log Safety

| Rule | Rationale |
|---|---|
| **No secrets in logs** | Credentials, API keys, and session tokens must never appear in log output |
| **No PII in logs** | Personally identifiable information creates compliance and privacy risks |
| **No session identifiers** | Session IDs in logs can enable session hijacking |
| **Log injection prevention** | Untrusted input in logs can exploit log viewers (XSS, RCE in parsers); sanitize all values before logging |
| **Trusted system logging** | Logging controls must run on a trusted system (server-side), not client-side |

## What to Log

Log both success and failure of security events:

- Authentication attempts, especially failures
- Access control failures
- Tampering events (unexpected state changes)
- Invalid or expired session token usage
- System exceptions
- Administrative functions and security configuration changes
- Bulk data operations and large exports

## Log Transport

- Use standard protocols such as **Syslog** (rsyslog with TLS) or OTLP
- Encrypt log transport when possible
- For cloud services, forward to the corporate SIEM (e.g., Splunk)
- Restrict log access to authorized individuals only

## Implementation Checklist

- [ ] Implement access logging for all connections to sensitive external data sources
- [ ] Include principal identity, operation, timestamp, and data accessed in log entries
- [ ] Provide functionality to forward logs to an external logging facility
- [ ] Support industry standard log protocols (syslog, OTLP, Fluentd)
- [ ] Use structured JSON format for log entries
- [ ] Make the external log destination configurable by the deploying organization
- [ ] Log access denials and authentication failures
- [ ] Log authentication successes, admin actions, and security config changes
- [ ] Ensure logs are tamper-protected (forward to immutable storage)
- [ ] No secrets, PII, or session identifiers appear in log output
- [ ] Log entries with untrusted data are sanitized to prevent injection
- [ ] Log transport is encrypted (rsyslog with TLS, OTLP over TLS)
- [ ] Log access is restricted to authorized individuals
