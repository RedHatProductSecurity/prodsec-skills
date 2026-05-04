---
name: insecure-defaults
description: "Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow apps to run insecurely in production. Use when auditing security, reviewing config management, or analyzing environment variable handling."
license: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
origin: Adapted from Trail of Bits Skills Marketplace (https://github.com/trailofbits/skills)
category: "secure_development"
subcategory: "secure-config"
---

# Insecure Defaults Detection

Finds **fail-open** vulnerabilities where apps run insecurely with missing configuration. Distinguishes exploitable defaults from fail-secure patterns that crash safely.

- **Fail-open (CRITICAL):** `SECRET = env.get('KEY') or 'default'` → App runs with weak secret
- **Fail-secure (SAFE):** `SECRET = env['KEY']` → App crashes if missing

## When to Use

- **Security audits** of production applications (auth, crypto, API security)
- **Configuration review** of deployment files, IaC templates, Docker configs
- **Code review** of environment variable handling and secrets management
- **Pre-deployment checks** for hardcoded credentials or weak defaults

## When NOT to Use

Do not use this skill for:
- **Test fixtures** explicitly scoped to test environments (files in `test/`, `spec/`, `__tests__/`)
- **Example/template files** (`.example`, `.template`, `.sample` suffixes)
- **Development-only tools** (local Docker Compose for dev, debug scripts)
- **Documentation examples** in README.md or docs/ directories
- **Build-time configuration** that gets replaced during deployment
- **Crash-on-missing behavior** where app won't start without proper config (fail-secure)

When in doubt: trace the code path to determine if the app runs with the default or crashes.

## Rationalizations to Reject

- **"It's just a development default"** → If it reaches production code, it's a finding
- **"The production config overrides it"** → Verify prod config exists; code-level vulnerability remains if not
- **"This would never run without proper config"** → Prove it with code trace; many apps fail silently
- **"It's behind authentication"** → Defense in depth; compromised session still exploits weak defaults
- **"We'll fix it before release"** → Document now; "later" rarely comes

## Workflow

Follow this workflow for every potential finding:

### 1. SEARCH: Perform Project Discovery and Find Insecure Defaults

Determine language, framework, and project conventions. Use this information to further discover things like secret storage locations, secret usage patterns, credentialed third-party integrations, cryptography, and any other relevant configuration. Further use information to analyze insecure default configurations.

**Example**
Search for patterns in `**/config/`, `**/auth/`, `**/database/`, and env files:
- **Fallback secrets:** `getenv.*\) or ['"]`, `process\.env\.[A-Z_]+ \|\| ['"]`, `ENV\.fetch.*default:`
- **Hardcoded credentials:** `password.*=.*['"][^'"]{8,}['"]`, `api[_-]?key.*=.*['"][^'"]+['"]`
- **Weak defaults:** `DEBUG.*=.*true`, `AUTH.*=.*false`, `CORS.*=.*\*`
- **Crypto algorithms:** `MD5|SHA1|DES|RC4|ECB` in security contexts

Tailor search approach based on discovery results.

Focus on production-reachable code, not test fixtures or example files.

### 2. VERIFY: Actual Behavior
For each match, trace the code path to understand runtime behavior.

**Questions to answer:**
- When is this code executed? (Startup vs. runtime)
- What happens if a configuration variable is missing?
- Is there validation that enforces secure configuration?

### 3. CONFIRM: Production Impact
Determine if this issue reaches production:

If production config provides the variable → Lower severity (but still a code-level vulnerability)
If production config missing or uses default → CRITICAL

### 4. REPORT: with Evidence

**Example report:**
```
Finding: Hardcoded JWT Secret Fallback
Location: src/auth/jwt.ts:15
Pattern: const secret = process.env.JWT_SECRET || 'default';

Verification: App starts without JWT_SECRET; secret used in jwt.sign() at line 42
Production Impact: Dockerfile missing JWT_SECRET
Exploitation: Attacker forges JWTs using 'default', gains unauthorized access
```

## Quick Verification Checklist

**Fallback Secrets:** `SECRET = env.get(X) or Y`
→ Verify: App starts without env var? Secret used in crypto/auth?
→ Skip: Test fixtures, example files

**Default Credentials:** Hardcoded `username`/`password` pairs
→ Verify: Active in deployed config? No runtime override?
→ Skip: Disabled accounts, documentation examples

**Fail-Open Security:** `AUTH_REQUIRED = env.get(X, 'false')`
→ Verify: Default is insecure (false/disabled/permissive)?
→ Safe: App crashes or default is secure (true/enabled/restricted)

**Weak Crypto:** MD5/SHA1/DES/RC4/ECB in security contexts
→ Verify: Used for passwords, encryption, or tokens?
→ Skip: Checksums, non-security hashing

**Permissive Access:** CORS `*`, permissions `0777`, public-by-default
→ Verify: Default allows unauthorized access?
→ Skip: Explicitly configured permissiveness with justification

**Debug Features:** Stack traces, introspection, verbose errors
→ Verify: Enabled by default? Exposed in responses?
→ Skip: Logging-only, not user-facing

**SD3 (Secure by Design, Default, Deployment) Patterns:**
→ Verify: Does the system fail open or fail closed when config is missing?
→ Verify: Is HTTPS the default protocol, or must users opt in?
→ Verify: Are update mechanisms signed and verified?
→ Verify: Are default-deny network policies in place?
→ Skip: Explicit fail-secure behavior (crashes or denies access on missing config)

More category examples: **Inlined: examples** below. Full catalog: *(see upstream Trail of Bits prodsec-skills for companion files)*.

---

## Inlined: examples (excerpt, upstream `references/examples.md`)

# Insecure Defaults: Examples and Counter-Examples

## Fallback Secrets

### ❌ VULNERABLE - Report These

**Python: Environment variable with fallback**
```python
# File: src/auth/jwt.py
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

# Used in security context
def create_token(user_id):
    return jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')
```
**Why vulnerable:** App runs with known secret if `SECRET_KEY` is missing. Attacker can forge tokens.

**JavaScript: Logical OR fallback**
```javascript
// File: config/database.js
const DB_PASSWORD = process.env.DB_PASSWORD || 'admin123';

const pool = new Pool({
  user: 'admin',
  password: DB_PASSWORD,
  database: 'production'
});
```
**Why vulnerable:** Database accepts hardcoded password in production if env var missing.

**Ruby: fetch with default**
```ruby
# File: config/secrets.rb
Rails.application.credentials.secret_key_base =
  ENV.fetch('SECRET_KEY_BASE', 'fallback-secret-base')
```
**Why vulnerable:** Rails session encryption uses weak known key as fallback.

### ✅ SECURE - Skip These

**Fail-secure: Crashes without config**
```python
# File: src/auth/jwt.py
SECRET_KEY = os.environ['SECRET_KEY']  # Raises KeyError if missing

# App won't start without SECRET_KEY - fail-secure
```

**Explicit validation**
```javascript
// File: config/database.js
if (!process.env.DB_PASSWORD) {
  throw new Error('DB_PASSWORD environment variable required');
}
const DB_PASSWORD = process.env.DB_PASSWORD;
```

**Test fixtures (clearly scoped)**
```python
# File: tests/fixtures/auth.py
TEST_SECRET = 'test-secret-key-123'  # OK - test-only

# Usage in test
def test_token_creation():
    token = create_token('user1', secret=TEST_SECRET)
```

---

## Default Credentials

### ❌ VULNERABLE - Report These

**Hardcoded admin account**
```python
# File: src/models/user.py
def bootstrap_admin():
    """Create default admin account if none exists"""
    if not User.query.filter_by(role='admin').first():
        admin = User(
            username='admin',
            password=hash_password('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
```
**Why vulnerable:** Default admin account created on first run with known credentials.

**API key in code**
```javascript
// File: src/integrations/payment.js
const STRIPE_API_KEY = process.env.STRIPE_KEY || 'sk_tes...';

const stripe = require('stripe')(STRIPE_API_KEY);
```
**Why vulnerable:** Uses test API key if env var missing. Might reach production.

Further sections (weak crypto defaults, CORS, debug flags, ORM defaults, container/env files): *(see upstream Trail of Bits prodsec-skills for companion files)* — full `references/examples.md`.
