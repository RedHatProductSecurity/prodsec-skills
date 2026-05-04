---
name: kafka-amq-security
description: >
  Secure Kafka and AMQ Streams deployments with encryption, authentication,
  and authorization. Use when building, reviewing, or auditing Kafka broker
  configuration, AMQ Streams custom resources, or Kafka client connectivity.
category: "secure_development"
subcategory: "messaging"
---

# Kafka and AMQ Streams Security

## Encryption

By default, Kafka transmits data in **plaintext**, leaving it vulnerable to man-in-the-middle attacks.

- Enable TLS/SSL encryption for all client-to-broker and broker-to-broker communication
- The performance cost of TLS is typically negligible on modern hardware
- TLS only protects data in transit; apply additional controls for data at rest

### AMQ Streams Encryption

AMQ Streams encrypts communication between brokers and operators using TLS by default. Client encryption depends on Kafka listener configuration:

- **Cluster CA** signs broker certificates; **Clients CA** signs client certificates
- The Cluster Operator automatically generates and renews CA certificates
- Users may provide their own CA certificates (must be renewed manually)
- Client applications must trust Cluster CA certificates unless TLS is explicitly disabled on external listeners

## Authentication

### Kafka Authentication

Use SSL or SASL for client-to-broker and broker-to-broker authentication:

| Method | Use Case |
|---|---|
| **SSL (mutual TLS)** | Most common for managed services; two-way certificate authentication |
| **SASL SCRAM-SHA-512** | Password-based; suitable for environments without certificate infrastructure |
| **SASL Kerberos** | Enterprise environments with existing Kerberos infrastructure |
| **OAuth 2.0** | Token-based; integrates with RHSSO/Keycloak |

### AMQ Streams Authentication

Authentication is **disabled by default** in AMQ Streams. Enable it per listener in the Kafka custom resource:

- Configure the `authentication` property on each broker listener
- Each listener can use a different authentication mechanism
- Clients must use KafkaUser credentials to connect once authentication is enabled

## Authorization

### Access Control Lists (ACLs)

Limit which clients can read and write to specific topics:

- Use ACLs with the format: "Principal P is Allowed/Denied Operation O From Host H on Resource R"
- Apply ACLs to Topics, Consumer Groups, Clusters, and Transactional IDs
- Restrict super users to the minimum necessary; super users bypass all ACL checks

### AMQ Streams Authorization Options

| Mechanism | Description |
|---|---|
| **Simple ACL** | Default Apache Kafka ACL plugin; rules stored in ZooKeeper, loaded at broker startup |
| **OAuth 2.0 / Keycloak** | Authorization rules managed in RHSSO/Keycloak; requires OAuth authentication |
| **Open Policy Agent (OPA)** | Externalized policy engine for fine-grained authorization |

Authorization is configured via the `authorization` property in the Kafka custom resource. If omitted, authorization is disabled.

## Network Security

- Place brokers in a **private network**
- Use port-based firewalls to restrict access to broker and ZooKeeper ports
- Use web-access firewalls to limit the set of allowed requests
- Do not expose broker ports to the public Internet unless required

## Monitoring

- Monitor access patterns to detect unknown entities accessing topics
- Alert on anomalous client behavior (unusual topic access, volume spikes)
- Integrate with Elasticsearch/Kibana or equivalent for real-time KPI monitoring

## Implementation Checklist

- [ ] TLS/SSL is enabled for all client-to-broker communication
- [ ] TLS is enabled for broker-to-broker (inter-broker) communication
- [ ] Authentication is configured on every listener (SSL, SASL, or OAuth)
- [ ] ACLs restrict topic access to authorized clients only
- [ ] Super users are limited to cluster administration accounts
- [ ] Brokers are deployed in a private network with firewall rules
- [ ] Monitoring and alerting are configured for access anomalies
- [ ] AMQ Streams CA certificates are managed and rotated

## References

- [Apache Kafka Security](https://kafka.apache.org/documentation/#security)
- [Securing access to Kafka (Streams for Apache Kafka 3.0)](https://docs.redhat.com/en/documentation/red_hat_streams_for_apache_kafka/3.0/html/using_streams_for_apache_kafka_on_rhel/assembly-securing-kafka-str)
- [Strimzi: Accessing Kafka](https://strimzi.io/blog/2019/04/17/accessing-kafka-part-1/)
