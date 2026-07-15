---
name: ai-code-review
description: >
  Security-focused review of AI-generated or AI-assisted code. Use when
  reviewing code produced by AI coding assistants, auditing AI-generated
  patches, verifying AI-assisted contributions before merge, or when a
  review needs to account for failure modes specific to AI code generation.
metadata:
  category: security_auditing
  subcategory: audit-workflow
---

# AI-Generated Code Security Review

Security review checklist and methodology for code produced by AI
coding assistants (Claude, Copilot, Cursor, Gemini, or any LLM-based
tool). AI-generated code has characteristic failure modes that differ
from human-written code and require specific review attention.

## When to Use

- Reviewing PRs or patches marked with `Assisted-by:` or
  `Generated-by:` attribution
- Auditing code known or suspected to be AI-generated
- As a supplementary checklist during any code review where AI
  assistance was used
- Verifying AI-generated security fixes or test code

## When NOT to Use

- General code review without AI involvement (use
  `module/skills/differential-review/SKILL.md`)
- Reviewing AI model behavior or prompt injection (use
  `module/skills/prompt-injection-mitigation/SKILL.md`)
- Evaluating AI tool security posture (use
  `module/skills/third-party-model-security/SKILL.md`
  or `module/skills/file-protection/SKILL.md`)

## AI-Specific Failure Modes

AI code generation has characteristic error patterns that differ
from typical human mistakes. Review for these specifically:

### 1. Hallucinated APIs and symbols

LLMs confidently generate calls to functions, methods, flags,
configuration keys, or library features that do not exist. These
compile or parse without errors but fail at runtime, or worse,
silently do nothing.

**Detection:**
- Verify every imported module, function call, and configuration
  key against the actual codebase and library documentation
- Check that method signatures match (argument count, types,
  return values)
- Search the project for the symbol: `rg "function_name"` — if
  it only appears in the new code, it may be hallucinated
- Check library version: AI may reference APIs from a different
  version than what the project uses

**Security impact:** A hallucinated security function (e.g., a
nonexistent `sanitize_input()` call) provides zero protection
while giving the appearance of safety.

### 2. Plausible-but-wrong logic

AI generates code that reads naturally and appears correct but
contains subtle logical errors — inverted conditions, off-by-one
errors, wrong comparison operators, or incorrect state transitions.
These are harder to catch than obviously broken code because they
pass casual reading.

**Detection:**
- Trace every conditional branch: does the True branch do what
  the variable name and context suggest?
- Check comparison operators: `<` vs `<=`, `==` vs `!=`,
  `and` vs `or`
- Verify loop bounds and termination conditions
- Check that error handling goes to the right branch (reject
  vs allow)

**Security impact:** An inverted authorization check
(`if user.is_admin` instead of `if not user.is_admin`) grants
access to everyone. The code reads plausibly either way.

### 3. Pattern drift from project conventions

AI generates code that follows general best practices but
diverges from the specific patterns, idioms, and conventions of
the project. This introduces inconsistency that makes the
codebase harder to audit and may bypass project-specific
security mechanisms.

**Detection:**
- Compare the new code against existing code doing similar
  things in the same project
- Check that the same base classes, decorators, middleware,
  and utility functions are used
- Verify that project-specific security patterns (custom
  validators, auth decorators, logging wrappers) are used
  instead of generic alternatives

**Security impact:** Using a generic auth check instead of the
project's custom auth decorator may skip logging, rate limiting,
or additional validation that the project relies on.

### 4. Incomplete error handling

AI often generates a working happy path but handles errors
with generic catch-all blocks, swallowed exceptions, or missing
cleanup. Error paths are where security vulnerabilities hide.

**Detection:**
- Check every `try/catch`, `except`, or error return: does
  it handle the error meaningfully or just log and continue?
- Verify that partial state is rolled back on failure
- Check that error responses do not leak internal details
  (stack traces, file paths, SQL queries, internal IPs)
