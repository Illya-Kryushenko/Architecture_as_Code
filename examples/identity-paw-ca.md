# Identity / PAW / Conditional Access Example

## Scenario
Privileged access to Azure resources must be restricted to compliant, managed devices.

## Risk
Credential theft via unmanaged or compromised endpoint.

## Control Objective
Ensure privileged access originates only from trusted devices.

## Controls
- Conditional Access
- Device compliance
- Privileged Identity Management

## Constraints
- Admin access requires compliant device
- No access from unmanaged endpoints

## Implementation Mapping
- Azure AD Conditional Access policy
- Intune compliance policies
- PIM role activation

## Signal (optional)

## Commentary
Break-glass accounts are excluded and monitored separately.

## See also

- [Full AaC model example](../examples/basic-model.yaml)
- [Architecture model specification](..docs/architecture-model.md)
