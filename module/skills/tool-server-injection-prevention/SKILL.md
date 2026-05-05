---
name: tool-server-injection-prevention
description: Prevent tool and server injection attacks (rug-pulls) in MCP servers. Use when building, distributing, or reviewing MCP server update mechanisms, versioning, or integrity verification.
category: "secure_development"
subcategory: "mcp-server"
---

# Tool/Server Injection Prevention for MCP Servers

## Security Requirement

MCP servers MUST protect against tool/server injection attacks, also known as "rug-pulls," where a malicious update replaces a trusted server or tool with a compromised version.

## Attack Scenario

1. User installs a trusted MCP server (version 1.0)
2. Attacker pushes a malicious update (version 1.1) to the distribution channel
3. User's MCP client auto-updates to version 1.1
4. Malicious server now has access to user's tools and data

## Required Mitigations

### Sign Updates

Digitally sign all server binaries, container images, and updates so clients and users can verify their integrity:

- Sign with Sigstore Cosign or equivalent
- Publish signatures alongside releases
- Include the signing key/certificate in the project documentation

### Support Version Pinning

Advise clients and users to pin to specific, trusted versions or checksums:

```yaml
# Pin to specific version
mcp_server:
  image: registry.example.com/mcp-server:v1.2.3@sha256:abc123...
  # Or pin to checksum
  checksum: "sha256:abc123def456..."
```

### Prevent Unauthorized Updates

| Control | Details |
|---|---|
| **Signed updates** | All updates must be signed; reject unsigned updates |
| **Version pinning** | Support and document version pinning for clients |
| **Changelog** | Publish detailed changelogs for every release |
| **Staged rollouts** | Roll out updates gradually to detect compromised releases early |
| **Rollback** | Support rollback to previous versions if a compromise is detected |

## Implementation Checklist

- [ ] Digitally sign all binaries and container images (e.g., Sigstore Cosign)
- [ ] Publish signatures alongside every release
- [ ] Document the signing key/certificate for users to verify
- [ ] Support and document version pinning (by tag + digest)
- [ ] Publish detailed changelogs for every release
- [ ] Do not auto-update without user consent or verification
- [ ] Support rollback to previous trusted versions
- [ ] Advise users to verify signatures before updating
