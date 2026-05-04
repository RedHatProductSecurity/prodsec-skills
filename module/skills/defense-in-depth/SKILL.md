---
name: defense-in-depth
description: >
  Apply defense-in-depth by layering multiple independent security controls.
  Use when reviewing system architecture, evaluating whether a single control
  is the only barrier, or assessing blast radius of a component compromise.
category: "secure_development"
subcategory: "security-principles"
---

# Defense in Depth

**Principle:** Security should be viewed holistically. Wherever possible, multiple levels of security controls should be used. No single control provides perfect security, but layering different controls makes attacks extremely complex and unlikely to succeed.

## Key Aspects

### Layered Security Controls

Implement multiple independent layers, each providing a different line of defense:

| Layer | Examples |
|---|---|
| **Network** | Firewalls, network segmentation, VPN, private subnets |
| **Host** | OS hardening, host-based IDS, patch management |
| **Application** | Input validation, authentication, authorization, output encoding |
| **Data** | Encryption at rest and in transit, access controls, backup |
| **Monitoring** | Intrusion detection, log aggregation, alerting, SIEM |

### Redundancy and Diversity

- If one layer is compromised, other layers still provide protection
- Use controls from different vendors or implementations to avoid a single vulnerability defeating all layers
- Avoid relying on a single security mechanism for any critical protection

### Compartmentalization

- Isolate system components to limit lateral movement after a compromise
- Use network segmentation, separate namespaces, and distinct trust zones
- Apply the blast radius test: "If this component is compromised, what else is affected?"

### Continuous Monitoring and Updating

- Continuously update and adapt security measures to address emerging threats
- Monitor all layers for anomalies, not just the perimeter
- Regularly test controls through penetration testing and red team exercises

## Architecture Review Questions

When reviewing a system's security architecture, ask:

1. What happens if the firewall/WAF is bypassed? Is there application-level input validation?
2. What happens if authentication is compromised? Are there authorization checks on every resource?
3. What happens if a service is breached? Can the attacker move laterally to other services?
4. What happens if a database is accessed? Is the data encrypted at rest?
5. What happens if an attacker operates undetected? Are there monitoring and alerting mechanisms?

If any answer is "nothing else protects us," that is a defense-in-depth gap.

## Implementation Checklist

- [ ] No critical asset is protected by a single security control alone
- [ ] Network segmentation separates components into trust zones
- [ ] Application-level controls (input validation, authz) exist independently of network controls
- [ ] Data is encrypted at rest and in transit
- [ ] Monitoring and alerting cover all layers (network, host, application)
- [ ] Blast radius of a single component compromise is limited by isolation
- [ ] Controls are regularly tested and updated

## References

- [NIST Glossary: Defense in Depth](https://csrc.nist.gov/glossary/term/defense_in_depth)
- [CISA: Defense in Depth Recommended Practice](https://www.cisa.gov/sites/default/files/recommended_practices/NCCIC_ICS-CERT_Defense_in_Depth_2016_S508C.pdf)
- [NIST SP 800-53 Rev. 5: Security and Privacy Controls](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf)
- [Saltzer & Schroeder: The Protection of Information in Computer Systems (1975)](https://web.mit.edu/saltzer/www/publications/protection/Basic.html)
