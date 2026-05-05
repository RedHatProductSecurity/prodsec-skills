# Security Testing skills

17 skills for finding vulnerabilities through automated testing — coverage-guided fuzzing and static analysis. Curated for relevance to open source and enterprise development.

## Usage

Reference any skill by path in your assistant prompt:

```text
Using `module/skills/cargo-fuzz/SKILL.md`: write a fuzzing harness for this parser.
```

```text
Using `module/skills/semgrep/SKILL.md`: scan this codebase for vulnerabilities.
```

Skills follow the AgentSkills layout: YAML front matter (`name`, `description`, `category`, `subcategory`) plus markdown body in `module/skills/<name>/SKILL.md`. They work with any assistant (Cursor, Claude Code, Copilot, etc.).

## Categories

### Fuzzing — 12 skills

| Skill | Focus |
|-------|-------|
| [`address-sanitizer`](../module/skills/address-sanitizer/SKILL.md) | Detect memory errors (buffer overflows, use-after-free) during C/C++ fuzzing with ASan |
| [`aflpp`](../module/skills/aflpp/SKILL.md) | Multi-core coverage-guided fuzzing of C/C++ with AFL++ |
| [`atheris`](../module/skills/atheris/SKILL.md) | Coverage-guided fuzzing of pure Python and Python C extensions |
| [`cargo-fuzz`](../module/skills/cargo-fuzz/SKILL.md) | Fuzzing Rust projects with cargo-fuzz and a libFuzzer backend |
| [`coverage-analysis`](../module/skills/coverage-analysis/SKILL.md) | Measuring code coverage to assess harness effectiveness and identify blockers |
| [`fuzzing-dictionary`](../module/skills/fuzzing-dictionary/SKILL.md) | Building domain-specific token dictionaries for parsers, protocols, and formats |
| [`fuzzing-obstacles`](../module/skills/fuzzing-obstacles/SKILL.md) | Patching checksums, global state, and other barriers to fuzzer progress |
| [`harness-writing`](../module/skills/harness-writing/SKILL.md) | Writing effective fuzz targets across languages |
| [`libafl`](../module/skills/libafl/SKILL.md) | Building custom fuzzers with LibAFL's modular fuzzing library |
| [`libfuzzer`](../module/skills/libfuzzer/SKILL.md) | Coverage-guided fuzzing of C/C++ code compiled with Clang |
| [`ossfuzz`](../module/skills/ossfuzz/SKILL.md) | Enrolling open source projects in OSS-Fuzz for continuous fuzzing |
| [`ruzzy`](../module/skills/ruzzy/SKILL.md) | Coverage-guided fuzzing of Ruby code and Ruby C extensions |

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
