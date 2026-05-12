---
name: pod-access-control
description: >
  Configure Kubernetes RBAC bindings, service accounts, namespaces, resource
  quotas, and service types for pods. Use when writing, reviewing, or auditing
  Deployments, ServiceAccounts, Roles, RoleBindings, ResourceQuotas, or
  Services for least-privilege access control.
category: "secure_development"
subcategory: "kubernetes"
---

# Pod Access Control

Configure least-privilege access control for Kubernetes workloads by scoping RBAC bindings, isolating namespaces, enforcing resource quotas, and restricting service exposure.

## Service Accounts

Every workload pod must use a dedicated, named service account — not the `default` service account. Default service accounts often carry excessive privileges and make it impossible to apply fine-grained RBAC per workload.

> **Required for:** all profiles (mandatory)

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: app-ns
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: app-ns
spec:
  template:
    spec:
      serviceAccountName: app-sa
```

## RBAC Bindings

### No ClusterRoleBindings

Workload pods must not use ClusterRoleBindings. Cluster-wide role bindings grant excessive privileges that enable lateral movement across the entire cluster. Use namespace-scoped RoleBindings instead.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-role-binding
  namespace: app-ns
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: app-role
subjects:
  - kind: ServiceAccount
    name: app-sa
    namespace: app-ns
```

### No Cross-Namespace RoleBindings

Workload RoleBindings must only exist in the workload's own namespace. Cross-namespace role bindings violate tenant isolation and create unintended privilege escalation paths.

> **Required for:** all profiles (mandatory)

### CRD-Scoped Roles

If a workload creates Custom Resource Definitions, it must supply a Role that only grants access to those CRDs — not to other API resources. This enforces least-privilege for custom resource access.

> **Required for:** Extended (mandatory), all others (optional)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-crd-role
  namespace: app-ns
rules:
  - apiGroups: ["app.example.com"]
    resources: ["myresources"]
    verbs: ["get", "list", "watch", "create", "update", "delete"]
```

## Namespace Management

Workload resources must be deployed to declared namespaces. Do not use:
- `default`
- Any namespace prefixed with `openshift-`
- Any namespace prefixed with `istio-` or `aspenmesh-`

These namespaces are reserved for platform components and service mesh infrastructure.

> **Required for:** all profiles (optional, recommended best practice)

## Resource Quotas

Workload namespaces must have a ResourceQuota applied to prevent unbounded resource consumption. Without quotas, a single workload can starve other applications of CPU and memory.

> **Required for:** Extended (mandatory), all others (optional)

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: app-quota
  namespace: app-ns
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "20"
```

## Resource Requests

All containers must specify CPU and memory resource requests. Requests enable the Kubernetes scheduler to make informed placement decisions and prevent resource contention.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
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

## Service Types

Services must not use `NodePort`. NodePort services expose applications directly on host ports, creating security risks and potential port conflicts with host services. Use `ClusterIP` (default) or `LoadBalancer` instead.

> **Required for:** all profiles (mandatory)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-svc
  namespace: app-ns
spec:
  type: ClusterIP
  selector:
    app: app
  ports:
    - port: 8080
      targetPort: 8080
```

## Implementation Checklist

- [ ] Each pod uses a dedicated, named service account (not `default`)
- [ ] No ClusterRoleBindings are used by workload pods
- [ ] RoleBindings exist only in the workload's own namespace
- [ ] CRD roles only grant access to CRDs, not other API resources
- [ ] Workloads are deployed to declared namespaces (not `default`, `openshift-*`, `istio-*`)
- [ ] Workload namespaces have ResourceQuota applied
- [ ] All containers specify CPU and memory resource requests
- [ ] Services do not use `NodePort`

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| Dedicated service account | [`access-control-pod-service-account`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-pod-service-account) | All profiles: mandatory |
| No ClusterRoleBindings | [`access-control-cluster-role-bindings`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-cluster-role-bindings) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No cross-namespace RoleBindings | [`access-control-pod-role-bindings`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-pod-role-bindings) | All profiles: mandatory |
| CRD-scoped roles | [`access-control-crd-roles`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-crd-roles) | Extended: mandatory, all others: optional |
| Declared namespaces | [`access-control-namespace`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-namespace) | All profiles: optional (recommended) |
| Namespace resource quota | [`access-control-namespace-resource-quota`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-namespace-resource-quota) | Extended: mandatory, all others: optional |
| Resource requests | [`access-control-requests`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-requests) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No NodePort services | [`access-control-service-type`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#access-control-service-type) | All profiles: mandatory |

## References

- [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)
- [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [Managing Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
