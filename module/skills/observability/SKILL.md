---
name: observability
description: >
  Configure Kubernetes workload observability including container logging,
  CRD status reporting, port naming conventions, image tagging, and API
  compatibility. Use when writing, reviewing, or auditing CRDs, container
  specs, Services, or preparing for OpenShift version upgrades.
category: "secure_development"
subcategory: "kubernetes"
---

# Workload Observability

Configure workloads for operational visibility by following logging, naming, tagging, and API compatibility best practices.

## Container Logging

Containers must log to stdout and stderr. Do not redirect logs to files inside the container — platform log collection (Fluentd, Vector, Loki) relies on capturing stdout/stderr streams.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
containers:
  - name: app
    image: registry.example.com/app:v1.2.3
    command: ["/app"]
```

Avoid patterns like redirecting output to a log file:
```
/app > /var/log/app.log 2>&1  # Don't do this
```

## CRD Status Sub-Resource

All Custom Resource Definitions must include a `status` sub-resource specification. The status sub-resource enables the platform to track the state of custom resources and allows controllers to report status separately from spec updates.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: myresources.app.example.com
spec:
  group: app.example.com
  names:
    kind: MyResource
    plural: myresources
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
      subresources:
        status: {}
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
            status:
              type: object
```

## Port Naming Conventions

Container port names must follow the format `<protocol>[-<suffix>]`. This convention enables service mesh integration and platform-level traffic management.

> **Required for:** Extended (mandatory), all others (optional)

| Valid | Invalid |
|-------|---------|
| `http` | `my-port` |
| `http-api` | `port-8080` |
| `grpc-data` | `app` |
| `tcp-metrics` | `metrics` |

```yaml
containers:
  - name: app
    ports:
      - containerPort: 8080
        name: http-api
      - containerPort: 9090
        name: http-metrics
      - containerPort: 50051
        name: grpc-data
```

## Image Tagging

All container images must have explicit tags. Do not rely on the implicit `latest` tag — it makes deployments non-reproducible and prevents rollback.

> **Required for:** Extended (mandatory), all others (optional)

```yaml
containers:
  - name: app
    image: registry.example.com/app:v1.2.3   # Good: explicit tag
    # image: registry.example.com/app         # Bad: implicit latest
    # image: registry.example.com/app:latest  # Bad: explicit latest
```

## API Compatibility

Workload APIs must be compatible with the next OpenShift version. Before upgrading, verify that no deprecated or removed APIs are in use by the workload's CRDs, webhooks, or API calls.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

Use `oc api-resources` and the [Kubernetes API deprecation guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/) to check for deprecated APIs before platform upgrades.

## Implementation Checklist

- [ ] All containers log to stdout/stderr (no log file redirection)
- [ ] All CRDs have `status` sub-resource defined
- [ ] Container port names follow `<protocol>[-<suffix>]` format
- [ ] All container images have explicit tags (not `latest`)
- [ ] Workload APIs are compatible with the next OpenShift version

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| Log to stdout/stderr | [`observability-container-logging`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#observability-container-logging) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| CRD status sub-resource | [`observability-crd-status`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#observability-crd-status) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |
| Port naming convention | [`manageability-container-port-name-format`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#manageability-container-port-name-format) | Extended: mandatory, all others: optional |
| Explicit image tags | [`manageability-containers-image-tag`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#manageability-containers-image-tag) | Extended: mandatory, all others: optional |
| API compatibility | [`observability-compatibility-with-next-ocp-release`](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md#observability-compatibility-with-next-ocp-release) | Telco/Far-Edge/Extended: mandatory, Non-Telco: optional |

## References

- [Kubernetes Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
- [Custom Resource Definitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
- [Kubernetes API Deprecation Guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
