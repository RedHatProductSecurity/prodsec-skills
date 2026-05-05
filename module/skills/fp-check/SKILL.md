---
name: fp-check
description: "Systematically verifies suspected security bugs to eliminate false positives. Produces TRUE POSITIVE or FALSE POSITIVE verdicts with documented evidence for each bug."
license: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
origin: Adapted from Trail of Bits Skills Marketplace (https://github.com/trailofbits/skills)
category: "security_auditing"
subcategory: "audit-workflow"
---

# False Positive Check

## When to Use

- "Is this bug real?" or "is this a true positive?"
- "Is this a false positive?" or "verify this finding"
- "Check if this vulnerability is exploitable"
- Any request to verify or validate a specific suspected bug

## When NOT to Use

- Finding or hunting for bugs ("find bugs", "security analysis", "audit code")
- General code review for style, performance, or maintainability
- Feature development, refactoring, or non-security tasks
- When the user explicitly asks for a quick scan without verification

## Rationalizations to Reject

If you catch yourself thinking any of these, STOP.

| Rationalization | Why It's Wrong | Required Action |
|---|---|---|
| "Rapid analysis of remaining bugs" | Every bug gets full verification | Return to task list, verify next bug through all phases |
| "This pattern looks dangerous, so it's a vulnerability" | Pattern recognition is not analysis | Complete data flow tracing before any conclusion |
| "Skipping full verification for efficiency" | No partial analysis allowed | Execute all steps per the chosen verification path |
| "The code looks unsafe, reporting without tracing data flow" | Unsafe-looking code may have upstream validation | Trace the complete path from source to sink |
| "Similar code was vulnerable elsewhere" | Each context has different validation, callers, and protections | Verify this specific instance independently |
| "This is clearly critical" | LLMs are biased toward seeing bugs and overrating severity | Complete devil's advocate review; prove it with evidence |

---

## Step 0: Understand the Claim and Context

Before any analysis, restate the bug in your own words. If you cannot do this clearly, ask the user for clarification by asking the user clarifying questions. Half of false positives collapse at this step — the claim doesn't make coherent sense when restated precisely.

Document:

- **What is the exact vulnerability claim?** (e.g., "heap buffer overflow in `parse_header()` when `content_length` exceeds 4096")
- **What is the alleged root cause?** (e.g., "missing bounds check before `memcpy` at line 142")
- **What is the supposed trigger?** (e.g., "attacker sends HTTP request with oversized Content-Length header")
- **What is the claimed impact?** (e.g., "remote code execution via controlled heap corruption")
- **What is the threat model?** What privilege level does this code run at? Is it sandboxed? What can the attacker already do before triggering this bug? (e.g., "unauthenticated remote attacker vs privileged local user"; "runs inside Chrome renderer sandbox" vs "runs as root with no sandbox")
- **What is the bug class?** Classify the bug and consult **## Inlined: Bug-Class-Specific Verification** for class-specific verification requirements that supplement the generic phases below.
- **Execution context**: When and how is this code path reached during normal execution?
- **Caller analysis**: What functions call this code and what input constraints do they impose?
- **Architectural context**: Is this part of a larger security system with multiple protection layers?
- **Historical context**: Any recent changes, known issues, or previous security reviews of this code area?

## Route: Standard vs Deep Verification

After Step 0, choose a verification path.

### Standard Verification

Use when ALL of these hold:

- Clear, specific vulnerability claim (not vague or ambiguous)
- Single component — no cross-component interaction in the bug path
- Well-understood bug class (buffer overflow, SQL injection, XSS, integer overflow, etc.)
- No concurrency or async involved in the trigger
- Straightforward data flow from source to sink

Follow **## Inlined: Standard Verification** below. No separate task tracker required — work through the linear checklist, documenting findings inline.

### Deep Verification

Use when ANY of these hold:

- Ambiguous claim that could be interpreted multiple ways
- Cross-component bug path (data flows through 3+ modules or services)
- Race conditions, TOCTOU, or concurrency in the trigger mechanism
- Logic bugs without a clear spec to verify against
- Standard verification was inconclusive or escalated
- User explicitly requests full verification

Follow **## Inlined: Deep Verification** below. Track phases with explicit tasks or a checklist and execute them in dependency order (parallelize independent work when practical).

### Default

Start with standard. Standard verification has two built-in escalation checkpoints that route to deep when complexity exceeds the linear checklist.

## Batch Triage

When verifying multiple bugs at once:

1. Run Step 0 for all bugs first — restating each claim often collapses obvious false positives immediately
2. Route each bug independently (some may be standard, others deep)
3. Process all standard-routed bugs first, then deep-routed bugs
4. After all bugs are verified, check for **exploit chains** — findings that individually failed gate review may combine to form a viable attack

## Final Summary

After processing ALL suspected bugs, provide:

1. **Counts**: X TRUE POSITIVES, Y FALSE POSITIVES
2. **TRUE POSITIVE list**: Each with brief vulnerability description
3. **FALSE POSITIVE list**: Each with brief reason for rejection

## References (in this document)

- [Standard Verification](#inlined-standard-verification) — Linear checklist for straightforward bugs
- [Deep Verification](#inlined-deep-verification) — Phased orchestration for complex bugs
- [Gate Reviews](#inlined-gate-reviews-and-verdicts) — Six mandatory gates and verdict format
- [Bug-Class Verification](#inlined-bug-class-specific-verification) — Class-specific requirements
- [False Positive Patterns](#inlined-false-positive-patterns--lessons-learned) — 13-item checklist and red flags
- [Evidence Templates](#inlined-evidence-templates) — Templates for evidence documentation

*(See upstream Trail of Bits prodsec-skills `fp-check` plugin for companion agents and automation.)*


---

## Inlined: Standard Verification

# Standard Verification

Linear single-pass checklist for straightforward bugs. No task creation — work through each step sequentially and document findings inline.

## Escalation Checkpoints

Two points in this checklist may trigger escalation to [deep-verification.md](#inlined-deep-verification):

1. **After Step 1 (Data Flow)**: Escalate if 3+ trust boundaries, callbacks/async control flow, or ambiguous validation chain
2. **After Step 5 (Devil's Advocate)**: Escalate if any question produces genuine uncertainty you cannot resolve

When escalating, hand off all evidence gathered so far — deep verification will continue from where you left off.

## Checklist

### Step 1: Data Flow

Trace data from source to the alleged vulnerability sink.

- Map trust boundaries crossed (internal/trusted vs external/untrusted)
- Identify all validation and sanitization between source and sink
- Check API contracts — many APIs have built-in bounds protection that prevents the alleged issue
- Check for environmental protections (compiler, runtime, OS, framework) that prevent exploitation entirely (not just raise the bar)
- Apply class-specific checks from [bug-class-verification.md](#inlined-bug-class-specific-verification)

**Key pitfall**: Analyzing the vulnerable code in isolation. Conditional logic upstream may make the vulnerability mathematically unreachable. Trace the full validation chain.

**Escalation check**: If you found 3+ trust boundaries, callbacks or async control flow in the path, or an ambiguous validation chain — escalate to deep verification.

### Step 2: Exploitability

Prove the attacker can trigger the vulnerability.

- **Attacker control**: Prove the attacker controls data reaching the vulnerable operation. Internal storage set by trusted components is not attacker-controlled.
- **Bounds proof**: For integer/bounds issues, create an explicit algebraic proof using the template in [evidence-templates.md](#inlined-evidence-templates). Verify: IF validation_check_passes THEN bounds_guarantee_holds.
- **Race feasibility**: For race conditions, prove concurrent access is actually possible. Single-threaded initialization and synchronized contexts cannot have races.

### Step 3: Impact

Determine whether exploitation has real security consequences.

- Distinguish real security impact (RCE, privesc, info disclosure) from operational robustness issues (crash recovery, cleanup failure)
- Distinguish primary security controls from defense-in-depth. Failure of a defense-in-depth measure is not a vulnerability if primary protections remain intact.

### Step 4: PoC Sketch

Create a pseudocode PoC showing the attack path. Executable and unit test PoCs are optional for standard verification.

```
Data Flow: [Source] → [Validation?] → [Transform?] → [Vulnerable Op] → [Impact]
Attacker controls: [what input, how]
Trigger: [pseudocode showing the exploit path]
```

See [evidence-templates.md](#inlined-evidence-templates) for the full PoC template.

### Step 5: Devil's Advocate Spot-Check

Answer these 7 questions. If any produces genuine uncertainty, escalate to deep verification.

**Against the vulnerability:**

1. Am I seeing a vulnerability because the pattern "looks dangerous" rather than because it actually is? (pattern-matching bias)
2. Am I incorrectly assuming attacker control over trusted data? (trust boundary confusion)
3. Have I rigorously proven the mathematical condition for vulnerability can occur? (proof rigor)
4. Am I confusing defense-in-depth failure with a primary security vulnerability? (defense-in-depth confusion)
5. Am I hallucinating this vulnerability? LLMs are biased toward seeing bugs everywhere — is this actually real or am I pattern-matching on scary-looking code? (LLM self-check)

**For the vulnerability (always ask — false-negative protection):**

6. Am I dismissing a real vulnerability because the exploit seems complex or unlikely?
7. Am I inventing mitigations or validation logic that I haven't verified in the actual source code? Re-read the code after reaching a conclusion.

**Escalation check**: If any question above produces genuine uncertainty you cannot resolve with the evidence at hand — escalate to deep verification.

### Step 6: Gate Review

Apply all six gates from [gate-reviews.md](#inlined-gate-reviews-and-verdicts) and all 13 items from [false-positive-patterns.md](#inlined-false-positive-patterns--lessons-learned) to reach a verdict.


---

## Inlined: Deep Verification

# Deep Verification

Full task-based verification for complex bugs. Use when routing from SKILL.md selects the deep path, or when standard verification escalates.

## If Escalated from Standard

When a bug escalates from standard verification:

1. Review all evidence gathered during the standard pass — do not repeat completed work
2. Identify which phases below are already satisfied by existing evidence
3. Create tasks only for remaining phases, starting from where standard left off
4. Preserve and reference all prior findings in new task descriptions

## Verification Task List

For each bug (Bug #N), define tasks with the dependency structure below. Record task IDs and dependencies in your tracker (spreadsheet, issue system, or checklist) so nothing starts before its prerequisites complete.

```
── Phase 1: Data Flow Analysis ──────────────────────────────────
"BUG #N - Phase 1.1: Map trust boundaries and trace data flow"
  Then in parallel (each blocked by 1.1):
  "BUG #N - Phase 1.2: Research API contracts and safety guarantees"
  "BUG #N - Phase 1.3: Environment protection analysis"
  "BUG #N - Phase 1.4: Cross-reference analysis"

── Phase 2: Exploitability Verification (blocked by Phase 1) ───
  In parallel:
  "BUG #N - Phase 2.1: Confirm attacker controls input data"
  "BUG #N - Phase 2.2: Mathematical bounds verification"
  "BUG #N - Phase 2.3: Race condition feasibility proof"
  Then (blocked by 2.1, 2.2, 2.3):
  "BUG #N - Phase 2.4: Adversarial analysis"

── Phase 3: Impact Assessment (blocked by Phase 2) ─────────────
  In parallel:
  "BUG #N - Phase 3.1: Demonstrate real security impact"
  "BUG #N - Phase 3.2: Primary control vs defense-in-depth"

── Phase 4: PoC Creation (blocked by Phase 3) ──────────────────
  "BUG #N - Phase 4.1: Create pseudocode PoC with data flow diagrams"
  Then in parallel (each blocked by 4.1):
  "BUG #N - Phase 4.2: Create executable PoC if feasible"
  "BUG #N - Phase 4.3: Create unit test PoC if feasible"
  "BUG #N - Phase 4.4: Negative PoC — show exploit preconditions"
  Then (blocked by 4.2, 4.3, 4.4):
  "BUG #N - Phase 4.5: Verify PoC demonstrates the vulnerability"

── Phase 5: Devil's Advocate (blocked by Phase 4) ──────────────
  "BUG #N - Phase 5.1: Devil's advocate review"

── Gate Review (blocked by Phase 5) ────────────────────────────
  "BUG #N - GATE REVIEW: Evaluate all six gates before verdict"
```

## Execution Rules

- Mark each task as in-progress when starting, completed only with concrete evidence
- **Parallel sub-phases**: Run independent sub-phases concurrently when possible (separate sessions or reviewers). Collect all results before proceeding to the next dependency gate.
- **Dependency gates**: Never start a phase until all tasks it depends on are completed.
- Apply all 13 checklist items from [false-positive-patterns.md](#inlined-false-positive-patterns--lessons-learned) to each bug

## Delegation (optional)

You may assign phase work to specialized reviewers or separate focused sessions:

| Focus | Phases | Purpose |
|-------|--------|---------|
| Data-flow pass | 1.1–1.4 | Trace data flow, map trust boundaries, check API contracts and environment protections |
| Exploitability pass | 2.1–2.4 | Prove attacker control, mathematical bounds, race condition feasibility |
| PoC pass | 4.1–4.5 | Pseudocode, executable, unit test, and negative PoCs |

Phases 3 (Impact Assessment), 5 (Devil's Advocate), and the Gate Review should be synthesized in one place — do not split accountability for the final verdict.

*(See upstream Trail of Bits prodsec-skills for named agents that mirror these phases.)*

## Phase Requirements

The task list above names every phase. Below are the key pitfalls and decision criteria for each — focus on what you might get wrong.

### Phase 1: Data Flow Analysis

**1.1**: Map trust boundaries (internal/trusted vs external/untrusted) and trace data from source to alleged vulnerability. Apply class-specific verification from [bug-class-verification.md](#inlined-bug-class-specific-verification). **Key pitfall**: Analyzing code in isolation without tracing the full validation chain. Conditional logic upstream may make the vulnerable code mathematically unreachable (see [false-positive-patterns.md](#inlined-false-positive-patterns--lessons-learned) items 1 and 1a).

**1.2**: Check API contracts before claiming overflows — many APIs have built-in bounds protection that prevents the alleged issue regardless of inputs.

**1.3**: Before concluding vulnerability, verify that no compiler, runtime, OS, or framework protections prevent exploitation. Note: mitigations like ASLR and stack canaries raise the exploitation bar but do not eliminate the vulnerability itself. Distinguish "prevents exploitation entirely" (e.g., Rust's safe type system) from "makes exploitation harder" (e.g., ASLR).

**1.4**: Check if similar code patterns exist elsewhere and are handled safely. Review test coverage, code review history, and design documentation for this area.

### Phase 2: Exploitability Verification

**2.1**: Prove attacker controls the data reaching the vulnerability. **Key pitfall**: Assuming network/external data reaches the operation without tracing the actual path — internal storage set by trusted components is not attacker-controlled.

**2.2**: Create explicit algebraic proofs for bounds-related issues. Use the template in [evidence-templates.md](#inlined-evidence-templates). Verify: IF validation_check_passes THEN bounds_guarantee_holds.

**2.3**: For race conditions, prove concurrent access is actually possible. **Key pitfall**: Assuming race conditions in single-threaded initialization or synchronized contexts.

**2.4**: Assess full attack surface: input control, validation bypass paths, timing dependencies, and state manipulation.

### Phase 3: Impact Assessment

**3.1**: Distinguish real security impact (RCE, privesc, info disclosure) from operational robustness issues.

**3.2**: Distinguish primary security controls from defense-in-depth. Failure of a defense-in-depth measure is not a vulnerability if primary protections remain intact.

### Phase 4: PoC Creation

**Always create a pseudocode PoC.** Additionally, create executable and/or unit test PoCs when feasible:

1. **Pseudocode with data flow diagrams** showing the attack path (always)
2. **Executable PoC** in the target language demonstrating the vulnerability (if feasible)
3. **Unit test PoC** exercising the vulnerable code path with crafted inputs (if feasible)

See [evidence-templates.md](#inlined-evidence-templates) for PoC templates.

**Negative PoC (Phase 4.4)**: Demonstrate the gap between normal operation and the exploit path — what preconditions must hold for the vulnerability to trigger, and why they don't hold under normal conditions.

### Phase 5: Devil's Advocate Review

Before final verdict, systematically challenge the vulnerability claim. Assume you are biased toward finding bugs and rating them as critical — actively work against that bias.

**Challenges arguing AGAINST the vulnerability:**

1. What non-vulnerability explanations exist for this code pattern?
2. How would the original developers justify this implementation?
3. What crucial system architecture context might be missing?
4. Am I seeing a vulnerability because the pattern "looks dangerous" rather than because it actually is?
5. Even if validation looks insufficient, does it actually prevent the claimed condition?
6. Am I incorrectly assuming attacker control over trusted data?
7. Have I rigorously proven the mathematical condition for vulnerability can occur?
8. Beyond theoretical possibility, is this practically exploitable?
9. Am I confusing defense-in-depth failure with a primary security vulnerability?
10. What compiler/runtime/OS protections might prevent exploitation?
11. Am I hallucinating this vulnerability? LLMs are biased toward seeing bugs everywhere and rating every finding as critical — is this actually a real, exploitable issue or am I pattern-matching on scary-looking code?

**Challenges arguing FOR the vulnerability (false-negative protection):**

12. Am I dismissing a real vulnerability because the exploit seems complex or unlikely?
13. Am I inventing mitigations or validation logic that I haven't verified in the actual source code? Re-read the code after reaching a conclusion.

See [evidence-templates.md](#inlined-evidence-templates) for the devil's advocate documentation template.

## Gate Review

Apply the six gates from [gate-reviews.md](#inlined-gate-reviews-and-verdicts) to reach a verdict.


---

## Inlined: Gate Reviews and Verdicts

Before reporting ANY bug as a vulnerability, all six gate reviews must pass. Evaluate these during the GATE REVIEW task after all phases are complete:

| Gate | Criterion | Pass | Fail |
|------|-----------|------|------|
| **1. Process** | All phases completed with documented evidence | Evidence exists for every phase | Phases lack concrete evidence |
| **2. Reachability** | Attacker can reach and control data at the vulnerability | Clear evidence of attacker-controlled path + PoC confirms | Cannot demonstrate attacker control or reachability |
| **3. Real Impact** | Exploitation leads to RCE, privesc, or info disclosure | Direct impact with concrete scenarios | Only operational robustness issue |
| **4. PoC Validation** | PoC (pseudocode, executable, or unit test) demonstrates the attack path | Shows attacker control, trigger, and impact | PoC fails to show attack path or impact |
| **5. Math Bounds** | Mathematical analysis confirms vulnerable condition is possible | Algebraic proof shows condition is possible | Math proves validation prevents it |
| **6. Environment** | No environmental protections entirely prevent exploitation | Protections do not eliminate vulnerability | Environmental protections block it entirely |

## Verdict Format

- **TRUE POSITIVE**: All gate reviews pass → `BUG #N TRUE POSITIVE — [brief vulnerability description]`
- **FALSE POSITIVE**: Any gate review fails → `BUG #N FALSE POSITIVE — [brief reason for rejection]`

If any phase fails verification, document the failure with evidence and continue all remaining phases. Issue the FALSE POSITIVE verdict only after all phases are complete.

## Example Verdict

```
BUG #3 FALSE POSITIVE — Integer underflow in packet_handler.c:142
  Gate 5 (Math Bounds) FAIL: validation at line 98 ensures packet_size >= 16,
  making (packet_size - header_size) >= 8. Underflow is mathematically impossible.
```


---

## Inlined: Bug-Class-Specific Verification

# Bug-Class-Specific Verification

Different bug classes require different verification approaches. After classifying the bug in Step 0, apply the class-specific requirements below **in addition to** the generic verification phases.

## Memory Corruption

Buffer overflow, heap overflow, stack overflow, out-of-bounds read/write, use-after-free, double-free, type confusion.

**Language safety check first:** Memory corruption in safe Rust, Go (without `unsafe.Pointer`/cgo), or managed languages (Java, C#, Python) is almost always a false positive — the type system or runtime prevents it. Verify whether the code is in an `unsafe` block (Rust), uses cgo/`unsafe.Pointer` (Go), or calls native code via JNI/P/Invoke. If the code is entirely in the safe subset, reject the memory corruption claim unless it involves a compiler bug or soundness hole.

**Verify:**

- What exactly gets corrupted? (which object, field, or memory region)
- What is the corruption size and offset? Can the attacker control them?
- Is the corruption a useful exploitation primitive (arbitrary read/write, vtable overwrite, function pointer overwrite) or just a crash?
- What allocator is in use (glibc, tcmalloc, jemalloc, Windows heap)? Does it have hardening that blocks exploitation?
- For UAF: trace the object lifetime — what frees it, what reuses the memory, can the attacker control the replacement object?
- For type confusion: prove the type mismatch exists and that misinterpretation of the data leads to a useful primitive.

## Logic Bugs

Authentication bypass, access control errors, incorrect state transitions, confused deputy, privilege escalation through API misuse.

**Verify:**

- Check against the specification, RFC, or design docs — not just the code. Does the implementation match the intended behavior?
- Map all state transitions. Can the system reach a state the developer didn't anticipate?
- Identify implicit assumptions that are never enforced in code.
- For auth bugs: verify ALL authentication/authorization paths, not just the one that appears broken. Is there a secondary check that catches it?
- Logic bugs pass every bounds check and mathematical proof — don't let clean static analysis convince you it's a false positive.

## Race Conditions

TOCTOU, data races, signal handling races, concurrent state modification.

**Verify:**

- What is the actual race window? Is it nanoseconds or seconds?
- Can the attacker widen the window (e.g., by stalling a thread with a slow NFS mount, large allocation, or CPU contention)?
- Verify the threading model: what threads/processes can actually access this data concurrently?
- Check all synchronization primitives in use — mutexes, atomics, RCU, lock-free structures.
- For TOCTOU on filesystem: can the attacker control the path between check and use (symlink races)?

## Integer Issues

Overflow, underflow, truncation, signedness errors, wraparound.

**Verify:**

- What are the exact integer types and their ranges at every point in the computation?
- Is the overflow signed (undefined behavior in C/C++ — compiler may exploit this) or unsigned (defined wraparound)?
- Trace the integer through all casts, conversions, and promotions. Where does truncation or sign extension occur?
- After the integer issue occurs, is the resulting value actually used in a dangerous way (allocation size, array index, loop bound)?
- Check if compiler warnings (`-Wconversion`, `-Wsign-compare`) flag this.

## Crypto Weaknesses

Weak algorithms, bad parameters, nonce reuse, padding oracle, insufficient randomness, timing side channels.

**Verify:**

- Check parameter choices against current standards (NIST, IETF) and known attacks. "AES-128" is fine; "DES" is not.
- Verify randomness sources. Is the PRNG cryptographically secure? Is it properly seeded?
- For nonce reuse: prove the same nonce can actually be used twice in practice, not just theoretically.
- For timing side channels: is the code actually reachable by an attacker who can measure timing? Network jitter may make remote timing attacks impractical.
- Compare the implementation against a reference implementation or test vectors from the spec.

## Injection

SQL injection, XSS, command injection, server-side template injection, path traversal, LDAP injection.

**Verify:**

- Trace attacker input from entry point to the sink (query, command, template, filesystem path). Is there any sanitization or escaping along the way?
- Check if the framework provides automatic escaping (e.g., parameterized queries, template auto-escaping). If so, is it actually enabled and not bypassed?
- For XSS: what context does the input land in (HTML body, attribute, JavaScript, URL)? Each requires different escaping.
- For path traversal: is the path canonicalized before the access check? Can `../` or null bytes bypass validation?
- Test actual payload delivery through all intermediate processing — encoding, decoding, and transformation steps may neutralize or enable the payload.

## Information Disclosure

Uninitialized memory reads, error message leaks, timing side channels, padding oracles.

**Verify:**

- What specific data leaks? Not all leaks are equal — a stack leak revealing ASLR base or canary is critical; one revealing a static string is worthless.
- Is the leaked data actually useful to an attacker for further exploitation (ASLR bypass, session tokens, crypto keys)?
- For uninitialized memory: prove the memory is actually uninitialized at the point of read, not just potentially uninitialized on some code path.
- For timing side channels: can the attacker make enough measurements with sufficient precision? What's the noise level?
- For error messages: does the error path actually reach the attacker, or is it logged server-side only?

## Denial of Service

Algorithmic complexity, resource exhaustion, crash bugs, infinite loops, memory bombs.

**Verify:**

- What is the resource consumption ratio? Attacker sends X bytes, server consumes Y resources. Is the amplification meaningful?
- Can the resource be reclaimed (connection closes, memory freed) or is it permanent exhaustion?
- For algorithmic complexity: what is the actual worst-case input? Prove it triggers worst-case behavior, don't just claim O(n²).
- For crash bugs: is the crash reliably triggerable, or does it depend on specific heap/stack layout?
- Does the service restart automatically? A crash that causes a 100ms restart is different from one that requires manual intervention.

## Deserialization

Unsafe deserialization, object injection, gadget chain exploitation.

**Verify:**

- Does the attacker actually control the serialized data that reaches the deserialization call?
- Does a usable gadget chain exist in the classpath/import graph? Without a gadget chain, unsafe deserialization is a design smell, not an exploitable bug.
- What deserialization library and version is in use? Are there known gadget chains for it?
- Are there type restrictions, allowlists, or look-ahead deserialization filters that block dangerous classes?
- For language-specific: Java `ObjectInputStream`, Python `pickle`, PHP `unserialize`, .NET `BinaryFormatter` each have different exploitation characteristics.


---

## Inlined: False Positive Patterns — Lessons Learned

# False Positive Patterns — Lessons Learned

Apply ALL items in this checklist to EACH potential bug during verification.

## Checklist

### 1. Trace Full Validation Chain

Don't analyze isolated code snippets. Trace backwards to find ALL validation that precedes potentially dangerous operations. Network packet size operations may look dangerous but often have bounds validation earlier in the function.

### 1a. Map Complete Conditional Logic Flow

Vulnerable-looking code may be unreachable due to conditional logic that creates mathematical guarantees. Example: array access `buffer[length-4]` appears unsafe when `length < 4`, but if the code is only reachable when `length > 12` due to earlier validation, the vulnerability is impossible.

**Verify:**

- What conditions must be met for execution to reach the alleged vulnerability?
- Do those conditions mathematically prevent the vulnerability scenario?
- Are there minimum size/length requirements that guarantee safe access?
- Does the conditional flow create impossible-to-violate bounds?

### 2. Identify Defensive Programming Patterns

Distinguish between actual vulnerabilities and defensive assertions/validations. `ASSERT(size == expected_size)` followed by size-controlled operations is defensive, not vulnerable. Verify that checks actually prevent the alleged vulnerability.

### 3. Confirm Exploitable Data Paths

Only report vulnerabilities with CONFIRMED exploitable data flow paths. Don't assume network-controlled data reaches dangerous functions without tracing the actual path step by step.

### 4. Understand Data Source Context

Distinguish between data sources and their trust levels. API return values, compile-time constants, and network data have different risk profiles. Determine the actual source and whether it is attacker-controlled.

### 5. Analyze Bounds Validation Logic

Look for mathematical relationships between validation checks and subsequent operations. If `packet_size >= MIN_SIZE` is checked and `MIN_SIZE >= sizeof(header)`, then `packet_size - sizeof(header)` cannot underflow.

### 6. Verify TOCTOU Claims

Time-of-check-time-of-use issues require proof that the checked value can change between check and use. If a size is checked and immediately used in the same function with no external modification possible, there is no TOCTOU.

### 7. Understand API Contract and Trust Boundaries

Always understand API contracts before claiming buffer overflows. Some APIs have built-in bounds protection and cannot write beyond the buffer regardless of input parameters.

### 8. Distinguish Internal Storage from External Input

Internal storage systems (configuration stores, registries) are controlled by trusted components, not attackers. Values set during installation by trusted components are not attacker-controlled.

### 9. Don't Confuse Pattern Recognition with Vulnerability Analysis

Code patterns that "look vulnerable" may be safely implemented due to context and API contracts. Size parameters being modified doesn't mean buffer overflow if the API prevents writing beyond bounds.

### 10. Verify Concurrent Access is Actually Possible

Don't assume race conditions exist without proving concurrent access patterns. Single-threaded initialization contexts cannot have race conditions. Verify the threading model and synchronization mechanisms.

### 11. Assess Real vs Theoretical Security Impact

Focus on vulnerabilities with actual security impact. Storage failure for non-critical data is an operational issue, not a security vulnerability. Ask: would this lead to code execution, privilege escalation, or information disclosure?

### 12. Understand Defense-in-Depth vs Primary Controls

Failure of defense-in-depth mechanisms is not always a vulnerability if primary protections exist. Token cleanup failure is not critical if tokens are single-use by design at the server.

### 13. Apply the Checklist Rigorously, Not Superficially

Having a checklist doesn't prevent false positives if it isn't applied systematically. For EVERY potential vulnerability, work through ALL checklist items before concluding.

---

## Red Flags for False Positives

### Pattern-Based False Positives

- Reporting vulnerabilities in validation/bounds-checking code itself
- Claiming TOCTOU without proving the value can change
- Ignoring preceding validation logic
- Assuming network data reaches operations without tracing the path
- Confusing defensive programming (assertions/checks) with vulnerabilities
- Analyzing vulnerable-looking patterns without tracing conditional logic that controls reachability
- Reporting "vulnerabilities" in error handling or cleanup code
- Flagging size calculations without understanding mathematical constraints
- Identifying "dangerous" functions without checking if inputs are bounded
- Claiming buffer overflows in fixed-size operations with compile-time bounds
- Reporting race conditions in single-threaded or synchronized contexts

### Context-Blind Analysis False Positives

- Analyzing code snippets without understanding broader system design
- Ignoring architectural guarantees (single-writer, trusted input sources)
- Missing that "vulnerable" code is unreachable due to earlier validation
- Confusing debug/development code paths with production paths
- Reporting issues in code that only runs during trusted installation/setup
- Flagging theoretical issues that cannot occur due to system architecture
- Missing that alleged vulnerabilities are prevented by framework or language guarantees
- Reporting issues in test-only or debug-only code paths as production vulnerabilities

### Mathematical/Bounds Analysis False Positives

- Reporting integer underflow without proving the mathematical condition can occur
- Claiming buffer overflow when bounds are mathematically guaranteed by validation
- Missing that conditional logic creates mathematical impossibility of vulnerable conditions
- Reporting off-by-one errors without checking if loop bounds prevent the condition
- Claiming memory corruption when allocation sizes are verified sufficient
- Reporting arithmetic overflow without checking if input ranges prevent the condition

### API Contract Misunderstanding False Positives

- Claiming buffer overflows when APIs have built-in bounds checking
- Reporting memory corruption for APIs that manage their own memory safely
- Missing that return values are already validated by the API contract
- Confusing API parameter modification with vulnerability when API prevents unsafe modification
- Reporting issues explicitly handled by the API's safety guarantees
- Missing that seemingly dangerous operations are safe due to API implementation details


---

## Inlined: Evidence Templates

# Evidence Templates

Use these templates when documenting verification evidence for each bug.

## Data Flow Documentation

```
Bug #N Data Flow Analysis
Source: [exact location] — Trust Level: [trusted/untrusted]
Path: Source → Validation1[file:line] → Transform[file:line] → Vulnerability[file:line]
Validation Points:
  - Check1: [condition] at [file:line] — [passes/fails/bypassed]
  - Check2: [condition] at [file:line] — [passes/fails/bypassed]
```

## Mathematical Bounds Proof

```
Bug #N Mathematical Analysis
Claim: Operation X is vulnerable to [overflow/underflow/bounds violation]
Given Constraints: [list all validation conditions]

Algebraic Proof:
1. [first constraint from validation]
2. [constant or known value]
3. [derived inequality]
...
N. Therefore: [vulnerability confirmed/debunked] (Q.E.D.)

Conclusion: [vulnerability is/is not mathematically possible]
```

**Example:**

```
Given: validation ensures (input_size >= MIN_SIZE)
Given: MIN_SIZE = 16, header_size = 8
Prove: (input_size - header_size) cannot underflow

1. input_size >= MIN_SIZE             (from validation)
2. MIN_SIZE = 16                      (constant)
3. header_size = 8                    (constant)
4. input_size >= 16                   (substitution of 1,2)
5. input_size - 8 >= 16 - 8          (subtract header_size from both sides)
6. input_size - header_size >= 8     (simplification)
7. Therefore: underflow impossible    (Q.E.D.)
```

## Attacker Control Analysis

```
Bug #N Attacker Control Analysis
Input Vector: [how attacker provides input]
Control Level: [full/partial/none]
Constraints: [what limits exist on attacker input]
Reachability: [can attacker-controlled data reach vulnerable operation?]
```

## PoC — Pseudocode with Data Flow Diagram

```
PoC for Bug #N: [Brief Description]

Data Flow Diagram:

[External Input] → [Validation Point] → [Processing] → [Vulnerable Operation]
     |                    |                   |                    |
  Attacker           (May be bypassed)    (Transforms data)   (Unsafe operation)
  Controlled              |                   |                    |
     |                    v                   v                    v
  [Malicious Data] → [Insufficient Check] → [Processed Data] → [Impact]

PSEUDOCODE:
function vulnerable_operation(user_data):
    validation_result = weak_validation(user_data)  // Explain why this fails
    processed_data = transform_data(user_data)      // Show transformation
    unsafe_operation(processed_data)               // Show vulnerability trigger
```

## Devil's Advocate Review

```
Bug #N Devil's Advocate Review
Vulnerability Claim: [brief description]

For each of the 13 questions from the devil's advocate review, document your answer:
1-11. [Challenges arguing AGAINST the vulnerability]
12-13. [Challenges arguing FOR the vulnerability — false-negative protection]

Final Assessment: [Vulnerability confirmed/debunked with reasoning]
```
