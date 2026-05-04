---
name: encrypted-communication
description: Enforce encrypted communication with external data sources. Use when designing, configuring, or reviewing network connections between AI systems and external databases, APIs, or data services.
category: "secure_development"
subcategory: "external-data-source"
---

# Encrypted Communication with External Data Sources

## Security Requirement

Network communication with external data sources MUST be encrypted. This applies to all connections, not just those carrying sensitive data.

## Rationale

Encrypted communication is required for:

1. **Confidentiality**: Prevent interception of data in transit
2. **Integrity**: Prevent tampering with data in transit
3. **Compliance**: Required by widespread security standards and zero trust architectures
4. **Zero trust**: In a zero trust model, no network path is considered trustworthy, so all communication must be encrypted regardless of whether it is "internal" or "external"

## Encryption Requirements

| Requirement | Details |
|---|---|
| **TLS version** | TLS 1.2 minimum; TLS 1.3 preferred |
| **Certificate validation** | Verify server certificates; do not disable certificate checks |
| **Strong cipher suites** | Use only modern, approved cipher suites |
| **Protocol enforcement** | Reject plaintext fallback; fail closed if encryption cannot be established |

## Common Data Source Connections

| Data Source | Encrypted Protocol |
|---|---|
| REST APIs | HTTPS (TLS) |
| PostgreSQL / MySQL | TLS-encrypted connections (`sslmode=verify-full`) |
| MongoDB | TLS (`tls=true&tlsAllowInvalidCertificates=false`) |
| Redis | TLS (Redis 6+) |
| Elasticsearch | HTTPS |
| S3 / Object storage | HTTPS |
| gRPC services | gRPC over TLS |

## Implementation Checklist

- [ ] Enable TLS on all connections to external data sources
- [ ] Use TLS 1.2 as minimum; prefer TLS 1.3
- [ ] Validate server certificates (do not skip verification)
- [ ] Use strong cipher suites only
- [ ] Reject plaintext connections; fail closed if TLS cannot be established
- [ ] Verify database connection strings include TLS parameters
- [ ] Audit all data source connections for unencrypted traffic
- [ ] Monitor for certificate expiration on data source endpoints
