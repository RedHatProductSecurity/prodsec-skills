---
name: authorization
description: Enforce authorization checks for external data source access in AI systems. Use when designing, configuring, or reviewing access controls between AI components and external databases or data services.
category: "secure_development"
subcategory: "external-data-source"
---

# Authorization for External Data Sources

## Security Requirement

It MUST be verified that the principal accessing an external data source has permissions to access or modify the data. Authentication alone (knowing who the principal is) is not sufficient; authorization (what they can do) must also be enforced.

## Authorization Scope

| Operation | Authorization Check |
|---|---|
| **Read data** | Does the principal have read permission for this specific data? |
| **Write data** | Does the principal have write permission? |
| **Modify schema** | Does the principal have administrative permissions? |
| **Delete data** | Does the principal have delete permission? |
| **Bulk export** | Does the principal have permission for bulk data access? |

## Principle of Least Privilege

Each AI system component should have only the minimum data access permissions needed:

| Component | Typical Permissions |
|---|---|
| RAG ingestion pipeline | Read-only on source data |
| Inference engine | No direct data source access (goes through RAG) |
| Agent with data tools | Read-only unless write is explicitly required |
| Admin/maintenance jobs | Broader access, time-limited and audited |

## Implementation Checklist

- [ ] Define the minimum data access permissions needed by each AI component
- [ ] Configure data source access controls to enforce least privilege
- [ ] Separate read and write permissions (do not grant write when only read is needed)
- [ ] Verify authorization on every data access request (not just at connection time)
- [ ] Regularly audit data source permissions and remove unnecessary access
- [ ] Use role-based or attribute-based access control at the data source level
