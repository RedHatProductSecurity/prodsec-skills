---
name: model-registry-logging
description: Enforce centralized security logging for model registries. Use when building, configuring, or reviewing logging and audit capabilities of model registries.
category: "secure_development"
subcategory: "model-registry"
---

# Centralized Logging for Model Registries

## Security Requirement

Model registry accesses, model uploads and downloads, and any security events MUST be sent to a centralized logging facility using standard protocols.

## Events to Log

| Event Category | Specific Events |
|---|---|
| **Access events** | User logins, API access, storage access |
| **Model lifecycle** | Model uploads, downloads, deletions, version changes |
| **Security events** | Signature verification failures, scanning results, access denials |
| **Administrative events** | Configuration changes, permission changes, user management |
| **Anomalies** | Unusual download patterns, access from unexpected sources |

## Logging Requirements

| Requirement | Details |
|---|---|
| **Centralized destination** | All logs sent to a central logging facility (SIEM, ELK, Splunk) |
| **Standard protocols** | Use standard log shipping protocols (syslog, OTLP, Fluentd) |
| **Structured format** | Logs in structured format (JSON) with consistent field names |
| **Identity included** | Every log entry includes the authenticated principal's identity |
| **Tamper protection** | Logs should not be modifiable by the application or its operators |
| **Retention** | Log retention per organizational and regulatory requirements |

## Example Log Entry

```json
{
  "timestamp": "2026-03-03T10:30:00Z",
  "event_type": "model.signature_verification_failed",
  "severity": "high",
  "principal": "pipeline:ci-model-upload",
  "model_id": "llama-3-fine-tuned-v2",
  "details": "Signature verification failed: unknown signing key",
  "source_ip": "10.0.1.50",
  "registry": "prod-model-registry"
}
```

## Implementation Checklist

- [ ] Configure centralized log destination (SIEM or logging platform)
- [ ] Use standard log shipping protocol (syslog, OTLP, or equivalent)
- [ ] Log all access events with authenticated principal identity
- [ ] Log all model lifecycle events (upload, download, delete)
- [ ] Log all security events (verification failures, scan results, access denials)
- [ ] Use structured JSON format with consistent field names
- [ ] Ensure log integrity (forward to tamper-protected storage)
- [ ] Set log retention per organizational policy
- [ ] Create alerts for high-severity security events
