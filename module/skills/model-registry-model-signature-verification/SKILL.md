---
name: model-registry-model-signature-verification
description: Verify model signatures in model registries to validate provenance. Use when building, configuring, or reviewing model registries, model upload pipelines, or model distribution workflows.
category: "secure_development"
subcategory: "model-registry"
---

# Model Signature Verification in Model Registries

## Security Requirement

Model registries SHOULD be capable of verifying the cryptographic signature of models to validate their provenance. This ensures that only models from trusted sources are stored and distributed.

## When to Verify

| Event | Action |
|---|---|
| **Model upload** | Verify signature before accepting the model into the registry |
| **Model download** | Provide signature for consumers to verify (or re-verify on their behalf) |
| **Periodic audit** | Re-verify signatures of stored models to detect storage-level tampering |

## Verification Requirements

- Accept models signed with trusted keys only
- Reject or flag models with invalid, expired, or missing signatures
- Log all verification results as security events
- Alert security teams on verification failures
- Support standard signing mechanisms (Sigstore/cosign, GPG, or equivalent)

## Implementation Checklist

- [ ] Implement signature verification on model upload/ingestion
- [ ] Maintain and manage a list of trusted signing keys or certificates
- [ ] Reject models with invalid or missing signatures (or quarantine for review)
- [ ] Store and expose signatures for downstream consumers to verify
- [ ] Log signature verification results (success and failure)
- [ ] Alert on signature verification failures
- [ ] Support periodic re-verification of stored models
