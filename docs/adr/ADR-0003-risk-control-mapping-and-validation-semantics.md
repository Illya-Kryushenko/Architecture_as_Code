# ADR-0003: Introduce explicit Risk-to-Control mapping and multi-level validation semantics

## Status
Accepted

## Date
2026-04-25

## Context

The initial model defined a conceptual chain:

Risk → Control Objective → Control → Implementation

However:

- the relationship between Risk and Control was not explicitly represented in the data model
- validation operated only at the resource level
- there was no consistent way to aggregate validation results into architectural outcomes
- risk coverage could not be evaluated reliably

This limited the ability to interpret validation results at the architecture level.

## Decision

The canonical architecture model is the source of truth for validation and coverage evaluation.
The model is updated to introduce explicit traceability and multi-level validation semantics:

1. Explicit Risk-to-Control mapping
   - Risks now include a list of associated controls (`controls` field)

2. Multi-level validation model
   Validation is evaluated at three levels:

   - Mapping level:
     PASS / FAIL / MISSING

   - Control level:
     COVERED / FAILED / INCOMPLETE / MISSING

   - Risk level:
     COVERED / EXPOSED

3. Aggregation rules
   - A control is COVERED only if all its mappings PASS
   - A control is FAILED if any mapping FAILS
   - A control is INCOMPLETE if some mappings PASS and others are MISSING
   - A control is MISSING if all mappings are MISSING
 
   - A risk is COVERED only if all linked controls are COVERED
   - If any linked control is not COVERED, the risk is EXPOSED

## Rationale

This decision enables:

- explicit traceability from risk to implementation
- deterministic evaluation of architectural coverage
- consistent interpretation of validation results
- demonstration of architecture-level reasoning from infrastructure state
- a clear separation between conceptual relationships and executable model semantics

It also aligns the model, example, and validator behavior.

## Consequences

Positive:
- The model becomes executable and interpretable
- Validation results can be propagated from implementation to risk level
- The example demonstrates multiple architectural states (FAILED, INCOMPLETE, EXPOSED)
- The system moves from resource validation to architecture validation

Negative:
- The model remains simplified (no formal graph structure)
- Control Objective is still conceptual and not represented as a first-class entity
- Signals are not yet used in validation
- Risk evaluation is binary (COVERED / EXPOSED)
- The model assumes deterministic evaluation without weighting or prioritization of controls