---
name: apache-camel-security
description: >
  Secure Apache Camel route deployments across endpoint, payload, route, and
  configuration layers. Use when building, reviewing, or auditing Camel
  routes, integration pipelines, or Camel-based microservices.
category: "secure_development"
subcategory: "secure-config"
---

# Apache Camel Security

Apache Camel is **unsecured by default**. Before deploying to production, security must be explicitly enabled at one or more layers.

## Security Layers

Camel provides four layers of security. Use only what is necessary -- avoid redundant encryption when transport security already covers the payload.

### 1. Endpoint Security

Secures the transport between Camel and external systems.

- Provides peer authentication (and sometimes authorization) at the transport level
- Configuration varies by transport type:
  - **JMS / ActiveMQ**: SSL/TLS and JAAS for client-to-broker and broker-to-broker
  - **Jetty**: HTTP Basic Authentication and SSL/TLS
- Use the [JSSE Utility](https://camel.apache.org/manual/latest/camel-configuration-utilities.html) (Camel 2.8+) to configure SSL/TLS across components

### 2. Payload Security

Encrypts and decrypts message payloads using `marshal()` and `unmarshal()` operations.

- Use `camel-crypto` for symmetric encryption with any JCE algorithm
- Use [XMLSecurity data format](https://access.redhat.com/documentation/en-us/red_hat_jboss_fuse/6.3/html/security_guide/arch-architecture-camel#Arch-Architecture-Camel-XMLSecurity) for XML payloads
- Payload encryption alone does **not** provide authentication or authorization
- Skip payload encryption when transport-level TLS is already active (avoid double encryption)

### 3. Route Security

Provides authentication and authorization within Camel route processing.

- Centralizes auth logic rather than implementing it per transport
- Handles auth errors with Camel's error handling framework
- Supported policy providers:
  - [Apache Shiro](https://camel.apache.org/components/4.0.x/others/shiro.html)
  - [Spring Security](https://camel.apache.org/components/4.0.x/others/spring-security.html)

### 4. Configuration Security

Protects sensitive values in configuration files (passwords, API keys).

- Use the [Jasypt](https://camel.apache.org/components/latest/others/jasypt.html) component to encrypt property values
- Camel automatically decrypts at runtime using the configured Jasypt password
- Never store secrets in plaintext in property files committed to version control

## Implementation Checklist

- [ ] At least one security layer is enabled before production deployment
- [ ] Endpoint TLS is configured for all external-facing transports
- [ ] JSSE Utility is used for SSL/TLS configuration
- [ ] Payload encryption is used only when transport encryption is insufficient
- [ ] Route security (Shiro or Spring Security) provides auth for route processing
- [ ] Sensitive configuration values are encrypted with Jasypt
- [ ] No plaintext secrets in property files or source control
- [ ] Redundant encryption layers are avoided (no double encryption)

## References

- [Apache Camel Security](https://camel.apache.org/manual/latest/security.html)
- [Red Hat JBoss Fuse Security Guide](https://access.redhat.com/documentation/en-us/red_hat_jboss_fuse/6.3/html/security_guide/arch-architecture-camel)
- [Camel JSSE Utility](https://camel.apache.org/manual/latest/camel-configuration-utilities.html)
