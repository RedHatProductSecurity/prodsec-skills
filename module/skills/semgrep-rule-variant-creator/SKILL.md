---
name: semgrep-rule-variant-creator
description: Creates language variants of existing Semgrep rules. Use when porting a Semgrep rule to specified target languages. Takes an existing rule and target languages as input, produces independent rule+test directories for each language.
license: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
origin: Adapted from Trail of Bits Skills Marketplace (https://github.com/trailofbits/skills)
category: "security_testing"
subcategory: "static-analysis"
---

# Semgrep Rule Variant Creator

Port existing Semgrep rules to new target languages with proper applicability analysis and test-driven validation.

## When to Use

**Ideal scenarios:**
- Porting an existing Semgrep rule to one or more target languages
- Creating language-specific variants of a universal vulnerability pattern
- Expanding rule coverage across a polyglot codebase
- Translating rules between languages with equivalent constructs

## When NOT to Use

Do NOT use this skill for:
- Creating a new Semgrep rule from scratch (use `semgrep-rule-creator` instead)
- Running existing rules against code
- Languages where the vulnerability pattern fundamentally doesn't apply
- Minor syntax variations within the same language

## Input Specification

This skill requires:
1. **Existing Semgrep rule** - YAML file path or YAML rule content
2. **Target languages** - One or more languages to port to (e.g., "Golang and Java")

## Output Specification

For each applicable target language, produces:
```
<original-rule-id>-<language>/
├── <original-rule-id>-<language>.yaml     # Ported Semgrep rule
└── <original-rule-id>-<language>.<ext>    # Test file with annotations
```

Example output for porting `sql-injection` to Go and Java:
```
sql-injection-golang/
├── sql-injection-golang.yaml
└── sql-injection-golang.go

sql-injection-java/
├── sql-injection-java.yaml
└── sql-injection-java.java
```

## Rationalizations to Reject

When porting Semgrep rules, reject these common shortcuts:

| Rationalization | Why It Fails | Correct Approach |
|-----------------|--------------|------------------|
| "Pattern structure is identical" | Different ASTs across languages | Always dump AST for target language |
| "Same vulnerability, same detection" | Data flow differs between languages | Analyze target language idioms |
| "Rule doesn't need tests since original worked" | Language edge cases differ | Write NEW test cases for target |
| "Skip applicability - it obviously applies" | Some patterns are language-specific | Complete applicability analysis first |
| "I'll create all variants then test" | Errors compound, hard to debug | Complete full cycle per language |
| "Library equivalent is close enough" | Surface similarity hides differences | Verify API semantics match |
| "Just translate the syntax 1:1" | Languages have different idioms | Research target language patterns |

## Strictness Level

This workflow is **strict** - do not skip steps:
- **Applicability analysis is mandatory**: Don't assume patterns translate
- **Each language is independent**: Complete full cycle before moving to next
- **Test-first for each variant**: Never write a rule without test cases
- **100% test pass required**: "Most tests pass" is not acceptable

## Overview

This skill guides the creation of language-specific variants of existing Semgrep rules. Each target language goes through an independent 4-phase cycle:

```
FOR EACH target language:
  Phase 1: Applicability Analysis → Verdict
  Phase 2: Test Creation (Test-First)
  Phase 3: Rule Creation
  Phase 4: Validation
  (Complete full cycle before moving to next language)
```

## Foundational Knowledge

**The `semgrep-rule-creator` skill is the authoritative reference for Semgrep rule creation fundamentals.** While this skill focuses on porting existing rules to new languages, the core principles of writing quality rules remain the same.

Consult `semgrep-rule-creator` for guidance on:
- **When to use taint mode vs pattern matching** - Choosing the right approach for the vulnerability type
- **Test-first methodology** - Why tests come before rules and how to write effective test cases
- **Anti-patterns to avoid** - Common mistakes like overly broad or overly specific patterns
- **Iterating until tests pass** - The validation loop and debugging techniques
- **Rule optimization** - Removing redundant patterns after tests pass

When porting a rule, you're applying these same principles in a new language context. If uncertain about rule structure or approach, refer to `semgrep-rule-creator` first.

## Four-Phase Workflow

### Phase 1: Applicability Analysis

Before porting, determine if the pattern applies to the target language.

**Analysis criteria:**
1. Does the vulnerability class exist in the target language?
2. Does an equivalent construct exist (function, pattern, library)?
3. Are the semantics similar enough for meaningful detection?

**Verdict options:**
- `APPLICABLE` → Proceed with variant creation
- `APPLICABLE_WITH_ADAPTATION` → Proceed but significant changes needed
- `NOT_APPLICABLE` → Skip this language, document why

Full guidance is **inlined below** (upstream `references/applicability-analysis.md`). *(see upstream Trail of Bits prodsec-skills for companion files)*

### Phase 2: Test Creation (Test-First)

**Always write tests before the rule.**

Create test file with target language idioms:
- Minimum 2 vulnerable cases (`ruleid:`)
- Minimum 2 safe cases (`ok:`)
- Include language-specific edge cases

```go
// ruleid: sql-injection-golang
db.Query("SELECT * FROM users WHERE id = " + userInput)

// ok: sql-injection-golang
db.Query("SELECT * FROM users WHERE id = ?", userInput)
```

### Phase 3: Rule Creation

1. **Analyze AST**: `semgrep --dump-ast -l <lang> test-file`
2. **Translate patterns** to target language syntax
3. **Update metadata**: language key, message, rule ID
4. **Adapt for idioms**: Handle language-specific constructs

See **Inlined: language syntax guide** below.

### Phase 4: Validation

```bash
# Validate YAML
semgrep --validate --config rule.yaml

# Run tests
semgrep --test --config rule.yaml test-file
```

**Checkpoint**: Output MUST show `All tests passed`.

For taint rule debugging:
```bash
semgrep --dataflow-traces -f rule.yaml test-file
```

Extended troubleshooting and examples: upstream `references/workflow.md` in the rule-creator plugin and **semgrep-rule-creator** in this repo.

## Quick Reference

| Task | Command |
|------|---------|
| Run tests | `semgrep --test --config rule.yaml test-file` |
| Validate YAML | `semgrep --validate --config rule.yaml` |
| Dump AST | `semgrep --dump-ast -l <lang> <file>` |
| Debug taint flow | `semgrep --dataflow-traces -f rule.yaml file` |


## Key Differences from Rule Creation

| Aspect | semgrep-rule-creator | This skill |
|--------|---------------------|------------|
| Input | Bug pattern description | Existing rule + target languages |
| Output | Single rule+test | Multiple rule+test directories |
| Workflow | Single creation cycle | Independent cycle per language |
| Phase 1 | Problem analysis | Applicability analysis per language |
| Library research | Always relevant | Optional (when original uses libraries) |

## Documentation

**REQUIRED**: Before porting rules, read relevant Semgrep documentation:

- [Rule Syntax](https://semgrep.dev/docs/writing-rules/rule-syntax) - YAML structure and operators
- [Pattern Syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax) - Pattern matching and metavariables
- [Pattern Examples](https://semgrep.dev/docs/writing-rules/pattern-examples) - Per-language pattern references
- [Testing Rules](https://semgrep.dev/docs/writing-rules/testing-rules) - Testing annotations
- [Trail of Bits Testing Handbook](https://appsec.guide/docs/static-analysis/semgrep/advanced/) - Advanced patterns

---

## Inlined: applicability analysis (upstream `references/applicability-analysis.md`)

# Applicability Analysis

Phase 1 of the variant creation workflow. Before porting a rule, analyze whether the vulnerability pattern applies to the target language.

## Analysis Process

For EACH target language, answer these questions:

### 1. Does the Vulnerability Class Exist?

**Determine if the vulnerability type is possible in the target language.**

Examples:
- Buffer overflow: Applies to C/C++, may apply to Rust (in unsafe blocks), does NOT apply to Python/Java
- SQL injection: Applies to any language with database access
- XSS: Applies to any language generating HTML output
- Memory leak: Relevant in C/C++, less relevant in garbage-collected languages
- Type confusion: Relevant in dynamically typed languages, less relevant in strongly typed

### 2. Does an Equivalent Construct Exist?

**Identify what the original rule detects and find equivalents.**

Parse the original rule to identify:
- **Sinks**: What dangerous functions/methods does it detect?
- **Sources**: Where does tainted data originate?
- **Pattern type**: Is it taint-mode or pattern-matching?

Then research the target language:
- What are the equivalent dangerous functions?
- What are the common source patterns?
- Are there language-specific idioms to consider?

### 3. Are the Semantics Similar Enough?

**Verify the pattern translates meaningfully.**

Consider:
- Does the vulnerability manifest the same way?
- Are there language-specific mitigations that change detection needs?
- Would the ported rule provide actual security value?

## Verdict Format

Document your analysis for each target language:

```
TARGET: <language>
VERDICT: APPLICABLE | APPLICABLE_WITH_ADAPTATION | NOT_APPLICABLE
REASONING: <specific analysis>
ADAPTATIONS_NEEDED: <if APPLICABLE_WITH_ADAPTATION>
EQUIVALENT_CONSTRUCTS:
  - Original: <function/pattern>
  - Target: <equivalent function/pattern>
```

## Verdict Definitions

### APPLICABLE

The pattern translates directly with minor syntax adjustments.

**Criteria:**
- Equivalent constructs exist with same semantics
- Vulnerability manifests identically
- Detection logic remains the same

**Example:**
```
Original: Python os.system(user_input)
Target: Go exec.Command(user_input)

VERDICT: APPLICABLE
REASONING: Both execute shell commands with user input. Vulnerability is
identical (command injection). Detection logic (taint from input to exec)
translates directly.
```

### APPLICABLE_WITH_ADAPTATION

The pattern can be ported but requires significant changes.

**Criteria:**
- Vulnerability class exists but manifests differently
- Equivalent constructs exist but with different APIs
- Additional patterns needed for target language idioms

**Example:**
```
Original: Python pickle.loads(untrusted)
Target: Java ObjectInputStream.readObject()

VERDICT: APPLICABLE_WITH_ADAPTATION
REASONING: Both detect deserialization vulnerabilities but the APIs differ
significantly. Java requires detection of ObjectInputStream creation and
readObject() calls, not a single function call.
ADAPTATIONS_NEEDED:
  - Different sink patterns (readObject vs loads)
  - May need pattern-inside for ObjectInputStream context
  - Consider readUnshared() variant
```

### NOT_APPLICABLE

The pattern should not be ported to this language.

**Criteria:**
- Vulnerability class doesn't exist in target language
- No equivalent construct exists
- Pattern would be meaningless or misleading

**Example:**
```
Original: C buffer overflow detection
Target: Python

VERDICT: NOT_APPLICABLE
REASONING: Python handles memory management automatically. Buffer overflows
in the traditional C sense don't exist. The vulnerability class is not
present in the target language.
```

## Common Applicability Patterns

### Always Translate (Language-Agnostic Vulnerabilities)

These vulnerability classes exist across most languages:
- SQL injection (any language with DB access)
- Command injection (any language with shell execution)
- Path traversal (any language with file operations)
- SSRF (any language with HTTP clients)
- XSS (any language generating HTML)

### Sometimes Translate (Context-Dependent)

These require careful analysis:
- Deserialization: Different mechanisms per language
- Cryptographic weaknesses: Language-specific crypto libraries
- Race conditions: Depends on concurrency model
- Integer overflow: Depends on type system

### Rarely Translate (Language-Specific)

These are often NOT_APPLICABLE for other languages:
- Memory corruption (C/C++ specific)
- Type juggling (PHP specific)
- Prototype pollution (JavaScript specific)
- GIL-related issues (Python specific)

## Library-Specific Rules

When the original rule targets a third-party library:

### Step 1: Identify the Library's Purpose

What functionality does the library provide?
- ORM / Database access
- HTTP client/server
- Serialization
- Templating
- etc.

### Step 2: Research Target Language Ecosystem

For the target language, identify:
- Standard library equivalents
- Popular third-party libraries with same functionality
- Language-specific idioms for this functionality

### Step 3: Decide on Scope

Options:
- **Native constructs only**: Port to standard library equivalents
- **Popular library**: Port to the most common library in target ecosystem
- **Multiple variants**: Create separate rules for multiple libraries

**Recommendation**: Start with standard library or most popular option. Additional library variants can be created separately if needed.

## Analysis Checklist

Before proceeding past Phase 1:

- [ ] Parsed original rule and identified pattern type
- [ ] Identified sinks, sources, and sanitizers (if taint mode)
- [ ] Researched equivalent constructs in target language
- [ ] Documented verdict with specific reasoning
- [ ] If APPLICABLE_WITH_ADAPTATION, listed required changes
- [ ] If NOT_APPLICABLE, documented clear explanation

## Example Analysis

**Original Rule**: Python command injection via subprocess

```yaml
rules:
  - id: python-command-injection
    mode: taint
    languages: [python]
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: subprocess.call($CMD, shell=True, ...)
```

**Target**: Go

```
TARGET: Go
VERDICT: APPLICABLE_WITH_ADAPTATION

REASONING:
- Command injection exists in Go (vulnerability class present)
- Go uses exec.Command() and exec.CommandContext() for command execution
- Go doesn't have shell=True equivalent; commands run directly by default
- Shell execution in Go requires explicit bash -c wrapping

EQUIVALENT_CONSTRUCTS:
  - Original sink: subprocess.call(cmd, shell=True)
  - Target sinks:
    - exec.Command("bash", "-c", cmd)
    - exec.Command("sh", "-c", cmd)
    - exec.Command(cmd) when cmd comes from user input

ADAPTATIONS_NEEDED:
1. Different sink patterns for Go's exec package
2. Source patterns need Go HTTP handler equivalents (r.URL.Query(), r.FormValue())
3. Consider both direct exec.Command and shell-wrapped variants
```

**Target**: Java

```
TARGET: Java
VERDICT: APPLICABLE

REASONING:
- Command injection exists in Java (vulnerability class present)
- Java uses Runtime.exec() and ProcessBuilder for command execution
- Direct equivalent functionality available

EQUIVALENT_CONSTRUCTS:
  - Original sink: subprocess.call(cmd, shell=True)
  - Target sinks:
    - Runtime.getRuntime().exec(cmd)
    - new ProcessBuilder(cmd).start()

ADAPTATIONS_NEEDED:
- Source patterns need Java servlet equivalents (request.getParameter())
- Consider both Runtime.exec and ProcessBuilder patterns
```

---

## Inlined: language syntax guide (excerpt, upstream `references/language-syntax-guide.md`)

# Language Syntax Translation Guide

Guidance for translating Semgrep patterns between languages. This is NOT a pre-built mapping—use these principles to research and adapt patterns for your specific case.

## General Translation Principles

### 1. Never Assume Syntax Equivalence

What looks similar may parse differently:

```python
# Python: method call on object
obj.method(arg)

# Go: might be method OR field access + function call
obj.Method(arg)      # Method call
obj.Field(arg)       # Field holding function, then called
```

**Always dump the AST** for your target language to see the actual structure.

### 2. Research Before Translating

For each construct in the original rule:
1. Search target language documentation for equivalent
2. Look for multiple ways the same thing can be written
3. Check if language idioms differ significantly

### 3. Preserve Detection Intent, Not Literal Syntax

The goal is detecting the same vulnerability, not matching identical syntax.

```yaml
# Original (Python) - detects eval of user input
pattern: eval($USER_INPUT)

# Go doesn't have eval() - what's the equivalent danger?
# Research shows: template execution, reflect-based eval, etc.
# Adapt to what actually creates the vulnerability in Go
```

## AST Analysis

### Always Dump the AST

```bash
semgrep --dump-ast -l <target-language> test-file
```

Compare how similar constructs are represented:

```python
# Python
cursor.execute(query)
```

```go
// Go
db.Query(query)
```

The AST structure may differ significantly even for conceptually similar operations.

### Key Differences to Watch

| Aspect | May Differ |
|--------|------------|
| Method calls | Receiver position, syntax |
| Function arguments | Named vs positional, defaults |
| String handling | Interpolation, concatenation |
| Error handling | Exceptions vs return values |
| Imports | How namespaces work |

## Metavariable Adaptation

### Metavariables Work Cross-Language

Semgrep metavariables (`$X`, `$FUNC`, etc.) work in all languages:

```yaml
# Works in Python
pattern: $OBJ.execute($QUERY)

# Works in Java
pattern: $OBJ.executeQuery($QUERY)

# Works in Go
pattern: $DB.Query($QUERY, ...)
```

### Ellipsis Behavior

`...` matches language-appropriate constructs:
- In Python: matches arguments, statements
- In Go: matches arguments, statements (handles multi-return)
- In Java: matches arguments, statements, annotations

## Common Translation Categories

### Database Queries

**Research for your target language:**
- Standard library database package
- Popular ORM frameworks
- Raw query execution methods

Common patterns to look for:
- Query execution methods
- Prepared statement patterns
- String interpolation into queries

### Command Execution

**Research for your target language:**
- Standard library process/exec package
- Shell execution vs direct execution
- Argument passing (array vs string)

### File Operations

**Research for your target language:**
- File open/read/write APIs
- Path construction methods
- Directory traversal patterns

### HTTP Handling

**Research for your target language:**
- Request parameter access
- Header access
- Body parsing

## Researching Equivalents

### Step 1: Identify What the Original Detects

Parse the original rule:
- What function/method is the sink?
- What's the vulnerability being detected?
- What makes it dangerous?

### Step 2: Search Target Language Docs

Search for:
- `"<target language> <functionality>"` (e.g., "golang exec command")
- `"<target language> <vulnerability>"` (e.g., "java sql injection")
- Standard library documentation
- [Semgrep Pattern Examples](https://semgrep.dev/docs/writing-rules/pattern-examples) - Per-language pattern references

### Step 3: Find All Variants

A single Python function may have multiple equivalents:

```python
# Python has one main way
os.system(cmd)
```

```java
// Java has multiple
Runtime.getRuntime().exec(cmd);
new ProcessBuilder(cmd).start();
ProcessBuilder.command(cmd).start();
```

Include all common variants in your rule.

### Step 4: Check for Idioms

Languages have preferred patterns:

```python
# Python: often inline
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

```go
// Go: typically uses placeholders
db.Query("SELECT * FROM users WHERE id = ?", userID)
// Vulnerability is when they DON'T use placeholders
db.Query("SELECT * FROM users WHERE id = " + userID)
```

## Source Pattern Translation

### Web Framework Sources

Original rule sources need framework-specific translation:

```yaml
# Python Flask
pattern: request.args.get(...)

# Java Servlet
pattern: $REQUEST.getParameter(...)

# Go net/http
pattern: $R.URL.Query().Get(...)
pattern: $R.FormValue(...)
```

Further sink/source examples and edge cases: *(see upstream Trail of Bits prodsec-skills for companion files)* — full `language-syntax-guide.md`.
