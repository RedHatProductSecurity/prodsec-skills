---
name: container-hardening
description: >
  Harden container images and runtime configuration. Use when building,
  reviewing, or auditing Containerfiles, Dockerfiles, container compose
  files, or Kubernetes pod security settings.
category: "secure_development"
subcategory: "kubernetes"
---

# Container Hardening

## Base Image Selection

- Use a **Universal Base Image (UBI)** from the official [Red Hat Container Registry](https://catalog.redhat.com/software/containers/search)
- Prefer **ubi-minimal** (`ubi8/ubi-minimal` or `ubi9/ubi-minimal`) to reduce attack surface
- Use the most up-to-date image available

### Image Tagging Strategy

| Source | Strategy |
|---|---|
| **Red Hat Catalog** | Omit floating tags to get the latest image; exception: Konflux project uses digest-based pinning with automated updates |
| **Non-Red Hat registries** | Pin the version or digest to ensure you use the intended image and not a tampered one |

## Minimize Installed Software

Remove non-essential packages and clean up package manager caches:

```dockerfile
RUN microdnf upgrade -y && \
    microdnf install -y <required-packages> && \
    microdnf remove -y <unnecessary-packages> && \
    microdnf clean all
```

Use `microdnf` on ubi-minimal images; `dnf` on full UBI images.

## Runtime Security

### Privilege Restrictions

Set `no-new-privileges` to prevent privilege escalation during container execution:

```yaml
securityContext:
  allowPrivilegeEscalation: false
```

Or in a compose file:

```yaml
security_opt:
  - no-new-privileges: true
```

### Read-Only Filesystem

Use read-only root filesystems wherever possible:

```yaml
securityContext:
  readOnlyRootFilesystem: true
```

Mount writable `tmpfs` volumes only where the application requires write access (e.g., `/tmp`, `/var/run`).

### Read-Only Volumes

Mount volumes as read-only unless the container must write to them:

```yaml
volumeMounts:
  - name: config
    mountPath: /etc/app
    readOnly: true
```

## Containerfile Linting

Use [Hadolint](https://github.com/hadolint/hadolint) to lint Containerfiles for best-practice violations and inline bash issues:

```bash
hadolint Containerfile
```

Hadolint catches common issues (running as root, missing version pins, unnecessary `sudo`) but should not be trusted without additional verification.

## Implementation Checklist

- [ ] Base image is a Red Hat UBI from the official catalog
- [ ] ubi-minimal is used unless a full UBI is justified
- [ ] Non-Red Hat base images are pinned by version or digest
- [ ] Non-essential packages are removed and caches cleaned
- [ ] `allowPrivilegeEscalation: false` (no-new-privileges) is set
- [ ] `readOnlyRootFilesystem: true` is set
- [ ] Volumes are mounted read-only unless writes are required
- [ ] A numeric non-root `USER` is set in the Containerfile
- [ ] Hadolint runs in CI on all Containerfiles
- [ ] Container images are rebuilt regularly to pick up base image updates

## References

- [Red Hat Container Registry](https://catalog.redhat.com/software/containers/search)
- [Understanding the UBI minimal images](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/building_running_and_managing_containers/index#con_understanding-the-ubi-minimal-images_assembly_types-of-container-images)
- [Hadolint](https://github.com/hadolint/hadolint)
- [Container Hardening Guide](https://docs.engineering.redhat.com/pages/viewpage.action?spaceKey=PLATSEC&title=Container+Hardening+Guide)
- [Docker Capabilities and no-new-privileges](https://raesene.github.io/blog/2019/06/01/docker-capabilities-and-no-new-privs/)
