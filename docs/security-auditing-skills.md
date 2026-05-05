# Security Auditing skills

4 skills for structured security review workflows — building context, reviewing diffs, eliminating false positives, and finding vulnerability variants.

## Usage

Reference any skill by path in your assistant prompt:

```text
Using `module/skills/differential-review/SKILL.md`: review the security impact of this diff.
```

Skills follow the AgentSkills layout: YAML front matter (`name`, `description`, `category`, `subcategory`) plus markdown body in `module/skills/<name>/SKILL.md`. They work with any assistant (Cursor, Claude Code, Copilot, etc.).

## Categories

### Audit workflow — 4 skills

| Skill | Focus |
|-------|-------|
| [`audit-context-building`](../module/skills/audit-context-building/SKILL.md) | Line-by-line codebase analysis to build deep architectural context before a security review |
| [`differential-review`](../module/skills/differential-review/SKILL.md) | Security-focused review of PRs, commits, and diffs with blast radius analysis |
| [`fp-check`](../module/skills/fp-check/SKILL.md) | Systematic verification of suspected bugs to eliminate false positives |
| [`variant-analysis`](../module/skills/variant-analysis/SKILL.md) | Finding related vulnerabilities across a codebase after discovering an initial issue |

## Provenance

- **Audit workflow skills**: Adapted from Trail of Bits Skills Marketplace ([trailofbits/skills](https://github.com/trailofbits/skills)). Upstream commit: `88947f59f1032c1f4d84d6fab244acff6f014728` (2026-04-07). License: CC BY-SA 4.0.
