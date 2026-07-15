# GE Core Skills

12 curated security skills for developers writing code daily, selected from
the [prodsec-skills](https://github.com/RedHatProductSecurity/prodsec-skills)
library. Each skill is a standalone directory with a `SKILL.md` following the
[agentskills.io specification](https://agentskills.io/specification).

See [docs/ge-core.md](../docs/ge-core.md) for the full index with per-skill
summaries and selection criteria.

## Skills

| Skill | Covers |
|-------|--------|
| [`ai-code-review`](ai-code-review/SKILL.md) | Security review of AI-generated code |
| [`ai-systems-security`](ai-systems-security/SKILL.md) | Securing LLM integrations, agents, and MCP servers |
| [`authentication`](authentication/SKILL.md) | Standard authentication for external data source connections |
| [`container-hardening`](container-hardening/SKILL.md) | Container image and runtime hardening |
| [`dependency-vulnerability-audit`](dependency-vulnerability-audit/SKILL.md) | CVE, license, and supply chain auditing of dependencies |
| [`input-validation-injection`](input-validation-injection/SKILL.md) | Injection defense and input validation strategy |
| [`logging`](logging/SKILL.md) | Audit logging for sensitive external data access |
| [`pod-access-control`](pod-access-control/SKILL.md) | Kubernetes RBAC, service accounts, and namespace isolation |
| [`scc-security`](scc-security/SKILL.md) | OpenShift Security Context Constraints |
| [`secrets-detection-patterns`](secrets-detection-patterns/SKILL.md) | Pattern-based detection of hardcoded secrets |
| [`secure-by-design`](secure-by-design/SKILL.md) | Secure defaults and SD3 principles |
| [`web-application-security`](web-application-security/SKILL.md) | OWASP-aligned server-side web controls |

## Usage

Reference a skill by path in your assistant prompt:

```
Using `ge-core/input-validation-injection/SKILL.md`: review this handler for injection risks.
```

Or install as a Claude Code plugin from this repository's marketplace:

```
/plugin install prodsec-skills-ge-core@prodsec-skills
```
