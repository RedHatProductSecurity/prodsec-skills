# prodsec-skills — AI Context Module (Main Spec)

This file is the **module-level** context for assistants consuming this repository as an [AI Context Module](https://lobstertrap.org/lola/concepts/skills-and-modules/#ai-context-module). It complements the repository root [`AGENTS.md`](../AGENTS.md), which describes **contributor** workflow (linting, commits, indexes).

## Purpose

This project maintains **128** curated, **tool-agnostic** security skills. Each skill is a directory under `module/skills/<skill-id>/` containing:

- **`SKILL.md`** — primary guidance (`name`, `description`, `category`, `subcategory` in YAML front matter, then markdown body).
- **`reference/`** (optional) — supporting procedures and templates loaded on demand.

Skills align with the [AgentSkills.io specification](https://agentskills.io/specification). Packaging layout is defined in **[ADR-0002](../docs/ADRs/0002-agentskills-standards.md)**.

## Principles (from the project constitution)

- **Tool-agnostic.** Do not assume Claude-only, Cursor-only, or vendor-specific syntax inside skills.
- **Specificity wins.** When two skills conflict, prefer the narrower context; otherwise choose the more security-conservative guidance (see [`docs/normative/constitution.md`](../docs/normative/constitution.md)).
- **Risk-proportionate alerting.** Use each skill's guidance with severity appropriate to impact.

## How assistants should use this module

1. **Choose a skill by trigger.** Read `description` in `SKILL.md` — it is written as an invocation condition, not a tag line.
2. **Load only what you need.** Prefer the single `SKILL.md` for a task; open files under `reference/` when the workflow says to.
3. **Resolve paths.** Treat `{SKILL_DIR}` as the directory containing the active `SKILL.md` (see skills that define this variable, e.g. `verify-secure-signing`).

## Inventory and browsing

- **By category:** Filter `module/skills/*/SKILL.md` by `category` and `subcategory` front matter (former directory paths are now metadata).
- **Human-maintained tables:** [`docs/skills-index.md`](../docs/skills-index.md) and the category guides:
  - [`docs/secure-development-skills.md`](../docs/secure-development-skills.md)
  - [`docs/security-testing-skills.md`](../docs/security-testing-skills.md)
  - [`docs/security-auditing-skills.md`](../docs/security-auditing-skills.md)
  - [`docs/developer-tooling-skills.md`](../docs/developer-tooling-skills.md)

## Example prompts (path-based)

```
Using `module/skills/input-output-sanitization/SKILL.md`: review this MCP server for injection risks.
```

```
Using `module/skills/cargo-fuzz/SKILL.md`: write a fuzzing harness for this parser.
```

```
Using `module/skills/differential-review/SKILL.md`: review the security impact of this diff.
```

## Collision-renamed skills (flat layout)

Seven historical filename collisions were disambiguated with a `<subcategory>-<name>` skill id (see ADR-0002):

| Skill id | Notes |
|----------|--------|
| `mcp-client-client-metadata-support` | MCP client OAuth client metadata |
| `mcp-client-dynamic-client-registration` | MCP client dynamic registration |
| `mcp-client-protected-resource-metadata` | MCP client protected resource metadata |
| `model-registry-logging` | Model registry logging (vs external-data-source `logging`) |
| `model-registry-model-security-scanning` | Registry scanning (vs inference-engine `model-security-scanning`) |
| `model-registry-model-signature-verification` | Registry signing (vs inference-engine `model-signature-verification`) |
| `model-registry-secure-storage` | Registry storage (vs `rag-system` `secure-storage`) |

## MCP integration

`mcps.json` in this directory reserves MCP server configuration for future use (`{"mcpServers": {}}`). Repository automation and optional scripts remain outside `module/` under `scripts/`.

## Experimental content

Work-in-progress skills may appear under `experimental/` at the repository root (not part of this packaged module until promoted).
