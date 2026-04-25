# Architecture Model (v1)

This document defines the core elements of the Architecture as Code (AaC) model, their relationships, and how they map to implementation and validation.

## Core Elements

### Risk
A potential threat or vulnerability that could compromise the system.

**Fields:**
- `id` – unique identifier (e.g., R-001)
- `name` – short description
- `control_objective` – what must be achieved to mitigate the risk

### Control Objective
A high-level goal that, if achieved, mitigates the risk.

### Control
A specific technical or procedural mechanism that implements the control objective.

**Fields:**
- `id` – unique identifier (e.g., C-001)
- `name` – short description
- `type` – e.g., TechnicalControl
- `constraints` – list of specific requirements

### Constraint
A concrete requirement that the implementation must satisfy.

**Fields:**
- `id` – unique identifier (e.g., CON-001)
- `description` – precise statement

### Implementation Mapping
Links a control to actual infrastructure resources (IaC).

**Fields:**
- `control_id` – reference to a control
- `resource_type` – Terraform resource type (e.g., `azurerm_windows_virtual_machine`)
- `tags` – required tags on the resource
- `parameters` – required configuration parameters

### Validation
The process of checking whether the implementation matches the model.

**Current approach:** validation against Terraform state, including resource type, tags, and selected parameters (see [validator](../aac/validator.py))

## Example

See [`examples/basic-model.yaml`](../examples/basic-model.yaml) for a complete example.

The example implements the following chain:

**Risk (R-001):** Privilege escalation via compromised admin endpoint  
↓  
**Control Objective:** Ensure privileged access originates only from trusted and managed devices  
↓  
**Control (C-001):** Privileged Access Workstation (PAW)  
↓  
**Constraint (CON-001):** Admin roles require compliant devices  
↓  
**Implementation Mapping:**  
- `azurerm_windows_virtual_machine` with `tags.role = PAW`  
- `azurerm_conditional_access_policy` with `parameters.grant_controls = ["requireCompliantDevice"]`  
↓  
**Validation:** Check that these resources exist in Terraform state and match required tags and parameters

**Current prototype coverage:** Only resource existence for `azurerm_windows_virtual_machine` is implemented. Conditional Access policy check is modeled but not yet validated.

## Relationships

- A **Risk** is mitigated by one or more **Control Objectives** (conceptual relationship).
- A **Control Objective** is implemented by one or more **Controls** (conceptual relationship).

- In the current model, **Controls are the primary link between risks and implementation**.

- A **Control** has one or more **Constraints**.
- A **Control** is linked to infrastructure via **Implementation Mappings**.

- **Validation** checks that Implementation Mappings match actual Terraform state.

## Open Standard

This model is versioned and open to change.

All contributions to the model definition are welcome.
