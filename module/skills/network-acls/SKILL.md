---
name: network-acls
description: Enforce network ACLs for external data source access in AI systems. Use when designing, configuring, or reviewing network security for connections between AI components and external databases or data services.
category: "secure_development"
subcategory: "external-data-source"
---

# Network ACLs for External Data Sources

## Security Recommendation

If access to external data sources will come from specific known sources, network ACLs SHOULD be implemented to allow access only from those known sources. This provides a network-level defense-in-depth layer on top of authentication and authorization.

## Defense-in-Depth Value

Network ACLs complement authentication and authorization by restricting **which network locations** can even attempt to connect:

```
Network ACLs (can this source IP/network connect at all?)
  → Authentication (is this principal who they claim to be?)
    → Authorization (does this principal have permission?)
      → Data access (execute the query/operation)
```

Even if credentials are compromised, network ACLs prevent their use from unauthorized network locations.

## ACL Strategies

| Strategy | Description |
|---|---|
| **IP allowlist** | Allow connections only from specific IP addresses or CIDR ranges |
| **Security groups** | Cloud-native network rules scoped to specific resources |
| **Network policies** | Kubernetes NetworkPolicy restricting pod-to-pod and egress traffic |
| **Service mesh** | Istio/Envoy authorization policies based on workload identity |
| **Firewall rules** | Traditional firewall rules at the network perimeter |

## Network Encryption and Exposure

- It should be possible to encrypt **all** network communications, both internal and external
- For cloud services, all network communications (internal and external) **must** be encrypted
- Endpoints that do not need to be exposed to the Internet must not be public-facing
- All TCP and UDP ports that are not required must be **closed by default**

## Implementation Checklist

- [ ] Identify all AI system components that need to access each external data source
- [ ] Document the source IP ranges or network identities for each component
- [ ] Configure network ACLs on the data source to allow only those known sources
- [ ] Default to deny-all, then explicitly allow required connections
- [ ] Use Kubernetes NetworkPolicy if running in Kubernetes
- [ ] Use cloud security groups if running in cloud infrastructure
- [ ] Regularly audit network ACLs and remove stale entries
- [ ] Monitor for connection attempts from unauthorized sources
- [ ] All network communications are encrypted (TLS) or encryption is configurable
- [ ] Non-Internet-facing endpoints are not publicly exposed
- [ ] Unused TCP/UDP ports are closed by default
