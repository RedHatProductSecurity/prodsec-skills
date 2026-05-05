---
name: containerization
description: Enforce container security best practices for MCP servers, including OpenShift integration. Use when containerizing MCP servers or reviewing container security configurations for MCP deployments.
category: "secure_development"
subcategory: "mcp-server"
---

# Containerization and OpenShift Integration for MCP Servers

## Security Recommendation

MCP servers SHOULD run in containers, leveraging container orchestration platform security features (e.g., OpenShift SCCs) for a hardened-by-default posture.

## Container Security Requirements

### Run as Non-Root

The container MUST run as a non-root user. OpenShift's default Security Context Constraints (SCCs) enforce this automatically.

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
```

### Drop All Capabilities

Remove all Linux capabilities and add back only what is strictly needed:

```yaml
securityContext:
  capabilities:
    drop: ["ALL"]
```

### Read-Only Root Filesystem

Use a read-only root filesystem. Mount a `tmpfs` only for directories that require temporary writes:

```yaml
securityContext:
  readOnlyRootFilesystem: true
volumeMounts:
  - name: tmp
    mountPath: /tmp
volumes:
  - name: tmp
    emptyDir:
      medium: Memory
```

### Kernel Hardening

| Mechanism | Details |
|---|---|
| **SELinux** | Enabled by default in OpenShift; confines container processes |
| **seccomp** | Apply seccomp profiles to restrict available system calls |

```yaml
securityContext:
  seccompProfile:
    type: RuntimeDefault
  seLinuxOptions:
    type: container_t
```

### Network Policies

Use Kubernetes NetworkPolicies as a pod-level firewall to control all ingress and egress traffic:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mcp-server-policy
spec:
  podSelector:
    matchLabels:
      app: mcp-server
  policyTypes: ["Ingress", "Egress"]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: mcp-client
      ports:
        - port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: auth-server
      ports:
        - port: 443
```

## Base Image Selection

- Use a **Universal Base Image (UBI)** from the official [Red Hat Container Registry](https://catalog.redhat.com/software/containers/search) as the foundation for MCP server containers
- Prefer **ubi-minimal** to reduce attack surface and installed package count
- Use the most up-to-date image available
- For Red Hat Catalog images, omit floating tags to ensure the latest image is pulled (exception: Konflux uses digest-based pinning with automated updates)
- For non-Red Hat images, **pin the version or digest** to prevent pulling a tampered image
- Remove non-essential packages and clean caches:

```dockerfile
RUN microdnf upgrade -y && microdnf install -y <required> && microdnf remove -y <unnecessary> && microdnf clean all
```

## Containerfile Linting

Use [Hadolint](https://github.com/hadolint/hadolint) to lint Containerfiles for best-practice violations. Run it in CI but verify findings manually -- do not trust it blindly.

## Implementation Checklist

- [ ] Base image is a Red Hat UBI (preferably ubi-minimal)
- [ ] Non-Red Hat base images are pinned by version or digest
- [ ] Non-essential packages are removed and caches cleaned
- [ ] Run container as non-root user (`runAsNonRoot: true`)
- [ ] Drop all Linux capabilities (`drop: ["ALL"]`)
- [ ] Use read-only root filesystem (`readOnlyRootFilesystem: true`)
- [ ] `allowPrivilegeEscalation: false` is set (no-new-privileges)
- [ ] Mount `tmpfs` only for directories needing temporary writes
- [ ] Apply seccomp profile (`RuntimeDefault` or custom)
- [ ] Ensure SELinux is enabled and container type is appropriate
- [ ] Deploy Kubernetes NetworkPolicies controlling ingress and egress
- [ ] Use OpenShift SCCs or equivalent to enforce security context defaults
- [ ] Hadolint runs in CI on all Containerfiles
- [ ] Scan container images for vulnerabilities before deployment
