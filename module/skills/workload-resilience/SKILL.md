---
name: workload-resilience
description: >
  Configure Kubernetes workload resilience including pod scheduling, scaling,
  high availability, and disruption budgets. Use when writing, reviewing, or
  auditing Deployments, StatefulSets, CRDs, or any workload that requires
  scaling, anti-affinity, topology spread, or PodDisruptionBudgets.
category: "secure_development"
subcategory: "kubernetes"
---

# Workload Resilience

Configure Kubernetes workloads to survive node failures, scale under load, and tolerate platform upgrades without service disruption.

## Pod Ownership

Deploy workloads as part of a ReplicaSet (via Deployment) or StatefulSet. Do not use naked pods or DaemonSets for application workloads — they lack proper lifecycle management for updates, scaling, and recovery.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## Pod Scheduling

Pods should not use `nodeSelector` or `nodeAffinity` unless the workload requires specialized hardware (e.g., GPUs, SR-IOV NICs). Hardcoded node placement reduces cluster flexibility and causes deployment failures when specific nodes are unavailable.

> **Required for:** Non-Telco (mandatory), all others (optional)

```yaml
# Avoid this unless hardware-specific scheduling is required
spec:
  nodeSelector:
    kubernetes.io/hostname: worker-1  # creates a single point of failure
```

If the workload requires affinity rules, add the label `AffinityRequired: 'true'` to the pod and define appropriate affinity rules.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### Tolerations

Do not modify the default `NoExecute`, `PreferNoSchedule`, or `NoSchedule` tolerations. Custom tolerations can allow pods to be scheduled on inappropriate nodes, violating scheduling policies.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## Scaling

Deployments, StatefulSets, and CRDs must support scale in/out operations. The platform tests this by scaling replicas down by 1 and then restoring the original count.

> **Required for:** Telco (mandatory), Extended (mandatory), Non-Telco (mandatory), Far-Edge (optional)

For workloads managed by a Horizontal Pod Autoscaler (HPA), ensure that scaling works correctly when the HPA's `minReplicas` and `maxReplicas` are adjusted.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: registry.example.com/app:v1.2.3
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi
```

## High Availability

High-availability workloads must have `replicas > 1` and define `podAntiAffinity` rules to spread replicas across nodes. Without anti-affinity, all replicas may land on the same node, creating a single point of failure.

> **Required for:** Telco (mandatory), Extended (mandatory), Non-Telco (mandatory), Far-Edge (optional)

```yaml
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: app
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: app
              topologyKey: kubernetes.io/hostname
```

### Topology Spread Constraints

If using `topologySpreadConstraints`, include constraints for both `kubernetes.io/hostname` and `topology.kubernetes.io/zone` topology keys. This ensures workloads are distributed across nodes and availability zones, preventing PodDisruptionBudgets from blocking platform upgrades.

Omitting `topologySpreadConstraints` entirely is also acceptable — the Kubernetes scheduler applies implicit hostname and zone constraints by default.

> **Required for:** Telco (mandatory), all others (optional)

```yaml
spec:
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: kubernetes.io/hostname
      whenUnsatisfiable: DoNotSchedule
      labelSelector:
        matchLabels:
          app: app
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: DoNotSchedule
      labelSelector:
        matchLabels:
          app: app
```

## Pod Disruption Budgets

Every workload with multiple replicas should have a PodDisruptionBudget (PDB). The PDB must have valid `minAvailable` or `maxUnavailable` values — `minAvailable` must not be zero, and `maxUnavailable` must not equal the total replica count.

> **Required for:** all profiles (mandatory)

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: app
```

### Zone-Aware PDBs

For multi-zone clusters, PDBs must tolerate an entire zone going offline during platform upgrades. Set `maxUnavailable >= ceil(replicas / zones)` or `minAvailable <= replicas - ceil(replicas / zones)`.

For example, with 3 replicas across 3 zones: `maxUnavailable: 1` allows draining all pods in one zone.

## Pod Recreation

Workloads must be recreatable on different nodes. The platform validates this by cordoning and draining a node hosting the workload, then verifying the pod is re-instantiated on another node with the correct replica count.

> **Required for:** all profiles (mandatory)

Ensure:
- The workload is managed by a ReplicaSet or StatefulSet (not a naked pod)
- Persistent storage is not node-local in multi-node clusters
- No `nodeSelector` or `nodeAffinity` pins the pod to a specific node
- Sufficient nodes are available in the cluster for rescheduling

## Implementation Checklist

- [ ] Workloads are deployed via Deployments or StatefulSets (no naked pods)
- [ ] Pods do not use `nodeSelector` or `nodeAffinity` unless hardware-specific
- [ ] Pods with `AffinityRequired: 'true'` label have affinity rules defined
- [ ] Default tolerations (`NoExecute`, `PreferNoSchedule`, `NoSchedule`) are not modified
- [ ] Deployments support scale in/out operations
- [ ] StatefulSets support scale in/out operations
- [ ] CRDs support scale in/out operations
- [ ] High-availability workloads have `replicas > 1` with `podAntiAffinity`
- [ ] `topologySpreadConstraints` (if used) include both hostname and zone keys
- [ ] PodDisruptionBudgets have valid `minAvailable` or `maxUnavailable`
- [ ] PDBs are zone-aware for multi-zone clusters
- [ ] Pods can be recreated on different nodes after cordon/drain

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| Pod ownership (ReplicaSet/StatefulSet) | `lifecycle-pod-owner-type` | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No nodeSelector/nodeAffinity | `lifecycle-pod-scheduling` | Non-Telco: mandatory, all others: optional |
| Affinity rules when labeled | `lifecycle-affinity-required-pods` | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No toleration bypass | `lifecycle-pod-toleration-bypass` | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Deployment scaling | `lifecycle-deployment-scaling` | Telco/Extended/Non-Telco: mandatory, Far-Edge: optional |
| StatefulSet scaling | `lifecycle-statefulset-scaling` | Telco/Extended/Non-Telco: mandatory, Far-Edge: optional |
| CRD scaling | `lifecycle-crd-scaling` | Telco/Extended/Non-Telco: mandatory, Far-Edge: optional |
| HA with podAntiAffinity | `lifecycle-pod-high-availability` | Telco/Extended/Non-Telco: mandatory, Far-Edge: optional |
| Topology spread constraints | `lifecycle-topology-spread-constraint` | Telco: mandatory, all others: optional |
| Pod disruption budgets | `observability-pod-disruption-budget` | All profiles: mandatory |
| Pod recreation after drain | `lifecycle-pod-recreation` | All profiles: mandatory |

## References

- [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/)
- [Pod Disruption Budgets](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
- [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
- [Inter-pod Affinity and Anti-affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
