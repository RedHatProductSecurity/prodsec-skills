---
name: constant-time-analysis
description: Detects timing side-channel vulnerabilities in cryptographic code. Use when implementing or reviewing crypto code, encountering division on secrets, secret-dependent branches, or constant-time programming questions in C, C++, Go, Rust, Swift, Java, Kotlin, C#, PHP, JavaScript, TypeScript, Python, or Ruby.
license: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
origin: Adapted from Trail of Bits Skills Marketplace (https://github.com/trailofbits/skills)
category: "secure_development"
subcategory: "crypto"
---

# Constant-Time Analysis

Analyze cryptographic code to detect operations that leak secret data through execution timing variations.

**Companion analyzer:** The upstream Trail of Bits **prodsec-skills** `constant-time-analysis` plugin ships `ct_analyzer/analyzer.py` and per-language reference docs *(see upstream Trail of Bits prodsec-skills for companion files)*.

## When to Use

```text
User writing crypto code? ──yes──> Use this skill
         │
         no
         │
         v
User asking about timing attacks? ──yes──> Use this skill
         │
         no
         │
         v
Code handles secret keys/tokens? ──yes──> Use this skill
         │
         no
         │
         v
Skip this skill
```

**Concrete triggers:**

- User implements signature, encryption, or key derivation
- Code contains `/` or `%` operators on secret-derived values
- User mentions "constant-time", "timing attack", "side-channel", "KyberSlash"
- Reviewing functions named `sign`, `verify`, `encrypt`, `decrypt`, `derive_key`

## When NOT to Use

- Non-cryptographic code (business logic, UI, etc.)
- Public data processing where timing leaks don't matter
- Code that doesn't handle secrets, keys, or authentication tokens
- High-level API usage where timing is handled by the library

## Language Selection

Based on the file extension or language context, use the matching upstream reference under `plugins/constant-time-analysis/skills/constant-time-analysis/references/`:

| Language   | File Extensions                   | Guide (upstream filename)        |
| ---------- | --------------------------------- | -------------------------------- |
| C, C++     | `.c`, `.h`, `.cpp`, `.cc`, `.hpp` | `compiled.md`                    |
| Go         | `.go`                             | `compiled.md`                    |
| Rust       | `.rs`                             | `compiled.md`                    |
| Swift      | `.swift`                          | `swift.md`                       |
| Java       | `.java`                           | `vm-compiled.md`                 |
| Kotlin     | `.kt`, `.kts`                     | `kotlin.md`                      |
| C#         | `.cs`                             | `vm-compiled.md`                 |
| PHP        | `.php`                            | `php.md`                         |
| JavaScript | `.js`, `.mjs`, `.cjs`             | `javascript.md`                  |
| TypeScript | `.ts`, `.tsx`                     | `javascript.md`                  |
| Python     | `.py`                             | `python.md`                      |
| Ruby       | `.rb`                             | `ruby.md`                        |

## Quick Start *(paths relative to upstream `constant-time-analysis` plugin)*

```bash
uv run ct_analyzer/analyzer.py <source_file>
uv run ct_analyzer/analyzer.py --warnings <source_file>
uv run ct_analyzer/analyzer.py --func 'sign|verify' <source_file>
uv run ct_analyzer/analyzer.py --json <source_file>
```

### Native compiled languages (C, C++, Go, Rust, Swift)

```bash
uv run ct_analyzer/analyzer.py --arch x86_64 crypto.c
uv run ct_analyzer/analyzer.py --arch arm64 crypto.c
uv run ct_analyzer/analyzer.py --opt-level O0 crypto.c
uv run ct_analyzer/analyzer.py --opt-level O3 crypto.c
```

### VM-compiled (Java, Kotlin, C#)

Bytecode/IL analysis; `--arch` / `--opt-level` do not apply.

### Prerequisites (summary)

| Language               | Requirements                                              |
| ---------------------- | --------------------------------------------------------- |
| C, C++, Go, Rust       | Compiler in PATH (`gcc`/`clang`, `go`, `rustc`)           |
| Swift                  | Xcode or Swift toolchain (`swiftc` in PATH)               |
| Java                   | JDK with `javac` and `javap` in PATH                      |
| Kotlin                 | Kotlin compiler + JDK (`javap`) in PATH                   |
| C#                     | .NET SDK + `ilspycmd`                                     |
| PHP                    | PHP with VLD extension or OPcache                         |
| JavaScript/TypeScript  | Node.js in PATH                                           |
| Python                 | Python 3.x in PATH                                        |
| Ruby                   | Ruby with `--dump=insns` support                          |

**macOS:** Homebrew Java / .NET may be keg-only — add to `PATH` (see upstream `vm-compiled.md`).

## Quick Reference

| Problem                | Detection                       | Fix                                          |
| ---------------------- | ------------------------------- | -------------------------------------------- |
| Division on secrets    | DIV, IDIV, SDIV, UDIV           | Barrett reduction or multiply-by-inverse     |
| Branch on secrets      | JE, JNE, BEQ, BNE               | Constant-time selection (cmov, bit masking)  |
| Secret comparison      | Early-exit memcmp               | Use `crypto/subtle` or constant-time compare |
| Weak RNG               | rand(), mt_rand, Math.random    | Use crypto-secure RNG                        |
| Table lookup by secret | Array subscript on secret index | Bit-sliced lookups                           |

## Interpreting Results

**PASSED** — No variable-time operations detected.

**FAILED** — Dangerous instructions found. Example:

```text
[ERROR] SDIV
  Function: decompose_vulnerable
  Reason: SDIV has early termination optimization; execution time depends on operand values
```

## Verifying Results (Avoiding False Positives)

**CRITICAL**: Not every flagged operation is a vulnerability. The tool has no data flow analysis — it flags ALL potentially dangerous operations regardless of whether they involve secrets.

For each flagged violation, ask: **Does this operation's input depend on secret data?**

1. **Identify the secret inputs** to the function (private keys, plaintext, signatures, tokens)
2. **Trace data flow** from the flagged instruction back to inputs
3. **Common false positive patterns:**

   ```c
   // FALSE POSITIVE: Division uses public constant, not secret
   int num_blocks = data_len / 16;  // data_len is length, not content

   // TRUE POSITIVE: Division involves secret-derived value
   int32_t q = secret_coef / GAMMA2;  // secret_coef from private key
   ```

4. **Document your analysis** for each flagged item

### Quick Triage Questions

| Question                                          | If Yes                | If No                 |
| ------------------------------------------------- | --------------------- | --------------------- |
| Is the operand a compile-time constant?           | Likely false positive | Continue              |
| Is the operand a public parameter (length, count)?| Likely false positive | Continue              |
| Is the operand derived from key/plaintext/secret? | **TRUE POSITIVE**     | Likely false positive |
| Can an attacker influence the operand value?      | **TRUE POSITIVE**     | Likely false positive |

## Limitations

1. **Static analysis only** — not runtime; misses cache / microarchitectural channels.
2. **No data flow analysis** — manual review required.
3. **Compiler/runtime variations** — output may differ by toolchain.

## Real-World Impact

- **KyberSlash (2023)**: Division in post-quantum ML-KEM implementations
- **Lucky Thirteen (2013)**: CBC padding validation timing
- **RSA timing attacks**: Division timing leaked key bits

## References

- [Cryptocoding Guidelines](https://github.com/veorq/cryptocoding)
- [KyberSlash](https://kyberslash.cr.yp.to/)
- [BearSSL Constant-Time](https://www.bearssl.org/constanttime.html)
