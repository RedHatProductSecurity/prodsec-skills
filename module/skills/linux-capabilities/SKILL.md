---
name: linux-capabilities
description: >
  Review and restrict Linux capabilities in Kubernetes containers. Use when
  writing, reviewing, or auditing pod security contexts that add or drop
  Linux capabilities such as BPF, NET_ADMIN, NET_RAW, SYS_ADMIN, IPC_LOCK,
  SYS_NICE, or SYS_PTRACE.
category: "secure_development"
subcategory: "kubernetes"
---

# Linux Capabilities

Restrict Linux capabilities to the minimum set required by each container. The default approach is to drop all capabilities and selectively add only those the workload needs.

## Default: Drop All Capabilities

Every container should drop all Linux capabilities unless specific ones are required:

```yaml
securityContext:
  capabilities:
    drop: ["ALL"]
```

At minimum, containers must drop `MKNOD`, `SETUID`, `SETGID`, and `KILL`. Dropping `ALL` is preferred as it is simpler and more restrictive.

## Dangerous Capabilities

The following capabilities are restricted by the certsuite and should not be added unless the workload has a documented exception.

### SYS_ADMIN

Provides extensive privileges including mounting filesystems, configuring namespaces, and performing many administrative operations. This is the most dangerous capability — effectively equivalent to running as root.

> **Required for:** all profiles (mandatory) — containers must not use SYS_ADMIN

### NET_ADMIN

Allows network configuration changes including interface configuration, firewall rules (iptables/nftables), and routing tables. Workload pods must not configure nftables or iptables — these should be managed by platform operators (e.g., Performance Addon Operator, Istio).

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

**Exception:** User plane or networking functions (e.g., SR-IOV, Multicast) may request an exception with documentation of which container needs the capability and why.

### NET_RAW

Enables raw socket creation and packet manipulation. Required together with NET_ADMIN for nftables modification, which workload pods should not do.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

**Exception:** User plane or networking functions may request an exception.

### BPF

Allows loading eBPF programs into the kernel. eBPF can bypass security controls, monitor other processes, and potentially compromise the host.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### IPC_LOCK

Allows locking memory pages with `mlock()`, `mlockall()`, `shmctl()`, and `mmap()`. Locked memory cannot be swapped, potentially causing denial of service.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

**Exception:** DPDK applications that require locked memory for packet buffers may request an exception.

## Required Capabilities

Some workloads must add specific capabilities to function correctly.

### SYS_NICE (Real-Time Kernel Nodes)

Pods scheduled to nodes with a real-time kernel must add `SYS_NICE` to allow DPDK applications to switch to `SCHED_FIFO` scheduling.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
securityContext:
  capabilities:
    drop: ["ALL"]
    add: ["SYS_NICE"]
```

### SYS_PTRACE (Process Namespace Sharing)

When `shareProcessNamespace: true` is set on a pod, containers that need to send signals to processes in other containers (e.g., `SIGHUP`) must have `SYS_PTRACE`.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
spec:
  shareProcessNamespace: true
  containers:
    - name: app
      securityContext:
        capabilities:
          drop: ["ALL"]
          add: ["SYS_PTRACE"]
```

## Implementation Checklist

- [ ] All containers drop all capabilities (`drop: ["ALL"]`) or at minimum `MKNOD`, `SETUID`, `SETGID`, `KILL`
- [ ] No containers use `SYS_ADMIN`
- [ ] No containers use `NET_ADMIN` unless documented exception for user plane functions
- [ ] No containers use `NET_RAW` unless documented exception for user plane functions
- [ ] No containers use `BPF`
- [ ] No containers use `IPC_LOCK` unless documented exception for DPDK
- [ ] Pods on real-time kernel nodes add `SYS_NICE`
- [ ] Pods with `shareProcessNamespace: true` add `SYS_PTRACE` where needed

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| No SYS_ADMIN | [`access-control-sys-admin-capability-check`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-sys-admin-capability-check) | All profiles: mandatory |
| No NET_ADMIN | [`access-control-net-admin-capability-check`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-net-admin-capability-check) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No NET_RAW | [`access-control-net-raw-capability-check`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-net-raw-capability-check) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No BPF | [`access-control-bpf-capability-check`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-bpf-capability-check) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No IPC_LOCK | [`access-control-ipc-lock-capability-check`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-ipc-lock-capability-check) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| SYS_NICE on RT nodes | [`access-control-sys-nice-realtime-capability`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-sys-nice-realtime-capability) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| SYS_PTRACE with shared PID | [`access-control-sys-ptrace-capability`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-sys-ptrace-capability) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |

## References

- [Linux Capabilities in OpenShift](https://cloud.redhat.com/blog/linux-capabilities-in-openshift)
- [Set Capabilities for a Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#set-capabilities-for-a-container)
- [Share Process Namespace between Containers](https://kubernetes.io/docs/tasks/configure-pod-container/share-process-namespace/)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
