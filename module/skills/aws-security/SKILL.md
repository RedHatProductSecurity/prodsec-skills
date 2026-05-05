---
name: aws-security
description: >
  Enforce AWS security baselines for IAM, networking, logging, and managed
  services like RDS. Use when building, reviewing, or auditing AWS
  infrastructure, IAM policies, VPC configuration, or RDS deployments.
category: "secure_development"
subcategory: "cloud-infrastructure"
---

# AWS Security

## General AWS Requirements

These apply to all AWS services (e.g., ElastiCache, RDS, MSK).

### Logging and Auditing

- Enable **AWS CloudTrail** to log all API and user activity
- Ensure CloudTrail logs are stored in a protected S3 bucket with versioning and encryption

### Network Security

- Deploy services in a **VPC** with properly configured security groups and network ACLs
- Restrict security group rules to the minimum required ports and source IPs
- Use private subnets for services that do not need Internet-facing access

### IAM

- Create **individual IAM accounts** for each person managing AWS resources; never use root credentials
- Grant each user the **minimum set of permissions** required for their duties
- Use **IAM groups** to manage permissions for multiple users
- **Rotate IAM credentials** regularly
- Never put sensitive identifying information (customer account numbers, PII) in free-form IAM fields such as Name

## Amazon RDS Security

### Encryption

- Encrypt data in transit using **SSL/TLS** connections
- Encrypt database storage and backups at rest using **AWS KMS**

### Credential Management

- Do not use the master credentials created during instance setup; they use the public schema without fine-grained permissions
- Create application-specific database users with least-privilege grants
- Configure **AWS Secrets Manager** to automatically rotate database credentials

### Patching and Access

- Use RDS versions that do not have known security vulnerabilities; apply patches promptly
- Restrict access using **security groups** that allow only specific IP addresses or EC2 instances
- Create individual IAM users for each person managing RDS; never use root

## Amazon ElastiCache / Redis

For detailed Redis and ElastiCache security guidance (authentication, encryption, ACLs, network isolation), see the dedicated skill: [`external-data-source/redis-elasticache-security.md`](../external-data-source/redis-elasticache-security.md). Apply the General AWS Requirements above (IAM, VPC, CloudTrail) to all ElastiCache deployments.

## Implementation Checklist

- [ ] CloudTrail is enabled and logging to a protected S3 bucket
- [ ] All services are deployed in a VPC with security groups and NACLs
- [ ] Individual IAM users are created; root credentials are not used
- [ ] IAM permissions follow least privilege; IAM groups are used
- [ ] IAM credentials are rotated on a schedule
- [ ] RDS connections use SSL/TLS
- [ ] RDS storage and backups are encrypted with KMS
- [ ] Application-specific DB users are created (master credentials not used by apps)
- [ ] AWS Secrets Manager rotates database credentials
- [ ] RDS versions are patched and current
- [ ] No sensitive data in free-form IAM fields

## References

- [Security best practices for Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.Security.html)
- [Amazon RDS Security](https://aws.amazon.com/rds/features/security/)
