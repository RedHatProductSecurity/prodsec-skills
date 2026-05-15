---
name: platform-integrity
description: >
  Validate Kubernetes platform configuration including boot parameters,
  hugepages, kernel state, sysctl settings, OpenShift lifecycle, and
  service mesh compliance. Use when auditing cluster node configuration
  or preparing for platform upgrades.
category: "secure_development"
subcategory: "kubernetes"
---

# Platform Integrity

Validate that the underlying platform configuration meets operational and security requirements. These checks verify node-level settings that affect all workloads on the cluster.

## Boot Parameters

Boot parameters must be configured through MachineConfig or the Performance Addon Operator — not set manually on nodes. Manual changes are lost on reboot and create configuration drift between nodes.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

> **OpenShift Note:** Use `MachineConfig` or `PerformanceProfile` CRs to manage boot parameters declaratively.

## Sysctl Configuration

Sysctl kernel parameters must match values defined in MachineConfig. Any sysctl values that differ from the MachineConfig-declared values indicate manual node modification or configuration drift.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## Kernel Taint

Node kernels must not be tainted. A tainted kernel indicates non-standard modules, out-of-tree drivers, or other modifications that may affect stability and supportability.

> **Required for:** all profiles (mandatory)

## Hugepages Configuration

### Configuration Method

Hugepage settings must be configured via MachineConfig — not manually on nodes. Manual hugepage allocation is lost on reboot.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### Hugepage Size Restrictions

Pods using hugepages must use a single size:

- **1Gi hugepages only** — for workloads requiring 1Gi pages

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

- **2Mi hugepages only** — for workloads requiring 2Mi pages

> **Required for:** Far-Edge (mandatory), all others (optional)

```yaml
resources:
  requests:
    hugepages-1Gi: 2Gi
    memory: 256Mi
  limits:
    hugepages-1Gi: 2Gi
    memory: 256Mi
```

## Hyperthreading

Baremetal worker nodes must have hyperthreading enabled. Hyperthreading provides additional logical CPUs that improve throughput for many workload types.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## OpenShift Lifecycle

### Cluster Version

The OpenShift version must not be end-of-life. Running unsupported versions means no security patches, bug fixes, or Red Hat support.

> **Required for:** all profiles (mandatory)

### Node OS Compatibility

The node operating system must be compatible with the deployed OpenShift version. Mismatched OS and platform versions can cause unpredictable behavior.

> **Required for:** all profiles (mandatory)

### Cluster Operator Health

All cluster operators must be in `Available` state. Degraded or unavailable operators indicate platform issues that can affect workload reliability.

> **Required for:** all profiles (mandatory)

## Service Mesh

If the `istio-system` namespace exists on the cluster, all workload pods must use Istio sidecar proxies. Pods without sidecars in a service mesh environment bypass traffic management, security policies, and observability features.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## Implementation Checklist

- [ ] Boot parameters are set via MachineConfig or PerformanceProfile (not manually)
- [ ] Sysctl values match MachineConfig declarations
- [ ] Node kernels are not tainted
- [ ] Hugepages are configured via MachineConfig (not manually)
- [ ] Pods using hugepages use a single size (1Gi or 2Mi)
- [ ] Baremetal worker nodes have hyperthreading enabled
- [ ] OpenShift version is not end-of-life
- [ ] Node OS is compatible with the OpenShift version
- [ ] All cluster operators are in Available state
- [ ] All pods have Istio sidecars if istio-system namespace exists

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| Boot params via MachineConfig | [`platform-alteration-boot-params`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-boot-params) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Sysctl matches MachineConfig | [`platform-alteration-sysctl-config`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-sysctl-config) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No tainted kernels | [`platform-alteration-tainted-node-kernel`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-tainted-node-kernel) | All profiles: mandatory |
| Hugepages via MachineConfig | [`platform-alteration-hugepages-config`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-hugepages-config) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| 1Gi hugepages only | [`platform-alteration-hugepages-1g-only`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-hugepages-1g-only) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| 2Mi hugepages only | [`platform-alteration-hugepages-2m-only`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-hugepages-2m-only) | Far-Edge: mandatory, all others: optional |
| Hyperthreading enabled | [`platform-alteration-hyperthread-enable`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-hyperthread-enable) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| OCP not end-of-life | [`platform-alteration-ocp-lifecycle`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-ocp-lifecycle) | All profiles: mandatory |
| Node OS compatible | [`platform-alteration-ocp-node-os-lifecycle`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-ocp-node-os-lifecycle) | All profiles: mandatory |
| Cluster operators healthy | [`platform-alteration-cluster-operator-health`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-cluster-operator-health) | All profiles: mandatory |
| Istio sidecars present | [`platform-alteration-service-mesh-usage`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#platform-alteration-service-mesh-usage) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |

## References

- [OpenShift MachineConfig](https://docs.openshift.com/container-platform/latest/post_installation_configuration/machine-configuration-tasks.html)
- [Managing Huge Pages](https://kubernetes.io/docs/tasks/manage-hugepages/scheduling-hugepages/)
- [OpenShift Life Cycle Policy](https://access.redhat.com/support/policy/updates/openshift)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
