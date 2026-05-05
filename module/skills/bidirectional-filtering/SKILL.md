---
name: bidirectional-filtering
description: Deploy runtime guardrails for bidirectional prompt and response filtering in AI systems. Use when designing, building, or reviewing AI architectures that need prompt injection protection, content filtering, or input/output safety controls.
category: "secure_development"
subcategory: "guardrails"
---

# Bidirectional Filtering with Runtime Guardrails

## Security Requirement

A guardrails component SHOULD be deployed between the users/applications (or API gateway) and the models. This component acts as a gateway or proxy that inspects and acts on data flowing in **both directions**.

This skill refers to runtime guardrails (a deployed component), not model-level safety training.

## Input Direction (User/App → Model)

Incoming prompts are raw or "tainted" input. The guardrails component analyzes them and applies rule-based actions:

| Action | Description |
|---|---|
| **Block** | Discard the prompt entirely, preventing it from reaching the model |
| **Mask** | Redact or obfuscate sensitive data (PII, credentials) before forwarding |
| **Modify** | Rewrite the prompt to remove dangerous patterns while preserving intent |
| **Pass** | Allow the prompt through unchanged |

Objectives:
- Prevent specific sensitive data from reaching the model
- Reduce the probability of prompt injection
- Enforce content policies on inputs

## Output Direction (Model → User/App)

Model responses are inspected before delivery to the user or application:

| Action | Description |
|---|---|
| **Block** | Suppress the response if it contains harmful or policy-violating content |
| **Mask** | Redact sensitive data the model may have included in its response |
| **Modify** | Remove or rewrite problematic portions of the response |
| **Pass** | Deliver the response unchanged |

Objectives:
- Prevent leakage of sensitive training data
- Enforce content safety policies on outputs
- Filter harmful, biased, or off-topic responses

## Architecture Position

```
User/App → API Gateway → Guardrails → Inference Engine → Model
                            ↕ (inspects both directions)
User/App ← API Gateway ← Guardrails ← Inference Engine ← Model
```

## Implementation Checklist

- [ ] Deploy a guardrails component between the API gateway and the inference engine
- [ ] Configure input rules for prompt analysis (block, mask, modify, pass)
- [ ] Configure output rules for response analysis (block, mask, modify, pass)
- [ ] Define PII detection and masking rules for both directions
- [ ] Define prompt injection detection rules for the input direction
- [ ] Define content safety policies for the output direction
- [ ] Log all guardrail actions (blocks, masks, modifications) for audit
- [ ] Monitor guardrail effectiveness and tune rules based on observed patterns
- [ ] Ensure the guardrails component does not become a single point of failure (deploy with redundancy)
