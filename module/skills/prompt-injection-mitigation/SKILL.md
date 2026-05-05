---
name: prompt-injection-mitigation
description: Mitigate prompt injection risks in LLM-based systems. Use when designing, building, or reviewing AI systems that accept user prompts, or when evaluating model safety for deployment.
category: "secure_development"
subcategory: "large-language-model"
---

# Prompt Injection Mitigation

## Security Recommendation

Prompt injection cannot be fully prevented. It can only be minimized. The approach combines multiple layers of defense rather than relying on a single control.

## Mitigation Strategies

### 1. Leverage Runtime Security Controls

Use architectural components that reduce prompt injection probability:

- **API gateway**: Rate limiting reduces the volume of probing attempts
- **Runtime guardrails**: Filter inputs and outputs to detect and block injection patterns (see `guardrails/bidirectional-filtering`)

### 2. Choose Safer Models

Model safety is primarily determined during pre-training and fine-tuning. If the solution does not pre-train or fine-tune its own models, select models that have been trained with safety as a priority.

| Evaluation Criteria | What to Look For |
|---|---|
| **Safety benchmarks** | Published safety evaluation scores and red-team results |
| **Alignment training** | RLHF, constitutional AI, or other alignment techniques applied |
| **Known vulnerabilities** | Check for disclosed prompt injection vulnerabilities |
| **Provider reputation** | Track record of the model provider on security and safety |

### 3. Human-in-the-Loop for Sensitive Actions

The best mitigation for prompt injection in agentic systems is keeping a human in the loop. Require explicit user confirmation before executing any sensitive or destructive action triggered by the LLM. This is especially critical for MCP-based agents where tool execution can have real-world impact.

### 4. Limit Model Capabilities

Reduce the impact of successful prompt injection by constraining what the model can do:

- Restrict tool/function calling capabilities to only what's needed
- Validate model outputs before executing any generated actions (see `eval_sandbox/output-validation-sandbox`)
- Apply output guardrails to filter dangerous responses

## Defense-in-Depth Layers

```
Rate Limiting (API Gateway)
  → Input Guardrails (prompt filtering)
    → Safer Model (alignment training)
      → Output Guardrails (response filtering)
        → Output Validation Sandbox (if model generates actions)
```

## Additional OWASP LLM Top 10 Threats

Beyond prompt injection, address these related LLM risks:

### Insecure Plugin/Tool Design (LLM07)

- Plugins called by the model must enforce strict parameterized input with type and range checks
- When freeform input is required, inspect it for potentially harmful method calls
- Apply least-privilege to plugin capabilities; remove unused functions

### Model Theft (LLM10)

- Implement strong access controls (RBAC, least privilege) on model repositories and training environments
- Monitor for extraction attempts via carefully crafted API queries
- Apply data security controls to model weights and parameters

### Data Poisoning and Supply Chain (LLM03, LLM05)

- Verify the supply chain of training data, especially when sourced externally
- Maintain attestations via ML-BOM (Machine Learning Bill of Materials) and verify model cards
- Carefully select and sanitize all data used for training or fine-tuning

### Sensitive Information Disclosure (LLM06)

- Use regularization techniques to prevent overfitting and memorization of sensitive training data
- Apply the rule of least privilege: do not train models on information that lower-privileged users should not see
- Limit access to external data sources during runtime orchestration
- Consider differential privacy techniques to preserve training data privacy

### Denial of Service (LLM04)

- Cap resource use per request or step so complex requests execute more slowly
- Enforce API rate limits per user and IP address

## Implementation Checklist

- [ ] Deploy runtime guardrails for input and output filtering
- [ ] Configure API gateway rate limiting to slow probing attacks
- [ ] Evaluate and document the safety properties of chosen models
- [ ] Prefer models with published safety benchmarks and alignment training
- [ ] Require user confirmation for sensitive or destructive LLM-triggered actions (human-in-the-loop)
- [ ] Restrict model tool/function calling to the minimum needed
- [ ] Validate model-generated actions in a sandbox before execution
- [ ] Monitor for prompt injection patterns in production logs
- [ ] Regularly re-evaluate model safety as new vulnerabilities are disclosed
- [ ] Plugins/tools enforce parameterized input with type and range checks
- [ ] Model repositories and training environments use RBAC and least privilege
- [ ] Training data supply chain is verified; ML-BOM and model cards are maintained
- [ ] Regularization and differential privacy are applied to protect training data
- [ ] Resource caps and rate limits prevent LLM denial of service
