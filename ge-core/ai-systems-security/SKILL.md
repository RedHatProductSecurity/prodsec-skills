---
name: ai-systems-security
description: >
  Secure AI-powered products and infrastructure. Use when integrating LLM
  APIs, deploying model-serving infrastructure, building agent workflows,
  connecting MCP servers, or reviewing AI system architecture for security
  gaps.
metadata:
  category: secure_development
  subcategory: ai-systems
---

# AI Systems Security

Security guidance for teams that **serve, integrate, or operate** LLMs and AI agents — not for teams training or fine-tuning models. Covers the attack surface introduced when products call LLM APIs, run agent workflows, or expose tool servers.

## When to Use

- Integrating an LLM API (OpenAI, Anthropic, self-hosted) into a product
- Deploying model-serving infrastructure (OpenShift AI, RHOAI, vLLM)
- Building or reviewing agent workflows that take actions on behalf of users
- Connecting MCP servers to agents or LLM-powered features
- Reviewing AI system architecture for security gaps

## When NOT to Use

- Reviewing AI-generated code for correctness (use `ai-code-review`)
- General web application security without AI components (use `web-application-security`)
- Container hardening without AI-specific concerns (use `container-hardening`)

---

## 1. Secure LLM Integration

### Third-party model providers

- Obtain **information security approval** for each provider before integration
- All connections **MUST use TLS** — never send prompts or receive responses over unencrypted channels
- **Never hardcode API keys** in source code, commit them to version control, or bake them into container images
- Store credentials in secret management systems (Vault, Kubernetes Secrets) or inject via environment variables at runtime
- Rotate API credentials on a regular schedule and monitor usage for unexpected patterns

```
Credential storage:
  FORBIDDEN: Hardcoded in source, committed to git, baked in images
  REQUIRED:  Secret management (Vault, K8s Secrets) or env vars injected at runtime
```

### Self-hosted models

- Scan models for malicious code before loading — avoid unsafe serialization formats (pickle) that execute code on deserialization; prefer SafeTensors
- Verify model provenance and integrity (signatures, checksums) before deployment
- Isolate model-serving processes with dedicated service accounts and restricted network access

---

## 2. Prompt Injection Defense

Prompt injection cannot be fully prevented by any single control. Use **layered defense**:

```
Rate Limiting → Input Guardrails → Safer Model → Output Guardrails → Sandbox
```

### Input guardrails (user → model)

- Block known injection patterns and adversarial prompts
- Mask PII and credentials before they reach the model
- Enforce input length limits and rate limiting per user/client

### Output guardrails (model → user)

- Block harmful, policy-violating, or data-leaking content
- Mask sensitive information the model may have surfaced from training data
- Validate model-generated actions before execution (see Section 6)

### Model selection

- Prefer models with published safety benchmarks, alignment training (RLHF/Constitutional AI), and disclosed vulnerability tracking
- Restrict model tool/function calling to only what is needed — minimize available capabilities

### Human-in-the-loop

- **Require explicit user confirmation before executing any sensitive or destructive LLM-triggered action** — this is the single most effective mitigation

---

## 3. Agent Identity and Permissions

### Distinct agent identity

- Each agent **MUST have its own identity** (service account, SPIFFE ID) — never inherit or impersonate a human user's identity
- Assign agent-specific scopes and permissions tailored to its purpose (least privilege)
- Include agent identity in all audit logs; distinguish agent actions from human actions

### Delegation

- When an agent acts on behalf of a user, use delegation mechanisms (OAuth Token Exchange with `act` claim) that preserve both identities
- A compromised agent should only be able to access its own permissions, not the delegating user's full access

```json
{
  "action": "tool:execute",
  "actor": {
    "type": "agent",
    "id": "agent:data-analyst-v2",
    "delegated_by": "user:jane.doe"
  }
}
```

---

## 4. Credential Hygiene

### No credential forwarding

**FORBIDDEN:** Never forward user credentials or authentication tokens to downstream tools or third-party APIs.

```python
# WRONG — never forward user tokens
headers = {"Authorization": f"Bearer {user_token}"}
requests.post(tool_url, headers=headers, json=params)
```

```python
# CORRECT — use the server's own credentials
server_token = get_server_credential_for(tool_url)
headers = {"Authorization": f"Bearer {server_token}"}
requests.post(tool_url, headers=headers, json=params)
```

### Separate credentials per downstream service

- MCP servers and agents must obtain their own credentials for downstream services via OAuth client flows, pre-registered service accounts, or Token Exchange
- Audit all outbound requests to verify user tokens never leak in headers, query parameters, or request bodies
- Add automated tests verifying user tokens are never forwarded

