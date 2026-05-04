---
name: rate-limiting
description: Enforce rate limiting at the API gateway to protect AI models from extraction attacks. Use when designing, building, or reviewing API gateways that protect inference engines or LLM endpoints.
category: "secure_development"
subcategory: "api-gateway"
---

# Rate Limiting at the API Gateway

## Security Requirement

API gateways protecting AI models SHOULD implement rate limiting. This is a critical defense against attacks that require sending large volumes of requests to the models.

## Attacks Mitigated by Rate Limiting

| Attack | Description |
|---|---|
| **Model data extraction** | Attempting to extract sensitive information the model learned during training |
| **Training data extraction** | Reconstructing training data from model responses |
| **Token extraction** | Stealing API tokens or credentials through repeated probing |
| **Weight extraction** | Reverse-engineering model weights through systematic queries |
| **Prompt injection probing** | Brute-forcing prompt injection payloads |

These attacks typically require sending thousands to millions of requests. Rate limiting makes them impractical or too slow to be worthwhile.

## Rate Limiting Strategies

| Strategy | Use Case |
|---|---|
| **Per-user/principal** | Limit requests per authenticated user over a time window |
| **Per-IP** | Limit unauthenticated or pre-auth requests by source IP |
| **Per-endpoint** | Different limits for different model endpoints based on sensitivity |
| **Adaptive/dynamic** | Adjust limits based on detected anomalous patterns |
| **Token-based** | Limit based on input/output token consumption, not just request count |

## Implementation Checklist

- [ ] Define rate limits per principal, IP, and endpoint
- [ ] Set limits low enough to impede extraction attacks but high enough for legitimate use
- [ ] Return standard `429 Too Many Requests` with `Retry-After` header
- [ ] Log rate limit violations with principal identity for incident response
- [ ] Consider adaptive rate limiting that tightens under detected attack patterns
- [ ] Apply token-based rate limits for LLM endpoints (input + output tokens)
- [ ] Monitor rate limit metrics for tuning and anomaly detection
