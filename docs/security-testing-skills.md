# Security Testing skills

6 skills for finding vulnerabilities through automated testing — coverage-guided fuzzing and static analysis. Curated for relevance to open source and enterprise development.

## Usage

Reference any skill by path in your assistant prompt:

```text
Using `module/skills/fuzzing/SKILL.md`: write a fuzzing harness for this parser.
```

```text
Using `module/skills/semgrep/SKILL.md`: scan this codebase for vulnerabilities.
```

Skills follow the AgentSkills layout: YAML front matter (`name`, `description`, `category`, `subcategory`) plus markdown body in `module/skills/<name>/SKILL.md`. They work with any assistant (Cursor, Claude Code, Copilot, etc.).

## Categories

### Fuzzing — 1 skill

| Skill | Focus |
|-------|-------|
| [`fuzzing`](../module/skills/fuzzing/SKILL.md) | Coverage-guided fuzzing for C/C++, Rust, Python, and Ruby — detects language, picks the right fuzzer, guides harness writing, sanitizers, corpus management, and campaign execution. Tool-specific references: [libFuzzer](../module/skills/fuzzing/references/libfuzzer.md), [AFL++](../module/skills/fuzzing/references/aflpp.md), [LibAFL](../module/skills/fuzzing/references/libafl.md), [cargo-fuzz](../module/skills/fuzzing/references/cargo-fuzz.md), [Atheris](../module/skills/fuzzing/references/atheris.md), [Ruzzy](../module/skills/fuzzing/references/ruzzy.md), [OSS-Fuzz](../module/skills/fuzzing/references/ossfuzz.md) |

### Static analysis — 5 skills

| Skill | Focus |
|-------|-------|
| [`codeql`](../module/skills/codeql/SKILL.md) | Interprocedural data flow and taint tracking analysis with CodeQL |
| [`sarif-parsing`](../module/skills/sarif-parsing/SKILL.md) | Parsing, filtering, and deduplicating SARIF output from any scanner |
| [`semgrep`](../module/skills/semgrep/SKILL.md) | Running Semgrep across a codebase with parallel subagents |
| [`semgrep-rule-creator`](../module/skills/semgrep-rule-creator/SKILL.md) | Writing custom Semgrep rules for security vulnerabilities and bug patterns |
| [`semgrep-rule-variant-creator`](../module/skills/semgrep-rule-variant-creator/SKILL.md) | Porting existing Semgrep rules to new target languages |

## Provenance

- **Fuzzing skills**: Adapted from Trail of Bits Skills Marketplace ([trailofbits/skills](https://github.com/trailofbits/skills)). Upstream commit: `88947f59f1032c1f4d84d6fab244acff6f014728` (2026-04-07). License: CC BY-SA 4.0.
- **Static analysis skills**: Adapted from Trail of Bits Skills Marketplace. Same upstream commit and license. Curated versions inline reference docs and drop tool-specific artifacts (plugin.json, hooks, scripts).
