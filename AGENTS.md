# AGENTS.md — Context for AI assistants

This is the canonical context file for agents working in this repository. Read it before making any changes.

## What this repo is

`prodsec-skills` is a security skills library. It contains security skills — structured guidance documents — that AI coding assistants (Claude Code, Cursor, Copilot, etc.) and agentic systems consume directly to apply security expertise during development.

**Goal**: Shift security left. Instead of catching issues in review, skills embed security recommendations into AI assistants so they apply guidance as code is written, tested, and audited.

**Consumers**: Any agent or agentic system. Skills are tool-agnostic markdown; any assistant that can read files can use them.

## Repository layout

| Path | Purpose |
|------|---------|
| `skills/` | Production-ready, curated skills |
| `skills/secure_development/` | 103 skills — AI/agentic infra security, cryptography, secure config, supply chain, security principles, technology-specific hardening (web, Kubernetes, messaging, cloud, languages) |
| `skills/security_testing/` | 17 skills — fuzzing (AFL++, libFuzzer, cargo-fuzz, LibAFL, Atheris, ruzzy) and static analysis (Semgrep, CodeQL, SARIF) |
| `skills/security_auditing/` | 4 skills — audit workflows: context building, differential review, false-positive checking, variant analysis |
| `skills/developer_tooling/` | 4 skills — devcontainers, git cleanup, modern Python, property-based testing |
| `experimental/` | Work-in-progress skills; contributions welcome |
| `docs/` | Design notes, getting-started guides |

## Skill format

Every skill is a markdown file with YAML front matter:

```markdown
---
name: skill-name
description: One-line description used by assistants to decide when to invoke.
---

Skill body...
```

The `description` field is critical — it determines when agents invoke the skill. Write it as a precise trigger condition, not a vague summary.

## How to reference a skill

Reference skills by path in a prompt:

```
Using `skills/secure_development/mcp-server/input-output-sanitization.md`: review this MCP server for injection risks.
```

## Conventions

- **Skill files**: Tool-agnostic markdown only. No tool-specific config (`plugin.json`, `allowed-tools`, hooks). Reference docs inline or link upstream.
- **Directory names**: kebab-case.
- **Commits**: Use conventional commits.
- **Secrets**: Never commit real credentials. Use synthetic values in docs and examples.
- **Provenance**: When pulling in skills from upstream sources (Trail of Bits, internal repos), record the source commit and license in the relevant `skills/<category>/README.md`.

## Adding or updating skills

1. Place the skill under the appropriate `skills/<category>/<subcategory>/` path.
2. Write a precise `description` front matter field.
3. Keep skills tool-agnostic — no Claude-specific, Cursor-specific, or Copilot-specific syntax.
4. If copying from an upstream source, note the source commit and license in the relevant `README.md`.
5. Trail of Bits skills are CC BY-SA 4.0 — adapted skills must carry the same license.
6. Unfinished or unreviewed skills go in `experimental/`, not `skills/`.
7. **Update all four indexes in the same commit as the skill file** — stale counts cause confusion for both humans and agents:

 | File | What to update |
 |------|----------------|
 | `skills/<category>/README.md` | Add the skill to its subcategory table; increment the subcategory skill count |
 | `skills/README.md` | Increment the category count and the total count in the header; update the subcategory row if listed |
 | `README.md` | Increment the category count and the "N skills across four categories" total |
 | `AGENTS.md` | Increment the `skills/<category>/` count in the Repository layout table |

## Things agents often get wrong here

- **Making skills tool-specific**: Skills must remain tool-agnostic. Do not add tool-specific directives, config keys, or syntax.
- **Omitting the `description` field**: Without it, assistants cannot auto-discover the skill. Always include it.
- **Committing directly to `skills/`**: Unfinished or unreviewed work goes in `experimental/` first.
- **Dropping provenance**: When adapting upstream skills, preserve the source commit and license in the category `README.md`.
- **Editing skill content without reading it first**: Always read the current file before making changes.

## Key files

- Glossary: [docs/glossary.md](docs/glossary.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Secure development skill index: [skills/secure_development/README.md](skills/secure_development/README.md)
- constitution: [docs/normative/constitution.md](docs/normative/constitution.md)
