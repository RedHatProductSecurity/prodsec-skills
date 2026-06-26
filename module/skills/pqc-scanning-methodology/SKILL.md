---
name: pqc-scanning-methodology
description: >
  Systematically scan a codebase for post-quantum cryptography readiness.
  Use when assessing PQC migration status, triaging cryptographic algorithm
  usage, building PQC remediation plans, writing Semgrep rules for quantum-
  vulnerable patterns, or when asked to evaluate quantum risk across a project.
category: "secure_development"
subcategory: "crypto"
---

# Post-Quantum Cryptography Scanning Methodology

Systematic approach to scanning a codebase for quantum-vulnerable
cryptography and building a remediation plan. Covers risk
classification, scanning techniques, triage, and migration strategy.

For algorithm selection guidance (what to use, what to avoid), see
`module/skills/algorithm-selection/SKILL.md`. This skill covers **how to find and triage**
quantum-vulnerable code at scale.

## Quantum Risk Classification

Classify every cryptographic usage by its quantum risk level:

| Risk | Criteria | Examples |
|------|----------|---------|
| **VULNERABLE** | Broken by Shor's algorithm (polynomial time) | RSA, ECDSA, ECDH, Ed25519, X25519, DSA, DH, ElGamal |
| **PARTIAL** | Weakened by Grover's algorithm (effective security halved) | AES-128, 3DES, HMAC-SHA1 |
| **SAFE** | Quantum-resistant at current parameters | AES-256, SHA-256/384/512, HMAC-SHA256, ChaCha20-Poly1305, ML-KEM, ML-DSA, SLH-DSA |
| **UNKNOWN** | Requires manual expert review | Custom implementations, proprietary algorithms, unusual constructions |

Key insight: **classify by algorithm, not key size.** RSA-4096 is still
quantum-vulnerable. ML-KEM-512 is quantum-safe (but has a lower security
margin than ML-KEM-768/1024 — see `module/skills/algorithm-selection/SKILL.md` for parameter
guidance). Key-size-based rules produce noise and miss the point.

## HNDL Severity Modifier

"Harvest Now, Decrypt Later" (HNDL): adversaries collect encrypted data
today to decrypt when cryptographically relevant quantum computers (CRQCs)
arrive. Increase severity by one level when the protected data has a
confidentiality requirement exceeding 10 years.

| HNDL risk level | Examples |
|-----------------|---------|
| **Highest** | Long-lived secrets (key vaults, CA private keys), encrypted databases and backups, archived sensitive records |
| **High** | TLS-protected data in transit (if captured by a passive observer) |
| **Low** | Ephemeral tokens, session keys, short-lived TOTP codes — no upgrade urgency |

## Scanning Priority Order

Focus analysis in this order — highest-impact usage first:

1. **HIGHEST**: Direct cryptographic operations — key generation,
   signing, encryption, key exchange, key derivation
2. **HIGH**: TLS/SSL configuration — cipher suites, protocol version
   constraints, LDAP/DB/AMQP TLS settings
3. **MEDIUM**: Authentication mechanisms — JWT algorithms (RS256,
   ES256), SAML signatures, OAuth/OIDC, JWKS key types, mTLS
4. **MEDIUM**: Transitive dependencies — crypto libraries used
   indirectly through frameworks, ORMs, or middleware
5. **LOWER**: Hash functions and symmetric crypto — only flag MD5,
   SHA-1, or AES-128 usage; SHA-256+ and AES-256 are safe

## Scanning Techniques

### Automated scanning with Semgrep or OpenGrep

Write rules that detect quantum-vulnerable patterns and classify them:

```yaml
rules:
  - id: pqc-rsa-keygen
    patterns:
      - pattern: rsa.generate_private_key(...)
    message: >
      RSA key generation — not quantum-safe.
      Consider ML-KEM/ML-DSA when available.
    languages: [python]
    severity: WARNING
    metadata:
      quantum_risk: VULNERABLE
      category: asymmetric-crypto

  - id: pqc-ecdsa-signing
    patterns:
      - pattern: ec.generate_private_key(...)
    message: >
      ECDSA key generation — not quantum-safe.
    languages: [python]
    severity: WARNING
    metadata:
      quantum_risk: VULNERABLE
      category: asymmetric-crypto

  - id: pqc-jwt-rs256
    patterns:
      - pattern: jwt.encode(..., algorithm="RS256", ...)
    message: >
      RS256 JWT — RSA signature, not quantum-safe.
    languages: [python]
    severity: WARNING
    metadata:
      quantum_risk: VULNERABLE
      category: auth-mechanism
```

Exclude test fixtures, documentation, and migration code to reduce
noise.

### Manual search patterns

