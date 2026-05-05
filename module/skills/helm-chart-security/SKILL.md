---
name: helm-chart-security
description: >
  Secure Helm chart development, dependency management, and secret handling.
  Use when building, reviewing, or auditing Helm charts, values files,
  Chart.yaml dependencies, or Helm-based deployment pipelines.
category: "secure_development"
subcategory: "kubernetes"
---

# Helm Chart Security

## Risk Areas

| Risk | Description |
|---|---|
| **Vulnerable dependencies** | Charts include external libraries and base images that may contain known vulnerabilities |
| **Unsecured values** | Secrets stored as plaintext in `values.yaml` or checked into source control |
| **Insecure configuration** | Misconfigured RBAC, missing security contexts, permissive network policies |
| **Supply chain attacks** | Tampered or malicious chart versions pulled from untrusted repositories |
| **Lack of visibility** | Complex deployments without adequate logging and monitoring |

## Dependency Management

- Regularly review the `dependencies` array in `Chart.yaml`
- Check upstream producers for vulnerability disclosures
- Update dependencies with `helm dependency update path/to/chart`
- No known SCA tool scans Helm chart dependencies directly; manual review is required

## Chart Provenance

### Verifying Provenance

Helm supports cryptographic verification of chart packages. Provenance is **not enabled by default** when acquiring charts.

- Always pass verification flags when fetching charts (`helm verify`)
- If a chart provides a `.tgz.prov` file, verify its signature before use

### Charts Without Provenance

When upstream charts do not provide provenance, **vendor the dependency** to include its source directly in your project for scanning:

```bash
helm plugin install https://github.com/SecKatie/helm-vendor-plugin
helm vendor
```

This unpacks dependencies so they can be scanned by existing automated tooling (checkov, etc.).

### Creating Provenance

Sign your chart releases using GPG:

```bash
helm generate-unsigned-provenance .
gpg --clearsign chart_name-x.y.z.tgz.prov
mv chart_name-x.y.z.tgz.prov.asc chart_name-x.y.z.tgz.prov
helm verify chart_name-x.y.z.tgz
```

## Secure Configuration

### Secure Defaults in values.yaml

Chart authors MUST provide secure defaults, not leave security configuration to users:

- Define security contexts with `readOnlyRootFilesystem: true`, `runAsNonRoot: true`
- Set resource limits to prevent resource exhaustion
- Include all security-related configurations in `values.yaml` for visibility and easy modification
- Use checkov to scan charts for configuration issues: `checkov -d . --framework helm`

### Infrastructure Security Scanning

Use [checkov](https://www.checkov.io/) to detect misconfigurations in Helm templates and Kubernetes manifests. Output SARIF for integration with CI systems:

```bash
checkov -d . --framework helm -o sarif
```

## Secret Management

**Never store secrets in `values.yaml` or check them into source control.**

- Inject secrets during CI, not at chart authoring time
- Use the [helm-secrets](https://github.com/jkroepke/helm-secrets) plugin for encrypted values or KMS references
- Supported KMS backends include Vault, AWS Secrets Manager, GCP Secrets Manager, Azure Key Vault, 1Password, and others
- For local development, use GPG or [age](https://github.com/FiloSottile/age) encryption

## Logging

- Output logs to **stderr** for pickup by the cluster log stack (Promtail/Loki/Grafana, Fluentd, etc.)
- Never log secrets, API keys, or PII
- Prevent log injection by sanitizing all values before logging
- Use **structured JSON** logging in production; provide human-readable format for development
- Default to the production logging configuration in the chart

## Implementation Checklist

- [ ] `Chart.yaml` dependencies are reviewed and up-to-date
- [ ] Chart provenance is verified on fetch (`helm verify`)
- [ ] Charts without provenance are vendored for scanning
- [ ] Released charts are signed with GPG
- [ ] `values.yaml` provides secure defaults for all security contexts
- [ ] No secrets are stored in `values.yaml` or source control
- [ ] helm-secrets or equivalent KMS integration is used for secret management
- [ ] checkov or equivalent scanner runs in CI on chart templates
- [ ] Logs go to stderr; no secrets in log output
- [ ] Structured JSON logging is the default in the chart

## References

- [Helm documentation](https://helm.sh/)
- [Helm Provenance and Integrity](https://helm.sh/docs/topics/provenance/)
- [checkov](https://www.checkov.io/)
- [helm-secrets plugin](https://github.com/jkroepke/helm-secrets)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
