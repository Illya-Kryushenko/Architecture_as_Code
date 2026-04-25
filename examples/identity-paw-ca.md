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
- **C-002** Managed Admin Endpoint Baseline
- **C-003** Administrative Endpoint Classification
- **C-004** Dedicated Administrative Isolation Components

## Constraints
- **CON-001** Admin roles require compliant devices
- **CON-002** Hardware security must be enabled (Secure Boot and vTPM)

Additional policy-level constraints:
- Admin access requires compliant device
- No access from unmanaged endpoints

## Implementation Mapping
Representative implementation components include:
- Azure AD Conditional Access policy
- Intune compliance policies
- PIM role activation

## Signal (optional)

## Commentary
Break-glass accounts are excluded and monitored separately.

## See also

- [Full AaC model example](../examples/basic-model.yaml)
- [Architecture model specification](../docs/architecture-model.md)
