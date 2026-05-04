---
name: authentication-enforcement
description: Enforce authentication and authorization at the API gateway for AI systems. Use when designing, building, or reviewing API gateways that front inference engines, LLM APIs, or AI model endpoints.
category: "secure_development"
subcategory: "api-gateway"
---

# Authentication Enforcement at the API Gateway

## Security Requirement

AI model APIs MUST require that all principals (humans and applications) are identified, authenticated, and authorized before requests reach the models. The API gateway is the primary enforcement point for this control.

AI software MUST implement a robust standard authentication mechanism or require integration with an identity provider **by default**. Reducing this security posture should only be an option the user explicitly chooses, never the default.

## What Is Not Acceptable as Default

- No authentication at all (even for internal-only APIs)
- A single shared API key for all users
- An empty API key
- API key-only authentication without IdP integration

These approaches may seem to "facilitate use" but are not acceptable for cloud services and should not be the default for products.

## Required Controls

| Control | Details |
|---|---|
| **Authentication** | Standard protocol (OAuth 2.1/OIDC) via IdP integration |
| **Authorization** | Verify the authenticated principal has permission for the requested operation |
| **Identity** | Every request must be attributable to a specific principal |

## Architectures Without an API Gateway

If the AI software architecture or platform does not include an API gateway, these security controls MUST be implemented by other components:

- Check if the inference engine has standard, well-known authentication mechanisms
- Verify the inference engine can identify and authenticate principals securely
- Ensure rate limiting and input validation are handled at the inference engine level
- Document the compensating controls and their limitations

## Implementation Checklist

- [ ] Deploy an API gateway in front of all AI model endpoints
- [ ] Configure the API gateway to require authentication by default
- [ ] Integrate with an OIDC Identity Provider for authentication
- [ ] Implement authorization checks based on principal identity
- [ ] Ensure every request is logged with the authenticated principal's identity
- [ ] If no API gateway: verify inference engine implements equivalent controls
- [ ] Verify that the default configuration requires authentication (not opt-in)