```bash
# Asymmetric crypto (VULNERABLE)
rg "RSA|ECDSA|ECDH|Ed25519|X25519|DSA\b|DH\b|ElGamal" \
  --type py --type go --type java --type rust

# TLS configuration
rg "ssl_version|PROTOCOL_TLS|TLSv1_2|min_version|cipher_suite" \
  --type py --type go --type yaml

# JWT algorithms
rg "RS256|RS384|RS512|ES256|ES384|ES512|PS256" \
  --type py --type go --type java

# Certificate operations
rg "x509|generate_private_key|load_pem|sign_certificate" \
  --type py --type go --type java

# Positive detection (SAFE — PQC algorithms already adopted)
rg "ML-KEM|ML-DSA|SLH-DSA|Kyber|Dilithium|SPHINCS" \
  --type py --type go --type java
```

### Dependency manifest scanning

Check `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`,
`package.json` for crypto libraries. Flag libraries that default to
quantum-vulnerable algorithms:

| Library | Language | Default risk |
|---------|----------|-------------|
| `pyca/cryptography` | Python | Provides both; check usage |
| `pycryptodome` | Python | Provides RSA/ECDSA |
| `crypto/rsa`, `crypto/ecdsa` | Go | VULNERABLE by definition |
| `ring` | Rust | Provides both; check usage |
| `bouncy-castle` | Java | Provides both; check usage |
| `openssl` | C/C++ | Depends on version and config |

## TLS 1.2 Protocol Blocker

TLS 1.2 cannot use PQC key exchange — the IETF decided PQC will not
be retrofitted to TLS 1.2. Code that forces TLS 1.2 via
`ssl.PROTOCOL_TLSv1_2`, `ssl_version = tlsv1_2`, `MinVersion: tls.VersionTLS12`,
or equivalent is a protocol-level blocker for PQC adoption.

Report this even if the underlying crypto library supports PQC.

TLS 1.3 with hybrid key exchange (e.g., `X25519MLKEM768`) is the
migration path. OpenSSL 3.5+ defaults to this for TLS 1.3
connections.

## Triaging Findings

For each finding, record:

| Field | Content |
|-------|---------|
| **Location** | File and line |
| **Algorithm** | Specific algorithm detected |
| **Quantum risk** | VULNERABLE / PARTIAL / SAFE / UNKNOWN |
| **Category** | asymmetric-crypto, tls-config, auth-mechanism, hash, symmetric |
| **HNDL modifier** | Yes (long-lived data) / No (ephemeral) |
| **Severity** | Based on quantum risk + HNDL modifier |
| **Configurable?** | Is the algorithm hardcoded or configurable? |
| **Action** | Replace / Configure / Accept risk / No action |

**Triage priority:**
1. VULNERABLE + HNDL (highest) — long-lived secrets with
   quantum-vulnerable protection
2. VULNERABLE + no HNDL — standard quantum-vulnerable usage
3. PARTIAL — weakened but not broken; plan migration
4. SAFE — no action needed; record as positive detection

## Migration Strategy

Follow the industry hybrid approach during the transition period:

- **Hybrid key exchange** provides defense-in-depth: if either the
  classical or PQC algorithm is broken, the other still protects
  the connection. Prefer X25519MLKEM768 for TLS 1.3.
- **Design for crypto agility**: abstract crypto behind interfaces,
  externalize algorithm selection to configuration, avoid hardcoding
  algorithm names.
- **Do not switch to pure PQC yet** for signatures — wait for
  hardware-backed (HSM/TPM) ML-DSA support. Continue using ECDSA
  for mTLS and code signing in the interim.
- **Telemetry**: capture negotiated groups, handshake sizes, and
  failure causes to monitor PQC adoption progress.

## Timeline Reference

| Date | Milestone |
|------|-----------|
| 2024-2025 | NIST finalized FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) |
| April 2025 | OpenSSL 3.5 released with production-ready PQC support |
| 2030-2035 | Cryptographically Relevant Quantum Computers expected |
| 2035 | U.S. government target for full PQC migration (NSM-10) |

## Output: PQC Assessment Report

Structure findings as:

```text
## PQC Assessment: <project name>

### Summary
- Total findings: N
- VULNERABLE: N (asymmetric crypto at risk from Shor's algorithm)
- PARTIAL: N (symmetric/hash weakened by Grover's algorithm)
- SAFE: N (already quantum-safe)
- HNDL-elevated: N (long-lived data with elevated urgency)

### Findings by Priority
[Grouped by triage priority, highest first]

### TLS Configuration
- TLS 1.2 forced: [locations] — protocol-level PQC blocker
- TLS 1.3 available: [locations] — ready for hybrid KEX

### Recommendations
1. [Immediate: critical HNDL items]
2. [Short-term: VULNERABLE items without HNDL]
3. [Medium-term: PARTIAL items, TLS 1.2 migration]
4. [Ongoing: crypto agility improvements]
```

## Relationship to Other Skills

- **`module/skills/algorithm-selection/SKILL.md`** — Covers which algorithms to use and
  which to avoid, including PQC recommendations. This skill covers
  how to systematically find and triage what a codebase currently uses.
- **`module/skills/semgrep-rule-creator/SKILL.md`** — Use to build custom Semgrep rules for
  PQC-specific patterns not covered by generic crypto rules.
- **`module/skills/supply-chain-risk-auditor/SKILL.md`** — Check transitive dependencies
  for quantum-vulnerable crypto libraries.
