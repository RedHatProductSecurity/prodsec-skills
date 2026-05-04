---
name: model-registry-model-security-scanning
description: Scan models for malicious code in model registries. Use when building, configuring, or reviewing model registry security, model ingestion pipelines, or model validation workflows.
category: "secure_development"
subcategory: "model-registry"
---

# Model Security Scanning in Model Registries

## Security Requirement

Models stored in registries SHOULD be scanned to identify malicious code within them. This is a gate control applied at the registry level, before models are distributed to inference engines.

## What to Scan For

| Threat | Detection Approach |
|---|---|
| **Pickle-based payloads** | Detect Python pickle serialization that can execute arbitrary code |
| **Embedded executables** | Scan for binary executables or scripts hidden in model files |
| **Unsafe serialization** | Flag models using formats known to allow code execution on deserialization |
| **Anomalous file structure** | Detect unexpected files or metadata within the model package |
| **Known malware signatures** | Match against known malicious model signatures |

## Scanning Pipeline

```
Model uploaded to registry
  → Signature verification (provenance check)
  → Security scanning (malicious content check)
    → If clean: mark as verified, make available
    → If suspicious: quarantine, alert security team
    → If malicious: reject, alert security team, log event
```

## Implementation Checklist

- [ ] Integrate model security scanning into the model ingestion pipeline
- [ ] Scan for unsafe serialization formats (pickle, legacy PyTorch)
- [ ] Scan for embedded executables and scripts
- [ ] Quarantine models that fail scanning (do not make them available)
- [ ] Alert the security team on scanning failures
- [ ] Log all scanning results for audit
- [ ] Update scanning rules as new model-based attack vectors are discovered
- [ ] Support re-scanning of existing models when new signatures are added
