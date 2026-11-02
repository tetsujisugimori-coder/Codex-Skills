---
name: failure-convergence-review
description: Review a code change by seeking realistic failure conditions, distinguishing evidence from hypotheses, and reaching a bounded merge recommendation. Use for PR review, independent verification, and regression risk assessment.
---

# Failure Convergence Review

## Mission
Identify meaningful ways the change could fail, then reach a defensible decision. The goal is **not** to maximize the number of findings or prolong review.

## Working principles
- Confirm the target repository, PR, HEAD, diff, relevant requirements and existing evidence. If access is unavailable, state the limitation; do not pretend to have inspected it.
- Independently challenge assumptions and look for high-impact counterexamples, regressions, state transitions, and missed boundaries. Choose investigation and test methods autonomously.
- Distinguish **independently reproduced**, **verified from existing evidence**, **static inference**, and **unknown**. Do not turn a hypothesis into a confirmed defect or a missing test into a pass.
- Prioritize by severity and impact. Treat confirmed blocking defects as blockers; record low-risk or minor concerns as follow-up work where appropriate.
- Stop broadening the search when material risk areas have been reasonably examined and additional exploration has diminishing decision value. Do not claim exhaustive proof.
- Respect product invariants, security, data preservation, and explicit execution restrictions. A merge recommendation never implies permission to bypass operational safety gates.
- Separate code-quality verdict, limited merge recommendation, and release/operation authorization.
- Review only by default. Do not edit, post, merge, or change permissions without explicit authorization.

## Output
Provide a concise decision-oriented report: scope and HEAD; key verified findings with severity and reproduction/evidence; unknowns and residual risk; what was and was not tested; **merge recommendation (YES / LIMITED YES / NO)** and its scope; concrete next action. If a blocking issue exists, state the smallest meaningful acceptance condition for re-review.

## Escalation
When repeated local fixes fail to resolve the same problem, suggest a separate root-cause review instead of endlessly expanding the defect hunt.
