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

Secure container images and runtime configuration to reduce attack surface, prevent privilege escalation, and ensure compliance with Kubernetes security best practices.

## Base Image Selection

- Use a **Universal Base Image (UBI)** from the official [Red Hat Container Registry](https://catalog.redhat.com/software/containers/search)
- Prefer **ubi-minimal** (`ubi8/ubi-minimal` or `ubi9/ubi-minimal`) to reduce attack surface
- Use the most up-to-date image available

> **Required for:** all profiles (mandatory)

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

### Non-Root Execution

Containers must not run as root. Set `runAsNonRoot: true` and provide a numeric non-root `USER` in the Containerfile.

> **Required for:** all profiles (mandatory)

```dockerfile
USER 1000
```

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
```

Either the pod-level or container-level `securityContext` can set these fields. Do not use UID 0 (root) or UID 1337 (reserved for Istio sidecar proxies).

> **Required for:** Extended (mandatory), all others (optional) — UID 1337 restriction

### Privilege Restrictions

Set `allowPrivilegeEscalation: false` to prevent privilege escalation during container execution:

> **Required for:** all profiles (mandatory)

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

> **Required for:** all profiles (optional, recommended best practice)

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

### Service Account Token

Disable automatic mounting of the Kubernetes API service account token unless the pod needs API access:

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
spec:
  automountServiceAccountToken: false
```

Pods that require API access (e.g., operators, controllers) should use a dedicated service account with minimal RBAC permissions and explicitly set `automountServiceAccountToken: true`.

### One Process Per Container

Each container should run a single process. This simplifies monitoring, log collection, debugging, and security assessment. Use sidecar containers for auxiliary tasks (log shipping, proxy, etc.) rather than running multiple daemons in one container.

> **Required for:** all profiles (optional, recommended best practice)

### No SSH Daemons

Containers must not run SSH daemons. SSH in containers creates additional attack surfaces and violates immutable infrastructure principles. Use `kubectl exec` or `oc debug` for troubleshooting instead.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## Security Context Categories

The certsuite defines 4 approved security context categories based on required Linux capabilities. Target **Category 1** (most restrictive) unless the workload requires advanced networking or DPDK.

> **Required for:** Extended (mandatory), all others (optional)

| Category | Description | Added Capabilities |
|----------|-------------|-------------------|
| **Category 1** | Limited access (default) | None |
| **Category 1 (no UID 0)** | Basic rights with mesh networks | None (`runAsNonRoot: true`) |
| **Category 2** | Advanced networking (VLAN tag, DSCP, priority) | `NET_ADMIN`, `NET_RAW` |
| **Category 3** | SR-IOV and DPDK | `NET_ADMIN`, `NET_RAW`, `IPC_LOCK` |

All categories require:
- **Drop capabilities**: `ALL` (or at minimum `MKNOD`, `SETUID`, `SETGID`, `KILL`)
- **No host access**: `hostIPC: false`, `hostNetwork: false`, `hostPID: false`, no `hostPort`
- **No privileged containers**: `privileged: false`
- **User identity**: `runAsUser` and `fsGroup` set, SELinux context present
- **Allowed volume types only**: ConfigMap, DownwardAPI, EmptyDir, PersistentVolumeClaim, Projected, Secret

### Example: Category 1 Security Context (Preferred)

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seLinuxOptions:
      type: container_t
  containers:
    - name: app
      image: registry.example.com/app:v1.2.3
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
```

## Base Image Integrity

Container base images must not be modified after startup. All required binaries and dependencies must be built into the image at build time.

> **Required for:** all profiles (mandatory)

Protected directories that must remain unchanged at runtime:
`/bin`, `/sbin`, `/lib`, `/lib64`, `/usr/bin`, `/usr/sbin`, `/usr/lib`, `/usr/lib64`, `/var/lib/rpm`, `/var/lib/dpkg`

> **OpenShift Note:** SELinux must be in Enforcing mode on all cluster nodes (mandatory across all profiles). Base images must be Red Hat UBI (mandatory across all profiles).

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
- [ ] `runAsNonRoot: true` is set at pod or container level
- [ ] A numeric non-root `USER` is set in the Containerfile
- [ ] Container UID is not 0 or 1337
- [ ] `allowPrivilegeEscalation: false` is set
- [ ] `readOnlyRootFilesystem: true` is set
- [ ] Volumes are mounted read-only unless writes are required
- [ ] `automountServiceAccountToken: false` unless API access is required
- [ ] Each container runs a single process
- [ ] No SSH daemons are running in containers
- [ ] Security context matches an approved category (Category 1-3)
- [ ] Required capabilities are dropped (`ALL`, or at minimum `MKNOD`, `SETUID`, `SETGID`, `KILL`)
- [ ] Container base image is not modified post-startup
- [ ] SELinux is in Enforcing mode on all cluster nodes
- [ ] Hadolint runs in CI on all Containerfiles
- [ ] Container images are rebuilt regularly to pick up base image updates

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| Privilege escalation disabled | `access-control-security-context-privilege-escalation` | All profiles: mandatory |
| Run as non-root | `access-control-security-context-non-root-user-id-check` | All profiles: mandatory |
| Read-only root filesystem | `access-control-security-context-read-only-file-system` | All profiles: optional |
| Security context category | `access-control-security-context` | Extended: mandatory, all others: optional |
| UID not 1337 | `access-control-no-1337-uid` | Extended: mandatory, all others: optional |
| One process per container | `access-control-one-process-per-container` | All profiles: optional |
| Service account token | `access-control-pod-automount-service-account-token` | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No SSH daemons | `access-control-ssh-daemons` | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Base image not modified | `platform-alteration-base-image` | All profiles: mandatory |
| SELinux enforcing | `platform-alteration-is-selinux-enforcing` | All profiles: mandatory |
| Red Hat base image | `platform-alteration-isredhat-release` | All profiles: mandatory |

## References

- [Red Hat Container Registry](https://catalog.redhat.com/software/containers/search)
- [Understanding the UBI minimal images](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/building_running_and_managing_containers/index#con_understanding-the-ubi-minimal-images_assembly_types-of-container-images)
- [Hadolint](https://github.com/hadolint/hadolint)
- [Container Hardening Guide](https://docs.engineering.redhat.com/pages/viewpage.action?spaceKey=PLATSEC&title=Container+Hardening+Guide)
- [Docker Capabilities and no-new-privileges](https://raesene.github.io/blog/2019/06/01/docker-capabilities-and-no-new-privs/)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
