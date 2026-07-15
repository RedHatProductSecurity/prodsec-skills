---
name: secrets-detection-patterns
description: >
  Detect hardcoded secrets in source code using pattern-based scanning for API
  keys, tokens, passwords, private keys, and connection strings. Use before
  committing, during code review, or for post-incident history scanning.
  Self-contained — no external tools required.
metadata:
  category: secure_development
  subcategory: secrets-detection
---

# Secrets Detection Patterns

## Overview

Pattern-based secrets detection for source code. This skill provides regex patterns, false positive filtering criteria, and remediation guidance for detecting hardcoded secrets. It is self-contained — no external tools (trufflehog, gitleaks) are required, though they are recommended as complementary tooling.

## Zero Tolerance Policy

Any confirmed secret in code results in a BLOCKED verdict. There is no passing threshold — secrets in code are a critical finding. A secret is either present or it is not.

## Redaction Rule

Reports must NEVER include actual secret values. Report secret type, file path, and line number only. Pattern matches are redacted to show type and location: e.g., "AWS Access Key at `src/config.js:42`".

## Scan Scope Options

- **Staged** — scan git staged files only (pre-commit gate)
- **All** — scan entire working directory
- **History** — scan git commit history (post-incident review)

---

## Detection Patterns

### Pattern 1: AWS Access Keys

Format: `AKIA` followed by 16 alphanumeric characters.

```
AKIA[0-9A-Z]{16}
```

### Pattern 2: AWS Secret Access Keys

40-character base64-like strings after a known label.

```
(aws_secret_access_key|aws_secret_key)\s*[=:]\s*[A-Za-z0-9/+=]{40}
```

### Pattern 3: GitHub Personal Access Tokens

Prefixes: `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`.

```
(ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9_]{36}
```

### Pattern 4: Private Key Material

RSA, EC, DSA, and OpenSSH private key headers.

```
-----BEGIN (RSA |EC |DSA |OPENSSH |PRIVATE )PRIVATE KEY-----
```

### Pattern 5: Generic Passwords (Labeled)

High-confidence labeled password assignments with values >= 8 characters.

```
(password|passwd|pwd|secret|api_key|apikey|api_secret|client_secret|auth_token|access_token)\s*[=:]\s*['"][^'"]{8,}['"]
```

### Pattern 6: Database Connection Strings

Connection strings with embedded credentials.

```
(mysql|postgresql|postgres|mongodb|redis|amqp|jdbc)://[^@\s]+:[^@\s]+@
```

### Pattern 7: JWT Tokens

Three-part base64url segments separated by dots, starting with `eyJ`.

```
eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}
```

### Pattern 8: Slack Tokens

Prefix: `xox[bpaso]-`.

```
xox[bpaso]-[A-Za-z0-9-]{10,}
```

### Pattern 9: Google API Keys

Prefix: `AIza`.

```
AIza[0-9A-Za-z_-]{35}
```

### Pattern 10: Stripe API Keys

Prefixes: `sk_live_`, `pk_live_`, `rk_live_`, `sk_test_`.

```
(sk_live_|pk_live_|rk_live_|sk_test_)[0-9a-zA-Z]{24,}
```

---

## False Positive Filtering

Classify a match as **FALSE POSITIVE** if:

- The match is in a **test fixture** file (path contains: `test/`, `tests/`, `spec/`, `fixtures/`, `__tests__/`, `testdata/`)
- The match is in a **documentation file** (`.md`, `.rst`, `.txt`, `.adoc`) showing an example format
- The match is in a **comment** explaining what a secret looks like (e.g., `# example: AKIA...`)
- The match is an **obvious placeholder** (e.g., `AKIAIOSFODNN7…` — AWS's documented sample key — `your-secret-here`, `<YOUR_API_KEY>`, `xxx...xxx`)
- The match is in a `.env.example`, `.env.sample`, or `.env.template` file
- The match is in a README or CONTRIBUTING file describing configuration
- The value is clearly a **test/dummy value** (e.g., `password: 'test'` in test files)
- The match is in a **mock or stub** (file path contains `mock`, `stub`, `fake`)

Classify a match as **CONFIRMED** if:

- The match appears in a source code file that would be executed
- The match appears in a configuration file that is NOT an example/template
- The match appears in a script file or Dockerfile
- The value appears to be a real credential format (not a placeholder)
- The match appears in a git diff as an added line (staged scope)

---

## Remediation Guidance

When secrets are detected:

1. **Remove the secret and rotate the credential** (strongly recommended)
2. **Add the file to .gitignore** if it must not be committed
3. **Use environment variables or a secrets manager** instead of hardcoded values
4. **If this is a test fixture or example**, rename the file to include `example` or `fixture` and use obviously fake values

If secrets have been committed to git history, consider:
- Rotating the credential immediately (the secret is compromised regardless of git cleanup)
- Using `git filter-branch` or BFG Repo-Cleaner to remove from history
- Scanning with `trufflehog` or `gitleaks` for comprehensive history review

## Complementary Tooling

For production use, consider also deploying:
- **trufflehog** — entropy-based scanning for unstructured secrets
- **gitleaks** — pre-commit hook integration with configurable rules
- **A secrets manager** (HashiCorp Vault, AWS Secrets Manager, etc.) to eliminate secrets from code entirely

Note: The patterns in this skill use regex-based detection only. Entropy-based detection (for unstructured high-entropy strings) requires external tooling.


