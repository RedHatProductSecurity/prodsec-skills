# Glossary

Shared vocabulary for the `prodsec-skills` project — security terms and concepts referenced across skills and docs.

---

## C

### CVE (Common Vulnerabilities and Exposures)

A unique identifier for a publicly disclosed vulnerability. Format: `CVE-YYYY-NNNNN`. The NVD maintains the reference database; vendors publish their own severity ratings independently.

### CVSS (Common Vulnerability Scoring System)

A standardized framework for rating vulnerability severity (0.0–10.0). Organizations may use CVSS v3.1 as the baseline and adjust ratings based on product-specific context (e.g., a vulnerability is less severe when a mitigating control is in place by default).

### CWE (Common Weakness Enumeration)

A taxonomy of software weaknesses (e.g., CWE-79: Cross-site Scripting, CWE-787: Out-of-bounds Write). Used to categorize the root cause of a vulnerability, distinct from the CVE identifier that names a specific instance.

## E

### Embargo

A time-limited agreement to keep vulnerability details non-public while a fix is developed and coordinated. Embargoed vulnerabilities are shared under NDA with affected vendors and downstream distributors before public disclosure.

### Errata

See [RHSA](#rhsa-red-hat-security-advisory).

## H

### Harness

The configuration and context layer that prepares an AI agent for a specific task. In the context of this repo, skills are assembled by the harness alongside system prompts and tool definitions to create a specialized agent. The harness is what transforms a generic LLM into an agent with a specific security role.

## M

### MCP (Model Context Protocol)

An open protocol for exposing tools to AI agents. MCP servers act as controlled access points — they receive tool calls from the agent and mediate access to external systems. Several skills in this repo address hardening MCP servers and clients (filter `module/skills` by `subcategory` `mcp-server` or `mcp-client`; see the [Skills index](skills-index.md)).

## P

### Provenance

The origin and chain of custody of a skill. When adapting skills from external sources (Trail of Bits, internal repositories), the source project, commit hash, and license must be recorded in the category `README.md`. Provenance enables auditing and license compliance.

### PSIRT (Product Security Incident Response Team)

A team responsible for receiving, triaging, coordinating, and disclosing vulnerabilities in a vendor's products. A PSIRT manages the full lifecycle from initial report through embargo coordination, fix development, and public advisory publication.

## S

### SBOM (Software Bill of Materials)

A structured inventory of all components in a software artifact — dependencies, transitive deps, versions, and licenses. SBOMs support vulnerability impact analysis and license compliance. Skills: [`sbom-provenance`](../module/skills/sbom-provenance/SKILL.md).

### Skill

A markdown file with YAML front matter that gives an AI agent scoped, actionable guidance for a specific security task. Skills in this repo are tool-agnostic — they work with Claude Code, Cursor, Copilot, or any assistant that can read files. The `description` field in the front matter is what agents use to determine when to invoke the skill.

### SPIFFE/SPIRE

**SPIFFE** (Secure Production Identity Framework for Everyone) is an open standard for workload identity. **SPIRE** is its reference implementation. Together they issue short-lived X.509 SVIDs (SPIFFE Verifiable Identity Documents) to workloads, enabling mTLS without long-lived credentials. Skills: [`service-to-service-mtls`](../module/skills/service-to-service-mtls/SKILL.md).

## T

### Tool-agnostic

A design property of skills in this repo. A tool-agnostic skill contains no syntax, directives, or configuration specific to any particular AI assistant (no Claude-specific blocks, no Cursor rules, no Copilot extensions). This ensures skills work across all tooling.

## Z

### Zero Trust

A security model in which no actor — user, service, or agent — is implicitly trusted based on network location or identity alone. Every request is authenticated and authorized against explicit policy. Relevant to agent security: agents must not trust inputs (prompts, tool results, issue bodies) because any could carry prompt injection or adversarial content.
