---
name: operator-security
description: >
  Enforce least-privilege RBAC and secure runtime configuration for Kubernetes
  Operators. Use when building, reviewing, or auditing Operator manifests,
  ClusterRoles, Roles, OLM bundles, or CRD definitions.
category: "secure_development"
subcategory: "kubernetes"
---

# Kubernetes Operator Security

Secure Operator manifests, OLM packaging, CRD governance, and runtime configuration for least-privilege operation.

## Design Principles

### Minimize Scope

- Restrict cluster-scope and namespace-scope permissions to the minimum required for the Operator to function
- Justify every cluster-scoped permission; move static cluster-scoped resource creation to the OLM catalog when possible
- Use `OperatorGroup` to specify the set of namespaces the Operator manages

### Namespace Isolation

- Deploy the Operator in a **separate namespace** from its operands
- Never deploy Operators in namespaces shared with non-privileged users
- Ensure non-privileged users cannot read Secrets in the Operator's namespace

### Fine-Grained Roles

- Prefer many small Roles with granular permissions over a few broad Roles
- Each Role should grant the minimum verbs and resources needed for a single responsibility

## RBAC Requirements

| Rule | Rationale |
|---|---|
| **No wildcards** -- list every verb and resource explicitly | Wildcards grant permissions to resources that may not exist yet |
| **No `cluster-admin`** | Grants unrestricted access to the entire cluster |
| **No self-escalating RBAC** | Roles must not grant the ability to create or modify their own RoleBindings |
| **No `Escalate` verb** | Allows circumventing RBAC restrictions |
| **No `Bind` verb** in role definitions | Allows binding to roles with higher privileges |

## Container Security

- Set a **numeric `USER`** in the Containerfile; never default to or assume `uid=0`
- Accept the high UID (billion+) that OpenShift assigns to the namespace
- Set `readOnlyRootFilesystem: true`
- Set `runAsNonRoot: true`
- Set `automountServiceAccountToken: false` unless the SA token is actually needed
- Never require **host paths** unless the Operator is part of the control plane
- Set `no-new-privileges: true` in the security context
- Use **group ID** permissions for shared file access instead of user ID

## OLM Installation

### Installation Source

Operators must be installed via the Operator Lifecycle Manager (OLM). Direct deployment of operator pods bypasses OLM's dependency resolution, upgrade management, and security controls.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### Installation Status

Operators must report a `Succeeded` installation status. Failed or pending installations indicate packaging or dependency issues.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### No SCC Privileges

Operators must not require Security Context Constraint (SCC) access privileges during installation.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### No Duplicate Operators

Only one instance of the same operator CSV should exist per cluster.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## CRD Governance

### OpenAPI Schema

All Custom Resource Definitions must include an OpenAPI v3 schema specification. This enables validation of custom resources at admission time.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### CRD Versioning

CRDs must have valid versioning with proper served/storage version configuration.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### Semantic Versioning

Operators must use semantic versioning (semver) for their CSV version.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### Single CRD Owner

Each CRD must be owned by only one operator. Multiple operators claiming ownership of the same CRD creates conflict and unpredictable behavior.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## Catalog Source Management

### Bundle Count

Catalog sources must contain fewer than 1000 bundles. Large catalogs degrade OLM performance and increase memory consumption.

> **Required for:** all profiles (optional, recommended best practice)

### OLM Skip Range

Operators with multiple versions in a catalog must have a valid OLM skip range configured to enable proper upgrade paths.

> **Required for:** all profiles (optional, recommended best practice)

## Namespace Scoping

Tenant namespaces can only contain operators with `SingleNamespaced` or `MultiNamespaced` install modes. Cluster-scoped operators should not be installed in tenant namespaces.

> **Required for:** all profiles (optional, recommended best practice)

## Resource Constraints

Operator pods must not enable hugepages. Hugepage allocation is a node-level resource that should be reserved for application workloads, not operator infrastructure.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

## Implementation Checklist

- [ ] Every ClusterRole and Role lists explicit verbs and resources (no wildcards)
- [ ] `cluster-admin` is not used
- [ ] No Role can escalate its own privileges
- [ ] `Escalate` and `Bind` verbs are not granted
- [ ] Operator runs in a dedicated namespace, separate from operands
- [ ] Containerfile sets a numeric non-root `USER`
- [ ] `readOnlyRootFilesystem: true` is set
- [ ] `runAsNonRoot: true` is set
- [ ] `automountServiceAccountToken: false` unless required
- [ ] No host path mounts unless justified (control plane only)
- [ ] `OperatorGroup` is used to scope namespace access
- [ ] Operator is installed via OLM
- [ ] Operator reports `Succeeded` installation status
- [ ] No SCC privileges required during installation
- [ ] Only one instance of the operator CSV per cluster
- [ ] All CRDs have OpenAPI v3 schema
- [ ] CRDs have valid versioning configuration
- [ ] Operator uses semantic versioning
- [ ] Each CRD is owned by only one operator
- [ ] Catalog source has fewer than 1000 bundles
- [ ] Operator pods do not enable hugepages

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| Installed via OLM | [`operator-install-source`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-install-source) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Installation succeeded | [`operator-install-status-succeeded`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-install-status-succeeded) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No SCC privileges | [`operator-install-status-no-privileges`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-install-status-no-privileges) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| No duplicate operators | [`operator-multiple-same-operators`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-multiple-same-operators) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| CRD OpenAPI schema | [`operator-crd-openapi-schema`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-crd-openapi-schema) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| CRD versioning | [`operator-crd-versioning`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-crd-versioning) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Semantic versioning | [`operator-semantic-versioning`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-semantic-versioning) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Single CRD owner | [`operator-single-crd-owner`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-single-crd-owner) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Catalog bundle count | [`operator-catalogsource-bundle-count`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-catalogsource-bundle-count) | All profiles: optional (recommended) |
| OLM skip range | [`operator-olm-skip-range`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-olm-skip-range) | All profiles: optional (recommended) |
| Namespace scoping | [`operator-single-or-multi-namespaced-allowed-in-tenant-namespaces`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-single-or-multi-namespaced-allowed-in-tenant-namespaces) | All profiles: optional (recommended) |
| No hugepages | [`operator-pods-no-hugepages`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#operator-pods-no-hugepages) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |

## References

- [Kubernetes Operators: good security practices](https://www.redhat.com/en/blog/kubernetes-operators-good-security-practices)
- [Operator Lifecycle Manager](https://olm.operatorframework.io/)
- [Custom Resource Definitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
- [Semantic Versioning](https://semver.org/)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
