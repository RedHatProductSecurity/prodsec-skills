# AGENTS.md — Context for AI assistants

This is the canonical context file for agents working **in this repository** (contributors, hygiene, CI). Read it before making any changes.

If you are consuming skills as an **installable module** (for example via Lola), read **[`module/AGENTS.md`](module/AGENTS.md)** first — it is the AI Main Spec for packaged skills.

## What this repo is

`prodsec-skills` is a security skills library. It contains security skills — structured guidance documents — that AI coding assistants (Claude Code, Cursor, Copilot, etc.) and agentic systems consume directly to apply security expertise during development.

**Goal**: Shift security left. Instead of catching issues in review, skills embed security recommendations into AI assistants so they apply guidance as code is written, tested, and audited.

**Consumers**: Any agent or agentic system. Skills are tool-agnostic markdown; any assistant that can read files can use them.

## Repository layout

| Path | Purpose |
|------|---------|
| `module/` | **AI Context Module** — packaged skills for assistants (`AGENTS.md`, `skills/<id>/SKILL.md`, `mcps.json`). See [ADR-0002](docs/ADRs/0002-agentskills-standards.md). |
| `module/skills/` | 128 production skills — flat directories, each with `SKILL.md` and optional `reference/` |
| `experimental/` | Work-in-progress skills; contributions welcome |
| `docs/` | Design notes, skill indexes, ADRs |
| `scripts/` | Validation and utilities (outside the module boundary) |

Skills are grouped logically by `category` and `subcategory` fields in each `SKILL.md`. Counts by category: **103** secure development, **17** security testing, **4** security auditing, **4** developer tooling — see [`docs/skills-index.md`](docs/skills-index.md).

## Skill format

Every skill primary file is `module/skills/<skill-id>/SKILL.md` with YAML front matter:

```markdown
---
name: skill-id
description: One-line description used by assistants to decide when to invoke.
category: secure_development
subcategory: mcp-server
---

Skill body...
```

The `description` field is critical — it determines when agents invoke the skill. Write it as a precise trigger condition, not a vague summary.

## How to reference a skill

Reference skills by path in a prompt:

```
Using `module/skills/input-output-sanitization/SKILL.md`: review this MCP server for injection risks.
```

## Conventions

- **Skill files**: Tool-agnostic markdown only. No tool-specific config (`plugin.json`, `allowed-tools`, hooks). Reference docs inline, under `reference/`, or link upstream.
- **Skill ids and directory names**: kebab-case; must match `name` in front matter.
- **Commits**: Use conventional commits.
- **Secrets**: Never commit real credentials. Use synthetic values in docs and examples.
- **Provenance**: When pulling in skills from upstream sources (Trail of Bits, internal repos), record the source commit and license in the relevant category doc under `docs/` (see [`docs/secure-development-skills.md`](docs/secure-development-skills.md)).

## Adding or updating skills

1. Add or edit `module/skills/<skill-id>/SKILL.md` (and optional `reference/`). Use unique `<skill-id>`; resolve collisions with the `<subcategory>-<name>` pattern described in [ADR-0002](docs/ADRs/0002-agentskills-standards.md).
2. Set `category`, `subcategory`, `name`, and `description` in front matter (`name` must equal the directory name).
3. Keep skills tool-agnostic — no Claude-specific, Cursor-specific, or Copilot-specific syntax.
4. If copying from an upstream source, note the source commit and license in the appropriate `docs/*-skills.md` provenance section.
5. Trail of Bits skills are CC BY-SA 4.0 — adapted skills must carry the same license.
6. Unfinished or unreviewed skills go in `experimental/`, not `module/skills/`.
7. **Update indexes in the same commit** — stale counts cause confusion for both humans and agents:

 | File | What to update |
 |------|----------------|
 | [`docs/skills-index.md`](docs/skills-index.md) | Add or adjust rows; fix category totals |
 | [`docs/secure-development-skills.md`](docs/secure-development-skills.md) (or sibling category doc) | Subcategory counts and provenance where applicable |
 | [`README.md`](README.md) | Category totals and examples |
 | [`module/AGENTS.md`](module/AGENTS.md) | Skill count or collision table if relevant |

## Things agents often get wrong here

- **Making skills tool-specific**: Skills must remain tool-agnostic. Do not add tool-specific directives, config keys, or syntax.
- **Omitting the `description` field**: Without it, assistants cannot auto-discover the skill. Always include it.
- **Mismatching `name` and directory**: `name` in front matter must equal `module/skills/<name>/`.
- **Committing directly to `module/skills/`**: Unfinished or unreviewed work goes in `experimental/` first.
- **Dropping provenance**: When adapting upstream skills, preserve the source commit and license in the docs.
- **Editing skill content without reading it first**: Always read the current file before making changes.

## Key files

- Glossary: [docs/glossary.md](docs/glossary.md)
- Skills catalog: [docs/skills-index.md](docs/skills-index.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Secure development guide: [docs/secure-development-skills.md](docs/secure-development-skills.md)
- constitution: [docs/normative/constitution.md](docs/normative/constitution.md)
