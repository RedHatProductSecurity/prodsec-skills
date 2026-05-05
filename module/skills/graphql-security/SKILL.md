---
name: graphql-security
description: >
  Secure GraphQL API deployments against introspection leaks, deep query
  abuse, and authorization bypass. Use when building, reviewing, or auditing
  GraphQL schemas, resolvers, or gateway configurations.
category: "secure_development"
subcategory: "web-security"
---

# GraphQL Security

GraphQL APIs introduce a threat surface distinct from REST. The flexible query language enables clients to request arbitrary data shapes, which can be abused for data exfiltration, denial of service, and authorization bypass if not constrained.

## Authorization

Authorization logic MUST live in the business-logic layer, not in individual resolvers.

Scattering authorization checks across resolvers creates gaps as the schema grows. Any resolver that forgets a check becomes an exploitable authorization flaw.

- Implement a single authorization layer beneath the GraphQL API
- Resolvers should delegate to this layer for every data access decision
- Apply the same authorization rules regardless of which query or mutation is used to reach the data
- See [GraphQL.org authorization guidance](https://graphql.org/learn/authorization/)

## Disable Introspection

GraphQL introspection exposes your full schema, including types, queries, mutations, and subscriptions. This is valuable for attackers mapping your attack surface.

- Disable introspection in staging and production environments
- Use the [graphql-disable-introspection](https://github.com/helfer/graphql-disable-introspection) plugin or equivalent validation rule
- Keep introspection enabled only in local development

## Depth Limiting

Deeply nested queries can trigger expensive recursive resolution, leading to resource exhaustion.

- Set a maximum query depth (typically 7-10 levels for most applications)
- Reject queries exceeding the depth limit before execution
- Use [graphql-depth-limit](https://github.com/stems/graphql-depth-limit) or equivalent

## Query Cost Analysis

Even within depth limits, queries can request expensive combinations of fields and connections.

- Assign a cost to each field and connection based on computational expense
- Set a maximum cost budget per query
- Reject queries exceeding the budget before execution
- Use [graphql-cost-analysis](https://github.com/pa-bru/graphql-cost-analysis) or equivalent

## Rate Limiting

GraphQL's single-endpoint design concentrates all operations on one URL, making rate limiting essential.

- Apply rate limits per client and per operation
- Use tighter limits on sensitive mutations (login, password reset, account creation)
- Use wider limits on read queries
- Use [graphql-rate-limit](https://github.com/teamplanes/graphql-rate-limit) or equivalent

## Implementation Checklist

- [ ] Authorization is enforced in the business-logic layer, not in resolvers
- [ ] Introspection is disabled in staging and production
- [ ] Query depth limit is configured and enforced
- [ ] Query cost analysis is enabled with per-field costs and a maximum budget
- [ ] Rate limiting is applied, with tighter limits on sensitive mutations
- [ ] Error messages do not leak schema details or internal structure
- [ ] Input validation is applied to all mutation arguments

## References

- [GraphQL.org best practices](https://graphql.org/learn/best-practices/)
- [OWASP GraphQL Security](https://owasp.org/www-chapter-vancouver/assets/presentations/2020-06_GraphQL_Security.pdf)
