---
name: third-party-model-security
description: Secure the use of third-party AI models hosted in the cloud. Use when integrating, configuring, or reviewing connections to third-party model endpoints like OpenAI, Anthropic, or other hosted LLM services.
category: "secure_development"
subcategory: "large-language-model"
---

# Third-Party Model Security

## Security Requirements

When using third-party models hosted in the cloud, the following security requirements apply:

### 1. Authorization

Third-party models used in the solution MUST be authorized by the organization's information security team. Do not integrate with arbitrary third-party model providers without security review and approval.

### 2. Encrypted Communication

Connections to third-party model endpoints MUST be encrypted. All API calls to external model services must use TLS (HTTPS). Never send prompts or receive responses over unencrypted channels.

### 3. Credential Management

Credentials for third-party model endpoints MUST NOT be stored in source code. They must be managed and stored securely.

| Storage Method | Acceptable |
|---|---|
| Hardcoded in source code | **NO** |
| Committed to version control | **NO** |
| Baked into container images | **NO** |
| Environment variables (injected at runtime) | Yes |
| Secret management system (Vault, K8s Secrets) | Yes (preferred) |
| Encrypted configuration with access controls | Yes |

## Implementation Checklist

- [ ] Obtain information security approval for each third-party model provider
- [ ] Verify all connections use TLS (HTTPS endpoints only)
- [ ] Verify no credentials are stored in source code or version control
- [ ] Store credentials in a secret management system
- [ ] Inject credentials at runtime via environment variables or mounted secrets
- [ ] Scan repositories for accidentally committed credentials
- [ ] Rotate third-party API credentials on a regular schedule
- [ ] Monitor third-party model usage for unexpected patterns or costs
