---
name: service-to-service-mtls
description: Enforce SPIFFE/SPIRE plus mTLS for service-to-service authentication. Use when designing, building, or reviewing authentication between services, workloads, or machines in AI systems.
category: "secure_development"
subcategory: "spiffe-spire"
---

# SPIFFE/SPIRE + mTLS for Service-to-Service Authentication

## Security Requirement

For service-to-service communication, the recommendation is to use SPIFFE/SPIRE+mTLS. This applies to all service-to-service scenarios including agent-to-agent and agent-to-MCP-server communications.

## What SPIFFE/SPIRE Provides

- **Workload identity**: SPIFFE (Secure Production Identity Framework for Everyone) provides a standard for identifying workloads via SPIFFE IDs
- **Credential issuance**: SPIRE (SPIFFE Runtime Environment) automatically issues and rotates X.509 certificates (SVIDs) for workloads
- **No credential exchange over network**: SPIRE handles attestation locally, eliminating the need to transmit credentials
- **Mutual authentication**: Both parties in a connection verify each other's identity via mTLS

## SPIFFE ID Format

```
spiffe://<trust-domain>/<workload-path>
```

Examples:
- `spiffe://example.com/inference-engine/prod`
- `spiffe://example.com/mcp-server/tools-api`
- `spiffe://example.com/agent/data-analyst`

## SPIFFE ID Extraction

At the application level, extract the SPIFFE ID from the TLS certificate to authenticate and authorize the service:

```python
from cryptography import x509

def extract_spiffe_id(peer_certificate):
    cert = x509.load_der_x509_certificate(peer_certificate)
    for ext in cert.extensions:
        if ext.oid == x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME:
            san = ext.value
            for uri in san.get_values_for_type(x509.UniformResourceIdentifier):
                if uri.startswith("spiffe://"):
                    return uri
    return None
```

## Service Mesh Integration

Service meshes (e.g., Istio/Envoy) may extract the SPIFFE ID automatically and expose it as:
- `x-forwarded-client-cert` headers
- RBAC principals in authorization policies

This can simplify application-level integration.

## Implementation Checklist

- [ ] Deploy SPIRE server in the infrastructure
- [ ] Deploy SPIRE agents on each node/host running services
- [ ] Register each service as a workload entry with a unique SPIFFE ID
- [ ] Configure services to obtain SVIDs from the local SPIRE agent
- [ ] Implement mTLS for all service-to-service connections
- [ ] Extract SPIFFE ID from peer certificates for authorization decisions
- [ ] Define authorization policies based on SPIFFE IDs
- [ ] Monitor SVID rotation and certificate health
- [ ] If using a service mesh, configure it to extract and propagate SPIFFE IDs
