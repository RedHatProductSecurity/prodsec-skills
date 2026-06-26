---
name: security-test-writing
description: >
  Write manual security tests that prove vulnerabilities are real and fixes are
  effective. Use when writing tests for security fixes, verifying vulnerability
  patches, building regression test suites for CVEs, or when a security review
  identifies gaps in test coverage for authorization, authentication, or input
  validation.
category: "security_testing"
subcategory: "manual-testing"
---

# Security Test Writing

Write tests that prove a vulnerability exists, verify that a fix
resolves it, and prevent regressions. Covers the "prove it before
fixing" methodology, negative test patterns, and security-specific
coverage checklists.

For automated fuzz testing, see the fuzzing skills under
`module/skills/harness-writing/SKILL.md`. For static analysis,
see `module/skills/semgrep-rule-creator/SKILL.md`. This skill covers **manually authored
security tests** — the kind that demonstrate a specific attack
scenario and verify the defense.

## When to Use

- A security vulnerability has been found and needs a test before
  the fix is written
- A security patch is being reviewed and lacks test coverage
- Building a regression test suite after a CVE fix
- A security audit identified missing authorization, authentication,
  or input validation tests
- Reviewing AI-generated test code for security completeness

## When NOT to Use

- Broad coverage improvement without a specific security finding
  (use standard test practices)
- Fuzz target writing (use `module/skills/harness-writing/SKILL.md`)
- Static analysis rule writing (use `module/skills/semgrep-rule-creator/SKILL.md`)

## Core Principle: Prove It Before Fixing

Write a failing test first that demonstrates the vulnerability is
real. Then write the fix. Then confirm the test passes.

```text
1. Write test → test FAILS (vulnerability confirmed)
2. Write fix  → test PASSES (fix verified)
3. Commit both test and fix together
```

This approach:
- **Proves the bug is real** — not a theoretical concern
- **Documents the exact attack** in executable form
- **Prevents regressions** — if someone reverts the fix, the test
  catches it
- **Verifies the fix is complete** — not just patching one path

## Security Test Coverage Checklist

Every security fix should have tests covering:

- [ ] **Negative test (attack rejected)**: The attack scenario that
  exploits the vulnerability must be rejected after the fix
- [ ] **Positive test (legitimate use works)**: The fix does not
  break legitimate functionality
- [ ] **All affected entry points**: If the vulnerability exists in
  multiple HTTP methods, endpoints, or code paths, test each one
- [ ] **All affected credential/role types**: Test with the minimum
  privilege level that could exploit the vulnerability, plus
  legitimate higher-privilege access
- [ ] **Boundary conditions**: Test at the edges — empty input,
  maximum size, null values, special characters

## Test Patterns by Vulnerability Class

### Authorization bypass

Test that unauthorized access is rejected and authorized access
still works:

```python
def test_unprivileged_user_cannot_access_admin_resource(self):
    """Restricted role must not reach the admin endpoint."""
    token = self.get_token(role="reader")
    response = self.client.post("/admin/resource", token=token)
    assert response.status_code == 403

def test_admin_user_can_access_admin_resource(self):
    """Admin role must still work after the fix."""
    token = self.get_token(role="admin")
    response = self.client.post("/admin/resource", token=token)
    assert response.status_code == 200
```

Test all HTTP methods — a common pattern is enforcing authorization
on POST but missing it on GET or DELETE:

```python
@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "DELETE"])
def test_authorization_enforced_on_all_methods(self, method):
    token = self.get_token(role="reader")
    response = self.client.open(
        "/protected/resource", method=method, token=token
    )
    assert response.status_code == 403
```

### Credential restriction bypass

Test that restricted credentials cannot perform privileged
operations:

```python
def test_restricted_credential_cannot_create_other_credentials(self):
    """A restricted app credential must not escalate privileges."""
    cred = self.create_credential(restricted=True)
    token = self.get_token(credential=cred)
    response = self.client.post(
        "/credentials", token=token, json={"type": "ec2"}
    )
    assert response.status_code == 403

def test_unrestricted_credential_can_create_other_credentials(self):
    cred = self.create_credential(restricted=False)
    token = self.get_token(credential=cred)
    response = self.client.post(
        "/credentials", token=token, json={"type": "ec2"}
    )
    assert response.status_code == 201
```

