# Secure Development skills

105 tool-agnostic secure development skills organized by category, covering **AI/agentic infrastructure security**, **code-level secure configuration**, **security design principles**, and **technology-specific hardening**.

## Usage

Reference any skill by path in your assistant prompt:

```
Using `module/skills/input-output-sanitization/SKILL.md`: review this MCP server for injection risks.
```

Skills follow the AgentSkills layout documented in [ADR-0002](ADRs/0002-agentskills-standards.md): YAML front matter (`name`, `description`, `category`, `subcategory`) plus markdown body in `module/skills/<name>/SKILL.md`. They work with any assistant (Cursor, Claude Code, Copilot, etc.).

Teams copying subsets into another repo can omit skill directories they do not need; use `category` / `subcategory` front matter to filter the catalog.

## Categories

### AI and agentic infrastructure security

| Subcategory | Skills | Focus |
|-------------|--------|-------|
| [`agent`](#agent) | 3 | Agent identity, agent-to-agent auth, agent-to-MCP-server auth (SPIFFE/mTLS) |
| [`api-gateway`](#api-gateway) | 4 | Authentication enforcement, routing, rate limiting, request validation for AI endpoints |
| [`api-keys`](#api-keys) | 1 | Avoiding API keys in production; prefer IdP-issued tokens |
| [`authorization-server`](#authorization-server) | 4 | OAuth 2.1 implementation, dynamic client registration, discovery for MCP |
| [`eval-sandbox`](#eval-sandbox) | 1 | Output validation in isolated sandboxes before use |
| [`external-data-source`](#external-data-source) | 6 | Auth, authz, encryption, logging, network ACLs, Redis/ElastiCache for external data connections |
| [`guardrails`](#guardrails) | 1 | Bidirectional filtering of prompts and model outputs |
| [`inference-engine`](#inference-engine) | 7 | Isolation, JWT enforcement, model scanning/signing, OIDC, token lifecycle |
| [`large-language-model`](#large-language-model) | 3 | File protection, prompt injection mitigation, third-party model security |
| [`mcp-client`](#mcp-client) | 5 | OAuth client metadata, discovery, dynamic registration, scopes, protected resources |
| [`mcp-server`](#mcp-server) | 18 | Hardening (local/remote), OAuth 2.1 resource server, RBAC, input/output sanitization, token handling, containerization, tool injection prevention |
| [`model-registry`](#model-registry) | 5 | Admin security, logging, model scanning/signing, secure storage |
| [`rag-system`](#rag-system) | 1 | Secure storage for RAG/vector/knowledge data |
| [`spiffe-spire`](#spiffe-spire) | 1 | SPIFFE/SPIRE + mTLS for service-to-service authentication |

### Code-level secure configuration and cryptography

| Subcategory | Skills | Focus |
|-------------|--------|-------|
| [`crypto`](#crypto) | 8 | Constant-time analysis, protocol diagramming, zeroization audit, test vectors (Wycheproof), algorithm selection and post-quantum readiness |
| [`secure-config`](#secure-config) | 5 | Insecure defaults, API sharp edges, agentic CI/CD action auditing, Apache Camel security, build YAML misconfiguration (GitLab CI, Tekton, Containerfile) |
| [`supply-chain`](#supply-chain) | 5 | Dependency risk auditing, SBOM/provenance, secure pipelines, software signing, vulnerability management |

### Security design principles

| Subcategory | Skills | Focus |
|-------------|--------|-------|
| [`security-principles`](#security-principles) | 5 | Defense in depth, least privilege and mediation, secure by design (SD3), simplicity and isolation, transparency and usability |

### Technology-specific security

| Subcategory | Skills | Focus |
|-------------|--------|-------|
| [`cloud-infrastructure`](#cloud-infrastructure) | 2 | AWS security baselines (IAM, VPC, CloudTrail, RDS, KMS), general database security |
| [`kubernetes`](#kubernetes) | 6 | Operator RBAC, OpenShift SCCs, Helm chart security, container hardening, health probes, workload resilience |
| [`languages`](#languages) | 3 | Go secure coding, compiler hardening (flags, sanitizers), C/C++ memory and string safety |
| [`messaging`](#messaging) | 2 | Kafka/AMQ Streams (TLS, SASL, ACLs), MQTT (auth, topic ACLs, payload encryption) |
| [`web-security`](#web-security) | 9 | Web application security, HTTP security headers, React XSS prevention, GraphQL hardening, client-side security (XSS/CSRF/CSP), input validation and injection, session management, file upload security, XML and serialization hardening |

---

## Subcategory details

> Filter `module/skills/*/SKILL.md` by `subcategory` front matter to browse programmatically. The tables below list the canonical skill ids per subcategory.

### agent

| Skill | Description |
|-------|-------------|
| [`agent-identity`](../module/skills/agent-identity/SKILL.md) | Establish verifiable identity for AI agents using SPIFFE SVIDs and mTLS |
| [`agent-to-agent-auth`](../module/skills/agent-to-agent-auth/SKILL.md) | Secure agent-to-agent communication with mutual TLS and token-based auth |
| [`agent-to-mcp-server-auth`](../module/skills/agent-to-mcp-server-auth/SKILL.md) | Authenticate AI agents to MCP servers using SPIFFE/mTLS |

### api-gateway

| Skill | Description |
|-------|-------------|
| [`authentication-enforcement`](../module/skills/authentication-enforcement/SKILL.md) | Enforce authentication and authorization at the API gateway for AI systems |
| [`internal-application-routing`](../module/skills/internal-application-routing/SKILL.md) | Route internal application traffic through the API gateway for AI systems |
| [`rate-limiting`](../module/skills/rate-limiting/SKILL.md) | Enforce rate limiting at the API gateway to protect AI models from extraction attacks |
| [`request-validation`](../module/skills/request-validation/SKILL.md) | Enforce request validation and filtering at the API gateway for AI systems |

### api-keys

| Skill | Description |
|-------|-------------|
| [`avoid-api-keys`](../module/skills/avoid-api-keys/SKILL.md) | Avoid long-lived API keys in production; use IdP-issued short-lived tokens instead |

### authorization-server

| Skill | Description |
|-------|-------------|
| [`client-metadata-support`](../module/skills/client-metadata-support/SKILL.md) | Support OAuth Client ID Metadata Documents in authorization servers for MCP ecosystems |
| [`discovery-mechanism`](../module/skills/discovery-mechanism/SKILL.md) | Enforce authorization server metadata discovery for MCP ecosystems |
| [`dynamic-client-registration`](../module/skills/dynamic-client-registration/SKILL.md) | Support OAuth 2.0 Dynamic Client Registration in authorization servers for MCP |
| [`oauth21-implementation`](../module/skills/oauth21-implementation/SKILL.md) | Enforce OAuth 2.1 implementation in authorization servers for MCP ecosystems |

### eval-sandbox

| Skill | Description |
|-------|-------------|
| [`output-validation-sandbox`](../module/skills/output-validation-sandbox/SKILL.md) | Validate model outputs in isolated sandboxes before use in production |

### external-data-source

| Skill | Description |
|-------|-------------|
| [`authentication`](../module/skills/authentication/SKILL.md) | Authenticate connections to external data sources from AI agents |
| [`authorization`](../module/skills/authorization/SKILL.md) | Authorize access to external data sources with least-privilege controls |
| [`encrypted-communication`](../module/skills/encrypted-communication/SKILL.md) | Enforce encrypted communication with external data sources |
| [`logging`](../module/skills/logging/SKILL.md) | Log access to external data sources for audit and anomaly detection |
| [`network-acls`](../module/skills/network-acls/SKILL.md) | Restrict external data source connectivity with network ACLs |
| [`redis-elasticache-security`](../module/skills/redis-elasticache-security/SKILL.md) | Harden Redis/ElastiCache used as external data sources for AI systems |

### guardrails

| Skill | Description |
|-------|-------------|
| [`bidirectional-filtering`](../module/skills/bidirectional-filtering/SKILL.md) | Filter both prompts and model outputs to enforce safety and policy boundaries |

### inference-engine

| Skill | Description |
|-------|-------------|
| [`isolation-sandboxing`](../module/skills/isolation-sandboxing/SKILL.md) | Enforce isolation and sandboxing of inference engine execution |
| [`jwt-token-enforcement`](../module/skills/jwt-token-enforcement/SKILL.md) | Enforce short-lived JWT access token validation for inference engines |
| [`model-security-scanning`](../module/skills/model-security-scanning/SKILL.md) | Scan AI models for malicious elements before loading in inference engines |
| [`model-signature-verification`](../module/skills/model-signature-verification/SKILL.md) | Verify model signatures before loading in inference engines |
| [`oidc-integration`](../module/skills/oidc-integration/SKILL.md) | Enforce OIDC IdP integration for inference engines |
| [`reject-api-keys`](../module/skills/reject-api-keys/SKILL.md) | Reject raw API key authentication in inference engines |
| [`token-lifecycle`](../module/skills/token-lifecycle/SKILL.md) | Enforce token rotation, revocation, and replay prevention for inference engines |

### large-language-model

| Skill | Description |
|-------|-------------|
| [`file-protection`](../module/skills/file-protection/SKILL.md) | Protect LLM model files against unauthorized access and modification |
| [`prompt-injection-mitigation`](../module/skills/prompt-injection-mitigation/SKILL.md) | Mitigate prompt injection risks in LLM-based systems |
| [`third-party-model-security`](../module/skills/third-party-model-security/SKILL.md) | Evaluate security posture when integrating third-party LLMs |

### mcp-client

| Skill | Description |
|-------|-------------|
| [`discovery-mechanisms`](../module/skills/discovery-mechanisms/SKILL.md) | Enforce support for OAuth 2.0 and OIDC discovery mechanisms in MCP clients |
| [`mcp-client-client-metadata-support`](../module/skills/mcp-client-client-metadata-support/SKILL.md) | Implement OAuth client metadata for MCP clients |
| [`mcp-client-dynamic-client-registration`](../module/skills/mcp-client-dynamic-client-registration/SKILL.md) | Support dynamic registration of MCP clients with authorization servers |
| [`mcp-client-protected-resource-metadata`](../module/skills/mcp-client-protected-resource-metadata/SKILL.md) | Discover and enforce protected resource metadata in MCP clients |
| [`oauth-scopes-handling`](../module/skills/oauth-scopes-handling/SKILL.md) | Handle OAuth scopes correctly in MCP clients |

### mcp-server

| Skill | Description |
|-------|-------------|
| [`consent-and-scoping`](../module/skills/consent-and-scoping/SKILL.md) | Implement explicit user consent and minimal tool scoping in MCP servers |
| [`containerization`](../module/skills/containerization/SKILL.md) | Containerize MCP servers with hardened runtime configuration |
| [`external-idp-integration`](../module/skills/external-idp-integration/SKILL.md) | Enforce MCP server integration with external centralized identity providers |
| [`hardening-local`](../module/skills/hardening-local/SKILL.md) | Harden locally-deployed MCP servers |
| [`hardening-remote`](../module/skills/hardening-remote/SKILL.md) | Harden remotely-deployed MCP servers |
| [`input-output-sanitization`](../module/skills/input-output-sanitization/SKILL.md) | Enforce input and output sanitization in MCP server request handling |
| [`logging-and-observability`](../module/skills/logging-and-observability/SKILL.md) | Enforce centralized structured logging and audit trails in MCP servers |
| [`no-credential-forwarding`](../module/skills/no-credential-forwarding/SKILL.md) | Prevent MCP servers from forwarding user credentials or tokens to downstream tools |
| [`oauth21-resource-server`](../module/skills/oauth21-resource-server/SKILL.md) | Enforce MCP servers to act as OAuth 2.1 resource servers by default |
| [`os-tool-security`](../module/skills/os-tool-security/SKILL.md) | Enforce least privilege and sandboxing for MCP server OS tool execution |
| [`protected-resource-metadata`](../module/skills/protected-resource-metadata/SKILL.md) | Enforce OAuth 2.0 Protected Resource Metadata implementation in MCP servers |
| [`rbac`](../module/skills/rbac/SKILL.md) | Implement role-based access control in MCP servers by mapping token claims to roles |
| [`roots-support`](../module/skills/roots-support/SKILL.md) | Enforce roots directive support in MCP servers |
| [`runtime-restrictions`](../module/skills/runtime-restrictions/SKILL.md) | Enforce timeouts and rate limiting in MCP servers to prevent abuse and DoS |
| [`sampling-controls`](../module/skills/sampling-controls/SKILL.md) | Control and restrict MCP server use of sampling |
| [`secure-token-handling`](../module/skills/secure-token-handling/SKILL.md) | Enforce secure token validation and storage in MCP servers |
| [`token-exchange-for-tools`](../module/skills/token-exchange-for-tools/SKILL.md) | Implement OAuth Token Exchange in MCP servers for secure downstream API access |
| [`tool-server-injection-prevention`](../module/skills/tool-server-injection-prevention/SKILL.md) | Prevent tool and server injection attacks (rug-pulls) in MCP servers |

### model-registry

| Skill | Description |
|-------|-------------|
| [`admin-interface-security`](../module/skills/admin-interface-security/SKILL.md) | Secure admin interfaces for model registry systems |
| [`model-registry-logging`](../module/skills/model-registry-logging/SKILL.md) | Audit and monitor access to model registries |
| [`model-registry-model-security-scanning`](../module/skills/model-registry-model-security-scanning/SKILL.md) | Scan model artifacts stored in registries for malicious payloads |
| [`model-registry-model-signature-verification`](../module/skills/model-registry-model-signature-verification/SKILL.md) | Verify model artifact signatures at registry pull time |
| [`model-registry-secure-storage`](../module/skills/model-registry-secure-storage/SKILL.md) | Secure storage configuration for model registry backends |

### rag-system

| Skill | Description |
|-------|-------------|
| [`secure-storage`](../module/skills/secure-storage/SKILL.md) | Secure vector store and knowledge base storage for RAG systems |

### spiffe-spire

| Skill | Description |
|-------|-------------|
| [`service-to-service-mtls`](../module/skills/service-to-service-mtls/SKILL.md) | Implement service-to-service mTLS with SPIFFE/SPIRE SVIDs |

### crypto

| Skill | Description |
|-------|-------------|
| [`algorithm-selection`](../module/skills/algorithm-selection/SKILL.md) | Choose secure cryptographic algorithms and parameters, with post-quantum readiness |
| [`constant-time-analysis`](../module/skills/constant-time-analysis/SKILL.md) | Identify and eliminate timing side-channels in cryptographic code |
| [`constant-time-testing`](../module/skills/constant-time-testing/SKILL.md) | Write tests to detect timing variations in constant-time implementations |
| [`crypto-protocol-diagram`](../module/skills/crypto-protocol-diagram/SKILL.md) | Diagram cryptographic protocols for review and threat modelling |
| [`mermaid-to-proverif`](../module/skills/mermaid-to-proverif/SKILL.md) | Translate Mermaid sequence diagrams of cryptographic protocols into ProVerif models |
| [`vector-forge`](../module/skills/vector-forge/SKILL.md) | Mutation-driven test vector generation for cryptographic implementations |
| [`wycheproof`](../module/skills/wycheproof/SKILL.md) | Run Wycheproof test vectors against cryptographic implementations |
| [`zeroize-audit`](../module/skills/zeroize-audit/SKILL.md) | Audit code for proper zeroization of sensitive cryptographic material |

### secure-config

| Skill | Description |
|-------|-------------|
| [`agentic-actions-auditor`](../module/skills/agentic-actions-auditor/SKILL.md) | Audit CI/CD and agentic workflow action permissions and supply chain risks |
| [`apache-camel-security`](../module/skills/apache-camel-security/SKILL.md) | Harden Apache Camel route configurations and component security |
| [`build-yaml-misconfiguration`](../module/skills/build-yaml-misconfiguration/SKILL.md) | Detect security misconfigurations in GitLab CI, Tekton, and Containerfile definitions |
| [`insecure-defaults`](../module/skills/insecure-defaults/SKILL.md) | Identify and remediate insecure default configurations in libraries and frameworks |
| [`sharp-edges`](../module/skills/sharp-edges/SKILL.md) | Identify dangerous API patterns and sharp edges that lead to security bugs |

### supply-chain

| Skill | Description |
|-------|-------------|
| [`sbom-provenance`](../module/skills/sbom-provenance/SKILL.md) | Generate, validate, and interpret SBOMs and provenance attestations |
| [`secure-pipeline`](../module/skills/secure-pipeline/SKILL.md) | Enforce SAST and SCA in CI/CD pipelines for AI software |
| [`software-signing`](../module/skills/software-signing/SKILL.md) | Sign and verify software artifacts with Sigstore/cosign |
| [`supply-chain-risk-auditor`](../module/skills/supply-chain-risk-auditor/SKILL.md) | Audit dependency risk across the software supply chain |
| [`vulnerability-management`](../module/skills/vulnerability-management/SKILL.md) | Manage known vulnerabilities across dependencies and container images |

### security-principles

| Skill | Description |
|-------|-------------|
| [`defense-in-depth`](../module/skills/defense-in-depth/SKILL.md) | Apply layered security controls to limit blast radius |
| [`least-privilege-and-mediation`](../module/skills/least-privilege-and-mediation/SKILL.md) | Enforce least privilege and complete mediation in access control design |
| [`secure-by-design`](../module/skills/secure-by-design/SKILL.md) | Apply SD3 (Secure by Design, Default, Deployment) principles |
| [`simplicity-and-isolation`](../module/skills/simplicity-and-isolation/SKILL.md) | Reduce attack surface through simplicity and component isolation |
| [`transparency-and-usability`](../module/skills/transparency-and-usability/SKILL.md) | Design security controls that are transparent and usable by default |

### cloud-infrastructure

| Skill | Description |
|-------|-------------|
| [`aws-security`](../module/skills/aws-security/SKILL.md) | AWS security baselines: IAM, VPC, CloudTrail, RDS, and KMS hardening |
| [`database-security`](../module/skills/database-security/SKILL.md) | Secure database configuration and access patterns |

### kubernetes

| Skill | Description |
|-------|-------------|
| [`container-hardening`](../module/skills/container-hardening/SKILL.md) | Harden container images and runtime configuration for Kubernetes |
| [`health-probes`](../module/skills/health-probes/SKILL.md) | Configure Kubernetes health probes, lifecycle hooks, and termination policies |
| [`helm-chart-security`](../module/skills/helm-chart-security/SKILL.md) | Audit and harden Helm chart security configurations |
| [`operator-security`](../module/skills/operator-security/SKILL.md) | Enforce least-privilege RBAC and secure runtime configuration for Kubernetes Operators |
| [`scc-security`](../module/skills/scc-security/SKILL.md) | Review OpenShift Security Context Constraints for correct privilege levels |
| [`workload-resilience`](../module/skills/workload-resilience/SKILL.md) | Configure Kubernetes workload resilience including pod scheduling, scaling, high availability, and disruption budgets |

### languages

| Skill | Description |
|-------|-------------|
| [`compiler-hardening`](../module/skills/compiler-hardening/SKILL.md) | Enable compiler hardening flags and sanitizers for C/C++ builds |
| [`go-security`](../module/skills/go-security/SKILL.md) | Enforce secure coding practices in Go applications |
| [`safe-c-functions`](../module/skills/safe-c-functions/SKILL.md) | Replace unsafe C string and memory functions with safe equivalents |

### messaging

| Skill | Description |
|-------|-------------|
| [`kafka-amq-security`](../module/skills/kafka-amq-security/SKILL.md) | Harden Kafka/AMQ Streams with TLS, SASL, and ACLs |
| [`mqtt-security`](../module/skills/mqtt-security/SKILL.md) | Secure MQTT brokers with authentication, topic ACLs, and payload encryption |

### web-security

| Skill | Description |
|-------|-------------|
| [`client-side-security`](../module/skills/client-side-security/SKILL.md) | Prevent XSS, CSRF, and CSP bypass in client-side web applications |
| [`file-handling-uploads`](../module/skills/file-handling-uploads/SKILL.md) | Secure file upload handling to prevent path traversal and malware |
| [`graphql-security`](../module/skills/graphql-security/SKILL.md) | Secure GraphQL API deployments against introspection leaks, deep query abuse, and authorization bypass |
| [`http-security-headers`](../module/skills/http-security-headers/SKILL.md) | Configure HTTP security headers (CSP, HSTS, X-Frame-Options, etc.) |
| [`input-validation-injection`](../module/skills/input-validation-injection/SKILL.md) | Validate and sanitize input to prevent injection attacks |
| [`react-security`](../module/skills/react-security/SKILL.md) | Enforce XSS prevention and secure rendering in React applications |
| [`session-management-cookies`](../module/skills/session-management-cookies/SKILL.md) | Harden session management and cookie security attributes |
| [`web-application-security`](../module/skills/web-application-security/SKILL.md) | General web application security review and hardening |
| [`xml-serialization-security`](../module/skills/xml-serialization-security/SKILL.md) | Prevent XXE and insecure deserialization in XML and serialization handling |

## Provenance

### AI/agentic infrastructure security skills (63 skills)

- **Source**: Internal security skills repository
- **Upstream commit**: `5d104a5863943aa0ac19b13ca5de7f191d7b7214` (2026-03-03)
- **Format**: Already tool-agnostic markdown; copied with directory names converted to kebab-case

### Code-level secure configuration and cryptography skills (15 skills)

- **Source**: Partly Trail of Bits Skills Marketplace ([trailofbits/skills](https://github.com/trailofbits/skills)), partly original
- **Trail of Bits upstream commit**: `88947f59f1032c1f4d84d6fab244acff6f014728` (2026-04-07)
- **Conversion**: Claude Code plugin format → flat tool-agnostic markdown; `plugin.json`, `hooks/`, and `allowed-tools` dropped; reference docs inlined or pointed to upstream
- **License**: Trail of Bits skills are [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). This adaptation maintains the same license.

### Traditional application security skills (8 skills)

- **Source**: CoSAI [Project CodeGuard](https://github.com/cosai-oasis/project-codeguard) (v1.3.1)
- **License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Conversion**: CodeGuard consolidated rules adapted to individual prodsec-skills format (YAML frontmatter, tool-agnostic markdown). OWASP backing sources used for enrichment. `build-yaml-misconfiguration` is a new skill authored for GitLab CI and Tekton, not a direct CodeGuard import.
- **Skills**: `client-side-security`, `file-handling-uploads`, `input-validation-injection`, `session-management-cookies`, `xml-serialization-security`, `safe-c-functions`, `algorithm-selection`, `build-yaml-misconfiguration` (see `module/skills/<name>/SKILL.md`)
- **Gap analysis**: See `docs/codeguard-gap-analysis.md` for import decisions, skipped items, and items deferred for future skills.

## Contributing

When updating these skills, follow the format conventions in [`AGENTS.md`](../AGENTS.md). For commits touching these files, add `Assisted-by:` or `Generated-by:` when AI-assisted.
