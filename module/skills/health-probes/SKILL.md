---
name: health-probes
description: >
  Configure Kubernetes health probes, lifecycle hooks, and termination
  policies. Use when writing, reviewing, or auditing pod specs, Deployments,
  StatefulSets, or Helm templates that define liveness, readiness, startup
  probes, postStart/preStop hooks, or terminationMessagePolicy.
category: "secure_development"
subcategory: "kubernetes"
---

# Health Probes and Lifecycle Management

Kubernetes uses health probes to determine when to restart a container, when to route traffic to a pod, and when a slow-starting application is ready. Lifecycle hooks provide initialization and graceful shutdown control. Together they enable self-healing workloads that recover from pod, host, and network failures.

## Probe Types

Every container should define all three probe types:

| Probe | Purpose | Failure Action |
|-------|---------|----------------|
| **Liveness** | Detects deadlocks and hangs after the application is running | Restarts the container |
| **Readiness** | Determines when a container can accept traffic | Removes the pod from Service endpoints |
| **Startup** | Protects slow-starting containers from premature liveness kills | Disables liveness/readiness checks until the app starts |

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

Without startup probes, slow-starting applications require large `initialDelaySeconds` on liveness probes, which delays failure detection after the application is running.

## Probe Mechanisms

Choose the mechanism that best fits the application:

### httpGet (Preferred for HTTP Services)

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
```

Returns success for any HTTP status 200-399.

### tcpSocket

```yaml
readinessProbe:
  tcpSocket:
    port: 5432
  initialDelaySeconds: 5
  periodSeconds: 10
```

Use for non-HTTP services (databases, message brokers) where opening a TCP connection confirms the service is listening.

### grpc

```yaml
livenessProbe:
  grpc:
    port: 50051
    service: health
  periodSeconds: 10
```

Requires Kubernetes 1.27+ and the application must implement the [gRPC Health Checking Protocol](https://github.com/grpc/grpc/blob/master/doc/health-checking.md).

### exec

> **Warning:** Exec probes have strict performance constraints. See [Exec Probe Performance Constraints](#exec-probe-performance-constraints) before using this mechanism.

```yaml
livenessProbe:
  exec:
    command:
      - /bin/sh
      - -c
      - pg_isready -U postgres
  periodSeconds: 15
  timeoutSeconds: 5
```

Runs a command inside the container. Success is exit code 0. Prefer `httpGet` or `tcpSocket` when possible — exec probes fork a process, which adds latency and CPU overhead.

## Configuration Best Practices

| Parameter | Guidance |
|-----------|----------|
| `initialDelaySeconds` | Use startup probes instead of large values here; keep low (0-10s) when a startup probe is present |
| `periodSeconds` | Must be **>= 10** for exec probes; 10-30s is typical for all probe types |
| `timeoutSeconds` | Should be shorter than `periodSeconds`; 1-5s is typical |
| `failureThreshold` | 3 is the default; increase for applications with occasional slow responses |
| `successThreshold` | Must be 1 for liveness and startup probes; can be higher for readiness |

### Example: Well-Configured Container

```yaml
containers:
  - name: app
    image: registry.example.com/app:v1.2.3
    ports:
      - containerPort: 8080
    startupProbe:
      httpGet:
        path: /healthz
        port: 8080
      periodSeconds: 5
      failureThreshold: 30     # allows up to 150s for startup
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      periodSeconds: 10
      timeoutSeconds: 3
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 3
    terminationMessagePolicy: FallbackToLogsOnError
```

## Lifecycle Hooks

Lifecycle hooks run code at container startup and shutdown without requiring changes to the application itself.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

### PostStart

Runs immediately after the container is created. Kubernetes does not change the container state to `Running` until the PostStart handler completes successfully.

```yaml
lifecycle:
  postStart:
    exec:
      command:
        - /bin/sh
        - -c
        - /app/init.sh
```

Use PostStart to:
- Verify required APIs or dependencies are available
- Register the instance with a service registry
- Run database migrations or schema checks

### PreStop

Runs immediately before the container receives SIGTERM. The container is not terminated until the PreStop handler completes (up to `terminationGracePeriodSeconds`).

```yaml
lifecycle:
  preStop:
    exec:
      command:
        - /bin/sh
        - -c
        - sleep 5 && /app/drain.sh
