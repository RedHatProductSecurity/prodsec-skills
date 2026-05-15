---
title: "3. CodeRabbit Integration for Automated Security Review"
status: Proposed
relates_to:
  - "*"
topics:
  - code-review
  - automation
  - distribution
  - coderabbit
---

# 3. CodeRabbit Integration for Automated Security Review

Date: 2026-05-13

## Status

Proposed

## Context

prodsec-skills provides 129 curated security skills that AI assistants consume
during development. Currently, skills are consumed at **write time** — an
assistant reads `SKILL.md` files while the developer works. There is no
mechanism for skills to influence **review time** — the automated code review
step that runs on every pull request.

[CodeRabbit](https://coderabbit.ai) is an AI-powered code review tool that
runs on PRs. It supports three integration surfaces relevant to prodsec-skills:

1. **Code guidelines** — CodeRabbit auto-detects `AGENTS.md`, `CLAUDE.md`, and
   custom file patterns as ambient review context. This provides background
   knowledge to the AI reviewer but does not enforce specific requirements.

2. **Path-based instructions** (`reviews.path_instructions`) — per-glob review
   guidance injected into the AI reviewer's prompt for matching files. Supports
   up to 20,000 characters per entry. This is the primary mechanism for
   translating skill checklists into review criteria.

3. **Pre-merge checks** (`pre_merge_checks.custom`) — AI-powered validation
   gates that pass or fail a PR. Up to 20 custom checks per organization
   (Pro+ only). These enforce hard security requirements.

Additionally, CodeRabbit integrates 40+ linters and security scanners
(gitleaks, Semgrep, Trivy, Checkov, Hadolint, OSV Scanner, actionlint,
ast-grep) that complement the AI review with deterministic analysis.

**The problem:** Skills are written as detailed, multi-page markdown documents.
CodeRabbit's path instructions are condensed prompts bound to file globs. A
translation layer is needed to map skill content into CodeRabbit's
configuration primitives without losing critical security guidance.

**Coverage tiers:** Not all 129 skills map to code review. Analysis shows
three tiers:

| Tier | Description | Skills | Strategy |
|------|-------------|--------|----------|
| Direct | Checklist items reviewable in diffs | ~60 | `path_instructions` + `pre_merge_checks` |
| Contextual | Background knowledge for the reviewer | ~40 | `code_guidelines` auto-detection |
| Out of scope | Requires runtime or tooling | ~29 | External CI tools (fuzzing, SAST orchestration) |

## Options

### Option 1: Hand-maintained `.coderabbit.yaml` in this repository

Ship a single `.coderabbit.yaml` at the repository root that condenses the
~60 direct-fit skills into path instructions grouped by subcategory, enables
security scanners, and defines pre-merge checks for the highest-severity
concerns.

**Mapping approach:** Each `path_instructions` entry maps one or more skill
subcategories to file globs. The instruction text is a manually condensed
summary of the checklist items from the constituent skills.

```
prodsec-skills subcategory → file glob → condensed checklist
```

**Example mapping (18 MCP server skills → 1 path instruction):**

```yaml
- path: "**/{mcp,tool_server,toolserver}/**/*"
  instructions: |
    MCP server review (prodsec-skills):
    - OAuth 2.1 resource server: validate tokens per RFC 9068
    - Enforce scope-based access per tool; no default-allow
    - RBAC: per-tool permissions mapped to token scopes/roles
    - Sanitize all tool inputs against declared schemas
    - Reject path traversal in file-accessing tools
    ...
```

**Pre-merge checks (6 hard gates):**

| Check | Mode | Skills covered |
|-------|------|----------------|
| `no-hardcoded-secrets` | error | Red Hat AI policy (guideline 3) |
| `no-weak-crypto` | error | algorithm-selection, constant-time-analysis |
| `no-injection-vectors` | error | input-validation-injection |
| `container-privileges` | error | container-hardening, scc-security |
| `no-sensitive-data-in-logs` | error | logging, Red Hat AI policy |
| `ai-attribution` | warning | Red Hat AI policy (guideline 6) |

**Scanners enabled:** gitleaks, Semgrep, Checkov, Hadolint, Trivy, OSV
Scanner, actionlint, ast-grep (with essential rules).

**Trade-offs:**

- (+) Immediately usable — adopters copy the file into their repo
- (+) Human-curated condensation preserves the most critical guidance
- (+) Easy to review and modify per-project
- (-) Manual maintenance: skill updates do not propagate automatically
- (-) Condensation loses nuance from the full skill documents
- (-) 20-check limit on pre-merge checks forces prioritization

### Option 2: Generated `.coderabbit.yaml` via a build pipeline

Add a script that parses `SKILL.md` frontmatter and checklist items, maps
subcategories to file globs via a lookup table, condenses content to fit
CodeRabbit's limits, and emits a `.coderabbit.yaml`.

```
module/skills/*/SKILL.md
        │
        ▼
  parse frontmatter + checklists
        │
        ▼
  subcategory → glob lookup table
        │
        ▼
  condense to ≤20k chars per glob
        │
        ▼
  validate against schema v2
        │
        ▼
  .coderabbit.yaml
```

**Trade-offs:**

- (+) Skill updates propagate to the config automatically
- (+) Scalable across many repos consuming prodsec-skills
- (+) Consistent condensation rules applied uniformly
- (-) Condensation by script may miss nuance that human curation catches
- (-) Additional tooling to maintain (parser, glob lookup table, tests)
- (-) Generated output needs human review before shipping
- (-) LLM-based condensation adds non-determinism; template-based
      condensation loses context

### Option 3: CodeRabbit code guidelines only (no path instructions)

Rely solely on CodeRabbit's auto-detection of `AGENTS.md` and add
`filePatterns` pointing at skill files. The AI reviewer receives the full
skill content as ambient context.

```yaml
knowledge_base:
  code_guidelines:
    filePatterns:
      - "prodsec-skills/module/skills/*/SKILL.md"
```

**Trade-offs:**

- (+) Zero condensation effort — skills consumed as-is
- (+) Full nuance preserved
- (-) No file-pattern targeting — all skills loaded for all files
- (-) Context window limits may cause the reviewer to ignore or
      deprioritize security guidance
- (-) No hard gates — code guidelines are advisory only
- (-) No deterministic scanner integration

## Decision

Adopt **Option 1** (hand-maintained `.coderabbit.yaml`) as the initial
integration, with a path toward Option 2 if adoption scales beyond 5
repositories.

The config file lives at the repository root (`.coderabbit.yaml`). Adopters
copy it into their own repositories and customize the globs and pre-merge
check modes for their codebase. The prodsec-skills repo itself serves as both
the canonical source and a reference implementation.

The config organizes path instructions into 20 blocks covering all direct-fit
skill subcategories:

| Block | Globs | Skills condensed |
|-------|-------|-----------------|
| Injection & input validation | `**/*.{py,js,ts,go,rs,java,rb,php,kt,swift,cs}` | input-validation-injection, web-application-security |
| Web & frontend | `**/*.{html,jsx,tsx,vue,svelte}` | react-security, client-side-security, http-security-headers, graphql-security, session-management-cookies, file-handling-uploads, xml-serialization-security |
| Cryptography | `**/*{crypt,cipher,sign,hash,tls,ssl,cert,key,token}*` | algorithm-selection, constant-time-analysis, zeroize-audit, wycheproof, crypto-protocol-diagram, constant-time-testing |
| Container hardening | `**/{Dockerfile,Containerfile}*` | container-hardening, isolation-sandboxing |
| Kubernetes & OpenShift | `**/*.{yaml,yml}` | scc-security, operator-security, helm-chart-security, container-hardening, health-probes |
| MCP server | `**/{mcp,tool_server,toolserver}/**/*` | 16 mcp-server skills |
| MCP client | `**/{mcp_client,mcp-client}/**/*` | 5 mcp-client skills |
| Inference engine | `**/{inference,model,serving,predict}/**/*` | isolation-sandboxing, jwt-token-enforcement, model-security-scanning, model-signature-verification, oidc-integration, token-lifecycle |
| Agent security | `**/{agent,agents,agentic}/**/*` | agent-identity, agent-to-agent-auth, agent-to-mcp-server-auth |
| LLM interaction | `**/{llm,prompt,chat,completion}**/*` | prompt-injection-mitigation, file-protection, third-party-model-security, bidirectional-filtering, output-validation-sandbox |
| Supply chain | dependency manifests | supply-chain-risk-auditor, sbom-provenance, software-signing, secure-pipeline, vulnerability-management |
| CI/CD | `.github/workflows/**/*` | secure-pipeline, build-yaml-misconfiguration, agentic-actions-auditor |
| Auth & OAuth | `**/{auth,oauth,oidc,login,session,saml}/**/*` | oauth21-implementation, authentication, authorization, session-management-cookies, avoid-api-keys, service-to-service-mtls |
| API gateway | `**/{gateway,proxy,ingress,route}/**/*` | authentication-enforcement, internal-application-routing, rate-limiting, request-validation |
| Go | `**/*.go` | go-security |
| C/C++ | `**/*.{c,cpp,cc,h,hpp}` | safe-c-functions, compiler-hardening |
| Database & external data | `**/{db,database,redis,cache,storage}/**/*` | database-security, authentication, encrypted-communication, redis-elasticache-security |
| Messaging | `**/{kafka,amq,mqtt,messaging,broker}/**/*` | kafka-amq-security, mqtt-security |
| Model registry | `**/{model_registry,model-registry,registry}/**/*` | model-registry-*, admin-interface-security |

**Skills not covered by this config (out-of-scope tier):**

- Fuzzing skills (12): require execution environments, not code review
- SAST orchestration (semgrep, codeql, sarif-parsing): CodeRabbit's built-in
  Semgrep covers basic cases; full orchestration requires CI
- Audit workflows (4): multi-step investigation; human-driven with skills as
  checklists
- Developer tooling (4): not security review concerns
- Security principles (5): ambient knowledge, covered by code guidelines
  auto-detection of `AGENTS.md`

**Red Hat-specific concerns addressed:**

- AI attribution enforcement via `ai-attribution` pre-merge check
- Sensitive data prevention via `no-hardcoded-secrets` and
  `no-sensitive-data-in-logs` checks
- UBI base image preference in container hardening instructions
- OpenShift SCC validation in Kubernetes instructions

**Maintenance commitment:** Review and update the config whenever skills are
added, removed, or materially changed. Track drift by comparing the skill
count in `docs/skills-index.md` against the block annotations in the config.

## Consequences

- Repositories that adopt this config get automated security review informed
  by prodsec-skills on every PR, closing the gap between write-time and
  review-time security guidance.

- The 20,000-character limit per path instruction forces aggressive
  condensation. Subcategories with many skills (MCP server: 18) lose the
  most nuance. Reviewers flagged by a condensed rule should consult the full
  `SKILL.md` for detailed guidance.

- Pre-merge checks are limited to 20 per organization and require Pro+.
  Organizations on free/Pro plans get path instructions and scanner
  integration but not hard gates.

- CodeRabbit's AI reviewer is non-deterministic. Path instructions are
  guidance, not rules — false positives and false negatives will occur.
  Teams should start pre-merge checks in `warning` mode and promote to
  `error` after tuning (2–4 weeks recommended).

- The hand-maintained config will drift from skills over time. If adoption
  exceeds 5 repositories, investing in the generation pipeline (Option 2)
  becomes worthwhile to reduce maintenance burden.

- Enabling 8 security scanners adds review latency. Teams with strict cycle
  time requirements may need to disable some scanners or limit them to
  security-sensitive paths.

- The `.coderabbit.yaml` in this repo serves as a reference implementation.
  Adopters are expected to customize globs for their project structure —
  the default globs use common conventions but will not match every
  codebase.