### Input validation / injection

Test that malicious input is rejected:

```python
def test_ldap_injection_in_username_rejected(self):
    """LDAP special characters in username must be escaped."""
    response = self.client.post("/login", json={
        "username": "admin)(|(objectClass=*)",
        "password": "anything",
    })
    assert response.status_code in (400, 401)
    # Verify no LDAP results were returned
    assert "admin" not in response.text

def test_valid_username_still_works(self):
    response = self.client.post("/login", json={
        "username": "legitimate_user",
        "password": "correct_password",
    })
    assert response.status_code == 200
```

### Header spoofing / middleware bypass

Test that spoofed headers do not grant elevated privileges:

```python
def test_spoofed_admin_header_not_trusted(self):
    """Forged privilege headers must be stripped by middleware."""
    response = self.client.get(
        "/api/resource",
        headers={"X-Is-Admin-Project": "True"},
        token=self.unprivileged_token,
    )
    assert response.status_code == 403

def test_legitimate_admin_header_set_by_middleware(self):
    """Real admin requests must still get the header from middleware."""
    response = self.client.get(
        "/api/resource",
        token=self.admin_token,
    )
    assert response.status_code == 200
```

### TOCTOU / race conditions

Test that the check and the action are atomic:

```python
def test_concurrent_withdrawal_does_not_double_spend(self):
    """Parallel requests must not bypass balance check."""
    self.set_balance(user_id, 100)
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [
            pool.submit(self.client.post, "/withdraw", json={"amount": 100})
            for _ in range(10)
        ]
        results = [f.result() for f in futures]
    successes = [r for r in results if r.status_code == 200]
    assert len(successes) == 1
    assert self.get_balance(user_id) == 0
```

## Common Anti-Patterns in Security Tests

Avoid these patterns that undermine test value:

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| **Asserting on mocks** | Proves nothing about real behavior | Assert on observable API responses or state changes |
| **Testing only the happy path** | Misses the actual vulnerability | Always include the negative (attack) case |
| **Testing with admin credentials** | Admin can do everything; proves nothing about authorization | Test with the minimum credential that should be rejected |
| **Hardcoding test to implementation** | Breaks on refactor; does not test the contract | Assert on behavior (HTTP status, response body) not internal state |
| **Single HTTP method** | Authorization bypass on other methods missed | Parameterize across all relevant methods |
| **No boundary values** | Edge cases are where vulnerabilities hide | Test empty, null, maximum, and malformed inputs |

## Reviewing AI-Generated Security Tests

When AI assistants generate security tests, verify:

- [ ] The test actually fails before the fix is applied (not a
  tautology that always passes)
- [ ] Assertions check the right thing — not just "no exception
  thrown" but the specific security property
- [ ] The test uses realistic attack payloads, not placeholder
  strings
- [ ] Mock objects do not mask the behavior being tested
- [ ] The credential/role used in the test matches the real threat
  model (attacker privilege level)
- [ ] APIs, methods, and configuration referenced in the test
  actually exist in the codebase

## Output

For each security fix, deliver:

1. **Failing test** that demonstrates the vulnerability (runs
   against the unfixed code)
2. **Passing test** that verifies the fix (runs against the fixed
   code)
3. **Coverage notes** listing which entry points, methods, and
   credential types are covered and any known gaps
4. **Regression value** — how the test prevents reintroduction
   of the vulnerability

## Relationship to Other Skills

- **`module/skills/harness-writing/SKILL.md`** — Automated coverage-guided testing. This skill
  covers manually authored tests for specific known vulnerabilities.
- **`module/skills/variant-analysis/SKILL.md`** — After finding one vulnerability, use
  variant analysis to find others, then write security tests for
  each variant found.
- **`module/skills/differential-review/SKILL.md`** — During code review, identify missing
  security tests and use this skill to write them.
- **`module/skills/inconsistency-detection/SKILL.md`** — When an inconsistency is found,
  write a test that demonstrates the gap before fixing it.
