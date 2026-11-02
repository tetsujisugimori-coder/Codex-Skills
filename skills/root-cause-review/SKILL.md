---
name: root-cause-review
description: Investigate a persistent software defect by questioning historical implementation constraints, separating invariants from design choices, and proposing a practical root-cause solution. Use when fixes repeatedly fail or diagnostics remain inconclusive.
---

# Root Cause Review

## Mission
Understand why a persistent problem remains unresolved and recommend a viable route to closure, rather than indefinitely finding new defects.

## Working principles
- Establish the current symptom, relevant evidence, and target revision. Distinguish what is observed from what is inferred.
- Treat prior implementation choices (local-fix-only, unchanged structure, selected algorithm, prescribed test approach) as revisable hypotheses, not permanent requirements.
- Preserve true product and safety invariants: data integrity, security, compatibility where required, and explicit restrictions on execution or deployment. Propose changes to these only for explicit approval, never silently apply them.
- Investigate plausible causal explanations and select discriminating checks autonomously. If root cause remains unknown, specify the minimum useful experiment rather than inventing certainty.
- Consider a simpler architecture or changed testing/observability strategy when justified; do not force a predefined menu of solutions.
- Recommend one actionable approach, explain tradeoffs and acceptance criteria, and distinguish review of a diagnostic PR from authorization to operate the product.
- By default investigate and propose only; do not modify code, post, merge, or alter safety settings without explicit instruction.

## Output
State confirmed facts; most likely cause and confidence (or UNKNOWN); inherited constraints worth revisiting; recommended approach and why; minimal next implementation/experiment; verification and closure criteria; remaining risks and any distinct merge/operational decisions.
