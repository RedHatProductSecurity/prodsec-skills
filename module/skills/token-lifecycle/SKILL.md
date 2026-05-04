---
name: token-lifecycle
description: Enforce token rotation, revocation, and replay prevention for inference engines. Use when implementing or reviewing refresh token handling, token revocation, or replay protection in inference engine authentication.
category: "secure_development"
subcategory: "inference-engine"
---

# Token Lifecycle Management for Inference Engines

## Security Requirement

Inference engines and their supporting infrastructure MUST implement proper token lifecycle management including refresh token rotation, replay prevention, and instant revocation capabilities.

## Refresh Token Rotation

Require IdP refresh token rotation with one of:

- **DPoP (Demonstrating Proof-of-Possession)**: Sender-constrained tokens that bind the token to the client's key pair, preventing token theft and replay.
- **PAR (Pushed Authorization Requests)**: Authorization request parameters are sent directly to the IdP, reducing exposure of sensitive parameters.

## Revocation

Implement a two-layer revocation strategy:

1. **IdP Revocation Endpoint**: Use the IdP's `/oauth/revoke` endpoint as the primary revocation mechanism.
2. **Local Blacklist**: Maintain a Redis-based or in-memory JWT blacklist keyed by `jti` for instant propagation without IdP round-trips.

## Implementation Checklist

- [ ] Configure IdP to enforce refresh token rotation on every use
- [ ] Implement DPoP or PAR for sender-constrained tokens
- [ ] Integrate with IdP's `/oauth/revoke` endpoint
- [ ] Deploy Redis or equivalent cache for local `jti` blacklist
- [ ] Sync revocation events between IdP and local blacklist
- [ ] Set refresh token max lifetime appropriate to use case
- [ ] Reject reused refresh tokens and revoke the entire token family on detection

## Example: Revocation Check Flow

```
Request arrives with JWT
  → Extract `jti` from token
  → Check local Redis blacklist for `jti`
    → If found: reject request (401)
    → If not found: proceed with standard JWT validation
  → On revocation event:
    → Call IdP /oauth/revoke
    → Add `jti` to local Redis blacklist with TTL = token's remaining `exp`
```
