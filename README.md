# Security Skills

Security skills for AI coding assistants and agentic systems. Skills encode security recommendations, guidelines, and best practices as structured markdown files that AI assistants (Claude Code, Cursor, Copilot, and others) consume directly while writing, testing, and auditing code.

The goal is to shift security left: apply security guidance during development, not after review.

## Get started

```bash
make bootstrap
```

Installs ruff, ty, pre-commit, and wires up git hooks so linting and ADR validation run automatically before each commit. Requires [`uv`](https://docs.astral.sh/uv/) on your PATH.

## Using a skill

Reference any skill by path in your assistant prompt:

```
Using `module/skills/input-output-sanitization/SKILL.md`: review this MCP server for injection risks.
```

```
Using `module/skills/cargo-fuzz/SKILL.md`: write a fuzzing harness for this parser.
```

```
Using `module/skills/differential-review/SKILL.md`: review the security impact of this diff.
```

Skills are tool-agnostic — the same files work in any assistant that can read them.

## Install via Lola

Install all skills to your AI assistant in one command using [Lola](https://github.com/LobsterTrap/lola):

```bash
lola mod add https://github.com/RedHatProductSecurity/prodsec-skills.git
lola install prodsec-skills --assistant claude-code
```

## Skill catalog

**128** skills across four categories. See [`docs/skills-index.md`](docs/skills-index.md) for the full index.

| Category | Skills | Purpose |
|----------|--------|---------|
| [`secure_development`](docs/secure-development-skills.md) | 103 | Building secure software — AI/agentic infrastructure, cryptography, supply chain, security principles, technology-specific hardening |
| [`security_testing`](docs/security-testing-skills.md) | 17 | Finding vulnerabilities — fuzzing and static analysis |
| [`security_auditing`](docs/security-auditing-skills.md) | 4 | Security review workflows |
| [`developer_tooling`](docs/developer-tooling-skills.md) | 4 | General-purpose development tooling |

## Repository layout

```
module/                  # AI Context Module (packaged for assistants / Lola)
  AGENTS.md              # AI Main Spec for the module
  mcps.json              # MCP server slot (reserved)
  skills/<skill-id>/     # One directory per skill
    SKILL.md
    reference/           # Optional supporting docs (AgentSkills layout)
scripts/                 # Validators and utilities (not part of the module)
docs/                    # Indexes, ADRs, design notes
experimental/            # Work in progress; contributions welcome
AGENTS.md                # Contributor context for this repo
```

Layout is specified in [ADR-0002](docs/ADRs/0002-agentskills-standards.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full details. The short version:

1. New or experimental skills go in `experimental/` first.
2. Skills must use the standard front matter format:
   ```markdown
   ---
   name: skill-name
   description: Precise one-line trigger condition for the skill.
   category: secure_development
   subcategory: mcp-server
   ---
   ```
3. Skills must be tool-agnostic — no assistant-specific syntax or config.
4. When adapting skills from upstream sources, record the source commit and license in the relevant `docs/*-skills.md` provenance section. Trail of Bits skills are CC BY-SA 4.0; adaptations carry the same license.

### Updating indexes when adding a skill

Every new skill file requires updates to the index files — do this in the same commit as the skill itself:

| File | What to update |
|------|----------------|
| `docs/skills-index.md` | Add or adjust rows; fix category totals |
| `docs/<category>-skills.md` | Add skill to subcategory table; update count |
| `README.md` (this file) | Increment the category count and total |
| `module/AGENTS.md` | Update skill count or collision table if relevant |

For architecture decisions and conventions, see [`AGENTS.md`](AGENTS.md).

## License

This project is licensed under the Apache License 2.0 — see [`LICENSE`](LICENSE) for details.

**Some skills are adapted from third-party sources under their own licenses:**

| Source | License | Skills | Details |
|--------|---------|--------|---------|
| [Trail of Bits Skills Marketplace](https://github.com/trailofbits/skills) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | 32 skills (fuzzing, static analysis, audit workflows, developer tooling, and select crypto/config/supply-chain skills) | ShareAlike — adaptations must use the same license |
| [CoSAI Project CodeGuard](https://github.com/cosai-oasis/project-codeguard) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | 8 skills (web security, C/C++ safety, algorithm selection, build YAML) | Attribution required |

Each affected skill file has `license` and `origin` fields in its YAML front matter. See [`NOTICE`](NOTICE) for the complete list and [`docs/secure-development-skills.md`](docs/secure-development-skills.md) for full provenance.
