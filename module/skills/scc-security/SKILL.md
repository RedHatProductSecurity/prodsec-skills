---
name: scc-security
description: >
  Review OpenShift Security Context Constraints for correct privilege levels.
  Use when auditing pod security, reviewing SCC assignments, or configuring
  container runtime permissions on OpenShift clusters.
category: "secure_development"
subcategory: "kubernetes"
---

# OpenShift Security Context Constraints (SCC)

SCCs control what actions pods can perform and what host resources they can access. If no security context is specified, OpenShift applies the **restricted** SCC by default.

## What SCCs Control

- Privileged container execution
- Linux capabilities requested by containers
- Host directory volume mounts
- SELinux context
- Container user and group IDs
- Host namespace and networking access
- FSGroup ownership of volumes
- Supplemental groups
- Read-only root filesystem requirement
- Volume types
- Seccomp profiles

## SCC Reference

| SCC | Description | When to Use |
|---|---|---|
| **restricted** | Denies all host features; requires namespace-allocated UID and SELinux label. Most restrictive. | Default for all workloads; prefer this unless a specific relaxation is justified |
| **nonroot** | Like restricted, but allows any non-root UID | When the container must run as a specific non-root UID |
| **anyuid** | Like restricted, but allows any UID/GID | When the container requires a specific UID (including root UID without root privileges) |
| **hostnetwork** | Allows host networking and ports; requires namespace UID/SELinux | Only for pods that must bind to host network interfaces |
| **hostaccess** | Allows all host namespaces; requires namespace UID/SELinux | Only for trusted pods requiring host namespace access |
| **hostmount-anyuid** | Like restricted, but allows host mounts and any UID | Only for pods requiring host filesystem access (e.g., persistent volume recycler) |
| **privileged** | Full access to all host features; any user, group, SELinux context | Only for cluster administration requiring maximum access |
| **node-exporter** | Purpose-built for the Prometheus node exporter | Only for the node exporter DaemonSet |
| **custom** | Administrator-defined constraints | Requires careful security review; document every relaxation |

## Security Review Guidelines

- Start from **restricted** and relax only when a specific capability is justified
- Document why a workload cannot run under restricted
- Custom SCCs require particular scrutiny: every relaxation from restricted must have a documented rationale
- Review that SCCs are bound to the correct ServiceAccounts, not overly broad groups
- Verify that no workload uses **privileged** SCC unless it is a cluster administration component
- Check that `runAsNonRoot: true` is set where possible
- Check that `readOnlyRootFilesystem: true` is set where possible

## Implementation Checklist

- [ ] All workloads use **restricted** SCC unless a specific exception is documented
- [ ] No workload uses **privileged** SCC without cluster-admin justification
- [ ] Custom SCCs document every relaxation from restricted
- [ ] SCC bindings target specific ServiceAccounts, not broad groups
- [ ] `runAsNonRoot: true` is set in the pod security context
- [ ] `readOnlyRootFilesystem: true` is set in container security contexts
- [ ] Host path mounts are justified and documented
- [ ] Host networking is only enabled for pods that require it

## References

- [Managing Security Context Constraints](https://docs.openshift.com/container-platform/4.17/authentication/managing-security-context-constraints.html)
- [Runtime Privilege and Linux Capabilities](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)
