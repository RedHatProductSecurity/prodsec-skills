---
name: simplicity-and-isolation
description: >
  Apply economy of mechanism and least common mechanism to reduce attack
  surface through simplicity and component isolation. Use when reviewing
  system architecture for unnecessary complexity, shared resources, or
  single points of failure.
category: "secure_development"
subcategory: "security-principles"
---

# Simplicity and Isolation

This skill combines two complementary design principles: **economy of mechanism** (keep it simple) and **least common mechanism** (minimize sharing between components).

## Economy of Mechanism

**Principle:** Designs should be simple, comprehensive, and should implement protection mechanisms so that unintended access paths do not exist.

The more complex something is, the harder it is to understand. If you cannot understand a system, you cannot properly secure it.

### Key Aspects

- **Simplicity:** A simpler design is easier to understand, analyze, audit, and maintain. Complexity introduces opportunities for vulnerabilities.
- **Minimize moving parts:** Fewer components mean a reduced attack surface and fewer unexpected interactions
- **Ease of understanding:** Security mechanisms must be understandable to be properly implemented and configured
- **Avoid unnecessary features:** Every feature increases the potential for exploitation. Include only what is essential.
- **Maintainability:** A clean, simple design allows seamless security updates without introducing regressions

### Application

- Remove unnecessary services, APIs, endpoints, and configuration options
- Prefer well-known, well-tested libraries over custom implementations
- Avoid "just in case" features that expand the attack surface without clear user need
- Keep security-critical code paths short and auditable

## Least Common Mechanism

**Principle:** Mechanisms used to access resources should not be shared, or sharing must be minimized. Every shared mechanism is a potential information path.

### Key Aspects

- **Minimize shared resources:** Reduce use of shared data structures, communication channels, and components to limit side-channel and data-leakage risks
- **Component isolation:** Isolate components so that compromise or failure of one does not propagate to others
- **Component independence:** Independent components are more robust; failure of one is less likely to affect others
- **Avoid single points of failure:** SPOFs jeopardize availability; distribute critical functionality
- **Cache isolation:** Exercise caution when caching user-specific data. Ensure strict data isolation between users to prevent cross-user data leakage.

### Application

- Use separate processes, containers, or namespaces for components with different trust levels
- Avoid shared databases between services that handle different sensitivity levels
- Do not share authentication tokens or sessions between services
- Isolate caches per user or per tenant; never serve one user's cached data to another

## Architecture Review Questions

1. Can this system be simplified without losing required functionality?
2. Are there shared resources (databases, caches, message queues) between components with different trust levels?
3. If one component is compromised, which other components are affected through shared mechanisms?
4. Are there single points of failure that would take down the entire system?
5. Could a side-channel through a shared resource leak sensitive data?

## Implementation Checklist

- [ ] The design has been reviewed for unnecessary complexity and features
- [ ] Security-critical code paths are short, simple, and auditable
- [ ] Components with different trust levels do not share databases or caches
- [ ] User-specific cached data is isolated per user/tenant
- [ ] No single point of failure exists for critical security functions
- [ ] Components are independently deployable and can fail without cascading
- [ ] Shared communication channels are minimized and access-controlled