- Verify that resources (connections, file handles, locks)
  are released on all code paths

**Security impact:** A swallowed authentication error may allow
an unauthenticated request to proceed. A missing rollback may
leave the system in an inconsistent state exploitable by a
subsequent request.

### 5. Stale or incorrect dependency usage

AI training data has a cutoff. Generated code may use deprecated
APIs, insecure defaults from older library versions, or patterns
that were correct in a previous version but are now vulnerable.

**Detection:**
- Check the project's actual dependency versions against what
  the AI code assumes
- Look for deprecated function calls or removed APIs
- Verify that security-relevant defaults match the current
  library version (e.g., TLS version, hash algorithm defaults)

**Security impact:** Using a deprecated crypto API with known
weaknesses, or relying on a default that changed from insecure
to secure (or vice versa) between versions.

### 6. Abandoned scaffolding

AI generates unfinished-work comments, placeholder implementations,
commented-out code blocks, or "temporary" workarounds that are
intended to be replaced but get committed as-is.

**Detection:**
- Search (case-insensitively) for `todo`, `fixme`, `hack`,
  `temporary`, `xxx` markers
- Look for commented-out code blocks
- Check for placeholder values (e.g., a password assigned `changeme`,
  a secret key assigned `development`)
- Verify that all functions have real implementations, not
  `pass` or `return None` stubs

**Security impact:** A placeholder secret, a disabled
validation, or a stub authentication function shipped to
production.

## Review Checklist

For each AI-generated or AI-assisted change:

### Verification

- [ ] All function calls, imports, and config keys verified
  against the actual codebase and dependency versions
- [ ] No hallucinated APIs or symbols
- [ ] Method signatures match (argument count, types, returns)

### Logic correctness

- [ ] Every conditional branch traced and verified
- [ ] Comparison operators correct (`<` vs `<=`, `==` vs `!=`)
- [ ] Authorization checks grant/deny the correct direction
- [ ] Loop termination conditions correct

### Project consistency

- [ ] Uses project-specific security patterns (not generic
  alternatives)
- [ ] Matches existing code style, base classes, and idioms
- [ ] Uses the same error handling patterns as surrounding code

### Error handling

- [ ] No swallowed exceptions on security-relevant paths
- [ ] Partial state rolled back on failure
- [ ] Error responses do not leak internal details
- [ ] Resources released on all code paths

### Completeness

- [ ] No to-do/fix-me/hack markers left in security-critical code
- [ ] No placeholder secrets or credentials
- [ ] No commented-out code that should be either deleted or
  uncommented
- [ ] No stub implementations (`pass`, `return None`, `throw
  new NotImplementedException()`)

### Security tests

- [ ] Tests actually fail before the fix (not tautologies)
- [ ] Assertions verify the security property, not just "no
  exception"
- [ ] Test credentials match the real threat model
- [ ] Mock objects do not mask the behavior being tested

## Output Format

For each finding:

| Field | Content |
|-------|---------|
| **Category** | Hallucinated API / Plausible-but-wrong / Pattern drift / Incomplete error handling / Stale dependency / Abandoned scaffolding |
| **Location** | File and line range |
| **Finding** | What is wrong or risky |
| **Evidence** | Why you believe it (missing symbol, inverted logic, project pattern not followed) |
| **Severity** | Critical / High / Medium / Low / Nit |
| **Suggestion** | Concrete fix |

## Relationship to Other Skills

- **`module/skills/differential-review/SKILL.md`** — General security-focused code review.
  This skill adds AI-specific failure modes on top.
- **`module/skills/fp-check/SKILL.md`** — When an AI-generated security finding is
  itself suspect, use fp-check to verify it.
- **`module/skills/inconsistency-detection/SKILL.md`** — AI-generated code that drifts
  from project patterns creates exactly the kind of inconsistency
  this technique detects.
