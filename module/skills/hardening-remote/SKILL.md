---
name: hardening-remote
description: Harden remotely deployed MCP servers with TLS, network segmentation, and server verification. Use when deploying, configuring, or reviewing MCP servers running as remote services.
category: "secure_development"
subcategory: "mcp-server"
---

# Hardening Remote MCP Servers

## Security Requirements

MCP servers deployed as remote services require additional hardening to protect client connections and restrict network access.

## TLS Everywhere

All client connections to the remote MCP server MUST use TLS:

| Requirement | Details |
|---|---|
| **TLS mandatory** | Reject all plaintext (non-TLS) connections |
| **TLS 1.2 minimum** | TLS 1.3 preferred |
| **Valid certificates** | Use certificates from a trusted CA; do not use self-signed certs in production |
| **Strong cipher suites** | Disable weak ciphers and protocols |
| **HSTS** | If HTTP-based, set Strict-Transport-Security header |

## Network Segmentation

| Control | Details |
|---|---|
| **Firewalls** | Restrict inbound traffic to only required ports from known sources |
| **NetworkPolicies** | In Kubernetes, use NetworkPolicies to control pod-level ingress and egress |
| **Private networks** | Place MCP servers in private subnets; use load balancers for public access |
| **Segmentation** | Isolate MCP servers from unrelated workloads |

## Cryptographic Server Verification

Clients MUST be able to verify the MCP server's identity:

- Use valid TLS certificates issued by trusted Certificate Authorities
- Support certificate pinning for high-security environments
- Rotate certificates before expiry

## Implementation Checklist

- [ ] Enforce TLS on all client connections; reject plaintext
- [ ] Use TLS 1.2 minimum, prefer TLS 1.3
- [ ] Use certificates from a trusted CA (not self-signed)
- [ ] Disable weak cipher suites and protocols
- [ ] Implement firewall rules to restrict inbound traffic to required ports
- [ ] Use Kubernetes NetworkPolicies for pod-level network control
- [ ] Place MCP servers in private network segments
- [ ] Rotate TLS certificates before expiry
- [ ] Monitor for certificate expiration and configuration drift
