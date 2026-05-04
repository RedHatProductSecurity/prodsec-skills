---
name: semgrep
description: >-
  Run Semgrep static analysis scan on a codebase using parallel subagents.
  Supports two scan modes — "run all" (full ruleset coverage) and "important
  only" (high-confidence security vulnerabilities). Automatically detects and
  uses Semgrep Pro for cross-file taint analysis when available. Use when asked
  to scan code for vulnerabilities, run a security audit with Semgrep, find
  bugs, or perform static analysis. Spawns parallel workers for multi-language
  codebases.
license: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
origin: Adapted from Trail of Bits Skills Marketplace (https://github.com/trailofbits/skills)
category: "security_testing"
subcategory: "static-analysis"
---

# Semgrep Security Scan

Run a Semgrep scan with automatic language detection, parallel execution across language groups, and merged SARIF output.

## Essential Principles

1. **Always use `--metrics=off`** — Semgrep sends telemetry by default; `--config auto` also phones home. Every `semgrep` command must include `--metrics=off` to prevent data leakage during security audits.
2. **User must approve the scan plan (Step 3 is a hard gate)** — The original "scan this codebase" request is NOT approval. Present exact rulesets, target, engine, and mode; wait for explicit "yes"/"proceed" before running scanners.
3. **Third-party rulesets are required, not optional** — Trail of Bits, 0xdea, and Decurity rules catch vulnerabilities absent from the official registry. Include them whenever the detected language matches.
4. **Run all scan workers in parallel** — Parallel execution is the core performance advantage. Do not run language scans strictly one-after-another when independence allows overlap.
5. **Always check for Semgrep Pro before scanning** — Pro enables cross-file taint tracking and catches ~250% more true positives. Skipping the check means silently missing critical inter-file vulnerabilities.

## When to Use

- Security audit of a codebase
- Finding vulnerabilities before code review
- Scanning for known bug patterns
- First-pass static analysis

## When NOT to Use

- Binary analysis → Use binary analysis tools
- Already have Semgrep CI configured → Use existing pipeline
- Need cross-file analysis but no Pro license → Consider CodeQL as alternative
- Creating custom Semgrep rules → Use `semgrep-rule-creator` skill
- Porting existing rules to other languages → Use `semgrep-rule-variant-creator` skill

## Output Directory

All scan results, SARIF files, and temporary data are stored in a single output directory.

- **If the user specifies an output directory** in their prompt, use it as `OUTPUT_DIR`.
- **If not specified**, default to `./static_analysis_semgrep_1`. If that already exists, increment to `_2`, `_3`, etc.

In both cases, **always create the directory** with `mkdir -p` before writing any files.

```bash
# Resolve output directory
if [ -n "$USER_SPECIFIED_DIR" ]; then
  OUTPUT_DIR="$USER_SPECIFIED_DIR"
else
  BASE="static_analysis_semgrep"
  N=1
  while [ -e "${BASE}_${N}" ]; do
    N=$((N + 1))
  done
  OUTPUT_DIR="${BASE}_${N}"
fi
mkdir -p "$OUTPUT_DIR/raw" "$OUTPUT_DIR/results"
```

The output directory is resolved **once** at the start of Step 1 and used throughout all subsequent steps.

```
$OUTPUT_DIR/
├── rulesets.txt                 # Approved rulesets (logged after Step 3)
├── raw/                         # Per-scan raw output (unfiltered)
│   ├── python-python.json
│   ├── python-python.sarif
│   ├── python-django.json
│   ├── python-django.sarif
│   └── ...
└── results/                     # Final merged output
    └── results.sarif
```

## Prerequisites

**Required:** Semgrep CLI (`semgrep --version`). If not installed, see [Semgrep installation docs](https://semgrep.dev/docs/getting-started/).

**Optional:** Semgrep Pro — enables cross-file taint tracking, inter-procedural analysis, and additional languages (Apex, C#, Elixir). Check with:

```bash
semgrep --pro --validate --config p/default 2>/dev/null && echo "Pro available" || echo "OSS only"
```

**Limitations:** OSS mode cannot track data flow across files. Pro mode uses `-j 1` for cross-file analysis (slower per ruleset, but parallel rulesets compensate).

## Scan Modes

Select mode in Step 2 of the workflow. Mode affects both scanner flags and post-processing.

| Mode | Coverage | Findings Reported |
|------|----------|-------------------|
| **Run all** | All rulesets, all severity levels | Everything |
| **Important only** | All rulesets, pre- and post-filtered | Security vulns only, medium-high confidence/impact |

**Important only** applies two filter layers:
1. **Pre-filter**: `--severity MEDIUM --severity HIGH --severity CRITICAL` (CLI flag)
2. **Post-filter**: JSON metadata — keeps only `category=security`, `confidence∈{MEDIUM,HIGH}`, `impact∈{MEDIUM,HIGH}`

Details and jq commands are in **Inlined: scan modes** below.

## Orchestration Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│ Coordinator (this skill)                                         │
│ Step 1: Detect languages + check Pro availability                │
│ Step 2: Select scan mode + rulesets                              │
│ Step 3: Present plan + rulesets, get approval [⛔ HARD GATE]    │
│ Step 4: Run parallel scans (approved rulesets + mode)            │
│ Step 5: Merge results and report                                 │
└──────────────────────────────────────────────────────────────────┘
         │ Step 4
         ▼
┌─────────────────┐
│ Scan workers    │
│ (parallel)      │
├─────────────────┤
│ Python scanner  │
│ JS/TS scanner   │
│ Go scanner      │
│ Docker scanner  │
└─────────────────┘
```

## Workflow

**Follow the five steps below** (expanded from upstream `scan-workflow.md`). Track them as a checklist; Step 3 is mandatory approval before any scan.

| Step | Action | Gate | Key reference |
|------|--------|------|----------------|
| 1 | Resolve output dir, detect languages + Pro availability | — | Glob/file patterns below |
| 2 | Select scan mode + rulesets | — | **Inlined: rulesets** |
| 3 | Present plan, get explicit approval | ⛔ HARD | Ask the user |
| 4 | Run parallel scans | — | **Inlined: scanner task prompt** |
| 5 | Merge results and report | — | Merge SARIF (below) |

**Merge SARIF (Step 5, no upstream script required):** After optional important-only JSON post-filter (see inlined scan-modes), merge per-run SARIF files:

```bash
jq -s '{"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "runs": [.[].runs[]]}' "$OUTPUT_DIR/raw"/*.sarif > "$OUTPUT_DIR/results/results.sarif"
```

Adjust the glob if you need a subset. The upstream repo also ships a Python merge helper; *(see upstream Trail of Bits prodsec-skills for companion files)*.

Verify merged output parses as JSON and report counts by severity/category.

## Rationalizations to Reject

| Shortcut | Why It's Wrong |
|----------|----------------|
| "User asked for scan, that's approval" | Original request ≠ plan approval. Present plan, await explicit "yes" |
| "Step 3 task is blocking, just mark complete" | Do not skip the real approval gate |
| "I already know what they want" | Assumptions cause scanning wrong directories/rulesets. Present plan for verification |
| "Just use default rulesets" | User must see and approve exact rulesets before scan |
| "Add extra rulesets without asking" | Modifying approved list without consent breaks trust |
| "Third-party rulesets are optional" | Trail of Bits, 0xdea, Decurity catch vulnerabilities not in official registry — REQUIRED |
| "Use --config auto" | Sends metrics; less control over rulesets |
| "One scan at a time" | Defeats parallelism; run independent ruleset scans in parallel where safe |
| "Pro is too slow, skip --pro" | Cross-file analysis catches many more true positives; worth the time |
| "Semgrep handles GitHub URLs natively" | URL handling fails on repos with non-standard YAML; always clone first |
| "Cleanup is optional" | Cloned repos pollute the user's workspace and accumulate across runs |
| "Use `.` or relative path as target" | Prefer absolute paths for workers to avoid ambiguity |
| "Let the user pick an output dir later" | Output directory must be resolved at Step 1, before any files are created |

## Reference Index

| Topic | Location |
|-------|----------|
| Ruleset catalog + selection | **Inlined: rulesets** below |
| Important-only filters | **Inlined: scan modes** below |
| Worker instructions | **Inlined: scanner task prompt** below |
| Full step-by-step narrative | *(see upstream Trail of Bits prodsec-skills for companion files)* — `workflows/scan-workflow.md` |

## Success Criteria

- [ ] Output directory resolved (user-specified or auto-incremented default)
- [ ] All generated files stored inside `$OUTPUT_DIR`
- [ ] Languages detected with file counts; Pro status checked
- [ ] Scan mode selected by user (run all / important only)
- [ ] Rulesets include third-party rules for all detected languages
- [ ] User explicitly approved the scan plan (Step 3 gate passed)
- [ ] All scan workers completed; parallel execution used where applicable
- [ ] Every `semgrep` command used `--metrics=off`
- [ ] Approved rulesets logged to `$OUTPUT_DIR/rulesets.txt`
- [ ] Raw per-scan outputs stored in `$OUTPUT_DIR/raw/`
- [ ] `results.sarif` exists in `$OUTPUT_DIR/results/` and is valid JSON
- [ ] Important-only mode: post-filter applied before merge; unfiltered results preserved in `raw/`
- [ ] Results summary reported with severity and category breakdown
- [ ] Cloned repos (if any) cleaned up from `$OUTPUT_DIR/repos/`

---

## Inlined: scan modes (upstream `references/scan-modes.md`)

# Scan Modes Reference

## Mode: Run All

Full scan with all rulesets and severity levels. Current default behavior. No filtering applied — all findings are reported and triaged.

## Mode: Important Only

Focused on high-confidence security vulnerabilities. Excludes code quality, best practices, and low-confidence audit findings.

### Pre-Filter: CLI Severity Flag

Add these flags to every `semgrep` command:

```bash
--severity MEDIUM --severity HIGH --severity CRITICAL
```

This excludes LOW/INFO severity findings at scan time, reducing output volume before post-filtering.

### Post-Filter: Metadata Criteria

After scanning, filter each JSON result file to keep only findings matching ALL of:

| Metadata Field | Accepted Values | Rationale |
|---|---|---|
| `extra.metadata.category` | `"security"` | Excludes correctness, best-practice, maintainability, performance |
| `extra.metadata.confidence` | `"MEDIUM"`, `"HIGH"` | Excludes low-precision rules (high false positive rate) |
| `extra.metadata.impact` | `"MEDIUM"`, `"HIGH"` | Excludes low-impact informational findings |

**Third-party rules** (Trail of Bits, 0xdea, Decurity, etc.) may not have `confidence`/`impact`/`category` metadata. Findings **without** these metadata fields are **kept** — we cannot filter what is not annotated, and third-party rules are typically security-focused.

### Semgrep Metadata Background

Semgrep security rules have these metadata fields (required for `category: security` in the official registry):

| Field | Purpose | Values |
|---|---|---|
| `severity` (top-level) | Overall rule severity, derived from likelihood × impact | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `category` | Rule category | `security`, `correctness`, `best-practice`, `maintainability`, `performance` |
| `confidence` | True positive rate of the rule (precision) | `LOW`, `MEDIUM`, `HIGH` |
| `impact` | Potential damage if vulnerability is exploited | `LOW`, `MEDIUM`, `HIGH` |
| `likelihood` | How likely the vulnerability is exploitable | `LOW`, `MEDIUM`, `HIGH` |
| `subcategory` | Finding type | `vuln`, `audit`, `secure default` |

Key relationship: `severity = f(likelihood, impact)` while `confidence` is independent (describes rule quality, not vulnerability severity).

### Post-Filter jq Command

Apply to each JSON result file after scanning:

```bash
# Filter a single result file
jq '{
  results: [.results[] |
    ((.extra.metadata.category // "security") | ascii_downcase) as $cat |
    ((.extra.metadata.confidence // "HIGH") | ascii_upcase) as $conf |
    ((.extra.metadata.impact // "HIGH") | ascii_upcase) as $imp |
    select(
      ($cat == "security") and
      ($conf == "MEDIUM" or $conf == "HIGH") and
      ($imp == "MEDIUM" or $imp == "HIGH")
    )
  ],
  errors: .errors,
  paths: .paths
}' "$f" > "${f%.json}-important.json"
```

Default values (`// "security"`, `// "HIGH"`) handle third-party rules without metadata — they pass all filters by default.

### Filter All Result Files in a Directory

Raw scan output lives in `$OUTPUT_DIR/raw/`. The filter creates `*-important.json` files alongside the originals — the raw files are preserved unmodified.

```bash
# Apply important-only filter to all scan result JSON files in raw/
for f in "$OUTPUT_DIR/raw"/*-*.json; do
  [[ "$f" == *-triage.json || "$f" == *-important.json ]] && continue
  jq '{
    results: [.results[] |
      ((.extra.metadata.category // "security") | ascii_downcase) as $cat |
      ((.extra.metadata.confidence // "HIGH") | ascii_upcase) as $conf |
      ((.extra.metadata.impact // "HIGH") | ascii_upcase) as $imp |
      select(
        ($cat == "security") and
        ($conf == "MEDIUM" or $conf == "HIGH") and
        ($imp == "MEDIUM" or $imp == "HIGH")
      )
    ],
    errors: .errors,
    paths: .paths
  }' "$f" > "${f%.json}-important.json"
  BEFORE=$(jq '.results | length' "$f")
  AFTER=$(jq '.results | length' "${f%.json}-important.json")
  echo "$f: $BEFORE → $AFTER findings (filtered $(( BEFORE - AFTER )))"
done
```

### Scanner Task Modifications

In important-only mode, add `[SEVERITY_FLAGS]` to each scanner command:

```bash
semgrep [--pro if available] --metrics=off [SEVERITY_FLAGS] --config [RULESET] --json -o [OUTPUT_DIR]/raw/[lang]-[ruleset].json --sarif-output=[OUTPUT_DIR]/raw/[lang]-[ruleset].sarif [TARGET] &
```

Where `[SEVERITY_FLAGS]` is:
- **Run all**: *(empty)*
- **Important only**: `--severity MEDIUM --severity HIGH --severity CRITICAL`

---

## Inlined: scanner task prompt (upstream `references/scanner-task-prompt.md`)

# Scanner task prompt template

Use when delegating per-language Semgrep runs (replace bracketed placeholders).

## Template

```
You are a Semgrep scanner for [LANGUAGE_CATEGORY].

## Task
Run Semgrep scans for [LANGUAGE] files and save results to [OUTPUT_DIR]/raw.

## Pro Engine Status: [PRO_AVAILABLE: true/false]

## Scan Mode: [SCAN_MODE: run-all/important-only]

## APPROVED RULESETS (from user-confirmed plan)
[LIST EXACT RULESETS USER APPROVED - DO NOT SUBSTITUTE]

Example:
- p/python
- p/django
- p/security-audit
- p/secrets
- https://github.com/trailofbits/semgrep-rules

## Commands to Run (in parallel)

### Clone GitHub URL rulesets first:
```bash
mkdir -p [OUTPUT_DIR]/repos
# For each GitHub URL ruleset, clone into [OUTPUT_DIR]/repos/[name]:
git clone --depth 1 https://github.com/org/repo [OUTPUT_DIR]/repos/repo-name
```

### Generate commands for EACH approved ruleset:
```bash
semgrep [--pro if available] --metrics=off [SEVERITY_FLAGS] [INCLUDE_FLAGS] --config [RULESET] --json -o [OUTPUT_DIR]/raw/[lang]-[ruleset].json --sarif-output=[OUTPUT_DIR]/raw/[lang]-[ruleset].sarif [TARGET] &
```

Wait for all to complete:
```bash
wait
```

### Clean up cloned repos:
```bash
[ -n "[OUTPUT_DIR]" ] && rm -rf [OUTPUT_DIR]/repos
```

## Critical Rules
- Use ONLY the rulesets listed above - do not add or remove any
- Always use --metrics=off (prevents sending telemetry to Semgrep servers)
- Use --pro when Pro is available (enables cross-file taint tracking)
- If scan mode is **important-only**, add `--severity MEDIUM --severity HIGH --severity CRITICAL` to every command
- If scan mode is **run-all**, do NOT add severity flags
- Run all rulesets in parallel with & and wait
- For GitHub URL rulesets, always clone into [OUTPUT_DIR]/repos/ and use the local path as --config (do NOT pass URLs directly to semgrep — its URL handling is unreliable for repos with non-standard YAML)
- Add `--include` flags for language-specific rulesets (e.g., `--include="*.py"` for p/python). Do NOT add `--include` to cross-language rulesets like p/security-audit, p/secrets, or third-party repos
- After all scans complete, delete [OUTPUT_DIR]/repos/ to avoid leaving cloned repos behind

## Output
Report:
- Number of findings per ruleset
- Any scan errors
- File paths of JSON results (in [OUTPUT_DIR]/raw/)
- [If Pro] Note any cross-file findings detected
```

## Variable Substitutions

| Variable | Description | Example |
|----------|-------------|---------|
| `[LANGUAGE_CATEGORY]` | Language group being scanned | Python, JavaScript, Docker |
| `[LANGUAGE]` | Specific language | Python, TypeScript, Go |
| `[OUTPUT_DIR]` | Output directory (absolute path, resolved in Step 1) | /path/to/static_analysis_semgrep_1 |
| `[PRO_AVAILABLE]` | Whether Pro engine is available | true, false |
| `[SEVERITY_FLAGS]` | Severity pre-filter flags | *(empty)* for run-all, `--severity MEDIUM --severity HIGH --severity CRITICAL` for important-only |
| `[INCLUDE_FLAGS]` | File extension filter for language-specific rulesets | `--include="*.py"` for Python rulesets, *(empty)* for cross-language rulesets like p/security-audit, p/secrets, or third-party repos |
| `[RULESET]` | Semgrep ruleset identifier or local clone path | p/python, [OUTPUT_DIR]/repos/semgrep-rules |
| `[TARGET]` | Absolute path to directory to scan | /path/to/codebase |

---

## Inlined: rulesets (upstream `references/rulesets.md`)

# Semgrep Rulesets Reference

## Complete Ruleset Catalog

### Security-Focused Rulesets

| Ruleset | Description | Use Case |
|---------|-------------|----------|
| `p/security-audit` | Comprehensive vulnerability detection, higher false positives | Manual audits, security reviews |
| `p/secrets` | Hardcoded credentials, API keys, tokens | Always include |
| `p/owasp-top-ten` | OWASP Top 10 web application vulnerabilities | Web app security |
| `p/cwe-top-25` | CWE Top 25 most dangerous software weaknesses | General security |
| `p/sql-injection` | SQL injection patterns and tainted data flows | Database security |
| `p/insecure-transport` | Ensures code uses encrypted channels | Network security |
| `p/gitleaks` | Hard-coded credentials detection (gitleaks port) | Secrets scanning |
| `p/findsecbugs` | FindSecBugs rule pack for Java | Java security |
| `p/phpcs-security-audit` | PHP security audit rules | PHP security |

### CI/CD Rulesets

| Ruleset | Description | Use Case |
|---------|-------------|----------|
| `p/default` | Default ruleset, balanced coverage | First-time users |
| `p/ci` | High-confidence security + logic bugs, low FP | CI pipelines |
| `p/r2c-ci` | Low false positives, CI-safe | CI/CD blocking |
| `p/r2c` | Community favorite, curated by Semgrep (618k+ downloads) | General scanning |
| `p/auto` | Auto-selects rules based on detected languages/frameworks | Quick scans |
| `p/comment` | Comment-related rules | Code review |

### Third-Party Rulesets

| Ruleset | Description | Maintainer |
|---------|-------------|------------|
| `p/gitlab` | GitLab-maintained security rules | GitLab |

---

## Ruleset Selection Algorithm

Follow this algorithm to select rulesets based on detected languages and frameworks.

### Step 1: Always Include Security Baseline

```json
{
  "baseline": ["p/security-audit", "p/secrets"]
}
```

- `p/security-audit` - Comprehensive vulnerability detection (always include)
- `p/secrets` - Hardcoded credentials, API keys, tokens (always include)

### Step 2: Add Language-Specific Rulesets

For each detected language, add the primary ruleset. If a framework is detected, add its ruleset too.

**GA Languages (production-ready):**

| Detection | Primary Ruleset | Framework Rulesets | Pro Rule Count |
|-----------|-----------------|-------------------|----------------|
| `.py` | `p/python` | `p/django`, `p/flask`, `p/fastapi` | 710+ |
| `.js`, `.jsx` | `p/javascript` | `p/react`, `p/nodejs`, `p/express`, `p/nextjs`, `p/angular` | 250+ (JS), 70+ (JSX) |
| `.ts`, `.tsx` | `p/typescript` | `p/react`, `p/nodejs`, `p/express`, `p/nextjs`, `p/angular` | 230+ |
| `.go` | `p/golang` | `p/go` (alias) | 80+ |
| `.java` | `p/java` | `p/spring`, `p/findsecbugs` | 190+ |
| `.kt` | `p/kotlin` | `p/spring` | 60+ |
| `.rb` | `p/ruby` | `p/rails` | 40+ |
| `.php` | `p/php` | `p/symfony`, `p/laravel`, `p/phpcs-security-audit` | 50+ |
| `.c`, `.cpp`, `.h` | `p/c` | - | 150+ |
| `.rs` | `p/rust` | - | 40+ |
| `.cs` | `p/csharp` | - | 170+ |
| `.scala` | `p/scala` | - | Community |
| `.swift` | `p/swift` | - | 60+ |

**Beta Languages (Pro recommended):**

| Detection | Primary Ruleset | Notes |
|-----------|-----------------|-------|
| `.ex`, `.exs` | `p/elixir` | Requires Pro for best coverage |
| `.cls`, `.trigger` | `p/apex` | Salesforce; requires Pro |

**Experimental Languages:**

| Detection | Primary Ruleset | Notes |
|-----------|-----------------|-------|
| `.sol` | No official ruleset | Use Decurity third-party rules |
| `Dockerfile` | `p/dockerfile` | Limited rules |
| `.yaml`, `.yml` | `p/yaml` | K8s, GitHub Actions, docker-compose patterns |
| `.json` | `r/json.aws` | AWS IAM policies; use `r/json.*` for specific rules |
| Bash scripts | - | Community support |
| Cairo, Circom | - | Experimental, smart contracts |

**Framework detection hints:**

| Framework | Detection Signals | Ruleset |
|-----------|------------------|---------|
| Django | `settings.py`, `urls.py`, `django` in requirements | `p/django` |
| Flask | `flask` in requirements, `@app.route` | `p/flask` |
| FastAPI | `fastapi` in requirements, `@app.get/post` | `p/fastapi` |
| React | `package.json` with react dependency, `.jsx`/`.tsx` files | `p/react` |
| Next.js | `next.config.js`, `pages/` or `app/` directory | `p/nextjs` |
| Angular | `angular.json`, `@angular/` dependencies | `p/angular` |
| Express | `express` in package.json, `app.use()` patterns | `p/express` |
| NestJS | `@nestjs/` dependencies, `@Controller` decorators | `p/nodejs` |
| Spring | `pom.xml` with spring, `@SpringBootApplication` | `p/spring` |
| Rails | `Gemfile` with rails, `config/routes.rb` | `p/rails` |
| Laravel | `composer.json` with laravel, `artisan` | `p/laravel` |
| Symfony | `composer.json` with symfony, `config/packages/` | `p/symfony` |

### Step 3: Add Infrastructure Rulesets

| Detection | Ruleset | Description |
|-----------|---------|-------------|
| `Dockerfile` | `p/dockerfile` | Container security, best practices |
| `.tf`, `.hcl` | `p/terraform` | IaC misconfigurations, CIS benchmarks, AWS/Azure/GCP |
| k8s manifests | `p/kubernetes` | K8s security, RBAC issues |
| CloudFormation | `p/cloudformation` | AWS infrastructure security |
| GitHub Actions | `p/github-actions` | CI/CD security, secrets exposure |
| `.yaml`, `.yml` | `p/yaml` | Generic YAML patterns (K8s, docker-compose) |
| AWS IAM JSON | `r/json.aws` | IAM policy misconfigurations (use `--config r/json.aws`) |

### Step 4: Add Third-Party Rulesets

These are **NOT optional**. Include automatically when language matches:

| Languages | Source | Why Required |
|-----------|--------|--------------|
| Python, Go, Ruby, JS/TS, Terraform, HCL | [Trail of Bits](https://github.com/trailofbits/semgrep-rules) | Security audit patterns from real engagements (AGPLv3) |
| C, C++ | [0xdea](https://github.com/0xdea/semgrep-rules) | Memory safety, low-level vulnerabilities |
| Solidity, Cairo, Rust | [Decurity](https://github.com/Decurity/semgrep-smart-contracts) | Smart contract vulnerabilities, DeFi exploits |
| Go | [dgryski](https://github.com/dgryski/semgrep-go) | Additional Go-specific patterns |
| Android (Java/Kotlin) | [MindedSecurity](https://github.com/mindedsecurity/semgrep-rules-android-security) | OWASP MASTG-derived mobile security rules |
| Java, Go, JS/TS, C#, Python, PHP | [elttam](https://github.com/elttam/semgrep-rules) | Security consulting patterns |
| Dockerfile, PHP, Go, Java | [kondukto](https://github.com/kondukto-io/semgrep-rules) | Container and web app security |
| PHP, Kotlin, Java | [dotta](https://github.com/federicodotta/semgrep-rules) | Pentest-derived web/mobile app rules |
| Terraform, HCL | [HashiCorp](https://github.com/hashicorp-forge/semgrep-rules) | HashiCorp infrastructure patterns |
| Swift, Java, Cobol | [akabe1](https://github.com/akabe1/akabe1-semgrep-rules) | iOS and legacy system patterns |
| Java | [Atlassian Labs](https://github.com/atlassian-labs/atlassian-sast-ruleset) | Atlassian-maintained Java rules |
| Python, JS/TS, Java, Ruby, Go, PHP | [Apiiro](https://github.com/apiiro/malicious-code-ruleset) | Malicious code detection, supply chain |

### Step 5: Verify Rulesets

Before finalizing, verify official rulesets load:

```bash
# Quick validation (exits 0 if valid)
semgrep --config p/python --validate --metrics=off 2>&1 | head -3
```

Or browse the [Semgrep Registry](https://semgrep.dev/explore).

### Output Format

```json
{
  "baseline": ["p/security-audit", "p/secrets"],
  "python": ["p/python", "p/django"],
  "javascript": ["p/javascript", "p/react", "p/nodejs"],
  "docker": ["p/dockerfile"],
  "third_party": ["https://github.com/trailofbits/semgrep-rules"]
}
```
