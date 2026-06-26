---
name: inconsistency-detection
description: >
  Find new vulnerabilities by comparing similar implementations within a codebase
  before any bug is known. Use when auditing sibling functions, parallel handlers,
  middleware variants, API endpoints with similar responsibilities, or any set of
  components that should enforce the same security invariants but may not.
category: "security_auditing"
subcategory: "audit-workflow"
---

# Inconsistency-Based Vulnerability Discovery

Find security vulnerabilities by detecting asymmetries between functionally
similar code. When two implementations do the same job but one lacks a
security guard the other has, the inconsistent one is usually the bug.

This technique operates **before any known bug** — it discovers new
vulnerabilities rather than searching for variants of an existing one.
For pattern hunting after a known bug, use `module/skills/variant-analysis/SKILL.md`.

## When to Use

- Auditing a codebase or module for the first time
- Reviewing code that has multiple implementations of similar logic
  (middlewares, drivers, handlers, API endpoints, policy enforcement points)
- After reading any code — as a systematic "what did I notice?" pass
- When a new vulnerability is found and you want to check if siblings
  are also affected

## When NOT to Use

- Searching for variants of a specific known bug (use `module/skills/variant-analysis/SKILL.md`)
- Building deep context for an unfamiliar codebase (use `module/skills/audit-context-building/SKILL.md`)
- Verifying whether a specific finding is a true positive (use `module/skills/fp-check/SKILL.md`)

## Why Inconsistencies Are Vulnerabilities

Codebases develop security invariants organically. When a validation
step, sanitization call, or authorization check appears in most
implementations but is missing from one, the absence is rarely
intentional — it is typically an oversight that becomes exploitable.

Real-world example: a project had two authentication middlewares.
One called `remove_auth_headers()` at request start to prevent header
spoofing. The other did not. A spoofed admin-privilege header survived
uncleared through the second middleware, producing a privilege
escalation vulnerability.

## The Three-Step Process

### Step 1 — Find sibling implementations

Identify groups of code that serve the same functional role. Common
families and search patterns:

```bash
# Middleware / interceptors
rg "class.*Middleware|def process_request|func.*Handler"

# API endpoint handlers
rg "def post|def get|def delete|@app.route|@router"

# Policy enforcement points
rg "enforce|authorize|check_permission|has_role"

# Input validators
rg "validate|sanitize|clean|escape"

# Auth token handlers
rg "verify_token|decode_jwt|authenticate"

# Error/cleanup handlers
rg "except|catch|finally|defer|rollback"

# Credential creators
rg "create_credential|generate_key|issue_token"
```

List all members of each family. The goal is exhaustive enumeration —
missing one sibling means missing a potential vulnerability.

### Step 2 — Compare security-relevant properties

For each family, build a comparison matrix. Check whether each member
has or lacks each property:

| Property | Impl A | Impl B | Impl C |
|----------|--------|--------|--------|
| Sanitizes input headers | Yes | Yes | **No** |
| Enforces authorization policy | Yes | Yes | Yes |
| Validates request body | Yes | **No** | Yes |
| Logs security events | Yes | Yes | **No** |
| Rolls back on failure | Yes | Yes | **No** |
| Checks credential restrictions | Yes | **No** | Yes |

Any cell marked **No** when its column-mates are Yes is a finding
candidate.

**Properties to compare** (adapt per codebase):

- **Header/input sanitization**: Does every entry point strip or
  validate untrusted headers, query params, or body fields?
- **Authorization enforcement**: Is the same policy rule checked on
  every HTTP method for the same resource (GET, POST, PUT, DELETE)?
- **Credential restriction checks**: Do all write operations verify
  that restricted credentials cannot perform privileged actions?
- **Error handling and cleanup**: Do all code paths roll back partial
  state on failure, or do some leave inconsistent state?
- **TLS certificate validation**: Do all HTTP clients validate
  certificates, or do some pass `verify=False` or equivalent?
- **Logging**: Do all error paths log the event, or do some swallow
  exceptions silently?
- **Rate limiting / resource bounds**: Do all endpoints enforce limits,
  or are some unprotected?

### Step 3 — Investigate and triage each asymmetry

For each inconsistency found:

1. **Determine if intentional**: Read git blame, commit messages, and
   comments. Some asymmetries are deliberate (documented exceptions).
2. **Assess exploitability**: Can an attacker reach the inconsistent
   code path? What privilege level is required? What is the impact?
3. **Write a failing test**: If the inconsistency is exploitable,
   write a test that demonstrates the vulnerability before writing
   the fix (prove it, then fix it).
4. **Check for broader impact**: Does the same asymmetry pattern
   appear in other parts of the codebase? Search beyond the
   immediate family.

## Output Format

For each finding:

| Field | Content |
|-------|---------|
| **Family** | The group of siblings compared (e.g., "auth middlewares") |
| **Inconsistency** | What property is present in siblings but absent here |
| **Location** | File and line range of the inconsistent implementation |
| **Siblings** | File and line range of implementations that have the property |
| **Severity** | Critical / High / Medium / Low |
| **Exploitability** | How an attacker would reach and exploit this gap |
| **Evidence** | Git blame, code references, missing call |

## Systematic Questions to Ask

After reading any code during an audit, pause and ask:

**Inconsistency across similar components:**
- Is there a security guard that one implementation has and its sibling
  doing the same job lacks?
- Does every function accepting untrusted input validate it the same way?
- Are error handling and cleanup paths consistent across similar operations?

**Trust boundaries:**
- Where does untrusted data enter? Does every entry point treat it as
  untrusted, or do some assume it was already sanitized upstream?
- Which components reset or clear state at the start of each request?
  Are there outliers that do not?

**Authorization completeness:**
- Is the same policy rule enforced on GET, POST, PUT, DELETE for the
  same resource — or only some HTTP methods?
- For each new endpoint, is there a corresponding authorization rule?

**Dataflow:**
- Trace untrusted input (header, URL parameter, JSON field, LDAP
  attribute) through the call chain. Where could it land without
  being validated?

## Broader Patterns

Beyond the specific inconsistency, the comparative technique
generalizes to any security-relevant property:

| Pattern | Question to ask |
|---------|----------------|
| Authorization guards | Which endpoints enforce authorization and which do not? |
| Input validation | Which API methods validate the request body and which trust it? |
| Credential checks | Which operations check credential restrictions and which skip? |
| Logging | Which error paths log the exception and which swallow it? |
| Rollback | Which DB operations roll back on failure and which leave partial state? |
| TLS validation | Which HTTP clients validate certificates and which skip verification? |

Any asymmetry in a security-relevant pattern is worth investigating.

## Relationship to Other Skills

- **`module/skills/variant-analysis/SKILL.md`** — Starts from a known bug and searches for
  variants. This skill starts from no known bug and discovers new ones
  by detecting asymmetries. They are complementary: inconsistency
  detection finds the first bug; variant analysis finds the rest.
- **`module/skills/audit-context-building/SKILL.md`** — Builds deep understanding of a
  codebase. Run it first to identify families of similar code, then
  apply this skill to compare them.
- **`module/skills/differential-review/SKILL.md`** — Reviews changes in a diff. This skill
  reviews the codebase holistically, not just what changed.
