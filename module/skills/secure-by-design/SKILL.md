---
name: secure-by-design
description: >
  Apply Secure by Design, by Default, and in Deployment (SD3) principles.
  Use when reviewing default configurations, setup processes, update
  mechanisms, or evaluating whether a system fails open or closed.
category: "secure_development"
subcategory: "security-principles"
---

# Secure by Design, by Default, in Deployment (SD3)

**Principle:** The default settings of a system or application are configured with strong security measures in place. Systems should be configured in a least-privilege model so that no unnecessary services, daemons, or accounts are enabled.

## Secure Default Configurations

- Ship products with secure defaults that protect users without requiring manual hardening
- Generate unique keys and secrets during first run or installation, not at build time
- Encourage users to review and customize settings, but ensure the uncustomized state is safe
- Minimizes risk from users or administrators who overlook or delay security configuration

## Fail Secure

- Design services to **fail closed**: when they fail, they deny access rather than granting it
- A security service that cannot be reached must result in a denied request, not an open door
- Apply this to authentication, authorization, input validation, and configuration loading

## Secure Baselines

- Create server and application security baselines as reference configurations
- Deploy new systems from these baselines to ensure consistency
- Systems adhering to baselines are less vulnerable and require less ongoing maintenance

## Encryption and Authentication by Default

- Enable encryption (TLS) and authentication by default, not as opt-in features
- Use **HTTPS** as the default communication protocol
- Protect data in transit and at rest as a baseline, not an upgrade

## No Hardcoded Credentials

- Never use hard-coded secrets, default passwords, or static account credentials in code
- Generate unique credentials at deployment time
- Use secrets management systems (Vault, AWS Secrets Manager, etc.)

## Default Deny Policies

- Only explicitly allowed actions are permitted
- No unnecessary services, daemons, or network ports are enabled
- Default network policies deny all traffic; allow rules are added explicitly

## Code Integrity and Updates

- Use **digital signatures** and **cryptographic hashes** to verify the integrity and authenticity of software updates
- Implement automated update mechanisms to reduce the window of vulnerability
- Test patches thoroughly before deployment
- Secure the update infrastructure itself with access controls and monitoring

## Implementation Checklist

- [ ] Default configuration is secure without manual hardening
- [ ] Unique secrets are generated at first run or installation (not hardcoded)
- [ ] Service failures result in denied access (fail closed), not open access
- [ ] TLS and authentication are enabled by default
- [ ] HTTPS is the default protocol for all communication
- [ ] No hardcoded credentials exist in the codebase
- [ ] Default network policies deny all traffic; allow rules are explicit
- [ ] Unnecessary services, ports, and accounts are disabled by default
- [ ] Software updates are signed and verified before installation
- [ ] Update infrastructure is secured with access controls and monitoring
- [ ] Security baselines exist and new deployments are built from them
