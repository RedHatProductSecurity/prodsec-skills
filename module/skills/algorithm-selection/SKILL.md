---
name: algorithm-selection
description: >
  Apply when selecting, reviewing, or configuring cryptographic
  algorithms, cipher suites, protocol versions, or key exchange
  mechanisms. Covers banned/deprecated/recommended algorithms,
  post-quantum readiness, key management, and OpenSSL API migration.
license: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
origin: Adapted from CoSAI Project CodeGuard (https://github.com/cosai-oasis/project-codeguard)
category: "secure_development"
subcategory: "crypto"
---

# Cryptographic Algorithm Selection and Post-Quantum Readiness

Reference for which cryptographic algorithms to use, which to avoid, and how to prepare for post-quantum cryptography.

## Banned (Insecure) Algorithms

NEVER use these algorithms. They are cryptographically broken.

| Type | Banned |
|------|--------|
| Hash | MD2, MD4, MD5, SHA-0 |
| Symmetric | RC2, RC4, Blowfish, DES, 3DES |
| Key Exchange | Static RSA, Anonymous Diffie-Hellman |

## Deprecated (Legacy/Weak) Algorithms

Avoid in new designs. Prioritize migration away from these.

| Type | Deprecated | Issue |
|------|-----------|-------|
| Hash | SHA-1 | Collision attacks demonstrated |
| Symmetric | AES-CBC, AES-ECB | Unauthenticated; ECB leaks patterns |
| Signature | RSA with PKCS#1 v1.5 padding | Padding oracle attacks |
| Key Exchange | DHE with weak/common primes | Vulnerable to precomputation attacks |

## Recommended and Post-Quantum Ready Algorithms

### Symmetric Encryption

- **Standard**: AES-GCM (AEAD), ChaCha20-Poly1305
- **PQC requirement**: prefer AES-256 keys -- resistant to Grover's algorithm
- **Avoid**: custom crypto or unauthenticated modes

### Key Exchange (KEM)

- **Standard**: ECDHE (X25519 or secp256r1)
- **Hybrid key exchange** (classical + PQC) when supported:
  - Preferred: `X25519MLKEM768` (X25519 + ML-KEM-768)
  - Alternative: `SecP256r1MLKEM768` (P-256 + ML-KEM-768)
  - High assurance: `SecP384r1MLKEM1024` (P-384 + ML-KEM-1024)
- **Pure PQC**: ML-KEM-768 (baseline) or ML-KEM-1024. Avoid ML-KEM-512 unless explicitly risk-accepted.
- Use vendor-documented identifiers (RFC 9242/9370). Remove legacy/draft "Hybrid-Kyber" groups and hardcoded OIDs.

### Signatures and Certificates

- **Standard**: ECDSA (P-256)
- **PQC migration**: continue using ECDSA (P-256) for mTLS and code signing until hardware-backed (HSM/TPM) ML-DSA is available.
- **Hardware requirement**: do not enable PQC ML-DSA signatures with software-only keys. Require HSM/TPM storage.

### Protocol Versions

- **(D)TLS**: enforce (D)TLS 1.3 only (or later)
- **IPsec**: enforce IKEv2 only
  - Use ESP with AEAD (AES-256-GCM)
  - Require PFS via ECDHE
  - Implement RFC 9242 and RFC 9370 for hybrid PQC (ML-KEM + ECDHE)
  - Ensure re-keys (CREATE_CHILD_SA) maintain hybrid algorithms
- **SSH**: enable only vendor-supported PQC/hybrid KEX (e.g., `sntrup761x25519`)

## Secure Implementation Guidelines

### General Best Practices

- **Configuration over code**: expose algorithm choices in config/policy to allow agility without code changes.
- **Key management**:
  - Use KMS/HSM for key storage
  - Generate keys with a CSPRNG
  - Separate encryption keys from signature keys
  - Rotate keys per policy
  - NEVER hardcode keys, secrets, or experimental OIDs
- **Telemetry**: capture negotiated groups, handshake sizes, and failure causes to monitor PQC adoption.
- **Avoid custom crypto**: use well-vetted libraries; never implement your own primitives.

### Deprecated OpenSSL APIs (C/C++)

Never use these deprecated functions. Use the EVP high-level APIs.

| Deprecated | Replacement |
|-----------|-------------|
| `AES_encrypt()`, `AES_decrypt()` | `EVP_EncryptInit_ex()` with `EVP_aes_256_gcm()` |
| `RSA_new()`, `RSA_free()`, `RSA_get0_n()` | `EVP_PKEY_new()`, `EVP_PKEY_free()` |
| `SHA1_Init()` | `EVP_DigestInit_ex()` with SHA-256 or stronger |
| `HMAC()` with SHA-1 | `EVP_Q_MAC()` with SHA-256 or stronger |

### AES-256-GCM Example (C/OpenSSL)

```c
EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
if (!ctx) handle_error();

if (EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, iv) != 1)
    handle_error();

int len, ciphertext_len;
if (EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len) != 1)
    handle_error();
ciphertext_len = len;

if (EVP_EncryptFinal_ex(ctx, ciphertext + len, &len) != 1)
    handle_error();
ciphertext_len += len;

EVP_CIPHER_CTX_free(ctx);
```

### HMAC-SHA256 Example (C/OpenSSL)

```c
EVP_Q_MAC(NULL, "HMAC", NULL, "SHA256", NULL,
          key, key_len, data, data_len,
          out, out_size, &out_len);
```

## Implementation Checklist

- [ ] No banned algorithms (MD5, RC4, DES, 3DES) in use anywhere
- [ ] SHA-1 and AES-CBC/ECB identified and scheduled for migration
- [ ] AES-GCM or ChaCha20-Poly1305 used for symmetric encryption
- [ ] ECDHE (X25519 or P-256) used for key exchange
- [ ] Hybrid PQC key exchange evaluated and enabled where supported
- [ ] TLS 1.3 enforced; TLS 1.0/1.1/1.2 disabled or on migration plan
- [ ] Keys stored in KMS/HSM; no hardcoded keys or secrets
- [ ] Algorithm choices in configuration, not hardcoded
- [ ] Deprecated OpenSSL APIs replaced with EVP equivalents
- [ ] PQC adoption telemetry in place
