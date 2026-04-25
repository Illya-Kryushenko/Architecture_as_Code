# Identity / PAW / Conditional Access Example

## Representation

This document is a human-readable representation of the canonical Architecture as Code model defined in `basic-model.yaml`.

## Scenario
Privileged access to Azure resources must be restricted to compliant, managed devices.

## Risk
**ID:** R-001  
Credential theft via unmanaged or compromised endpoint.

## Control Objective
Ensure privileged access originates only from trusted devices.

## Controls

- **C-001** Privileged Access Workstation (PAW)  
  Dedicated hardened administrative workstation used for privileged operations.

- **C-002** Managed Admin Endpoint Baseline  
  Administrative endpoints must comply with an approved baseline configuration.

- **C-003** Administrative Endpoint Classification  
  Administrative endpoints must be explicitly identified and classified.

- **C-004** Dedicated Administrative Isolation Components  
  Additional infrastructure components must enforce isolation of privileged environments.

---

## Constraints

### Model-defined constraints

- **CON-001** Admin roles require compliant devices  
- **CON-002** Hardware security must be enabled (Secure Boot and vTPM)  
- **CON-003** Admin endpoint must use the approved PAW baseline  
- **CON-004** Endpoint monitoring extension must be present  
- **CON-005** Administrative endpoints must carry the required classification tag  
- **CON-006** Dedicated isolation components must be deployed for privileged access  
- **CON-007** Supporting policy artifacts must exist in the managed environment  

### Additional policy-level constraints

- Admin access requires compliant device  
- No access from unmanaged endpoints  

---

## Implementation Mapping

Representative implementation components include:

### Endpoint (PAW)

- Azure virtual machines configured as PAW
- Required:
  - `role = PAW` tag
  - Secure Boot enabled
  - vTPM enabled

### Identity and Access Control

- Azure AD Conditional Access policies enforcing compliant device requirement
- PIM role activation policies

### Endpoint Management

- Intune compliance policies
- Monitoring / security extensions deployed on administrative endpoints

### Isolation and Network Controls

- Dedicated firewall components for privileged environments
- Network security groups enforcing restricted access patterns

---

## Signal (conceptual)

Potential observable signals include:

- Entra ID sign-in logs  
- Conditional Access evaluation logs  
- Defender alerts  

These signals can be used to validate that controls are effective in runtime.

---

## Commentary

Break-glass accounts are excluded from standard controls and must be monitored separately.

This example demonstrates how:

- control failures (misconfiguration or missing components)
- partial implementations
- and missing infrastructure elements

can be detected and propagated to higher-level risk exposure.

---

## See also

- [Full AaC model example](../examples/basic-model.yaml)
- [Architecture model specification](../docs/architecture-model.md)
