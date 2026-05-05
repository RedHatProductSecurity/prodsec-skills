---
name: authentication
description: Enforce standard authentication for external data source connections. Use when integrating, configuring, or reviewing connections from AI systems to external databases, APIs, or data services.
category: "secure_development"
subcategory: "external-data-source"
---

# Authentication for External Data Sources

## Security Requirement

External data sources MUST require that the principal (user or service) connecting to them is identified and authenticated. The authentication MUST use standard protocols.

## Standard Authentication Protocols

| Protocol | Use Case |
|---|---|
| **OAuth 2.1 / OIDC** | Web APIs, REST services, cloud data sources |
| **SPIFFE/SPIRE + mTLS** | Service-to-service connections within infrastructure |
| **SAML** | Federated enterprise data sources |
| **Kerberos** | On-premise databases and services (Active Directory environments) |
| **Client certificates (mTLS)** | Machine-to-machine data source access |

## What Is Not Acceptable

- Unauthenticated connections to data sources containing any data
- Shared credentials used by all services
- Credentials embedded in connection strings in source code
- Long-lived API keys without rotation (see `api_keys/avoid-api-keys`)

## Implementation Checklist

- [ ] Identify all external data sources accessed by the AI system
- [ ] Require authentication for every data source connection
- [ ] Use standard authentication protocols (OAuth, mTLS, Kerberos)
- [ ] Use unique credentials per service or workload (no shared credentials)
- [ ] Store credentials in a secret management system
- [ ] Rotate credentials on a regular schedule
- [ ] Log authentication events (successes and failures)
