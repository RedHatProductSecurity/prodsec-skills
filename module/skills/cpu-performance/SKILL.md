---
name: cpu-performance
description: >
  Configure CPU isolation, scheduling policies, storage provisioning, and
  image pull policies for latency-sensitive Kubernetes workloads. Use when
  writing, reviewing, or auditing pod specs for telco, far-edge, or
  real-time workloads that require deterministic CPU performance.
category: "secure_development"
subcategory: "kubernetes"
---

# CPU and Performance Configuration

Configure workloads for deterministic CPU performance, correct scheduling policies, and reliable storage and image management.

## CPU Isolation

For workloads requiring exclusive CPU access (Guaranteed QoS with dedicated CPUs), all containers in the pod must meet these requirements:

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

- CPU requests and limits must be **identical** and specified in **whole units** (e.g., `2`, not `2.5` or `2000m`)
- `runtimeClassName` must be specified
- Annotations must disable CPU and IRQ load-balancing

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  annotations:
    cpu-load-balancing.crio.io: "disable"
    irq-load-balancing.crio.io: "disable"
spec:
  template:
    spec:
      runtimeClassName: performance-rt
      containers:
        - name: app
          resources:
            requests:
              cpu: "2"
              memory: 256Mi
            limits:
              cpu: "2"
              memory: 256Mi
```

## CPU Pool Scheduling Policies

Containers must use the correct scheduling policy for their CPU pool type.

### Exclusive CPU Pool

Workloads in the exclusive CPU pool must use real-time (RT) scheduling policy with priority less than 10.

> **Required for:** Far-Edge (mandatory), all others (optional)

### Isolated CPU Pool

Workloads in the isolated CPU pool must also use RT scheduling policy.

> **Required for:** Far-Edge (mandatory), all others (optional)

### Shared CPU Pool

Workloads in the shared CPU pool must use non-RT scheduling policies (e.g., `SCHED_OTHER`) to share CPU time fairly with other applications and kernel threads.

> **Required for:** Far-Edge (mandatory), all others (optional)

### CPU Pool Consistency

If one container in a pod selects an exclusive CPU pool, all containers in that pod must select the same CPU pool type.

> **Required for:** Far-Edge (mandatory), all others (optional)

## Image Pull Policy

Containers must use `IfNotPresent` as the image pull policy. This ensures pods can restart even if the image registry is temporarily unavailable.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
containers:
  - name: app
    image: registry.example.com/app:v1.2.3
    imagePullPolicy: IfNotPresent
```

## Pod Ownership

Workload pods must be deployed as part of a ReplicaSet (via Deployment) or StatefulSet. Do not use naked pods or DaemonSets — they lack proper lifecycle management for updates, scaling, and recovery.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## Storage Provisioning

### Persistent Volume Reclaim Policy

Persistent volumes used by workloads must have a reclaim policy of `Delete`. This ensures storage is cleaned up when the workload is removed from the cluster.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-pv
spec:
  persistentVolumeReclaimPolicy: Delete
```

### Storage Provisioner

Multi-node clusters must not use local storage provisioners (`kubernetes.io/no-provisioner`, `topolvm.io`). Local storage is only appropriate for single-node clusters, where only one local provisioner type should be installed (LVMS or no-provisioner).

> **Required for:** all profiles (mandatory)

## Implementation Checklist

- [ ] CPU-isolated workloads have identical CPU requests and limits in whole units
- [ ] CPU-isolated pods specify `runtimeClassName` and disable CPU/IRQ load-balancing
- [ ] Exclusive/isolated CPU pool workloads use RT scheduling policy
- [ ] Shared CPU pool workloads use non-RT scheduling policy (`SCHED_OTHER`)
- [ ] All containers in a pod use the same CPU pool type
- [ ] `imagePullPolicy: IfNotPresent` is set on all containers
- [ ] Workloads are deployed via Deployments or StatefulSets (no naked pods)
- [ ] Persistent volumes have `persistentVolumeReclaimPolicy: Delete`
- [ ] Multi-node clusters do not use local storage provisioners

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| CPU isolation | [`lifecycle-cpu-isolation`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#lifecycle-cpu-isolation) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Exclusive CPU pool RT scheduling | [`performance-exclusive-cpu-pool-rt-scheduling-policy`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#performance-exclusive-cpu-pool-rt-scheduling-policy) | Far-Edge: mandatory, all others: optional |
| Isolated CPU pool RT scheduling | [`performance-isolated-cpu-pool-rt-scheduling-policy`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#performance-isolated-cpu-pool-rt-scheduling-policy) | Far-Edge: mandatory, all others: optional |
| Shared CPU pool non-RT scheduling | [`performance-shared-cpu-pool-non-rt-scheduling-policy`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#performance-shared-cpu-pool-non-rt-scheduling-policy) | Far-Edge: mandatory, all others: optional |
| CPU pool consistency | [`performance-exclusive-cpu-pool`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#performance-exclusive-cpu-pool) | Far-Edge: mandatory, all others: optional |
| Image pull policy | [`lifecycle-image-pull-policy`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#lifecycle-image-pull-policy) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Pod ownership | [`lifecycle-pod-owner-type`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#lifecycle-pod-owner-type) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| PV reclaim policy | [`lifecycle-persistent-volume-reclaim-policy`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#lifecycle-persistent-volume-reclaim-policy) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Storage provisioner | [`lifecycle-storage-provisioner`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#lifecycle-storage-provisioner) | All profiles: mandatory |

## References

- [CPU Manager for Kubernetes](https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/)
- [Topology Manager](https://kubernetes.io/docs/tasks/administer-cluster/topology-manager/)
- [Configure Quality of Service for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/)
- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
