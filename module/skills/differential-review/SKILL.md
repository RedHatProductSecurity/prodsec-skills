---
name: differential-review
description: >
  Performs security-focused differential review of code changes (PRs, commits, diffs).
  Adapts analysis depth to codebase size, uses git history for context, calculates
  blast radius, checks test coverage, and generates comprehensive markdown reports.
  Automatically detects and prevents security regressions.
license: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
origin: Adapted from Trail of Bits Skills Marketplace (https://github.com/trailofbits/skills)
category: "security_auditing"
subcategory: "audit-workflow"
---

# Differential Security Review

Security-focused code review for PRs, commits, and diffs.

## Core Principles

1. **Risk-First**: Focus on auth, crypto, value transfer, external calls
2. **Evidence-Based**: Every finding backed by git history, line numbers, attack scenarios
3. **Adaptive**: Scale to codebase size (SMALL/MEDIUM/LARGE)
4. **Honest**: Explicitly state coverage limits and confidence level
5. **Output-Driven**: Always generate comprehensive markdown report file

---

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Small PR, quick review" | Heartbleed was 2 lines | Classify by RISK, not size |
| "I know this codebase" | Familiarity breeds blind spots | Build explicit baseline context |
| "Git history takes too long" | History reveals regressions | Never skip Phase 1 |
| "Blast radius is obvious" | You'll miss transitive callers | Calculate quantitatively |
| "No tests = not my problem" | Missing tests = elevated risk rating | Flag in report, elevate severity |
| "Just a refactor, no security impact" | Refactors break invariants | Analyze as HIGH until proven LOW |
| "I'll explain verbally" | No artifact = findings lost | Always write report |

---

## Quick Reference

### Codebase Size Strategy

| Codebase Size | Strategy | Approach |
|---------------|----------|----------|
| SMALL (<20 files) | DEEP | Read all deps, full git blame |
| MEDIUM (20-200) | FOCUSED | 1-hop deps, priority files |
| LARGE (200+) | SURGICAL | Critical paths only |

### Risk Level Triggers

| Risk Level | Triggers |
|------------|----------|
| HIGH | Auth, crypto, external calls, value transfer, validation removal |
| MEDIUM | Business logic, state changes, new public APIs |
| LOW | Comments, tests, UI, logging |

---

## Workflow Overview

```
Pre-Analysis → Phase 0: Triage → Phase 1: Code Analysis → Phase 2: Test Coverage
    ↓              ↓                    ↓                        ↓
Phase 3: Blast Radius → Phase 4: Deep Context → Phase 5: Adversarial → Phase 6: Report
```

---

## Decision Tree

**Starting a review?**

```
├─ Need detailed phase-by-phase methodology?
│  └─ Jump to: [Differential Review Methodology](#differential-review-methodology)
│     (Pre-Analysis + Phases 0-4: triage, code analysis, test coverage, blast radius)
│
├─ Analyzing HIGH RISK change?
│  └─ Jump to: [Adversarial Vulnerability Analysis (Phase 5)](#adversarial-vulnerability-analysis-phase-5)
│
├─ Writing the final report?
│  └─ Jump to: [Report Generation (Phase 6)](#report-generation-phase-6)
│
├─ Looking for specific vulnerability patterns?
│  └─ Jump to: [Common Vulnerability Patterns](#common-vulnerability-patterns)
│
└─ Quick triage only?
   └─ Use Quick Reference above, skip detailed docs
```

---

## Quality Checklist

Before delivering:

- [ ] All changed files analyzed
- [ ] Git blame on removed security code
- [ ] Blast radius calculated for HIGH risk
- [ ] Attack scenarios are concrete (not generic)
- [ ] Findings reference specific line numbers + commits
- [ ] Report file generated
- [ ] User notified with summary

---

## Integration

**audit-context-building** (`audit-context-building.md` in this folder):
- Pre-Analysis: Build baseline context
- Phase 4: Deep context on HIGH RISK changes

**Formal reporting:** Transform findings into formal audit reports using your team's workflow.

*(See upstream Trail of Bits prodsec-skills for the `issue-writer` companion skill if you use that distribution.)*

---

## Example Usage

### Quick Triage (Small PR)
```
Input: 5 file PR, 2 HIGH RISK files
Strategy: Use Quick Reference
1. Classify risk level per file (2 HIGH, 3 LOW)
2. Focus on 2 HIGH files only
3. Git blame removed code
4. Generate minimal report
Time: ~30 minutes
```

### Standard Review (Medium Codebase)
```
Input: 80 files, 12 HIGH RISK changes
Strategy: FOCUSED (see [Differential Review Methodology](#differential-review-methodology))
1. Full workflow on HIGH RISK files
2. Surface scan on MEDIUM
3. Skip LOW risk files
4. Complete report with all sections
Time: ~3-4 hours
```

### Deep Audit (Large, Critical Change)
```
Input: 450 files, auth system rewrite
Strategy: SURGICAL + audit-context-building
1. Baseline context with audit-context-building
2. Deep analysis on auth changes only
3. Blast radius analysis
4. Adversarial modeling
5. Comprehensive report
Time: ~6-8 hours
```

---

## When NOT to Use This Skill

- **Greenfield code** (no baseline to compare)
- **Documentation-only changes** (no security impact)
- **Formatting/linting** (cosmetic changes)
- **User explicitly requests quick summary only** (they accept risk)

For these cases, use standard code review instead.

---

## Red Flags (Stop and Investigate)

**Immediate escalation triggers:**
- Removed code from "security", "CVE", or "fix" commits
- Access control modifiers removed (onlyOwner, internal → external)
- Validation removed without replacement
- External calls added without checks
- High blast radius (50+ callers) + HIGH risk change

These patterns require adversarial analysis even in quick triage.

---

## Tips for Best Results

**Do:**
- Start with git blame for removed code
- Calculate blast radius early to prioritize
- Generate concrete attack scenarios
- Reference specific line numbers and commits
- Be honest about coverage limitations
- Always generate the output file

**Don't:**
- Skip git history analysis
- Make generic findings without evidence
- Claim full analysis when time-limited
- Forget to check test coverage
- Miss high blast radius changes
- Output report only to chat (file required)

---

## Supporting Documentation (in this file)

- [Differential Review Methodology](#differential-review-methodology) — Phases 0-4
- [Adversarial Vulnerability Analysis (Phase 5)](#adversarial-vulnerability-analysis-phase-5)
- [Report Generation (Phase 6)](#report-generation-phase-6)
- [Common Vulnerability Patterns](#common-vulnerability-patterns)

---

**For first-time users:** Start with [Differential Review Methodology](#differential-review-methodology).

**For experienced users:** Use this page's Quick Reference and Decision Tree to jump to the section you need.


---

# Differential Review Methodology

Detailed phase-by-phase workflow for security-focused code review.

## Pre-Analysis: Baseline Context Building

**FIRST ACTION - Build complete baseline understanding:**

If the **audit-context-building** workflow is available (see `audit-context-building.md` in this folder):

1. Check out the baseline commit: `git checkout <baseline_commit>`
2. Apply ultra-granular context building to the entire relevant scope (e.g. `packages/contracts/contracts/` for Solidity, `src/` for Rust, or repository root).
3. Focus on invariants, trust boundaries, validation patterns, call graphs, and state flows.

*(See upstream Trail of Bits prodsec-skills for companion automation or agent wiring.)*

**Capture from baseline analysis:**
- System-wide invariants (what must ALWAYS be true across all code)
- Trust boundaries and privilege levels (who can do what)
- Validation patterns (what gets checked where - defense-in-depth)
- Complete call graphs for critical functions (who calls what)
- State flow diagrams (how state changes)
- External dependencies and trust assumptions

**Why this matters:**
- Understand what the code was SUPPOSED to do before changes
- Identify implicit security assumptions in baseline
- Detect when changes violate baseline invariants
- Know which patterns are system-wide vs local
- Catch when changes break defense-in-depth

**Store baseline context for reference during differential analysis.**

After baseline analysis, checkout back to head commit to analyze changes.

---

## Phase 0: Intake & Triage

**Extract changes:**
```bash
# For commit range
git diff <base>..<head> --stat
git log <base>..<head> --oneline

# For PR
gh pr view <number> --json files,additions,deletions

# Get all changed files
git diff <base>..<head> --name-only
```

**Assess codebase size:**
```bash
find . -name "*.sol" -o -name "*.rs" -o -name "*.go" -o -name "*.ts" | wc -l
```

**Classify complexity:**
- **SMALL**: <20 files → Deep analysis (read all deps)
- **MEDIUM**: 20-200 files → Focused analysis (1-hop deps)
- **LARGE**: 200+ files → Surgical (critical paths only)

**Risk score each file:**
- **HIGH**: Auth, crypto, external calls, value transfer, validation removal
- **MEDIUM**: Business logic, state changes, new public APIs
- **LOW**: Comments, tests, UI, logging

---

## Phase 1: Changed Code Analysis

For each changed file:

1. **Read both versions** (baseline and changed)

2. **Analyze each diff region:**
   ```
   BEFORE: [exact code]
   AFTER: [exact code]
   CHANGE: [behavioral impact]
   SECURITY: [implications]
   ```

3. **Git blame removed code:**
   ```bash
   # When was it added? Why?
   git log -S "removed_code" --all --oneline
   git blame <baseline> -- file.sol | grep "pattern"
   ```

   **Red flags:**
   - Removed code from "fix", "security", "CVE" commits → CRITICAL
   - Recently added (<1 month) then removed → HIGH

4. **Check for regressions (re-added code):**
   ```bash
   git log -S "added_code" --all -p
   ```

   Pattern: Code added → removed for security → re-added now = REGRESSION

5. **Micro-adversarial analysis** for each change:
   - What attack did removed code prevent?
   - What new surface does new code expose?
   - Can modified logic be bypassed?
   - Are checks weaker? Edge cases covered?

6. **Generate concrete attack scenarios:**
   ```
   SCENARIO: [attack goal]
   PRECONDITIONS: [required state]
   STEPS:
     1. [specific action]
     2. [expected outcome]
     3. [exploitation]
   WHY IT WORKS: [reference code change]
   IMPACT: [severity + scope]
   ```

---

## Phase 2: Test Coverage Analysis

**Identify coverage gaps:**
```bash
# Production code changes (exclude tests)
git diff <range> --name-only | grep -v "test"

# Test changes
git diff <range> --name-only | grep "test"

# For each changed function, search for tests
grep -r "test.*functionName" test/ --include="*.sol" --include="*.js"
```

**Risk elevation rules:**
- NEW function + NO tests → Elevate risk MEDIUM→HIGH
- MODIFIED validation + UNCHANGED tests → HIGH RISK
- Complex logic (>20 lines) + NO tests → HIGH RISK

---

## Phase 3: Blast Radius Analysis

**Calculate impact:**
```bash
# Count callers for each modified function
grep -r "functionName(" --include="*.sol" . | wc -l
```

**Classify blast radius:**
- 1-5 calls: LOW
- 6-20 calls: MEDIUM
- 21-50 calls: HIGH
- 50+ calls: CRITICAL

**Priority matrix:**

| Change Risk | Blast Radius | Priority | Analysis Depth |
|-------------|--------------|----------|----------------|
| HIGH | CRITICAL | P0 | Deep + all deps |
| HIGH | HIGH/MEDIUM | P1 | Deep |
| HIGH | LOW | P2 | Standard |
| MEDIUM | CRITICAL/HIGH | P1 | Standard + callers |

---

## Phase 4: Deep Context Analysis

**If the audit-context-building workflow is available**, use it on the changed function and its dependencies to help answer the questions below. Scope the file(s) containing the changed function; focus on flow analysis, call graphs, invariants, and root cause.

*(See upstream Trail of Bits prodsec-skills for companion automation.)*

**That workflow helps you answer:**

1. **Map complete function flow:**
   - Entry conditions (preconditions, requires, modifiers)
   - State reads (which variables accessed)
   - State writes (which variables modified)
   - External calls (to contracts, APIs, system)
   - Return values and side effects

2. **Trace internal calls:**
   - List all functions called
   - Recursively map their flows
   - Build complete call graph

3. **Trace external calls:**
   - Identify trust boundaries crossed
   - List assumptions about external behavior
   - Check for reentrancy risks

4. **Identify invariants:**
   - What must ALWAYS be true?
   - What must NEVER happen?
   - Are invariants maintained after changes?

5. **Five Whys root cause:**
   - WHY was this code changed?
   - WHY did the original code exist?
   - WHY might this break?
   - WHY is this approach chosen?
   - WHY could this fail in production?

**If that workflow is not used**, manually perform the line-by-line analysis above using your editor, search, and code tracing.

**Cross-cutting pattern detection:**
```bash
# Find repeated validation patterns
grep -r "require.*amount > 0" --include="*.sol" .
grep -r "onlyOwner" --include="*.sol" .

# Check if any removed in diff
git diff <range> | grep "^-.*require.*amount > 0"
```

**Flag if removal breaks defense-in-depth.**

---

**Next steps:**
- For HIGH RISK changes, proceed to [Adversarial Vulnerability Analysis (Phase 5)](#adversarial-vulnerability-analysis-phase-5)
- For report generation, see [Report Generation (Phase 6)](#report-generation-phase-6)


---

# Adversarial Vulnerability Analysis (Phase 5)

Structured methodology for finding vulnerabilities through attacker modeling.

**When to use:** After completing deep context analysis (Phase 4), apply this to all HIGH RISK changes.

---

## 1. Define Specific Attacker Model

**WHO is the attacker?**
- Unauthenticated external user
- Authenticated regular user
- Malicious administrator
- Compromised contract/service
- Front-runner/MEV bot

**WHAT access/privileges do they have?**
- Public API access only
- Authenticated user role
- Specific permissions/tokens
- Contract call capabilities

**WHERE do they interact with the system?**
- Specific HTTP endpoints
- Smart contract functions
- RPC interfaces
- External APIs

---

## 2. Identify Concrete Attack Vectors

```
ENTRY POINT: [Exact function/endpoint attacker can access]

ATTACK SEQUENCE:
1. [Specific API call/transaction with parameters]
2. [How this reaches the vulnerable code]
3. [What happens in the vulnerable code]
4. [Impact achieved]

PROOF OF ACCESSIBILITY:
- Show the function is public/external
- Demonstrate attacker has required permissions
- Prove attack path exists through actual interfaces
```

---

## 3. Rate Realistic Exploitability

**EASY:** Exploitable via public APIs with no special privileges
- Single transaction/call
- Common user access level
- No complex conditions required

**MEDIUM:** Requires specific conditions or elevated privileges
- Multiple steps or timing requirements
- Elevated but obtainable privileges
- Specific system state needed

**HARD:** Requires privileged access or rare conditions
- Admin/owner privileges needed
- Rare edge case conditions
- Significant resources required

---

## 4. Build Complete Exploit Scenario

```
ATTACKER STARTING POSITION:
[What the attacker has at the beginning]

STEP-BY-STEP EXPLOITATION:
Step 1: [Concrete action through accessible interface]
  - Command: [Exact call/request]
  - Parameters: [Specific values]
  - Expected result: [What happens]

Step 2: [Next action]
  - Command: [Exact call/request]
  - Why this works: [Reference to code change]
  - System state change: [What changed]

Step 3: [Final impact]
  - Result: [Concrete harm achieved]
  - Evidence: [How to verify impact]

CONCRETE IMPACT:
[Specific, measurable impact - not "could cause issues"]
- Exact amount of funds drained
- Specific privileges escalated
- Particular data exposed
```

---

## 5. Cross-Reference with Baseline Context

From baseline analysis (see [Differential Review Methodology](#differential-review-methodology)), check:
- Does this violate a system-wide invariant?
- Does this break a trust boundary?
- Does this bypass a validation pattern?
- Is this a regression of a previous fix?

---

## Vulnerability Report Template

Generate this for each finding:

```markdown
## [SEVERITY] Vulnerability Title

**Attacker Model:**
- WHO: [Specific attacker type]
- ACCESS: [Exact privileges]
- INTERFACE: [Specific entry point]

**Attack Vector:**
[Step-by-step exploit through accessible interfaces]

**Exploitability:** EASY/MEDIUM/HARD
**Justification:** [Why this rating]

**Concrete Impact:**
[Specific, measurable harm - not theoretical]

**Proof of Concept:**
```code
// Exact code to reproduce
```

**Root Cause:**
[Reference specific code change at file.sol:L123]

**Blast Radius:** [N callers affected]
**Baseline Violation:** [Which invariant/pattern broken]
```

---

## Example: Complete Adversarial Analysis

**Change:** Removed `require(amount > 0)` check from `withdraw()` function

### 1. Attacker Model
- **WHO:** Unauthenticated external user
- **ACCESS:** Can call public contract functions
- **INTERFACE:** `withdraw(uint256 amount)` at 0x1234...

### 2. Attack Vector
**ENTRY POINT:** `withdraw(0)`

**ATTACK SEQUENCE:**
1. Call `withdraw(0)` from attacker address
2. Code bypasses amount check (removed)
3. Withdraw event emitted with 0 amount
4. Accounting updated incorrectly

**PROOF:** Function is `external`, no auth required

### 3. Exploitability
**RATING:** EASY
- Single transaction
- Public function
- No special state required

### 4. Exploit Scenario
**ATTACKER POSITION:** Has user account with 0 balance

**EXPLOITATION:**
```solidity
Step 1: attacker.withdraw(0)
  - Passes removed validation
  - Emits Withdraw(user, 0)
  - Updates withdrawnAmount[user] += 0

Step 2: Off-chain indexer sees Withdraw event
  - Credits attacker for 0 withdrawal
  - But accounting thinks withdrawal happened

Step 3: Accounting mismatch exploited
  - Total supply decremented
  - User balance not changed
  - System invariants broken
```

**IMPACT:**
- Protocol accounting corrupted
- Can be used to manipulate LP calculations
- Estimated $50K impact on pool prices

### 5. Baseline Violation
- Violates invariant: "All withdrawals must transfer non-zero value"
- Breaks validation pattern: Amount checks present in all other value transfers
- Regression: Check added in commit abc123 "Fix zero-amount exploit"

---

**Next:** Document all findings in final report (see [Report Generation (Phase 6)](#report-generation-phase-6))


---

# Report Generation (Phase 6)

Comprehensive markdown report structure and formatting guidelines.

---

## Report Structure

Generate markdown report with these mandatory sections:

### 1. Executive Summary

- Severity distribution table
- Risk assessment (CRITICAL/HIGH/MEDIUM/LOW)
- Final recommendation (APPROVE/REJECT/CONDITIONAL)
- Key metrics (test gaps, blast radius, red flags)

**Template:**
```markdown
# Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | X |
| 🟠 HIGH | Y |
| 🟡 MEDIUM | Z |
| 🟢 LOW | W |

**Overall Risk:** CRITICAL/HIGH/MEDIUM/LOW
**Recommendation:** APPROVE/REJECT/CONDITIONAL

**Key Metrics:**
- Files analyzed: X/Y (Z%)
- Test coverage gaps: N functions
- High blast radius changes: M functions
- Security regressions detected: P
```

---

### 2. What Changed

- Commit timeline with visual
- File summary table
- Lines changed stats

**Template:**
```markdown
## What Changed

**Commit Range:** `base..head`
**Commits:** X
**Timeline:** YYYY-MM-DD to YYYY-MM-DD

| File | +Lines | -Lines | Risk | Blast Radius |
|------|--------|--------|------|--------------|
| file1.sol | +50 | -20 | HIGH | CRITICAL |
| file2.sol | +10 | -5 | MEDIUM | LOW |

**Total:** +N, -M lines across K files
```

---

### 3. Critical Findings

For each HIGH/CRITICAL issue:

```markdown
### [SEVERITY] Title

**File**: path/to/file.ext:lineNumber
**Commit**: hash
**Blast Radius**: N callers (HIGH/MEDIUM/LOW)
**Test Coverage**: YES/NO/PARTIAL

**Description**: [clear explanation]

**Historical Context**:
- Git blame: Added in commit X (date)
- Message: "[original commit message]"
- [Why this code existed]

**Attack Scenario**:
[Concrete exploitation steps from adversarial.md]

**Proof of Concept**:
```code demonstrating issue```

**Recommendation**:
[Specific fix with code]
```

**Example:**
```markdown
### 🔴 CRITICAL: Authorization Bypass in Withdraw

**File**: TokenVault.sol:156
**Commit**: abc123def
**Blast Radius**: 23 callers (HIGH)
**Test Coverage**: NO

**Description**:
Removed `require(msg.sender == owner)` check allows any user to withdraw funds.

**Historical Context**:
- Git blame: Added 2024-06-15 (commit def456)
- Message: "Add owner check per audit finding #45"
- Code existed to prevent unauthorized withdrawals

**Attack Scenario**:
1. Attacker calls `withdraw(1000 ether)`
2. No authorization check (removed)
3. 1000 ETH transferred to attacker
4. Protocol funds drained

**Proof of Concept**:
```solidity
// As any address
vault.withdraw(vault.balance());
// Success - funds stolen
```

**Recommendation**:
```solidity
function withdraw(uint256 amount) external {
+   require(msg.sender == owner, "Unauthorized");
    // ... rest of function
}
```
```

---

### 4. Test Coverage Analysis

- Coverage statistics
- Untested changes list
- Risk assessment

**Template:**
```markdown
## Test Coverage Analysis

**Coverage:** X% of changed code

**Untested Changes:**
| Function | Risk | Impact |
|----------|------|--------|
| functionA() | HIGH | No validation tests |
| functionB() | MEDIUM | Logic untested |

**Risk Assessment:**
N HIGH-risk functions without tests → Recommend blocking merge
```

---

### 5. Blast Radius Analysis

- High-impact functions table
- Dependency graph
- Impact quantification

**Template:**
```markdown
## Blast Radius Analysis

**High-Impact Changes:**
| Function | Callers | Risk | Priority |
|----------|---------|------|----------|
| transfer() | 89 | HIGH | P0 |
| validate() | 45 | MEDIUM | P1 |
```

---

### 6. Historical Context

- Security-related removals
- Regression risks
- Commit message red flags

**Template:**
```markdown
## Historical Context

**Security-Related Removals:**
- Line 45: `require` removed (added 2024-03 for CVE-2024-1234)
- Line 78: Validation removed (added 2023-12 "security hardening")

**Regression Risks:**
- Code pattern removed in commit X, re-added in commit Y
```

---

### 7. Recommendations

- Immediate actions (blocking)
- Before production (tracking)
- Technical debt (future)

**Template:**
```markdown
## Recommendations

### Immediate (Blocking)
- [ ] Fix CRITICAL issue in TokenVault.sol:156
- [ ] Add tests for withdraw() function

### Before Production
- [ ] Security audit of auth changes
- [ ] Load test blast radius functions

### Technical Debt
- [ ] Refactor validation pattern consistency
```

---

### 8. Analysis Methodology

- Strategy used (DEEP/FOCUSED/SURGICAL)
- Files analyzed
- Coverage estimate
- Techniques applied
- Limitations
- Confidence level

**Template:**
```markdown
## Analysis Methodology

**Strategy:** FOCUSED (80 files, medium codebase)

**Analysis Scope:**
- Files reviewed: 45/80 (56%)
- HIGH RISK: 100% coverage
- MEDIUM RISK: 60% coverage
- LOW RISK: Excluded

**Techniques:**
- Git blame on all removals
- Blast radius calculation
- Test coverage analysis
- Adversarial modeling for HIGH RISK

**Limitations:**
- Did not analyze external dependencies
- Limited to 1-hop caller analysis

**Confidence:** HIGH for analyzed scope, MEDIUM overall
```

---

### 9. Appendices

- Commit reference table
- Key definitions
- Contact info

---

## Formatting Guidelines

**Tables:** Use markdown tables for structured data

**Code blocks:** Always include syntax highlighting
```solidity
// Solidity code
```
```rust
// Rust code
```

**Status indicators:**
- ✅ Complete
- ⚠️ Warning
- ❌ Failed/Blocked

**Severity:**
- 🔴 CRITICAL
- 🟠 HIGH
- 🟡 MEDIUM
- 🟢 LOW

**Before/After comparisons:**
```markdown
**BEFORE:**
```code
old code
```

**AFTER:**
```code
new code
```
```

**Line number references:** Always include
- Format: `file.sol:L123`
- Link to commit: `file.sol:L123 (commit abc123)`

---

## File Naming and Location

**Priority order for output:**
1. Current working directory (if project repo)
2. User's Desktop or another agreed location
3. A dedicated `security-reviews/` or `docs/` subdirectory in the project (team convention)

**Filename format:**
```
<PROJECT>_DIFFERENTIAL_REVIEW_<DATE>.md

Example: VeChain_Stargate_DIFFERENTIAL_REVIEW_2025-12-26.md
```

---

## User Notification Template

After generating report:

```markdown
Report generated successfully!

📄 File: [filename]
📁 Location: [path]
📏 Size: XX KB
⏱️ Review Time: ~X hours

Summary:
- X findings (Y critical, Z high)
- Final recommendation: APPROVE/REJECT/CONDITIONAL
- Confidence: HIGH/MEDIUM/LOW

Next steps:
- Review findings in detail
- Address CRITICAL/HIGH issues before merge
- Consider chaining with your team's formal report workflow for stakeholders
```

---

## Integration with formal reporting

After generating differential review, transform into audit report:

Use your team's issue or formal report workflow to transform the markdown into stakeholder-facing format if needed.

*(See upstream Trail of Bits prodsec-skills for the `issue-writer` companion skill if you use that distribution.)*

This creates polished documentation for non-technical stakeholders.

---

## Error Handling

If file write fails:
1. Try Desktop location
2. Try temp directory
3. As last resort, output full report to chat
4. Notify user to save manually

**Always prioritize persistent artifact generation over ephemeral chat output.**


---

# Common Vulnerability Patterns

Quick reference for detecting common security issues in code changes.
Examples use Python and Go to illustrate patterns, but the underlying
vulnerabilities apply across a full stack — system software,
OpenShift operators, Ansible modules, C/C++ daemons, Rust tooling, and
beyond. Adapt examples to the language and framework of the code under review.

Domain-specific auditing skills in this repository complement the patterns below.

---

## Security Regressions

**Pattern:** Code previously removed for a security fix is re-added in a later change.

**Detection:**
```bash
# Search for code that was removed in a security-related commit
git log -S "pattern" --all --grep="security\|fix\|CVE"
git diff <range> | grep "^+"
```

**Red flags:**
- Commit message of the original removal contains "security", "fix", "CVE", "vulnerability"
- Code removed less than 6 months ago
- No explanation in current PR for re-addition

#### Python

```python
# VULNERABLE: handler removed in commit abc123 "Fix SQL injection CVE-2024-5678"
# is re-added in current PR without the fix
@app.get("/users")
def list_users(name: str):
    query = f"SELECT * FROM users WHERE name = '{name}'"  # REGRESSION: raw f-string SQL
    return db.execute(query).fetchall()

# SAFE: the parameterized version that the fix introduced
@app.get("/users")
def list_users(name: str):
    return db.execute("SELECT * FROM users WHERE name = :n", {"n": name}).fetchall()
```

#### Go

```go
// VULNERABLE: endpoint removed in commit abc123 "Fix path traversal CVE-2024-9012"
// is re-added without sanitization
func serveFile(w http.ResponseWriter, r *http.Request) {
    path := r.URL.Query().Get("file")
    http.ServeFile(w, r, filepath.Join("/data", path)) // REGRESSION: unsanitized path
}

// SAFE: resolve the full path and verify it stays under the allowed root
func serveFile(w http.ResponseWriter, r *http.Request) {
    name := filepath.Clean(r.URL.Query().Get("file"))
    full := filepath.Join("/data", name)
    if !strings.HasPrefix(full, "/data/") {
        http.Error(w, "forbidden", http.StatusForbidden)
        return
    }
    http.ServeFile(w, r, full)
}
```

**Risk:** A previously patched vulnerability is silently reintroduced.

---

## Double Accounting Bugs

**Pattern:** The same accounting operation (balance update, counter increment, quota deduction) is applied twice for a single logical event.

**Detection:**
```bash
# Look for duplicate state mutations in related functions
grep -rn "balance\|quota\|count\|credit\|debit" --include="*.py" --include="*.go"
git diff <range> | grep -E "^\+.*(balance|quota|credit|debit)"
```

#### Python

```python
# VULNERABLE: balance deducted in both request and processing stages
def request_withdrawal(user_id: str, amount: Decimal):
    user = db.query(User).get(user_id)
    user.balance -= amount  # first deduction
    db.commit()
    withdrawal_queue.enqueue(user_id, amount)

def process_withdrawal(user_id: str, amount: Decimal):
    user = db.query(User).get(user_id)
    user.balance -= amount  # second deduction -- BUG
    db.commit()
    transfer_funds(user_id, amount)

# SAFE: deduct once, mark the withdrawal as processed
def request_withdrawal(user_id: str, amount: Decimal):
    user = db.query(User).get(user_id)
    user.balance -= amount
    db.commit()
    withdrawal_queue.enqueue(user_id, amount)

def process_withdrawal(user_id: str, amount: Decimal):
    # Balance already deducted during request; only execute transfer
    transfer_funds(user_id, amount)
    mark_complete(user_id, amount)
```

#### Go

```go
// VULNERABLE: inventory decremented in both reservation and fulfillment
func ReserveItem(db *sql.DB, itemID int, qty int) error {
    _, err := db.Exec("UPDATE inventory SET stock = stock - $1 WHERE id = $2", qty, itemID)
    return err // first decrement
}

func FulfillOrder(db *sql.DB, itemID int, qty int) error {
    _, err := db.Exec("UPDATE inventory SET stock = stock - $1 WHERE id = $2", qty, itemID) // BUG: second decrement
    return err
}

// SAFE: decrement once during reservation; fulfillment only ships
func FulfillOrder(db *sql.DB, itemID int, qty int) error {
    _, err := db.Exec("UPDATE orders SET status = 'shipped' WHERE item_id = $1 AND qty = $2", itemID, qty)
    return err
}
```

**Risk:** Users lose funds or resources twice, or the system drifts into an inconsistent state.

---

## Missing Validation

**Pattern:** Input validation or error checks are removed or absent without an equivalent replacement.

**Detection:**
```bash
# Removed validation keywords across languages
git diff <range> | grep "^-" | grep -E "raise|assert|validate|ValueError|HTTPException|if err|return err|http\.Error|errors\."
```

**Questions to ask:**
- Was validation moved to a different layer (middleware, schema)?
- Is the removal intentional and safe, or does it expose a vulnerability?
- Does the removed check guard against attacker-controlled input?

#### Python

```python
# VULNERABLE: validation removed from FastAPI handler
@router.post("/transfer")
def transfer(body: dict):
    # No validation -- amount could be negative, zero, or absurdly large
    execute_transfer(body["from_account"], body["to_account"], body["amount"])

# SAFE: Pydantic model enforces constraints
from pydantic import BaseModel, Field

class TransferRequest(BaseModel):
    from_account: str = Field(min_length=1)
    to_account: str = Field(min_length=1)
    amount: Decimal = Field(gt=0, le=1_000_000)

@router.post("/transfer")
def transfer(body: TransferRequest):
    execute_transfer(body.from_account, body.to_account, body.amount)
```

#### Go

```go
// VULNERABLE: no input validation in HTTP handler
func transferHandler(w http.ResponseWriter, r *http.Request) {
    var req TransferRequest
    json.NewDecoder(r.Body).Decode(&req) // error ignored, fields unchecked
    executeTransfer(req.From, req.To, req.Amount)
}

// SAFE: validate all fields before use
func transferHandler(w http.ResponseWriter, r *http.Request) {
    var req TransferRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid request body", http.StatusBadRequest)
        return
    }
    if req.Amount <= 0 || req.Amount > 1_000_000 {
        http.Error(w, "amount out of range", http.StatusBadRequest)
        return
    }
    if req.From == "" || req.To == "" {
        http.Error(w, "missing account", http.StatusBadRequest)
        return
    }
    executeTransfer(req.From, req.To, req.Amount)
}
```

**Risk:** Attackers supply malformed or malicious input that bypasses business rules.

---

## Integer Overflow and Type Coercion Errors

**Pattern:** Arithmetic on integers that can silently wrap around or lose precision during type conversion. In languages with fixed-width integers (Go, C, Rust) values wrap or truncate; in Python, implicit int-to-float conversion loses precision for large values.

**Detection:**
```bash
# Narrowing conversions and casts
grep -rn "int8\|int16\|uint8\|uint16\|int32\|uint32" --include="*.go"
grep -rn "as u8\|as u16\|as i16\|as i32" --include="*.rs"
grep -rn "(int16)\|(int32)\|(uint8)" --include="*.go"
# Python: implicit float conversion or unchecked large int
grep -rn "int(.*\.\|float(\|struct\.pack\|ctypes" --include="*.py"
```

#### Python

```python
# VULNERABLE: large user-supplied integer silently loses precision as float
def allocate_buffer(size_str: str) -> bytearray:
    size = int(size_str)
    factor = 1.5
    adjusted = int(size * factor)  # float multiplication -- loses precision for large ints
    return bytearray(adjusted)

# SAFE: keep arithmetic in integer domain and bound the input
def allocate_buffer(size_str: str) -> bytearray:
    size = int(size_str)
    if size <= 0 or size > 10 * 1024 * 1024:
        raise ValueError("size out of allowed range")
    adjusted = size + size // 2  # integer-only arithmetic
    return bytearray(adjusted)
```

#### Go

```go
// VULNERABLE: user-controlled value converted to int16, silently wraps
func setPort(input string) (int16, error) {
    v, err := strconv.Atoi(input)
    if err != nil {
        return 0, err
    }
    return int16(v), nil // 70000 wraps to 4464
}

// SAFE: validate range before narrowing conversion
func setPort(input string) (int16, error) {
    v, err := strconv.Atoi(input)
    if err != nil {
        return 0, err
    }
    if v < 0 || v > math.MaxInt16 {
        return 0, fmt.Errorf("port %d out of int16 range", v)
    }
    return int16(v), nil
}
```

**Risk:** Silent wrap-around or precision loss leads to under-allocated buffers, incorrect accounting, or bypassed limits.

---

## TOCTOU / Check-Then-Act Race Conditions

**Pattern:** A condition is checked and then acted upon, but the underlying state can change between the check and the action. This applies to database rows, file system state, and in-memory data accessed across async or concurrent boundaries.

**Detection:**
```bash
# Check-then-insert patterns in ORM or SQL code
grep -rn "if.*query.*first\|if.*exists\|if not.*get" --include="*.py"
# Check-then-act on shared state without atomicity
git diff <range> | grep "^+" | grep -E "\w+\[.*\]|\bLoad\b" | grep -v "sync\.\|mu\.\|atomic\."
# File-system TOCTOU (any language)
grep -rn "os\.path\.exists\|os\.access\|os\.Stat" --include="*.py" --include="*.go"
```

#### Python

```python
# VULNERABLE: check-then-insert without atomicity (SQLAlchemy)
def create_user(db: Session, email: str):
    existing = db.query(User).filter_by(email=email).first()
    if existing is None:
        # Another request can insert the same email between check and insert
        db.add(User(email=email))
        db.commit()

# SAFE: use a unique constraint and handle the conflict
def create_user(db: Session, email: str):
    try:
        db.add(User(email=email))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("email already registered")
```

#### Go

```go
// VULNERABLE: read-then-write on shared map without lock
var cache = make(map[string]int)

func Increment(key string) {
    val := cache[key]   // read
    cache[key] = val + 1 // write -- race if called from multiple goroutines
}

// SAFE: protect with a mutex
var (
    cache = make(map[string]int)
    mu    sync.Mutex
)

func Increment(key string) {
    mu.Lock()
    defer mu.Unlock()
    cache[key]++
}
```

**Risk:** Duplicate records, corrupted state, or privilege escalation when two operations interleave.

---

## Access Control Bypass

**Pattern:** Authentication or authorization checks are removed, relaxed, or skipped for certain routes or operations.

**Detection:**
```bash
# Removed auth decorators, middleware, or guard functions
git diff <range> | grep "^-" | grep -E "Depends\(|@login_required|@requires_auth|get_current_user|Permission|middleware|AuthRequired|RequireRole|checkAuth"
```

**Questions:**
- Who can now call this endpoint or function?
- Was the check moved to a different layer, or truly removed?
- What is the new trust boundary?

#### Python

```python
# VULNERABLE: auth dependency removed from FastAPI route
@router.put("/admin/config")
def update_config(body: ConfigUpdate):
    # Anyone can call this -- Depends(get_current_admin) was removed
    apply_config(body)

# SAFE: auth dependency enforced
@router.put("/admin/config")
def update_config(body: ConfigUpdate, admin: User = Depends(get_current_admin)):
    apply_config(body)
```

#### Go

```go
// VULNERABLE: auth middleware removed from route registration
mux.HandleFunc("/admin/config", updateConfigHandler)

// SAFE: auth middleware wraps the handler
mux.Handle("/admin/config", AuthRequired(http.HandlerFunc(updateConfigHandler)))
```

**Risk:** Unauthenticated or low-privilege users access admin functionality.

---

## Concurrency Race Conditions

**Pattern:** Shared mutable state accessed from multiple threads, goroutines, or async tasks without synchronization (locks, channels, atomics, or similar primitives).

**Detection:**
```bash
# Goroutines or threads launched near shared state
grep -rn "go func\|go .*(" --include="*.go"
grep -rn "threading\.\|asyncio\.\|concurrent\.futures" --include="*.py"
# Shared mutable globals
grep -rn "var.*=.*make\(map" --include="*.go"
```

#### Python

```python
# VULNERABLE: shared dict mutated from multiple async tasks
user_sessions: dict[str, int] = {}

async def track_login(user_id: str):
    count = user_sessions.get(user_id, 0)
    await asyncio.sleep(0)  # yields control -- another task can interleave
    user_sessions[user_id] = count + 1

# SAFE: use an asyncio.Lock to serialize access
session_lock = asyncio.Lock()

async def track_login(user_id: str):
    async with session_lock:
        user_sessions[user_id] = user_sessions.get(user_id, 0) + 1
```

#### Go

```go
// VULNERABLE: goroutines write to shared slice without synchronization
var results []string

func collect(items []string) {
    for _, item := range items {
        go func(s string) {
            results = append(results, s) // data race
        }(item)
    }
}

// SAFE: use a mutex or channel
var (
    results []string
    mu      sync.Mutex
)

func collect(items []string) {
    var wg sync.WaitGroup
    for _, item := range items {
        wg.Add(1)
        go func(s string) {
            defer wg.Done()
            mu.Lock()
            results = append(results, s)
            mu.Unlock()
        }(item)
    }
    wg.Wait()
}
```

**Risk:** Data corruption, lost updates, panics, or non-deterministic behavior that is difficult to reproduce.

---

## Insecure Time-Based Logic

**Pattern:** Using wall-clock time for security-sensitive decisions such as token expiry, replay prevention, or rate limiting without accounting for clock skew, NTP jumps, or attacker-controlled clocks.

**Detection:**
```bash
# Wall-clock usage in security paths
grep -rn "time\.time()\|datetime\.now()\|datetime\.utcnow()" --include="*.py"
grep -rn "time\.Now()\|time\.Since\|time\.Until" --include="*.go"
grep -rn "System\.currentTimeMillis\|Instant\.now" --include="*.java"
```

#### Python

```python
# VULNERABLE: in-process rate limiter uses wall clock -- NTP jump backward
# resets the timer and allows a burst of requests
import time
last_request: dict[str, float] = {}

def is_rate_limited(user_id: str, min_interval: float = 1.0) -> bool:
    now = time.time()
    if now - last_request.get(user_id, 0.0) < min_interval:
        return True
    last_request[user_id] = now
    return False

# SAFE: monotonic clock is unaffected by NTP or system clock changes
last_request: dict[str, float] = {}

def is_rate_limited(user_id: str, min_interval: float = 1.0) -> bool:
    now = time.monotonic()
    if now - last_request.get(user_id, 0.0) < min_interval:
        return True
    last_request[user_id] = now
    return False
```

#### Go

```go
// VULNERABLE: replay window based on wall clock
func isRequestFresh(ts time.Time) bool {
    return time.Since(ts) < 30*time.Second // clock skew can make stale requests appear fresh
}

// SAFE: nonce prevents replay regardless of clock accuracy;
// time.Since on a parsed timestamp is still wall-clock-based, so the
// window check is best-effort -- the nonce is the real protection.
var seen sync.Map // NOTE: in production, prune entries older than the replay window to prevent unbounded growth

func isRequestFresh(ts time.Time, nonce string) bool {
    if time.Since(ts) > 30*time.Second {
        return false
    }
    if _, loaded := seen.LoadOrStore(nonce, struct{}{}); loaded {
        return false // replay detected
    }
    return true
}
```

**Risk:** Attackers replay expired tokens, bypass rate limits, or exploit clock skew to extend time-gated access.

---

## Unchecked Errors / Swallowed Exceptions

**Pattern:** Error return values are silently discarded or exceptions are caught with a bare handler and silently suppressed, hiding failures that should abort or alter control flow.

**Detection:**
```bash
# Ignored error return values (Go)
grep -rn "_, _ =" --include="*.go"
grep -rn ", _ :=" --include="*.go"
# Bare except or pass-only handlers (Python)
grep -rn "except:" --include="*.py"
grep -rn "except .*:" --include="*.py" -A1 | grep "pass"
# Ignored Result (Rust)
grep -rn "let _ =" --include="*.rs"
```

#### Python

```python
# VULNERABLE: bare except swallows all errors including auth failures
def authenticate(token: str) -> User:
    try:
        return verify_and_decode(token)
    except:
        pass  # silently returns None -- caller may treat None as "no auth required"

# SAFE: catch specific exceptions, let unexpected errors propagate
def authenticate(token: str) -> User:
    try:
        return verify_and_decode(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as exc:
        raise HTTPException(status_code=401, detail=str(exc))
```

#### Go

```go
// VULNERABLE: Write and Close errors silently discarded -- partial or
// unflushed data is treated as success with no indication to the caller
func writeConfig(path string, data []byte) {
    f, err := os.Create(path)
    if err != nil {
        return // caller receives no error; config silently not written
    }
    f.Write(data) // error ignored -- partial write undetected
    f.Close()     // error ignored -- OS buffer may not be flushed
}

// SAFE: check every error; named return allows the deferred Close error to propagate
func writeConfig(path string, data []byte) (err error) {
    f, err := os.Create(path)
    if err != nil {
        return fmt.Errorf("create %s: %w", path, err)
    }
    defer func() {
        if cerr := f.Close(); cerr != nil && err == nil {
            err = cerr
        }
    }()
    _, err = f.Write(data)
    return
}
```

**Risk:** Silent failures lead to partial writes, data loss, authentication bypass, or inconsistent system state.

---

## Denial of Service / Unbounded Operations

**Pattern:** Operations that grow without bound based on user-controlled input: unbounded queries, thread/goroutine leaks, infinite loops, or unlimited memory allocation.

**Detection:**
```bash
# Unbounded queries or missing LIMIT
grep -rn "\.all()\|fetchall()\|SELECT \*" --include="*.py"
grep -rn "QueryRow\|Query(" --include="*.go" | grep -v "LIMIT"
# Goroutines or threads launched without lifecycle management
grep -rn "go func\|go .*(" --include="*.go"
# Missing pagination or size limits in new code
git diff <range> | grep -E "^\+.*(\.all\(\)|fetchall|SELECT \*|go func)"
```

#### Python

```python
# VULNERABLE: returns entire table to the client
@router.get("/events")
def get_events(db: Session):
    return db.query(Event).all()  # unbounded -- millions of rows crash the service

# SAFE: enforce pagination limits
@router.get("/events")
def get_events(db: Session, offset: int = 0, limit: int = Query(default=50, le=200)):
    return db.query(Event).offset(offset).limit(limit).all()
```

#### Go

```go
// VULNERABLE: goroutine launched per request with no cancellation
func streamHandler(w http.ResponseWriter, r *http.Request) {
    go func() {
        for {
            data := fetchData() // runs forever if client disconnects
            fmt.Fprintln(w, data)
        }
    }()
}

// SAFE: use a ticker so the goroutine yields between iterations instead
// of spinning at full CPU speed when fetchData() returns quickly
func streamHandler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    ticker := time.NewTicker(1 * time.Second)
    defer ticker.Stop()
    go func() {
        for {
            select {
            case <-ctx.Done():
                return // client disconnected -- stop the goroutine
            case <-ticker.C:
                data := fetchData()
                fmt.Fprintln(w, data)
            }
        }
    }()
}
```

**Risk:** Resource exhaustion (CPU, memory, database connections, goroutines/threads) causes service outages.

---

## Sensitive Data in Logs

**Pattern:** Passwords, API keys, tokens, PII, or other secrets written to application logs.

**Detection:**
```bash
# Logging calls that may include sensitive fields
grep -rn "logging\.\|logger\.\|log\.\|slog\.\|zap\." --include="*.py" --include="*.go" | grep -iE "password|token|secret|key|ssn|credit"
```

#### Python

```python
# VULNERABLE: password and token logged in plaintext
import logging
logger = logging.getLogger(__name__)

def login(username: str, password: str):
    logger.info(f"Login attempt: user={username} password={password}")  # password in logs
    token = authenticate(username, password)
    logger.debug(f"Generated token: {token}")  # token in logs
    return token

# SAFE: redact sensitive fields before logging
def login(username: str, password: str):
    logger.info("Login attempt: user=%s", username)  # no password
    token = authenticate(username, password)
    logger.debug("Token generated for user=%s", username)  # no token value
    return token
```

#### Go

```go
// VULNERABLE: secret logged via structured logger
func Login(username, password string) (string, error) {
    slog.Info("login attempt", "user", username, "password", password) // password in logs
    token, err := authenticate(username, password)
    if err != nil {
        return "", err
    }
    slog.Info("token issued", "token", token) // token in logs
    return token, nil
}

// SAFE: omit sensitive fields from log entries
func Login(username, password string) (string, error) {
    slog.Info("login attempt", "user", username) // no password
    token, err := authenticate(username, password)
    if err != nil {
        return "", err
    }
    slog.Info("token issued", "user", username) // no token value
    return token, nil
}
```

**Risk:** Secrets exposed in log aggregation systems, crash dumps, or stdout are accessible to anyone with log access and may violate compliance requirements (GDPR, PCI-DSS).

---

## Quick Detection Commands

**Find removed validation or error checks:**
```bash
git diff <range> | grep "^-" | grep -E "raise|assert|validate|ValueError|HTTPException|if err|return err|http\.Error|errors\."
```

**Find new external calls or HTTP clients:**
```bash
git diff <range> | grep "^+" | grep -E "requests\.|httpx\.|urllib|aiohttp|http\.Get|http\.Post|http\.NewRequest|net\.Dial"
```

**Find changed auth decorators or middleware:**
```bash
git diff <range> | grep -E "^[-+].*(Depends\(|@login_required|@requires_auth|get_current_user|middleware|AuthRequired|RequireRole|checkAuth)"
```

**Find arithmetic on user-controlled values:**
```bash
git diff <range> | grep "^+" | grep -E "int\(.*\.(query|form|json|body)|float\(|strconv\.(Atoi|Parse)|int16\(|int32\("
```

**Find logging of sensitive fields:**
```bash
git diff <range> | grep "^+" | grep -iE "(log|logger|slog|zap)\b.*\b(password|token|secret|key|ssn|credit)"
```

---

**For detailed analysis workflow, see [Differential Review Methodology](#differential-review-methodology)**
**For building exploit scenarios, see [Adversarial Vulnerability Analysis (Phase 5)](#adversarial-vulnerability-analysis-phase-5)**