### Granular OAuth scoping

- Define scopes at the **tool and action level** (e.g., `email.send`, `files.read`, `database.query`) — never use blanket scopes like `tools.all`
- Users must explicitly consent to scopes with clear descriptions
- Enforce scope checks on **every tool invocation** as a hard limit regardless of LLM requests

---

## 5. Input/Output Filtering

Deploy a guardrails component between the API gateway and inference engine that inspects traffic in both directions:

```
User/App ↔ API Gateway ↔ Guardrails ↔ Inference Engine ↔ Model
```

### Input direction

| Action | When to use |
|--------|-------------|
| **Block** | Known injection patterns, adversarial inputs |
| **Mask** | PII, credentials, sensitive data before model sees it |
| **Modify** | Rewrite dangerous patterns into safe equivalents |
| **Pass** | Clean input that passes all checks |

### Output direction

| Action | When to use |
|--------|-------------|
| **Block** | Harmful content, policy violations |
| **Mask** | Sensitive training data leakage, internal system details |
| **Modify** | Remove problematic portions while preserving useful content |
| **Pass** | Clean output that passes all checks |

Log all guardrail actions and monitor filter effectiveness. The guardrails component must not be a single point of failure.

---

## 6. Sandboxed Execution

When models generate executable code, API calls, or system commands, validate them in an isolated sandbox before execution.

### Sandbox requirements

- Cannot access production data or services
- Cannot modify the host system
- No external network access unless explicitly required and scoped
- Cannot escalate privileges
- Resource-limited (CPU, memory, time)

### Isolation mechanisms

Use one or more: rootless containers with read-only filesystems, MicroVMs (Firecracker, gVisor), seccomp profiles + Linux namespaces, network isolation (NetworkPolicies), or resource limits (cgroups).

Monitor sandbox health and detect escape attempts. Log all executions.

---

## 7. MCP Server Security

### Authentication

- Authenticate all agent-to-MCP-server connections using SPIFFE/mTLS (preferred) or OAuth client credentials
- Fall back to OAuth user delegation only if SPIFFE infrastructure is unavailable

### Injection prevention

- **Never use `os.system()` or `shell=True`** — always use parameterized APIs

```python
# CORRECT — parameterized, no shell
subprocess.run(["echo", user_input], shell=False)

# FORBIDDEN — shell injection risk
os.system(f"echo {user_input}")
subprocess.run(f"echo {user_input}", shell=True)
```

### Hardening

- Run MCP servers under a dedicated unprivileged user account, never as root
- Drop all unnecessary Linux capabilities
- Apply the principle of least privilege for filesystem, network, and system access
- Drop specific privileges before executing each tool command

### Update integrity

- Sign all server binaries and container images digitally
- Support and document version pinning — enable clients to pin to specific versions and digests

```yaml
mcp_server:
  image: registry.example.com/mcp-server:v1.2.3@sha256:abc123...
```

- Do not auto-update without user consent or verification
- Publish changelogs for every release and support rollback to previous trusted versions

---

## Review Checklist

For any AI system architecture review, verify:

- [ ] All LLM API connections use TLS; credentials are in secret management, not source code
- [ ] Input and output guardrails are deployed; prompt injection defense is layered
- [ ] Human-in-the-loop required for destructive or sensitive actions
- [ ] Agents have their own identity and scoped permissions, separate from users
- [ ] User credentials are never forwarded through agents or MCP servers
- [ ] OAuth scopes are granular (per tool/action), not blanket
- [ ] Model-generated code/commands are validated in a sandbox before execution
- [ ] MCP servers use parameterized APIs, run non-root, and are signed/pinned
- [ ] Audit logs distinguish agent actions from human actions
- [ ] Self-hosted models are scanned for malicious code and verified for integrity

## Relationship to Other Skills

- **[`ai-code-review`](../ai-code-review/SKILL.md)** — Reviewing code *generated by* AI assistants for correctness. This skill covers the *systems* that run AI.
- **[`prompt-injection-mitigation`](https://github.com/RedHatProductSecurity/prodsec-skills/blob/main/module/skills/prompt-injection-mitigation/SKILL.md)** — Deep dive on prompt injection techniques and mitigations. This skill summarizes the key points.
- **[`agent-identity`](https://github.com/RedHatProductSecurity/prodsec-skills/blob/main/module/skills/agent-identity/SKILL.md)** — Full treatment of agent identity management. This skill covers the essentials.
- **[`container-hardening`](https://github.com/RedHatProductSecurity/prodsec-skills/blob/main/module/skills/container-hardening/SKILL.md)** — General container security. This skill adds AI-specific container concerns (model serving, MCP servers).
