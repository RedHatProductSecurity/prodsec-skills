---
name: database-security
description: >
  Enforce database security for schema design, access control, encryption,
  and operational hardening. Use when building, reviewing, or auditing
  database schemas, connection handling, credential management, or database
  deployment configuration.
category: "secure_development"
subcategory: "cloud-infrastructure"
---

# Database Security

## Design

### Encryption

- Encrypt all communication with the database (TLS in transit)
- Encrypt the database at rest (filesystem, tablespace, or application-level encryption)

### Auditing

- Enable database auditing to log accesses and configuration changes
- Audit logs should capture authentication events, privilege changes, and data access patterns

### Data Integrity

- Separate test databases from production databases; never share credentials between environments
- Back up data regularly and document the backup and restore process
- Use [polyinstantiation](https://cyberhoot.com/cybrary/polyinstantiation/) to provide multiple views of the same object, preventing unauthorized users from inferring sensitive data
- Apply [database normalization](https://www.geeksforgeeks.org/normal-forms-in-dbms/) to reduce data redundancy and improve integrity
- Implement triggers to enforce referential integrity, prevent invalid operations, and apply complex security rules

## Implementation

### Least-Privilege Access

- Applications MUST connect with the **lowest possible level of privilege**
- Use different credentials for every trust level (regular user, read-only user, guest, administrator)
- Users and applications MUST use separate accounts; never share authentication between them

### Credential Management

- Use secure credentials for all database access
- **Never hardcode connection strings** in application code; store them in a separate configuration file on a trusted system, encrypted
- Rotate credentials regularly

## Configuration

### Default Hardening

- Remove or change **all default administrative passwords**; use strong passphrases or MFA
- Turn off all unnecessary database functionality (stored procedures, utility packages, unnecessary services)
- Remove default vendor content (sample schemas, example databases)
- Install only the minimum set of features and options required (surface area reduction)

### Backend Isolation

- Isolate database servers from other systems and limit host connections
- Disable network (TCP) access when possible; use local socket files or named pipes
- Configure database to bind only on localhost when appropriate
- Restrict network port access to specific hosts with firewall rules
- Place database server in separate DMZ isolated from application server
- Never allow direct connections from thick clients to backend database

### Transport Layer Security

- Use TLS 1.2+ with modern ciphers (AES-GCM, ChaCha20) for client connections
- Verify digital certificate validity in client applications
- Ensure all database traffic is encrypted, not just initial authentication

### Platform-Specific Hardening

- **SQL Server**: Disable xp_cmdshell, CLR execution, SQL Browser service, Mixed Mode Authentication (unless required)
- **MySQL/MariaDB**: Run mysql_secure_installation, disable FILE privilege for users
- **PostgreSQL**: Follow PostgreSQL security documentation guidelines
- **MongoDB**: Implement MongoDB security checklist requirements
- **Redis**: Follow Redis security guide recommendations

## Implementation Checklist

- [ ] All database connections use TLS encryption
- [ ] Database storage is encrypted at rest
- [ ] Auditing is enabled for access and configuration changes
- [ ] Test and production databases are separated with distinct credentials
- [ ] Backups are performed regularly with a documented restore process
- [ ] Applications use the lowest-privilege database account
- [ ] Different credentials are used per trust level (user, admin, readonly)
- [ ] Connection strings are not hardcoded; they are stored encrypted on a trusted system
- [ ] Default administrative passwords are changed
- [ ] Unnecessary features, stored procedures, and sample schemas are removed
- [ ] User accounts and application accounts are separate
- [ ] Database isolated in separate network segment; no direct thick-client connections
- [ ] Platform-specific hardening applied (see above)
- [ ] Transaction logs stored on separate disk from main database files
- [ ] Encrypted backups with tested restore procedures

## References

- [Polyinstantiation](https://cyberhoot.com/cybrary/polyinstantiation/)
- [Solutions to the polyinstantiation problem](https://www.comp.nus.edu.sg/~tankl/cs5322/readings/poly.pdf)
- [Database normalization](https://www.geeksforgeeks.org/normal-forms-in-dbms/)
