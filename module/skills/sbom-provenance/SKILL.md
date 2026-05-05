---
name: sbom-provenance
description: Generate Software Bill of Materials (SBOM) for AI software releases. Use when building release pipelines, reviewing supply chain security, or preparing compliance documentation for AI systems.
category: "secure_development"
subcategory: "supply-chain"
---

# SBOM and Provenance

## Security Requirement

All releases of AI software MUST include a Software Bill of Materials (SBOM) to provide transparency about the components and dependencies included in the software.

## What an SBOM Contains

| Component | Details |
|---|---|
| **Direct dependencies** | All libraries and packages directly used |
| **Transitive dependencies** | Dependencies of dependencies |
| **Versions** | Exact versions of all components |
| **Licenses** | License information for each component |
| **Hashes** | Cryptographic hashes for integrity verification |
| **Supplier information** | Who provides each component |

## Standard Formats

| Format | Description |
|---|---|
| **SPDX** | ISO standard (ISO/IEC 5962:2021); widely supported |
| **CycloneDX** | OWASP standard; strong security focus |

## Generation Tools

```bash
# Generate SBOM for a container image (CycloneDX)
syft registry.example.com/mcp-server:v1.0.0 -o cyclonedx-json > sbom.json

# Generate SBOM for a Python project (SPDX)
syft dir:. -o spdx-json > sbom.spdx.json
```

## Provenance

Beyond the SBOM, generate build provenance that attests:
- What source code was built
- What build system was used
- What build parameters were applied
- When the build occurred

SLSA (Supply Chain Levels for Software Artifacts) framework provides a maturity model for provenance.

## Package Manager Security

When consuming or publishing packages through package managers (NPM, NuGet, Maven, pip, etc.):

### Publishing

- Use **scoped API keys** to limit permissions per key to specific packages and actions
- Use **registry signing** to protect against unauthorized package modifications
- **Sign packages** with your own certificates to provide authenticity and integrity verification

### Consuming

- Verify package updates regularly to reduce attack surface
- Use one package manager per project; avoid vendoring standalone libraries outside the package manager
- Use built-in vulnerability checking features where available (e.g., `dotnet list package --vulnerable`)

## Implementation Checklist

- [ ] Generate an SBOM for every release (SPDX or CycloneDX format)
- [ ] Include SBOM alongside release artifacts
- [ ] Automate SBOM generation in the CI/CD pipeline
- [ ] Generate build provenance attestations
- [ ] Sign SBOMs and provenance documents
- [ ] Scan SBOMs for known vulnerabilities
- [ ] Update SBOMs when dependencies change
- [ ] Published packages use scoped API keys with minimum permissions
- [ ] Published packages are signed; registry signing is enabled
- [ ] Dependencies are regularly checked for updates and vulnerabilities
- [ ] One package manager is used per project (no standalone vendored libs)
