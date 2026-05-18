# Contributing

Thank you for your interest in contributing to Security Skills! This document covers the guidelines for contributing new skills, improving existing ones, and maintaining quality.

## Getting started

```bash
make bootstrap
```

This installs ruff, ty, [skillsaw](https://github.com/stbenjam/skillsaw), pre-commit, and wires up git hooks for automatic linting and validation. Requires [`uv`](https://docs.astral.sh/uv/).

## Contribution workflow

1. **Fork** the repository and create a feature branch.
2. **Add or update** skills following the conventions below.
3. **Run `make lint`** to validate formatting, front matter, and skill quality (includes [skillsaw](https://github.com/stbenjam/skillsaw) linting).
4. **Open a pull request** with a clear description of what the skill covers and why.

## Skill conventions

### Format

Every skill is a markdown file with YAML front matter:

```markdown
---
name: skill-name
description: Precise one-line trigger condition for the skill.
---

Skill body...
```

- The `description` field is critical — it determines when agents invoke the skill. Write it as a precise trigger condition, not a vague summary.
- Skills must be **tool-agnostic** — no assistant-specific syntax, config keys, or directives.
- Use kebab-case for directory and file names.

### Placement

- **Production-ready skills** go in `skills/<category>/<subcategory>/`.
- **Work-in-progress or unreviewed skills** go in `experimental/`.
- Skills graduate from `experimental/` to `skills/` after review.

### Index updates

Every new skill file requires updates to **four index files** in the same commit:

| File | What to update |
|------|----------------|
| `skills/<category>/README.md` | Add the skill to its subcategory table; increment the subcategory skill count |
| `skills/README.md` | Increment the category count and the total count in the header |
| `README.md` | Increment the category count and the total |
| `AGENTS.md` | Increment the `skills/<category>/` count in the Repository layout table |

### Provenance

When adapting skills from upstream sources:

- Record the source commit and license in the relevant `skills/<category>/README.md`.
- Trail of Bits skills are [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — adaptations must carry the same license.
- CoSAI CodeGuard skills are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### Quality guidelines

- **No secrets**: Never commit real credentials, API keys, or tokens. Use synthetic values in examples.
- **Actionable content**: Skills should provide concrete, implementable guidance — not vague advice.
- **Reference upstream docs**: Link to official documentation rather than duplicating it.
- **Test your skill**: Try using it with an AI assistant to verify it produces useful results.

## AI-assisted contributions

If you use AI tools to help write skills, please note this in your pull request description. Use commit trailers where appropriate:

```
Assisted-by: <name of code assistant>
Generated-by: <name of code assistant>
```

## Code of conduct

Be respectful and constructive. We welcome contributions from everyone regardless of experience level.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE). Skills adapted from CC BY-SA 4.0 or CC BY 4.0 sources retain their original license.
