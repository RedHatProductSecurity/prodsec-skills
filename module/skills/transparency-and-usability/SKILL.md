---
name: transparency-and-usability
description: >
  Apply open design, psychological acceptability, and compromise recording
  to build transparent, usable, and observable security. Use when reviewing
  whether security relies on obscurity, whether controls are usable, or
  whether breach detection and response capabilities exist.
category: "secure_development"
subcategory: "security-principles"
---

# Transparency, Usability, and Compromise Recording

This skill combines three design principles that ensure security is transparent, usable, and observable.

## Open Design

**Principle:** Security mechanisms should not depend on secrecy of design. Protection relies on securely managed keys and credentials, not on hidden algorithms or architectures.

### Key Aspects

- **No security through obscurity:** Do not rely on attackers not knowing how the system works. Assume the design is known.
- **Transparency:** Open sharing of source code, development processes, and security mechanisms promotes understanding and enables external review
- **Scrutiny and engagement:** Broader community review improves quality and catches vulnerabilities that internal teams miss
- **Comprehensive documentation:** Provide architecture diagrams, component descriptions, interface specifications, and security mechanism documentation. Undocumented systems cannot be properly reviewed.

### Application

- Document system architecture, data flows, trust boundaries, and security mechanisms
- Ensure that if the design were fully disclosed, the system would still be secure (only keys/secrets protect it)
- Participate in security reviews and welcome external scrutiny

## Psychological Acceptability

**Principle:** Security controls should align with user expectations so that users routinely and automatically apply them correctly.

### Key Aspects

- **Ease of use:** Controls that are difficult to use will be bypassed or disabled. Security mechanisms must be intuitive.
- **Balanced cost:** The cost (time, friction, complexity) of security controls should not exceed the value of the asset being protected
- **Appropriate notification:** When security controls activate, provide enough information for users to understand why, without disclosing system internals

### Application

- Design authentication flows that match user expectations (SSO, MFA with clear prompts)
- Avoid security configurations that require expert knowledge to get right; provide safe defaults
- Make the secure path the easy path (pit of success)
- Test security UX with real users; measure bypass and error rates

## Compromise Recording

**Principle:** Reliable mechanisms must document and track security incidents, because no system is entirely immune to breaches.

### Key Aspects

- **Detection and notification:** Implement mechanisms to promptly detect and notify stakeholders of potential compromises
- **Forensic analysis:** Enable forensic investigation to understand the nature, extent, and impact of breaches
- **Incident response:** Facilitate effective response strategies to contain and mitigate breach impact
- **Accountability and transparency:** Establish clear processes for handling incidents; keep stakeholders informed
- **Continuous improvement:** Use insights from incidents to strengthen security controls

### Application

- Log all security-relevant events: authentication attempts, authorization failures, configuration changes, data access patterns
- Ensure logs are tamper-resistant and stored in a central, protected facility
- Implement automated alerting for anomalous patterns
- Maintain and test incident response procedures regularly
- Conduct post-incident reviews and update controls based on findings

## Implementation Checklist

- [ ] System security does not depend on design secrecy (only keys/secrets)
- [ ] Architecture, data flows, and trust boundaries are documented
- [ ] Security mechanisms are documented and reviewable
- [ ] Security controls are usable and tested with real users
- [ ] The secure path is the default and easiest path
- [ ] Security notifications inform without over-disclosing system internals
- [ ] All security events are logged centrally (auth, authz, config changes)
- [ ] Logs are protected from tampering and unauthorized access
- [ ] Automated alerting is configured for anomalous patterns
- [ ] Incident response procedures exist and are tested regularly
- [ ] Post-incident reviews feed back into control improvements