```

Use PreStop to:
- Drain active connections and in-flight requests
- Deregister from service registries or load balancers
- Flush buffers, close database connections, release locks
- Allow time for endpoint propagation (the `sleep` pattern above gives kube-proxy time to update iptables rules before the application stops accepting connections)

## Exec Probe Performance Constraints

Exec probes fork a process inside the container on every probe interval. For latency-sensitive and performance-critical workloads, this overhead can cause unacceptable jitter.

### CPU-Pinned Workloads

Workloads with CPU pinning (Guaranteed QoS with exclusive CPUs) must **not** use exec probes. Use `httpGet` or `tcpSocket` instead.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

**Why:** Exec probes spawn a process that competes for the pinned CPUs, interrupting latency-sensitive operations and degrading deterministic scheduling guarantees.

### Real-Time Applications

Containers running real-time applications must **not** use exec probes.

> **Required for:** Far-Edge (mandatory), all others (optional)

**Why:** Process forking causes latency spikes that violate real-time scheduling constraints.

### Cluster-Wide Exec Probe Limits

Limit exec probes to fewer than **10** across the entire workload in a cluster. Each exec probe must have `periodSeconds >= 10`.

> **Required for:** all profiles (optional, recommended best practice)

**Why:** Excessive exec probes consume system resources and can degrade overall cluster performance in resource-constrained environments.

## Termination Message Policy

Set `terminationMessagePolicy: FallbackToLogsOnError` on all containers. This ensures that when a container exits with an error, Kubernetes captures the last chunk of the container's log output as the termination message, making failure diagnosis possible without external log aggregation.

> **Required for:** Telco (mandatory), Far-Edge (mandatory), Extended (mandatory), Non-Telco (optional)

```yaml
containers:
  - name: app
    image: registry.example.com/app:v1.2.3
    terminationMessagePolicy: FallbackToLogsOnError
```

The default policy (`File`) only reads from `/dev/termination-log`, which most applications do not write to, resulting in empty termination messages on failure.

## Implementation Checklist

- [ ] All containers define a **liveness** probe
- [ ] All containers define a **readiness** probe
- [ ] All containers define a **startup** probe
- [ ] `periodSeconds` is >= 10 for all exec probes
- [ ] CPU-pinned workloads (Guaranteed QoS with exclusive CPUs) do not use exec probes
- [ ] Real-time applications do not use exec probes
- [ ] Fewer than 10 exec probes are configured cluster-wide for the workload
- [ ] PostStart hooks are configured for initialization logic
- [ ] PreStop hooks are configured for graceful shutdown
- [ ] `terminationMessagePolicy: FallbackToLogsOnError` is set on all containers
- [ ] Probe timeouts and thresholds are tuned for the application's startup and response characteristics

## Certsuite Test Mapping

| Guidance | Certsuite Test ID | Profiles |
|----------|-------------------|----------|
| Liveness probe required | `lifecycle-liveness-probe` | Telco: mandatory, Far-Edge: mandatory, Extended: mandatory, Non-Telco: optional |
| Readiness probe required | `lifecycle-readiness-probe` | Telco: mandatory, Far-Edge: mandatory, Extended: mandatory, Non-Telco: optional |
| Startup probe required | `lifecycle-startup-probe` | Telco: mandatory, Far-Edge: mandatory, Extended: mandatory, Non-Telco: optional |
| PostStart hook configured | `lifecycle-container-poststart` | Telco: mandatory, Far-Edge: mandatory, Extended: mandatory, Non-Telco: optional |
| PreStop hook configured | `lifecycle-container-prestop` | Telco: mandatory, Far-Edge: mandatory, Extended: mandatory, Non-Telco: optional |
| No exec probes on CPU-pinned workloads | `performance-cpu-pinning-no-exec-probes` | Telco: mandatory, Far-Edge: mandatory, Extended: mandatory, Non-Telco: optional |
| Exec probe count and period limits | `performance-max-resources-exec-probes` | All profiles: optional |
| No exec probes on real-time apps | `performance-rt-apps-no-exec-probes` | Far-Edge: mandatory, all others: optional |
| Termination message policy | `observability-termination-policy` | Telco: mandatory, Far-Edge: mandatory, Extended: mandatory, Non-Telco: optional |

## References

- [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Container Lifecycle Hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/)
- [Pod Lifecycle — Termination](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)
- [gRPC Health Checking Protocol](https://github.com/grpc/grpc/blob/master/doc/health-checking.md)
- [Red Hat Best Practices for Kubernetes Guide](https://redhat-best-practices-for-k8s.github.io/guide/)
- [Red Hat Best Practices Test Suite for Kubernetes (certsuite)](https://github.com/redhat-best-practices-for-k8s/certsuite)
