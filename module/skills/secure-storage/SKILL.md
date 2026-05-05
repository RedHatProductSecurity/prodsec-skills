---
name: secure-storage
description: Protect RAG system data against unauthorized access and modification. Use when designing, deploying, or reviewing Retrieval-Augmented Generation systems, vector databases, or knowledge base storage.
category: "secure_development"
subcategory: "rag-system"
---

# Secure Storage for RAG Systems

## Security Requirement

Data used by RAG systems (or other plugin systems) MUST be protected against unauthorized access and modification. If RAG data is modified maliciously, the LLM system will provide that malicious information to users as if it were legitimate.

## Risks of Unprotected RAG Data

| Risk | Impact |
|---|---|
| **Data poisoning** | Attacker modifies RAG data to inject false or harmful information |
| **Unauthorized access** | Sensitive knowledge base data exposed to unauthorized users |
| **Integrity compromise** | Tampered RAG data causes the LLM to produce incorrect outputs |
| **Trust exploitation** | Users trust RAG-augmented responses, amplifying the impact of poisoned data |

## Required Controls

| Control | Description |
|---|---|
| **Access control** | Only authorized services and users can read RAG data |
| **Write protection** | Only authorized data pipelines can modify RAG data |
| **Integrity verification** | Detect unauthorized modifications to RAG data |
| **Encryption at rest** | Encrypt RAG data storage (vector databases, document stores) |
| **Audit logging** | Log all access and modifications to RAG data |
| **Input validation** | Validate and sanitize data before ingestion into the RAG store |

## Implementation Checklist

- [ ] Restrict read access to RAG storage to authorized services only
- [ ] Restrict write access to authorized data ingestion pipelines only
- [ ] Enable encryption at rest for vector databases and document stores
- [ ] Implement integrity checks to detect unauthorized modifications
- [ ] Log all access and modifications to RAG data
- [ ] Validate and sanitize data during ingestion (prevent injection of malicious content)
- [ ] Regularly audit RAG data sources and access patterns
- [ ] Implement backup and recovery for RAG data to recover from poisoning attacks
