# Developer Tooling skills

4 general-purpose development tooling skills — devcontainers, branch cleanup, modern Python, and property-based testing.

## Usage

Reference any skill by path in your assistant prompt:

```text
Using `module/skills/devcontainer-setup/SKILL.md`: add Dev Container support to this project.
```

```text
Using `module/skills/property-based-testing/SKILL.md`: write property-based tests for this parser.
```

Skills follow the AgentSkills layout: YAML front matter (`name`, `description`, `category`, `subcategory`) plus markdown body in `module/skills/<name>/SKILL.md`. They work with any assistant (Cursor, Claude Code, Copilot, etc.).

## Categories

### Testing — 1 skill

| Skill | Focus |
|-------|-------|
| [`property-based-testing`](../module/skills/property-based-testing/SKILL.md) | Property-based testing with Hypothesis (Python), proptest (Rust), and others |

### Tooling — 3 skills

| Skill | Focus |
|-------|-------|
| [`devcontainer-setup`](../module/skills/devcontainer-setup/SKILL.md) | Adding Dev Container support with language-specific tooling and persistent volumes |
| [`git-cleanup`](../module/skills/git-cleanup/SKILL.md) | Safely analyzing and cleaning up merged, squash-merged, and stale branches |
| [`modern-python`](../module/skills/modern-python/SKILL.md) | Configuring Python projects with uv, ruff, and ty |

## Provenance

- **Developer tooling skills**: Adapted from Trail of Bits Skills Marketplace ([trailofbits/skills](https://github.com/trailofbits/skills)). Upstream commit: `88947f59f1032c1f4d84d6fab244acff6f014728` (2026-04-07). License: CC BY-SA 4.0.
