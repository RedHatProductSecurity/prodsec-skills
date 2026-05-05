---
name: isolation-sandboxing
description: Enforce isolation and sandboxing of inference engine execution. Use when deploying, configuring, or reviewing inference engines like vLLM that load and serve AI models, especially third-party models.
category: "secure_development"
subcategory: "inference-engine"
---

# Inference Engine Isolation and Sandboxing

## Security Recommendation

The inference engine loads and executes model code, potentially including third-party or untrusted code. It SHOULD be executed in an isolated, sandboxed environment to limit the impact of malicious models or vulnerabilities in the inference software.

## Risks Mitigated

| Risk | Mitigation Through Isolation |
|---|---|
| **Malicious model execution** | Sandbox limits what malicious code can access and do |
| **Inference software vulnerability** | Isolation may prevent exploitation or limit blast radius |
| **Data exfiltration** | Network isolation prevents unauthorized outbound connections |
| **Lateral movement** | Process and namespace isolation prevents access to other workloads |

## Isolation Approaches

| Approach | Isolation Level | Examples |
|---|---|---|
| **Container** | Process + filesystem + network | Podman, Docker with restricted capabilities |
| **MicroVM** | Hardware-level | Firecracker, Kata Containers |
| **Dedicated VM** | Full hypervisor isolation | KVM, dedicated cloud instances |
| **Namespace + seccomp** | Syscall + resource | Linux namespaces with seccomp profiles |
| **SELinux / AppArmor** | Mandatory access control | Confine the inference process |

## Implementation Checklist

- [ ] Run the inference engine in a container or VM with restricted capabilities
- [ ] Drop all unnecessary Linux capabilities (`--cap-drop=ALL`, add back only what's needed)
- [ ] Apply a seccomp profile to restrict available syscalls
- [ ] Run as a non-root user inside the container/VM
- [ ] Use read-only filesystem where possible; mount model files as read-only
- [ ] Apply network policies to restrict outbound connections
- [ ] Set resource limits (CPU, memory, GPU) to prevent resource exhaustion
- [ ] If using SELinux/AppArmor, apply a policy confining the inference process
- [ ] Monitor the inference engine for anomalous behavior (unexpected network connections, file access)
