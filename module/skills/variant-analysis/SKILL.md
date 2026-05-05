---
name: variant-analysis
description: Find similar vulnerabilities and bugs across codebases using pattern-based analysis. Use when hunting bug variants, building CodeQL/Semgrep queries, analyzing security vulnerabilities, or performing systematic code audits after finding an initial issue.
license: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
origin: Adapted from Trail of Bits Skills Marketplace (https://github.com/trailofbits/skills)
category: "security_auditing"
subcategory: "audit-workflow"
---

# Variant Analysis

You are a variant analysis expert. Your role is to help find similar vulnerabilities and bugs across a codebase after identifying an initial pattern.

## When to Use

Use this skill when:
- A vulnerability has been found and you need to search for similar instances
- Building or refining CodeQL/Semgrep queries for security patterns
- Performing systematic code audits after an initial issue discovery
- Hunting for bug variants across a codebase
- Analyzing how a single root cause manifests in different code paths

## When NOT to Use

Do NOT use this skill for:
- Initial vulnerability discovery (use audit-context-building or domain-specific audits instead)
- General code review without a known pattern to search for
- Writing fix recommendations (use issue-writer instead)
- Understanding unfamiliar code (use audit-context-building for deep comprehension first)

## The Five-Step Process

### Step 1: Understand the Original Issue

Before searching, deeply understand the known bug:
- **What is the root cause?** Not the symptom, but WHY it's vulnerable
- **What conditions are required?** Control flow, data flow, state
- **What makes it exploitable?** User control, missing validation, etc.

### Step 2: Create an Exact Match

Start with a pattern that matches ONLY the known instance:
```bash
rg -n "exact_vulnerable_code_here"
```
Verify: Does it match exactly ONE location (the original)?

### Step 3: Identify Abstraction Points

| Element | Keep Specific | Can Abstract |
|---------|---------------|--------------|
| Function name | If unique to bug | If pattern applies to family |
| Variable names | Never | Always use metavariables |
| Literal values | If value matters | If any value triggers bug |
| Arguments | If position matters | Use `...` wildcards |

### Step 4: Iteratively Generalize

**Change ONE element at a time:**
1. Run the pattern
2. Review ALL new matches
3. Classify: true positive or false positive?
4. If FP rate acceptable, generalize next element
5. If FP rate too high, revert and try different abstraction

**Stop when false positive rate exceeds ~50%**

### Step 5: Analyze and Triage Results

For each match, document:
- **Location**: File, line, function
- **Confidence**: High/Medium/Low
- **Exploitability**: Reachable? Controllable inputs?
- **Priority**: Based on impact and exploitability

For deeper strategic guidance, see **## Inlined: Variant Analysis Methodology** at the end of this document.

## Tool Selection

| Scenario | Tool | Why |
|----------|------|-----|
| Quick surface search | ripgrep | Fast, zero setup |
| Simple pattern matching | Semgrep | Easy syntax, no build needed |
| Data flow tracking | Semgrep taint / CodeQL | Follows values across functions |
| Cross-function analysis | CodeQL | Best interprocedural analysis |
| Non-building code | Semgrep | Works on incomplete code |

## Key Principles

1. **Root cause first**: Understand WHY before searching for WHERE
2. **Start specific**: First pattern should match exactly the known bug
3. **One change at a time**: Generalize incrementally, verify after each change
4. **Know when to stop**: 50%+ FP rate means you've gone too generic
5. **Search everywhere**: Always search the ENTIRE codebase, not just the module where the bug was found
6. **Expand vulnerability classes**: One root cause often has multiple manifestations

## Critical Pitfalls to Avoid

These common mistakes cause analysts to miss real vulnerabilities:

### 1. Narrow Search Scope

Searching only the module where the original bug was found misses variants in other locations.

**Example:** Bug found in `api/handlers/` → only searching that directory → missing variant in `utils/auth.py`

**Mitigation:** Always run searches against the entire codebase root directory.

### 2. Pattern Too Specific

Using only the exact attribute/function from the original bug misses variants using related constructs.

**Example:** Bug uses `isAuthenticated` check → only searching for that exact term → missing bugs using related properties like `isActive`, `isAdmin`, `isVerified`

**Mitigation:** Enumerate ALL semantically related attributes/functions for the bug class.

### 3. Single Vulnerability Class

Focusing on only one manifestation of the root cause misses other ways the same logic error appears.

**Example:** Original bug is "return allow when condition is false" → only searching that pattern → missing:
- Null equality bypasses (`null == null` evaluates to true)
- Documentation/code mismatches (function does opposite of what docs claim)
- Inverted conditional logic (wrong branch taken)

**Mitigation:** List all possible manifestations of the root cause before searching.

### 4. Missing Edge Cases

Testing patterns only with "normal" scenarios misses vulnerabilities triggered by edge cases.

**Example:** Testing auth checks only with valid users → missing bypass when `userId = null` matches `resourceOwnerId = null`

**Mitigation:** Test with: unauthenticated users, null/undefined values, empty collections, and boundary conditions.

## Resources

Ready-to-use CodeQL (`.ql`) and Semgrep (`.yaml`) rule templates and a variant report template ship with the upstream plugin.

*(See upstream Trail of Bits prodsec-skills `variant-analysis` plugin under `resources/codeql/` and `resources/semgrep/` for those files.)*

Use **## Inlined: Variant Report Template** at the end of this document for report structure.


---

## Inlined: Variant Analysis Methodology

# The Philosophy of Generic but Precise Variant Analysis

This document covers the strategic thinking behind effective variant analysis.

## Why Variants Exist

Vulnerabilities cluster because developers make consistent mistakes:

1. **Developer habits**: Same person writes similar code, makes similar errors
2. **Copy-paste propagation**: Boilerplate spreads bugs across the codebase
3. **API misuse patterns**: Complex APIs invite consistent misunderstandings
4. **Framework idioms**: Framework patterns create predictable vulnerability shapes
5. **Incomplete fixes**: Original bug fixed in one place, missed elsewhere

Understanding WHY variants exist helps predict WHERE to find them.

## Root Cause Analysis

Before searching, extract the essential vulnerability pattern:

### Ask These Questions

1. **What operation is dangerous?** (e.g., `eval()`, `system()`, raw SQL)
2. **What data makes it dangerous?** (e.g., user-controlled input)
3. **What's missing?** (e.g., sanitization, validation, bounds check)
4. **What context enables it?** (e.g., authentication state, error handling path)

### The Root Cause Statement

Formulate a clear statement:

> "This vulnerability exists because [UNTRUSTED DATA] reaches [DANGEROUS OPERATION] without [REQUIRED PROTECTION]."

Examples:
- "User input reaches `eval()` without sanitization"
- "Attacker-controlled size reaches `malloc()` without overflow check"
- "Untrusted path reaches `open()` without canonicalization"

This statement IS your search pattern.

## The Abstraction Ladder

Patterns exist at different abstraction levels. Start at Level 0 and climb.

### Level 0: Exact Match

Match the literal vulnerable code:

```python
# Original vulnerable code
query = "SELECT * FROM users WHERE id=" + request.args.get('id')
```

```bash
# Level 0 pattern
rg 'SELECT \* FROM users WHERE id=" \+ request\.args\.get'
```

- **Matches**: 1 (the original)
- **False positives**: 0
- **Value**: Confirms the bug exists, baseline for generalization

### Level 1: Variable Abstraction

Replace variable names with wildcards:

```yaml
# Level 1 pattern
pattern: $QUERY = "SELECT * FROM users WHERE id=" + $INPUT
```

- **Matches**: 3-5 (same query pattern, different variables)
- **False positives**: Low
- **Value**: Find copy-paste variants

### Level 2: Structural Abstraction

Generalize the structure:

```yaml
# Level 2 pattern
patterns:
  - pattern: $Q = "..." + $INPUT
  - pattern-inside: |
      def $FUNC(...):
        ...
        cursor.execute($Q)
```

- **Matches**: 10-30 (any string concat used in query)
- **False positives**: Medium
- **Value**: Find pattern variants

### Level 3: Semantic Abstraction

Abstract to the security property:

```yaml
# Level 3 pattern (taint mode)
mode: taint
pattern-sources:
  - pattern: request.args.get(...)
  - pattern: request.form.get(...)
pattern-sinks:
  - pattern: cursor.execute(...)
```

- **Matches**: 50-100+ (any user input to any query)
- **False positives**: High (many will have proper parameterization)
- **Value**: Comprehensive coverage, requires triage

### Choosing Your Level

| Goal | Recommended Level |
|------|-------------------|
| Verify a specific fix | Level 0 |
| Find copy-paste bugs | Level 1 |
| Audit a component | Level 2 |
| Full security assessment | Level 3 |

## The Generalization Process

### Rule: One Change at a Time

Never generalize multiple elements simultaneously:

```
BAD:  exact code -> fully abstract pattern
GOOD: exact code -> abstract var1 -> abstract var2 -> abstract operation
```

Each step:
1. Make ONE change
2. Run the pattern
3. Review ALL new matches
4. Decide: acceptable FP rate?
5. Continue or revert

### Decision Points

At each generalization step, ask:

**Should I abstract this variable name?**
- YES if: Different names could have same bug
- NO if: The name indicates a specific semantic meaning you want to preserve

**Should I abstract this literal value?**
- YES if: Any value would trigger the bug
- NO if: Only specific values (like `2` in a shift operation) are dangerous

**Should I use `...` wildcards?**
- YES if: Argument position doesn't matter
- NO if: Only specific argument positions are sinks

**Should I add taint tracking?**
- YES if: Need to verify data actually flows from source to sink
- NO if: Presence of pattern is sufficient evidence

## False Positive Management

### Acceptable FP Rates by Context

| Context | Acceptable FP Rate |
|---------|-------------------|
| Automated CI blocking | <5% |
| Developer warning | <20% |
| Security audit triage | <50% |
| Research/exploration | <80% |

### Common FP Sources and Filters

**Dead code**: Add reachability constraints
```yaml
pattern-not-inside: |
  if False:
    ...
```

**Test code**: Exclude test directories
```bash
rg "pattern" --glob '!**/test*' --glob '!**/*_test.*'
```

**Already sanitized**: Add sanitizer patterns
```yaml
pattern-not: dangerous_func(sanitize($X))
```

**Literal values**: Exclude non-user-controlled data
```yaml
pattern-not: dangerous_func("...")  # Literal string
```

## Multi-Repository Campaign

For large-scale hunts: **Recon** (ripgrep to find hotspots) → **Deep Analysis** (Semgrep/CodeQL on hotspots) → **Refinement** (reduce FPs) → **Automation** (CI-ready rules).

## Tracking Your Hunt

Maintain a tracking document:

```markdown
## Variant Analysis: [Original Bug ID]

### Root Cause
[Statement of the vulnerability pattern]

### Patterns Tried
| Pattern | Level | Matches | True Pos | False Pos | Notes |
|---------|-------|---------|----------|-----------|-------|
| exact   | 0     | 1       | 1        | 0         | Baseline |
| ...     | ...   | ...     | ...      | ...       | ...   |

### Confirmed Variants
| Location | Severity | Status | Notes |
|----------|----------|--------|-------|
| file:line| High     | Fixed  | ...   |

### False Positive Patterns
- Pattern X: Always FP because [reason]
- Pattern Y: FP in [context] but TP in [context]
```

## Anti-Patterns to Avoid

### Starting Too Generic

**Wrong**: Jump straight to semantic analysis
**Right**: Start with exact match, generalize incrementally

### Generalizing Everything

**Wrong**: Abstract all elements at once
**Right**: Abstract one element, verify, repeat

### Ignoring False Positives

**Wrong**: "I'll triage later"
**Right**: Analyze FPs immediately, they guide pattern refinement

### Tool Loyalty

**Wrong**: "I only use CodeQL"
**Right**: Use ripgrep for recon, Semgrep for iteration, CodeQL for precision

### Pattern Hoarding

**Wrong**: Keep all patterns regardless of FP rate
**Right**: Delete patterns that don't provide value

## Expanding Vulnerability Classes

A single root cause can manifest in multiple ways. Before concluding your search, systematically expand to related vulnerability classes.

### The Expansion Checklist

For each root cause, ask:

1. **What other attributes/functions have similar semantics?**
   - If bug involves `isAuthenticated`, also check: `isActive`, `isAdmin`, `isVerified`, `isLoggedIn`
   - If bug involves `userId`, also check: `ownerId`, `creatorId`, `authorId`

2. **What other boolean logic errors could occur?**
   - Inverted conditions (`if not x` vs `if x`)
   - Wrong default return value (`return true` vs `return false`)
   - Short-circuit evaluation errors

3. **What edge cases exist for the data types involved?**
   - Null/None/undefined comparisons
   - Empty string vs null
   - Zero vs null
   - Empty array/collection

4. **What documentation mismatches could exist?**
   - Function does opposite of docstring
   - Parameter meaning inverted
   - Return value semantics reversed

### Semantic Analysis

Some bugs can only be found by comparing code behavior to documented intent:

**Pattern:** Function name or docstring suggests one behavior, code does another

```python
# Docstring says "Returns True if access should be DENIED"
# But code returns True when user HAS permission (should be allowed)
def check_restricted_permission(user, perm):
    """Returns True if access should be DENIED."""
    if user.has_perm(perm):
        return True  # BUG: This grants access to users with permission
    return False
```

**Detection strategy:**
1. Search for functions with "deny", "restrict", "block", "forbid" in names
2. Manually verify return value semantics match the name/docs
3. Create rules that flag suspicious patterns for manual review

### Null Equality Bypasses

A common class of authorization bypass:

```python
# If anonymous_user.id is None and guest_order.owner_id is None
# Then None == None evaluates to True, bypassing the check
if order.owner_id == current_user.id:
    return True  # Allows access
```

**Detection strategy:**
1. Find all owner/permission checks using equality comparisons
2. Trace what values the compared fields can have
3. Check if both sides can be null simultaneously

## Summary: The Expert Mindset

1. **Understand before searching**: Root cause analysis is non-negotiable
2. **Start specific**: Your first pattern should match exactly one thing
3. **Climb the ladder**: Generalize one step at a time
4. **Measure as you go**: Track matches and FP rates at each step
5. **Know when to stop**: High FP rate means you've gone too far
6. **Iterate ruthlessly**: Refine patterns based on what you learn
7. **Document everything**: Your tracking doc is as valuable as your patterns
8. **Expand vulnerability classes**: One root cause has many manifestations
9. **Check semantics**: Verify code matches documentation intent
10. **Test edge cases**: Null values and boundary conditions reveal hidden bugs


---

## Inlined: Variant Report Template

# Variant Analysis Report

## Summary

| Field | Value |
|-------|-------|
| **Original Bug** | [BUG_ID / CVE] |
| **Analysis Date** | [DATE] |
| **Codebase** | [REPO/PROJECT] |
| **Variants Found** | [COUNT] |

## Original Vulnerability

**Root Cause:** [e.g., "User input reaches SQL query without parameterization"]

**Location:** `[path/to/file.py:LINE]` in `function_name()`

```python
# Vulnerable code
```

## Search Methodology

| Version | Pattern | Tool | Matches | TP | FP |
|---------|---------|------|---------|----|----|
| v1 | [exact] | ripgrep | 1 | 1 | 0 |
| v2 | [abstract] | semgrep | N | N | N |

**Final Pattern:**
```yaml
# Pattern used
```

## Findings

### Variant #1: [BRIEF_TITLE]

| Severity | Confidence | Status |
|----------|------------|--------|
| High | High | Confirmed |

**Location:** `[path/to/file.py:LINE]`

```python
# Vulnerable code
```

**Analysis:** [Why this is a true/false positive]

**Exploitability:**
- [ ] Reachable from external input
- [ ] User-controlled data
- [ ] No sanitization

---

<!-- Copy variant template above for additional findings -->

## False Positive Patterns

| Pattern | Count | Reason |
|---------|-------|--------|
| [pattern] | N | [why safe] |

## Recommendations

### Immediate
1. Fix variant in [location]

### Preventive
1. Add Semgrep rule to CI

```yaml
# CI-ready rule
```
