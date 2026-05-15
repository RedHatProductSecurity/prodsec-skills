---
name: network-security
description: >
  Configure Kubernetes network security including host access restrictions,
  network policies, port management, and connectivity requirements. Use when
  writing, reviewing, or auditing pod specs, Services, NetworkPolicies,
  or NetworkAttachmentDefinitions.
category: "secure_development"
subcategory: "kubernetes"
---

# Network Security

Restrict host access, enforce network policies, declare all ports, and ensure connectivity across default and secondary networks.

## Host Access Restrictions

Workload pods must not access host resources. All of the following must be disabled:

> **Required for:** all profiles (mandatory)

| Field | Required Value |
|-------|---------------|
| `spec.hostIPC` | `false` |
| `spec.hostNetwork` | `false` (or not set) |
| `spec.hostPID` | `false` |
| `spec.volumes[].hostPath` | Not used |
| `spec.containers[].ports[].hostPort` | Not used |

```yaml
spec:
  hostIPC: false
  hostNetwork: false
  hostPID: false
  containers:
    - name: app
      ports:
        - containerPort: 8080
```

**Why:** Host IPC exposes inter-process communication, host network removes network isolation, host PID exposes all host processes, host path mounts expose the host filesystem, and host ports create port conflicts and bypass network controls.

## Network Policies

Workload namespaces should have a default deny-all NetworkPolicy for both ingress and egress traffic. After applying the default deny, add specific policies to allow only required traffic flows.

> **Required for:** all profiles (optional, recommended best practice)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: app-ns
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

Then allow specific traffic:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-app-ingress
  namespace: app-ns
spec:
  podSelector:
    matchLabels:
      app: app
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: frontend-ns
      ports:
        - port: 8080
          protocol: TCP
```

## Port Management

### Declare All Container Ports

All ports a container listens on must be declared in the container spec. Platforms may block undeclared ports.

> **Required for:** Extended (mandatory), all others (optional)

```yaml
containers:
  - name: app
    ports:
      - containerPort: 8080
        name: http
      - containerPort: 9090
        name: metrics
```

### Reserved Ports

Containers must not listen on ports reserved by OpenShift: **22623** and **22624**. These are used by the Machine Config Server.

> **Required for:** all profiles (mandatory)

Containers must also not use ports reserved by partners.

> **Required for:** Extended (mandatory), all others (optional)

### No NodePort Services

Services must use `ClusterIP` (default) or `LoadBalancer` — not `NodePort`. See the [pod-access-control](../pod-access-control/SKILL.md) skill for details.

## Dual-Stack Services

Services should be configured as IPv6 single-stack or dual-stack (IPv4/IPv6). Avoid IPv4-only service configurations to support modern network architectures.

> **Required for:** Extended (mandatory), all others (optional)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-svc
spec:
  ipFamilyPolicy: PreferDualStack
  ipFamilies:
    - IPv6
    - IPv4
  selector:
    app: app
  ports:
    - port: 8080
```

## Connectivity

Workload containers must be able to communicate via ICMPv4 and ICMPv6 on the default OpenShift network. If using Multus secondary networks, connectivity must also work on those networks.

> **Required for (default network):** Telco/Far-Edge/Extended (mandatory), Non-Telco (mandatory for ICMPv4, optional for ICMPv6)

> **Required for (Multus networks):** Telco/Far-Edge/Extended (mandatory), Non-Telco (optional)

To exclude a pod from connectivity tests, add the label `redhat-best-practices-for-k8s.com/skip_connectivity_tests`.

## SR-IOV Configuration

### NetworkAttachmentDefinition MTU

SR-IOV NetworkAttachmentDefinitions must have an explicit MTU value set to prevent packet fragmentation and performance issues.

> **Required for:** all profiles (mandatory)

### Restart-on-Reboot Label

Pods using SR-IOV network interfaces must have the `restart-on-reboot` label to ensure recovery from node reboots.

> **Required for:** Extended/Far-Edge (mandatory), Telco (optional), Non-Telco (optional)

## Implementation Checklist

- [ ] `hostIPC: false` on all pods
- [ ] `hostNetwork: false` (or not set) on all pods
- [ ] `hostPID: false` on all pods
- [ ] No `hostPath` volume mounts
- [ ] No `hostPort` on any container
- [ ] Default deny-all NetworkPolicy on workload namespaces
- [ ] All container ports declared in the pod spec
- [ ] No containers listen on OpenShift-reserved ports (22623, 22624)
- [ ] No containers listen on partner-reserved ports
- [ ] Services use dual-stack or IPv6 single-stack (not IPv4-only)
- [ ] Workloads pass ICMPv4 and ICMPv6 connectivity on default network
- [ ] Workloads pass ICMPv4 and ICMPv6 connectivity on Multus networks (if used)
- [ ] SR-IOV NetworkAttachmentDefinitions have explicit MTU
- [ ] SR-IOV pods have `restart-on-reboot` label

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| No host IPC | [`access-control-pod-host-ipc`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-pod-host-ipc) | All profiles: mandatory |
| No host network | [`access-control-pod-host-network`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-pod-host-network) | All profiles: mandatory |
| No host PID | [`access-control-pod-host-pid`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-pod-host-pid) | All profiles: mandatory |
| No host path | [`access-control-pod-host-path`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-pod-host-path) | All profiles: mandatory |
| No host port | [`access-control-container-host-port`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-container-host-port) | All profiles: mandatory |
| Default deny-all NetworkPolicy | [`networking-network-policy-deny-all`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-network-policy-deny-all) | All profiles: optional (recommended) |
| Declare all ports | [`networking-undeclared-container-ports-usage`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-undeclared-container-ports-usage) | Extended: mandatory, all others: optional |
| No OCP-reserved ports | [`networking-ocp-reserved-ports-usage`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-ocp-reserved-ports-usage) | All profiles: mandatory |
| No partner-reserved ports | [`networking-reserved-partner-ports`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-reserved-partner-ports) | Extended: mandatory, all others: optional |
| Dual-stack services | [`networking-dual-stack-service`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-dual-stack-service) | Extended: mandatory, all others: optional |
| ICMPv4 connectivity | [`networking-icmpv4-connectivity`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-icmpv4-connectivity) | All profiles: mandatory |
| ICMPv4 Multus connectivity | [`networking-icmpv4-connectivity-multus`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-icmpv4-connectivity-multus) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| ICMPv6 connectivity | [`networking-icmpv6-connectivity`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-icmpv6-connectivity) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| ICMPv6 Multus connectivity | [`networking-icmpv6-connectivity-multus`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-icmpv6-connectivity-multus) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| SR-IOV MTU | [`networking-network-attachment-definition-sriov-mtu`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-network-attachment-definition-sriov-mtu) | All profiles: mandatory |
| SR-IOV restart-on-reboot | [`networking-restart-on-reboot-sriov-pod`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#networking-restart-on-reboot-sriov-pod) | Extended/Far-Edge: mandatory, Telco/Non-Telco: optional |

## References

- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Dual-stack Services](https://kubernetes.io/docs/concepts/services-networking/dual-stack/)
- [SR-IOV Network Operator](https://docs.openshift.com/container-platform/latest/networking/hardware_networks/about-sriov.html)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
