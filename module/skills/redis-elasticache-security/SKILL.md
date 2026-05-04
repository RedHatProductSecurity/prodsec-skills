---
name: redis-elasticache-security
description: >
  Secure Redis and Amazon ElastiCache for Redis deployments with
  authentication, encryption, and network isolation. Use when building,
  reviewing, or auditing Redis cache configuration, ElastiCache clusters,
  or application-to-cache connectivity.
category: "secure_development"
subcategory: "external-data-source"
---

# Redis and ElastiCache Security

Amazon ElastiCache for Redis is a managed caching service. It does not have unique security guidelines; instead, apply authentication, networking, and general AWS security controls.

## Authentication

- Enable **Redis AUTH** to require a password for client connections
- For ElastiCache, use **IAM authentication** where supported to avoid managing static passwords
- Rotate AUTH tokens regularly
- Never use default or empty passwords

## Encryption

### In Transit

- Enable **TLS encryption** for all client-to-cache and replication connections
- For ElastiCache, enable in-transit encryption in the replication group or cluster configuration
- Applications must use TLS-capable Redis client libraries

### At Rest

- For ElastiCache, enable at-rest encryption using **AWS KMS**
- Encryption at rest protects backups and snapshots

## Network Isolation

- Deploy Redis/ElastiCache in a **private subnet** within a VPC
- Configure **security groups** to allow connections only from authorized application instances
- Do not expose Redis ports to the public Internet
- Use **network ACLs** as an additional layer of defense

## Access Control

- Use Redis ACLs (Redis 6+) to create per-application users with minimum required commands and key patterns
- Do not use the default user for application access
- Disable dangerous commands (`FLUSHALL`, `FLUSHDB`, `CONFIG`, `DEBUG`) in production

## Operational Security

- Keep Redis/ElastiCache versions patched and current
- Monitor connection patterns and command usage for anomalies
- Enable AWS CloudTrail for ElastiCache API activity logging
- Configure backup retention and test restore procedures

## Implementation Checklist

- [ ] Redis AUTH or IAM authentication is enabled
- [ ] TLS is enabled for all client and replication connections
- [ ] At-rest encryption is enabled (KMS for ElastiCache)
- [ ] Redis is deployed in a private VPC subnet
- [ ] Security groups restrict access to authorized instances only
- [ ] Redis ACLs are configured with per-application least-privilege users
- [ ] Dangerous commands are disabled in production
- [ ] Versions are patched and current
- [ ] CloudTrail logs ElastiCache API activity

## References

- [AWS ElastiCache Security](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/encryption.html)
- [Redis Security](https://redis.io/docs/management/security/)
