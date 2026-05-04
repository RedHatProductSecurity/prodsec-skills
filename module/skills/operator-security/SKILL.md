---
name: operator-security
description: >
  Enforce least-privilege RBAC and secure runtime configuration for Kubernetes
  Operators. Use when building, reviewing, or auditing Operator manifests,
  ClusterRoles, Roles, or OLM bundles.
category: "secure_development"
subcategory: "kubernetes"
---

# Kubernetes Operator Security

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

## References

- [Kubernetes Operators: good security practices](https://www.redhat.com/en/blog/kubernetes-operators-good-security-practices)
