---
name: software-signing
description: Enforce digital signing of software binaries and container images. Use when building, releasing, or reviewing CI/CD pipelines for AI software, MCP servers, or any distributed components.
category: "secure_development"
subcategory: "supply-chain"
---

# Software Signing

## Security Requirement

All binaries and container images MUST be digitally signed so that users and automated systems can verify their integrity and provenance.

## What to Sign

| Artifact | Signing Method |
|---|---|
| **Container images** | Sigstore Cosign, Docker Content Trust |
| **Binaries** | GPG signatures, Sigstore |
| **Helm charts** | Helm provenance files (GPG signed) |
| **Python packages** | GPG or Sigstore signatures |
| **npm packages** | npm provenance (Sigstore-based) |

## Sigstore Cosign Example

```bash
# Sign a container image
cosign sign --key cosign.key registry.example.com/mcp-server:v1.0.0

# Verify a container image
cosign verify --key cosign.pub registry.example.com/mcp-server:v1.0.0
```

## Keyless Signing (Sigstore Fulcio)

For open source projects, use keyless signing with Sigstore Fulcio to avoid key management:

```bash
# Keyless sign (uses OIDC identity)
cosign sign registry.example.com/mcp-server:v1.0.0

# Verify with identity
cosign verify \
  --certificate-identity=ci@example.com \
  --certificate-oidc-issuer=https://accounts.google.com \
  registry.example.com/mcp-server:v1.0.0
```

## Implementation Checklist

- [ ] Sign all container images in the CI/CD pipeline
- [ ] Sign all release binaries
- [ ] Publish signatures alongside release artifacts
- [ ] Document verification instructions for users
- [ ] Store signing keys securely (HSM, KMS, or Sigstore keyless)
- [ ] Rotate signing keys on a regular schedule (if not using keyless)
- [ ] Verify signatures in deployment pipelines before running artifacts
