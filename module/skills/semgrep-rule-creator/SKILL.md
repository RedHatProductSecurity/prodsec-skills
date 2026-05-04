---
name: semgrep-rule-creator
description: Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns. Use when writing Semgrep rules or building custom static analysis detections.
license: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
origin: Adapted from Trail of Bits Skills Marketplace (https://github.com/trailofbits/skills)
category: "security_testing"
subcategory: "static-analysis"
---

# Semgrep Rule Creator

Create production-quality Semgrep rules with proper testing and validation.

## When to Use

**Ideal scenarios:**
- Writing Semgrep rules for specific bug patterns
- Writing rules to detect security vulnerabilities in your codebase
- Writing taint mode rules for data flow vulnerabilities
- Writing rules to enforce coding standards

## When NOT to Use

Do NOT use this skill for:
- Running existing Semgrep rulesets
- General static analysis without custom rules (use `static-analysis` skill)

## Rationalizations to Reject

When writing Semgrep rules, reject these common shortcuts:

- **"The pattern looks complete"** → Still run `semgrep --test --config <rule-id>.yaml <rule-id>.<ext>` to verify. Untested rules have hidden false positives/negatives.
- **"It matches the vulnerable case"** → Matching vulnerabilities is half the job. Verify safe cases don't match (false positives break trust).
- **"Taint mode is overkill for this"** → If data flows from user input to a dangerous sink, taint mode gives better precision than pattern matching.
- **"One test is enough"** → Include edge cases: different coding styles, sanitized inputs, safe alternatives, and boundary conditions.
- **"I'll optimize the patterns first"** → Write correct patterns first, optimize after all tests pass. Premature optimization causes regressions.
- **"The AST dump is too complex"** → The AST reveals exactly how Semgrep sees code. Skipping it leads to patterns that miss syntactic variations.

## Anti-Patterns

**Too broad** - matches everything, useless for detection:
```yaml
# BAD: Matches any function call
pattern: $FUNC(...)

# GOOD: Specific dangerous function
pattern: eval(...)
```

**Missing safe cases in tests** - leads to undetected false positives:
```python
# BAD: Only tests vulnerable case
# ruleid: my-rule
dangerous(user_input)

# GOOD: Include safe cases to verify no false positives
# ruleid: my-rule
dangerous(user_input)

# ok: my-rule
dangerous(sanitize(user_input))

# ok: my-rule
dangerous("hardcoded_safe_value")
```

**Overly specific patterns** - misses variations:
```yaml
# BAD: Only matches exact format
pattern: os.system("rm " + $VAR)

# GOOD: Matches all os.system calls with taint tracking
mode: taint
pattern-sources:
  - pattern: input(...)
pattern-sinks:
  - pattern: os.system(...)
```

## Strictness Level

This workflow is **strict** - do not skip steps:
- **Read documentation first**: See [Documentation](#documentation) before writing Semgrep rules
- **Test-first is mandatory**: Never write a rule without tests
- **100% test pass is required**: "Most tests pass" is not acceptable
- **Optimization comes last**: Only simplify patterns after all tests pass
- **Avoid generic patterns**: Rules must be specific, not match broad patterns
- **Prioritize taint mode**: For data flow vulnerabilities
- **One YAML file - one Semgrep rule**: Each YAML file must contain only one Semgrep rule; don't combine multiple rules in a single file
- **No generic rules**: When targeting a specific language for Semgrep rules - avoid generic pattern matching (`languages: generic`)
- **Forbidden `todook` and `todoruleid` test annotations**: `todoruleid: <rule-id>` and `todook: <rule-id>` annotations in tests files for future rule improvements are forbidden

## Overview

This skill guides creation of Semgrep rules that detect security vulnerabilities and code patterns. Rules are created iteratively: analyze the problem, write tests first, analyze AST structure, write the rule, iterate until all tests pass, optimize the rule.

**Approach selection:**
- **Taint mode** (prioritize): Data flow issues where untrusted input reaches dangerous sinks
- **Pattern matching**: Simple syntactic patterns without data flow requirements

**Why prioritize taint mode?** Pattern matching finds syntax but misses context. A pattern `eval($X)` matches both `eval(user_input)` (vulnerable) and `eval("safe_literal")` (safe). Taint mode tracks data flow, so it only alerts when untrusted data actually reaches the sink—dramatically reducing false positives for injection vulnerabilities.

**Iterating between approaches:** It's okay to experiment. If you start with taint mode and it's not working well (e.g., taint doesn't propagate as expected, too many false positives/negatives), switch to pattern matching. Conversely, if pattern matching produces too many false positives on safe cases, try taint mode instead. The goal is a working rule—not rigid adherence to one approach.

**Output structure** - exactly 2 files in a directory named after the rule-id:
```
<rule-id>/
├── <rule-id>.yaml     # Semgrep rule
└── <rule-id>.<ext>    # Test file with ruleid/ok annotations
```

## Quick Start

```yaml
rules:
  - id: insecure-eval
    languages: [python]
    severity: HIGH
    message: User input passed to eval() allows code execution
    mode: taint
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: eval(...)
```

Test file (`insecure-eval.py`):
```python
# ruleid: insecure-eval
eval(request.args.get('code'))

# ok: insecure-eval
eval("print('safe')")
```

Run tests (from rule directory): `semgrep --test --config <rule-id>.yaml <rule-id>.<ext>`

## Quick Reference

Detailed syntax and workflow are **inlined below** (from upstream `references/quick-reference.md` and `references/workflow.md`). *(see upstream Trail of Bits prodsec-skills for companion files)*

## Workflow

Copy this checklist and track progress:

```
Semgrep Rule Progress:
- [ ] Step 1: Analyze the Problem
- [ ] Step 2: Write Tests First
- [ ] Step 3: Analyze AST structure
- [ ] Step 4: Write the rule
- [ ] Step 5: Iterate until all tests pass (semgrep --test)
- [ ] Step 6: Optimize the rule (remove redundancies, re-test)
- [ ] Step 7: Final Run
```

Full step descriptions are in **Inlined: workflow** below.

## Documentation

**REQUIRED**: Before writing any rule, read **all** of these Semgrep documentation sources (fetch or open the URLs in a browser / via HTTP):

1. [Rule Syntax](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/rule-syntax.md)
2. [Pattern Syntax](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/pattern-syntax.mdx)
3. [Testing Rules](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/testing-rules.md)
4. [Taint analysis](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/data-flow/taint-mode/overview.md)
5. [Advanced techniques for taint analysis](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/data-flow/taint-mode/advanced.md)
6. [Constant propagation](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/data-flow/constant-propagation.md)
7. [Trail of Bits Testing Handbook - Semgrep chapter](https://raw.githubusercontent.com/trailofbits/testing-handbook/refs/heads/main/content/docs/static-analysis/semgrep/10-advanced.md)

---

## Inlined: quick reference (upstream `references/quick-reference.md`)

# Semgrep Rule Quick Reference

## Required Rule Fields

```yaml
rules:
  - id: rule-id               # Unique identifier (lowercase, hyphens)
    languages: [python]       # Target language(s)
    severity: HIGH            # LOW, MEDIUM, HIGH, CRITICAL (ERROR/WARNING/INFO are legacy)
    message: Description      # Shown when rule matches
    pattern: code(...)        # OR use patterns/pattern-either/mode:taint
```

## Pattern Operators

### Basic Matching
```yaml
# 'pattern' is the basic unit of matching
pattern: foo(...)

# 'patterns' forms a logical AND - all must match
patterns:
  - pattern: $X
  - pattern-not: safe($X)

# 'pattern-either' forms a logical OR - any can match
pattern-either:
  - pattern: foo(...)
  - pattern: bar(...)

# 'pattern-regex' performs PCRE2 regex matching (multiline mode)
pattern-regex: ^foo.*bar$
```

### Matching Operators
- `$VAR` - Metavariable, match a single expression
  - **Must be uppercase**: `$X`, `$FUNC`, `$VAR_1` (NOT `$x`, `$var`)
- `$_` - Anonymous metavariable, matches but doesn't bind
- `$...VAR` - Ellipsis metavariable, match zero or more arguments
- `...` - Ellipsis, match anything in between statements or expressions
- `<... [pattern] ...>` - Deep expression operator, match nested expression

### Typed Metavariables

Constrain metavariables to specific types (reduces false positives):

```yaml
# C/C++ - match only int16_t parameters
pattern: (int16_t $X)

# C/C++ - match function with typed parameter
pattern: some_func((int $ARG))

# Java - match Logger type
pattern: (java.util.logging.Logger $LOGGER).log(...)

# Go - match pointer type (uses colon syntax)
pattern: ($READER : *zip.Reader).Open($INPUT)

# TypeScript - match specific type
pattern: ($X: DomSanitizer).sanitize(...)

# Use in taint mode to track only specific types as sources:
pattern-sources:
  - pattern: (int $X)        # Only int parameters are taint sources
  - pattern: (int16_t $X)    # Only int16_t parameters
  - pattern: int $X = $INIT; # Local variable declarations
```

### Scope Operators
```yaml
pattern-inside: |              # Must be inside this pattern
  def $FUNC(...):
    ...
pattern-not-inside: |          # Must NOT be inside this pattern
  with $CTX:
    ...
```

### Negation
```yaml
pattern-not: safe(...)         # Exclude this pattern
pattern-not-regex: ^test_      # Exclude by regex
```

### Metavariable Filters
```yaml
metavariable-regex:
  metavariable: $FUNC
  regex: (unsafe|dangerous).*

metavariable-pattern:
  metavariable: $ARG
  pattern: request.$X

metavariable-comparison:
  metavariable: $NUM
  comparison: $NUM > 1024
```

### Focus
```yaml
# In pattern matching mode: report finding on this metavariable only
focus-metavariable: $TARGET

# In taint mode: constrain where taint flows in sources, sinks, and sanitizers
pattern-sources:
  - patterns:
      - pattern: mutate_argument(&$REF_VAR)
      - focus-metavariable: $REF_VAR
    by-side-effect: only
```

## Taint Mode

```yaml
rules:
  - id: taint-rule
    mode: taint
    languages: [python]
    severity: HIGH
    message: Tainted data reaches sink
    pattern-sources:
      - pattern: user_input()
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: eval(...)
      - pattern: os.system(...)
    pattern-sanitizers:           # Optional
      - pattern: sanitize(...)
      - pattern: escape(...)
```

### Taint Options
```yaml
pattern-sources:
  - pattern: source(...)
    exact: true                   # Only exact match is source (default: false)
    by-side-effect: true          # Taints by side effect (also accepts: only)

pattern-sanitizers:
  - pattern: sanitize($X)
    exact: true                   # Only exact match (default: false)
    by-side-effect: true          # Sanitizes by side effect

pattern-sinks:
  - pattern: sink(...)
    exact: false                  # Subexpressions also sinks (default: true)
```

## Test File Annotations

Only allowed annotations are `ruleid: rule-id` and `ok: rule-id`.

```python
# ruleid: rule-id
vulnerable_code()              # This line MUST match

# ok: rule-id
safe_code()                    # This line MUST NOT match
```

DO NOT use multi-line comments for test annotations, for example:
`/* ruleid: ... */`

## Debugging Commands

```bash
# Test rules
semgrep --test --config <rule-id>.yaml <rule-id>.<ext>

# Validate YAML syntax
semgrep --validate --config <rule-id>.yaml

# Run with dataflow traces (for taint mode rules)
semgrep --dataflow-traces --config <rule-id>.yaml <rule-id>.<ext>

# Dump AST to understand code structure
semgrep --dump-ast --lang <language> <rule-id>.<ext>

# Run single rule
semgrep --config <rule-id>.yaml <rule-id>.<ext>

# Run single pattern
semgrep --lang <language> --pattern <pattern> <rule-id>.<ext>
```

## Troubleshooting

### Common Pitfalls

1. **Wrong annotation line**: `ruleid:` must be on the line IMMEDIATELY BEFORE the finding. No other text or code
2. **Too generic patterns**: Avoid `pattern: $X` without constraints
3. **YAML syntax errors**: Validate with `semgrep --validate`

### Pattern Not Matching

1. Check AST structure: `semgrep --dump-ast --lang <language> <rule-id>.<ext>`
2. Verify metavariable binding
3. Check for whitespace/formatting differences
4. Try more general pattern first, then narrow down

### Taint Not Propagating

1. Use `--dataflow-traces` to see flow
2. Check if sanitizer is too broad
3. Verify source pattern matches
4. Check sink focus-metavariable

### Too Many False Positives

1. Add `pattern-not` for safe cases
2. Add sanitizers for validation functions
3. Use `pattern-inside` to limit scope
4. Use `metavariable-regex` to filter

---

## Inlined: workflow (upstream `references/workflow.md`)

# Semgrep Rule Creation Workflow

Detailed workflow for creating production-quality Semgrep rules.

## Step 1: Analyze the Problem

Before writing any code:

1. **Fetch external documentation**: See [Documentation](#documentation) above for required reading
2. **Understand the exact bug pattern and explain the bug for a junior developer**: What vulnerability, issue or pattern should be detected?
3. **Identify the target language**: What is specific about the bug and that language?
4. **Determine the approach**:
   - **Pattern matching**: Syntactic patterns without data flow
   - **Taint mode**: Data flows from untrusted source to dangerous sink

### When to Use Taint Mode

Taint mode is a powerful feature in Semgrep that can track the flow of data from one location to another. By using taint mode, you can:

- **Track data flow across multiple variables**: Trace how data moves across different variables, functions, components, and identify insecure flow paths (e.g., situations where a specific sanitizer is not used).
- **Find injection vulnerabilities**: Identify injection vulnerabilities such as SQL injection, command injection, and XSS attacks.
- **Write simple and resilient Semgrep rules**: Simplify rules that are resilient to code patterns nested in if statements, loops, and other structures.

## Step 2: Write Tests First

**Why test-first?** Writing tests before the rule forces you to think about both vulnerable AND safe cases. Rules written without tests often have hidden false positives (matching safe cases) or false negatives (missing vulnerable variants). Tests make these visible immediately.

Create directory and test file with annotations (`# ruleid:`, `# ok:` only). See quick reference above for full syntax.

### Directory Structure

```
<rule-id>/
├── <rule-id>.yaml     # Semgrep rule
└── <rule-id>.<ext>    # Test file with ruleid/ok annotations
```

**CRITICAL**:
1. The comment (`# ruleid:` or `# ok:` ) must be on the line IMMEDIATELY BEFORE the code. Semgrep reports findings on the line after the annotation.
2. The comment must contain ONLY the comment marker and annotation (e.g., `# ruleid: my-rule`). No other text, comments, or code on the same line.

### Test Case Design

You must include test cases for:
- Clear vulnerable cases (must match)
- Clear safe cases (must not match)
- Edge cases and variations
- Different coding styles
- Sanitized/validated input (must not match)
- Unrelated code (must not match) - normal code with no relation to the rule's target pattern
- Nested structures (e.g., inside if statements, loops, try/catch blocks, callbacks)

## Step 3: Analyze AST Structure

**Why analyze AST?** Semgrep matches against the AST, not raw text. Code that looks similar may parse differently (e.g., `foo.bar()` vs `foo().bar`). The AST dump shows exactly what Semgrep sees, preventing patterns that fail due to unexpected tree structure. Understanding how exactly Semgrep parses code is crucial for writing precise patterns.

```bash
semgrep --dump-ast --lang <language> <rule-id>.<ext>
```

Example output helps understand:
- How function calls are represented
- How variables are bound
- How control flow is structured

## Step 4: Write the Rule

Choose the appropriate pattern operators and write the rule.

For pattern operator syntax (basic matching, scope operators, metavariable filters, focus), see **Inlined: quick reference** above.

### Validate and Test

#### Validate YAML Syntax

```bash
semgrep --validate --config <rule-id>.yaml
```

#### Run Tests

```bash
cd <rule-directory>
semgrep --test --config <rule-id>.yaml <rule-id>.<ext>
```

#### Expected Output

```
1/1: ✓ All tests passed
```

#### Debug Failures

If tests fail, check:
1. **Missed lines**: Rule didn't match when it should
   - Pattern too specific
   - Missing pattern variant
2. **Incorrect lines**: Rule matched when it shouldn't
   - Pattern too broad
   - Need `pattern-not` exclusion

#### Debug Taint Mode Rules

```bash
semgrep --dataflow-traces --config <rule-id>.yaml <rule-id>.<ext>
```

Shows:
- Source locations
- Sink locations
- Data flow path
- Why taint didn't propagate (if applicable)

## Step 5: Iterate Until Tests Pass
Work on writing Semgrep rule (patterns) iteratively to ensure the Semgrep rule works correctly.

Each time when you introduce any changes, test Semgrep rule:

```bash
semgrep --test --config <rule-id>.yaml <rule-id>.<ext>
```

For debugging taint mode rules:
```bash
semgrep --dataflow-traces --config <rule-id>.yaml <rule-id>.<ext>
```

**Verification checkpoint**: Output MUST show "All tests passed". **Only proceed when validation passes**.


**Verification checkpoint**: Proceed to Step 6: Optimize the Rule when:
- "All tests passed"
- No "missed lines" (false negatives)
- No "incorrect lines" (false positives)

### Common Fixes

| Problem | Solution |
|---------|----------|
| Too many matches | Add `pattern-not` exclusions |
| Missing matches | Add `pattern-either` variants |
| Wrong line matched | Adjust `focus-metavariable` |
| Taint not flowing | Check sanitizers aren't too broad |
| Taint false positive | Add sanitizer pattern |

## Step 6: Optimize the Rule

After all tests pass, remove redundant patterns (quote variants, ellipsis subsets, redundant patterns).

### Semgrep Pattern Equivalences

Semgrep treats certain patterns as equivalent:

| Written | Also Matches | Reason |
|---------|--------------|--------|
| `"string"` | `'string'` | Quote style normalized (in languages where both are equivalent) |
| `func(...)` | `func()`, `func(a)`, `func(a,b)` | Ellipsis matches zero or more |
| `func($X, ...)` | `func($X)`, `func($X, a, b)` | Trailing ellipsis is optional |

### Common Redundancies to Remove

**1. Quote Variants** (depends on the language)

Before:
```yaml
pattern-either:
  - pattern: hashlib.new("md5", ...)
  - pattern: hashlib.new('md5', ...)
```

After:
```yaml
pattern-either:
  - pattern: hashlib.new("md5", ...)
```

**2. Ellipsis Subsets**

Before:
```yaml
pattern-either:
  - pattern: dangerous($X, ...)
  - pattern: dangerous($X)
  - pattern: dangerous($X, $Y)
```

After:
```yaml
pattern: dangerous($X, ...)
```

**3. Consolidate with Metavariables**

Before:
```yaml
pattern-either:
  - pattern: md5($X)
  - pattern: sha1($X)
  - pattern: sha256($X)
```

After:
```yaml
patterns:
  - pattern: $FUNC($X)
  - metavariable-regex:
      metavariable: $FUNC
      regex: ^(md5|sha1|sha256)$
```

### Optimization Checklist

1. Remove patterns differing only in quote style
2. Remove patterns that are subsets of `...` patterns
3. Consolidate similar patterns using metavariable-regex
4. Remove duplicate patterns in pattern-either
5. Simplify nested pattern-either when possible
6. Replace complex regex patterns with metavariable-comparison
7. **Re-run tests after each optimization**

### Verify After Optimization

```bash
semgrep --test --config <rule-id>.yaml <rule-id>.<ext>
```

**CRITICAL**: Always re-run tests after optimization. Some "redundant" patterns may actually be necessary due to AST structure differences. If any test fails, revert the optimization that caused it.

**Task complete ONLY when**: All tests pass after optimization.


## Step 7: Final Run
Run the Semgrep rule you created using: `semgrep --config <rule-id>.yaml <rule-id>.<ext>`.

Ensure that message:
 1. Contains a short and concise explanation of the matched pattern
 2. Has no uninterpolated metavariables (e.g., $OP, $VAR). All metavariables referenced in the message must be captured by the pattern so they interpolate to actual code.

Fix any message issues and re-run that Semgrep rule after each fix.
