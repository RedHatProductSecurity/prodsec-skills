---
name: internal-application-routing
description: Route internal application traffic through the API gateway for AI systems. Use when designing AI system architecture or reviewing network topology for inference engines and model endpoints.
category: "secure_development"
subcategory: "api-gateway"
---

# Internal Application Routing Through API Gateway

## Security Recommendation

Internal applications SHOULD also route their requests through the API gateway rather than connecting directly to guardrails or inference engines. This ensures internal traffic benefits from the same security controls as external traffic.

## Rationale

| Concern | Without Gateway | With Gateway |
|---|---|---|
| **Authentication** | Must be implemented per-service | Centralized enforcement |
| **Rate limiting** | No protection from internal abuse | Consistent rate limits |
| **Request validation** | Each service must validate independently | Centralized validation |
| **Logging/audit** | Fragmented, inconsistent | Unified audit trail |
| **Lateral movement** | Internal compromise can reach models directly | Gateway acts as chokepoint |

## Architecture

```
External clients ──→ API Gateway ──→ Guardrails ──→ Inference Engine
                         ↑
Internal apps ───────────┘  (also routed through gateway)
```

Not recommended:

```
External clients ──→ API Gateway ──→ Guardrails ──→ Inference Engine
                                         ↑               ↑
Internal apps ───────────────────────────┘───────────────┘
                                (bypassing gateway - NOT recommended)
```

## Implementation Checklist

- [ ] Route all internal application traffic through the API gateway
- [ ] Apply the same authentication requirements to internal and external traffic
- [ ] Ensure rate limiting covers internal applications
- [ ] Use network policies to prevent direct access from internal apps to inference engines
- [ ] If direct access is required for specific cases, document the justification and compensating controls
