# GE Core Skills — Curated Security Skills for Global Engineering

**12 skills** curated for Red Hat developers writing code daily, distilled from the 130-skill [prodsec-skills](https://github.com/RedHatProductSecurity/prodsec-skills) library. They live in the top-level [`ge-core/`](../ge-core/) directory as standalone, self-contained skills.

## Selection Criteria

- Applicable to **all** Red Hat developers, not just security specialists
- Covers the threats developers encounter every day: injection, secrets, container misconfig, access control
- Aligned with Red Hat's technology stack: containers, OpenShift, Kubernetes, enterprise auth
- Prioritizes actionable guidance over theoretical background

## Usage

Reference any skill by path in your assistant prompt:

```
Using `ge-core/input-validation-injection/SKILL.md`: review this handler for injection risks.
```

Each skill is a single `SKILL.md` conforming to the [Agent Skills](https://agentskills.io/specification) standard: `name` and `description` frontmatter (with `category`/`subcategory` under `metadata`) followed by the markdown body. They work with any assistant that can read files (Claude Code, Cursor, Copilot, and others).

## Skills

### Injection and Web Security

| Skill | What it covers |
|-------|----------------|
| [`input-validation-injection`](../ge-core/input-validation-injection/SKILL.md) | SQL, LDAP, and OS command injection, prototype pollution, and general validation strategy. Allow-list validation at trust boundaries, parameterized queries, safe APIs. Adapted from CoSAI Project CodeGuard (CC BY 4.0). |
| [`web-application-security`](../ge-core/web-application-security/SKILL.md) | OWASP-aligned server-side controls: CORS whitelisting, CSRF tokens, session management, MFA, anti-enumeration, centralized access control. Everything enforced server-side. |

### Secrets

| Skill | What it covers |
|-------|----------------|
| [`secrets-detection-patterns`](../ge-core/secrets-detection-patterns/SKILL.md) | Detect hardcoded API keys, tokens, passwords, private keys, and connection strings using pattern-based scanning with false-positive filtering. Zero-tolerance verdict model; self-contained, no external tools required. |

### Container Security

| Skill | What it covers |
|-------|----------------|
| [`container-hardening`](../ge-core/container-hardening/SKILL.md) | UBI base images, non-root execution, security contexts, minimal installs, image scanning. Red Hat container best practices for Containerfiles, compose files, and pod security settings. |

### OpenShift / Kubernetes Security

| Skill | What it covers |
|-------|----------------|
| [`scc-security`](../ge-core/scc-security/SKILL.md) | OpenShift Security Context Constraints: controlling privileged execution, Linux capabilities, host resource access, SELinux contexts. |
| [`pod-access-control`](../ge-core/pod-access-control/SKILL.md) | Kubernetes RBAC bindings, dedicated service accounts, namespace isolation, resource quotas, service exposure. Least-privilege workloads that resist lateral movement. |

### Supply Chain Security

| Skill | What it covers |
|-------|----------------|
| [`dependency-vulnerability-audit`](../ge-core/dependency-vulnerability-audit/SKILL.md) | CVE scanning via real CLI scanners per ecosystem (npm, pip, Go, Cargo, Maven, Ruby), plus license compliance and supply chain risk. Honest INCOMPLETE verdict when no scanner is available. |

### Authentication

| Skill | What it covers |
|-------|----------------|
| [`authentication`](../ge-core/authentication/SKILL.md) | Standard authentication for external data source connections: OAuth 2.1/OIDC, SPIFFE/SPIRE mTLS, SAML, Kerberos, client certificates. Rejects shared credentials and keys embedded in connection strings. |

### Foundational Principles

| Skill | What it covers |
|-------|----------------|
| [`secure-by-design`](../ge-core/secure-by-design/SKILL.md) | Secure by Design, by Default, and in Deployment (SD3): ship secure defaults, fail closed, generate unique secrets at install time, least-privilege configuration. |
| [`logging`](../ge-core/logging/SKILL.md) | Audit logging for access to sensitive external data sources: who accessed what and when, access denials, no secrets or PII in logs, SIEM/external logging integration. |

### AI Security

| Skill | What it covers |
|-------|----------------|
| [`ai-code-review`](../ge-core/ai-code-review/SKILL.md) | Review AI-generated code for its characteristic failure modes: hallucinated APIs, plausible-but-wrong logic, pattern drift, incomplete error handling, stale dependencies, abandoned scaffolding. |
| [`ai-systems-security`](../ge-core/ai-systems-security/SKILL.md) | Secure products that serve, integrate, or operate LLMs and agents: prompt injection defense, agent identity, credential hygiene, I/O filtering, sandboxed execution, MCP server security. |
