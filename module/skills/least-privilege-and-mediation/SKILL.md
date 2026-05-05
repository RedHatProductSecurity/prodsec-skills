---
name: least-privilege-and-mediation
description: >
  Enforce least privilege and complete mediation in access control design.
  Use when reviewing authorization models, RBAC configurations, API access
  controls, or evaluating whether every request is properly authorized.
category: "secure_development"
subcategory: "security-principles"
---

# Least Privilege and Complete Mediation

These two principles work together: **least privilege** limits what an entity can do, and **complete mediation** ensures that every access attempt is checked against those limits.

## Least Privilege

**Principle:** Individuals and entities should only be given sufficient access and permissions to complete their assigned duties, no more.

### Key Aspects

- **Least privilege by default:** Start with zero access and grant permissions incrementally as justified
- **Minimal access permissions:** Limit scope to reduce impact of fraud, compromise, or user error
- **Reduced attack surface:** Fewer permissions mean fewer opportunities for exploitation
- **User accountability:** When permissions are specific and narrow, audit trails are meaningful and anomalous activity is detectable

### Application

| Context | Least-Privilege Practice |
|---|---|
| **Database** | Application accounts use the lowest privilege level; separate accounts per trust level |
| **Kubernetes** | No wildcards in RBAC; no `cluster-admin`; explicit verbs and resources |
| **Cloud IAM** | Individual accounts; IAM groups; no root credentials for daily operations |
| **OS/containers** | Non-root users; `readOnlyRootFilesystem`; `no-new-privileges` |
| **API access** | Scoped tokens; short-lived credentials; per-operation authorization |

## Complete Mediation

**Principle:** Every request by a subject to access an object must undergo a valid and effective authorization process that the subject cannot bypass or disable.

This is a pillar of **Zero Trust Architecture**: never assume a request is authorized because it came from inside the network or from a previously authenticated session.

### Key Aspects

- **Access verification:** Validate every access attempt, including internal service-to-service calls
- **Fine-grained access control:** Define precisely what actions each user or process is authorized to perform
- **Enhanced accountability:** Comprehensive access logs enable forensic analysis and incident response
- **Systematic testing:** Maintain an access-control test matrix that maps user roles to resources and validates that controls are correctly enforced

### Application

- Enforce authorization on **every request**, including AJAX calls, background jobs, and internal APIs
- Do not rely on referrer headers, client-side state, or session age as authorization factors
- Re-validate privileges on long-lived sessions
- Implement a **single site-wide authorization component** to ensure consistency
- **Fail secure:** If the authorization service is unreachable, deny access

## Implementation Checklist

- [ ] All accounts and service identities start with zero access (default deny)
- [ ] Permissions are granted per duty, not per convenience
- [ ] Every request passes through the authorization layer (no bypass paths)
- [ ] Authorization is enforced server-side, not client-side
- [ ] A single centralized authorization component handles all access decisions
- [ ] Authorization fails closed (deny on error or unreachable service)
- [ ] Privileges are re-validated on long-lived sessions
- [ ] An access-control test matrix exists and is executed regularly
- [ ] Audit logs capture all access attempts (success and failure)

## References

- [Saltzer & Schroeder: The Protection of Information in Computer Systems (1975)](https://web.mit.edu/saltzer/www/publications/protection/Basic.html)
- [NIST SP 800-53 AC-6: Least Privilege](https://csrc.nist.gov/projects/cprt/catalog#/cprt/framework/version/SP_800_53_5_1_1/home?element=AC-6)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [NIST Zero Trust Architecture (SP 800-207)](https://csrc.nist.gov/pubs/sp/800/207/final)
