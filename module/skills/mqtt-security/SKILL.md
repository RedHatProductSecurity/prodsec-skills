---
name: mqtt-security
description: >
  Secure MQTT broker and client deployments with authentication, topic ACLs,
  and transport encryption. Use when building, reviewing, or auditing MQTT
  broker configuration, client connectivity, or IoT messaging security.
category: "secure_development"
subcategory: "messaging"
---

# MQTT Security

## Client Authentication

MQTT brokers can verify client identity through three mechanisms, listed from weakest to strongest:

### Client IDs

- All MQTT clients must provide a client ID
- The client ID links subscriptions to the client and TCP connection
- Client IDs must be unique; use them for basic identification, not as a sole authentication factor

### Username and Password

- Brokers can require a valid username/password before permitting connections
- Credentials are transmitted in **cleartext** without transport encryption -- always combine with TLS
- The username can also be used to restrict access to topics
- This is the most common authentication method

### x509 Client Certificates

- The most secure authentication method, but the most complex to deploy
- Requires provisioning and managing certificates on every client
- Best suited for a small number of clients requiring high assurance
- Provides mutual authentication between client and broker

## Topic Access Control

- Restrict which clients can subscribe to and publish on specific topics
- Use the **username** as the primary access control identifier
- The **client ID** can serve as a secondary control mechanism
- Apply least-privilege: grant only the specific topics each client needs

## Data Protection

### TLS Transport Encryption

- TLS encrypts the entire MQTT connection, including headers, topic names, and payload
- This is a TCP/IP-level protection, not MQTT-specific
- Protects all parts of the MQTT message, not just the payload
- Requires TLS client support, which may not be available on constrained IoT devices

### Payload Encryption

- Application-level encryption of the message payload only
- Provides **end-to-end** encryption (client to client), not just client to broker
- Does not require broker configuration or support
- Does **not** protect credentials (username/password) on the connection itself
- Use when TLS is not feasible on constrained devices or when end-to-end confidentiality is required

### Choosing Between TLS and Payload Encryption

| Factor | TLS | Payload Encryption |
|---|---|---|
| **Scope** | Full connection (headers + payload) | Payload only |
| **End-to-end** | No (terminates at broker) | Yes (client to client) |
| **Credential protection** | Yes | No |
| **Device requirements** | TLS stack required | Crypto library required |
| **Broker configuration** | Required | Not required |

For maximum security, use both: TLS for transport and payload encryption for end-to-end confidentiality.

## Implementation Checklist

- [ ] TLS is enabled on all broker listeners
- [ ] Client authentication is required (username/password or x509 certificates)
- [ ] Credentials are never transmitted without TLS
- [ ] Topic ACLs restrict publish/subscribe access per client
- [ ] x509 certificates are used for high-assurance clients
- [ ] Payload encryption is used when end-to-end confidentiality is required
- [ ] Client IDs are unique and tracked
- [ ] Default/anonymous access is disabled on production brokers

## References

- [MQTT v5.0 OASIS Standard — Section 5: Security](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901261)
- [OWASP MQTT Security Guide](https://owasp.org/www-project-mqtt-guide/)
- [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
