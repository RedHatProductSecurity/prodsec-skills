---
name: model-security-scanning
description: Scan AI models for malicious elements before loading in inference engines. Use when building or reviewing inference engines, model loading pipelines, or model distribution systems.
category: "secure_development"
subcategory: "inference-engine"
---

# Model Security Scanning in Inference Engines

## Security Recommendation

Inference engines SHOULD scan models for malicious elements before loading them. This is a defense-in-depth control that complements signature verification.

## Threats Detected by Scanning

| Threat | Description |
|---|---|
| **Malicious code in weights** | Some weight formats (e.g., Python pickle) can embed arbitrary executable code |
| **Backdoored models** | Models with hidden behaviors triggered by specific inputs |
| **Embedded scripts** | Configuration files or metadata containing executable payloads |
| **Unsafe serialization formats** | Formats that execute code during deserialization |

## Unsafe Weight Formats

The inference engine SHOULD advise against or refuse to load weight formats that can include malicious code:

| Format | Risk Level | Recommendation |
|---|---|---|
| **Python pickle** (`.pkl`, `.pickle`) | High | Avoid; can execute arbitrary Python code on load |
| **PyTorch legacy** (`.pt`, `.pth` using pickle) | High | Prefer SafeTensors format instead |
| **SafeTensors** (`.safetensors`) | Low | Preferred; no code execution during deserialization |
| **GGUF** | Low | Safe format for quantized models |
| **ONNX** | Medium | Generally safe but verify custom operators |

## Implementation Checklist

- [ ] Implement model scanning in the model loading pipeline
- [ ] Detect and flag unsafe serialization formats (pickle-based weights)
- [ ] Prefer SafeTensors or other safe formats; warn or block unsafe formats
- [ ] Scan model metadata and configuration files for embedded scripts
- [ ] Log scanning results as security events
- [ ] Allow security teams to configure scanning policies (warn vs. block)
- [ ] Integrate with model registry scanning if available
