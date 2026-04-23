**Architecture As Code for Cloud Adoption Framework and Zero Trust**
*WhitePaper*

**Introduction**
Modern cloud architectures are increasingly defined using Infrastructure as Code (IaC) technologies such as Terraform and Bicep. IaC provides a precise, reproducible description of deployed systems. However, it does not explain why the system is built in a certain way. It reflects implementation, but not intent.
At the same time, architectural frameworks such as Microsoft Cloud Adoption Framework (CAF) and Zero Trust provide structured and valuable guidance but remain largely descriptive. They exist as documents, recommendations, and reference architectures, rather than executable or verifiable models.
This proposal introduces a concept of transforming CAF and Zero Trust from descriptive guidance into an executable, machine-readable architecture model.
Beyond technical traceability, the concept addresses an additional strategic gap: architecture as a portable asset. Today, architectural knowledge is trapped in documents, slide decks, and proprietary templates. A single architecture cannot be shared between organizations, rendered into different partner formats, or automatically adapted to varying methodological frameworks (TOGAF, CAF, Well-Architected, internal standards). 
This proposal introduces a canonical architecture model that separates semantic content from representation, enabling one architecture to generate multiple views without loss of meaning or manual rework.
**Core Idea**
Architecture is represented as a structured model rather than static documentation. This model captures intent, constraints, decisions, and mappings to implementation. 
The minimal modeling unit is a traceable chain from:
Risk → Control → Constraint → Implementation → Validation
From this model, multiple outputs can be generated: human-readable documents, validation rules, and IaC scaffolding.
**Human vs Machine Representation**
The architecture model is the single source of truth. Human-readable documents are generated views.
The document contains structured sections, which are generated, canonical, and enforceable, and commentary sections, which are human-authored and explanatory. Structured content defines architecture. Commentary explains it.
**Representation Profiles and Document Views**
The system should separate the canonical architecture model from the way that model is rendered for human consumption. The same architecture may need to be presented in a neutral format, in a company-specific format, or in a vendor-oriented vocabulary without changing the underlying model.
This implies three layers:
•	Canonical layer – the structured architecture model (YAML/JSON with enforced schema). Remains the single source of truth.
•	Representation layer – rendering profiles that define terminology, document structure, section ordering, naming conventions, and visibility rules. Profiles may be organization-specific (client A, client B, 3d party), methodology-specific (TOGAF, CAF, Well-Architected), or domain-specific (security view, operations view, compliance view).
•	Output layer – concrete artifacts: Solution Architecture Report, Technical Solution Design, HLD, LLD, security view, governance view, audit package.
The initial implementation should support one neutral representation profile only. However, the model must be designed so that future profiles can render the same architecture using a company-preferred or methodology-specific style.
Critical rule: Representation profiles may change terminology, section order, and visual grouping, but they must not change the meaning of model elements. The model is canonical. Profiles are representational, not semantic authorities.
**Strategic implication**
This design enables interoperability across organizational boundaries. If 3d party company and a client both adopt the canonical model (or mutually translatable profiles), architectural handover ceases to be a document exchange and becomes a model exchange. Each party can render the architecture into its own preferred document format without manual reinterpretation. The same mechanism works for subcontractor integration: a security specialist receives only the security view, works in its own tooling, and returns updates that merge into the canonical model.
**Multi-Profile Management**
A single architecture may need to be rendered into multiple profiles simultaneously. The system should support:
•	Profile inheritance – a client-specific profile extends the neutral profile, overriding only terminology and section order.
•	Profile composition – a security review profile selects specific model elements (risks, controls, constraints) and renders them with auditor-friendly language.
•	Profile versioning – profiles evolve separately from the model. Old profiles remain available for legacy document regeneration.
The implementation complexity of multi-profile support is non-trivial, but architecture must not preclude it.
**Coverage and Completeness Control**
A representation problem remains even when multiple views are supported: a given human-readable document may omit architectural elements that exist in the model. This is not automatically wrong, because different document types have different purposes. However, omissions must be explicit and controlled.
The system should therefore include a coverage or completeness control layer. Instead of forcing every document to show every element, the system should detect which model elements are represented in each view, which are intentionally excluded, and which are missing without justification.
The goal is not to make every document exhaustive. The goal is to guarantee that nothing important becomes invisible by accident. Every model element should either be represented in each view or explicitly marked as excluded for a stated reason.
**Implementation approach**
Coverage control should be implemented as a separate report or review mode rather than as visual noise in the main document. A standard human-readable document remains clean. A separate coverage summary or debug view shows which risks, controls, constraints, decisions, or implementation mappings are not reflected in the current representation.
A combined view may also be useful for expert review. In such mode, rendered narrative text is paired with the corresponding canonical fragment from the structured model. This is not the default document mode, but it is valuable for traceability, model debugging, and design reviews.
**Drift Detection and Two-Way Consistency**
The model exists to describe intent. Implementation exists in IaC (Terraform). Over time, they diverge. The system must support:
1.	Model → IaC consistency check – does the implemented infrastructure match the architecture intent? This includes resource existence, configuration parameters, and relationships.
2.	IaC → Model completeness check – are there implemented components that have no corresponding model element (orphaned resources)?
3.	Selective override – some divergence may be intentional (e.g., a temporary change for incident response). The model should allow explicit waiver annotations with expiration dates.
Initially, drift detection operates on Terraform state (not directly on Azure APIs). This reduces complexity and leverages Terraform as a structured representation of reality. Future versions may add direct Azure API integration for resources not managed by Terraform. Terraform is used as a structured, quarriable representation of implemented state, not only as a deployment tool.
**End-to-End Example: Identity / PAW / Conditional Access**
Scenario: An organization implements a Zero Trust privileged access model using Privileged Access Workstations (PAW), Conditional Access (CA), and Entra ID roles.
Risk: Privilege escalation via compromised administrator endpoint.
Control Objective: Ensure privileged access originates only from trusted and managed devices.
Control: Privileged Access Workstation (PAW). Supporting controls include Conditional Access enforcement, device compliance enforcement, and Privileged Identity Management (PIM).
Constraints: Administrative roles must require compliant devices, access from non-managed devices must be blocked, and privileged roles must be activated via PIM.
Architecture model representation, in simplified form, can be viewed as Risk to Control to Constraint to Implementation to Signal.
Implementation mapping includes Intune for device compliance, Conditional Access policies for access enforcement, Entra ID role assignment, and PIM for just-in-time privilege elevation.
Enforcement can start as soft enforcement, such as detecting users assigned admin roles without PIM or detecting missing Conditional Access policies. It can later evolve into hard enforcement such as denying role assignment without PIM or denying sign-in from non-compliant devices.
Signals and verification include Entra ID sign-in logs, Conditional Access logs, and Defender alerts. Drift detection would identify cases such as direct role assignment instead of PIM or a disabled Conditional Access policy.
From Example to Canonical Encoding
The example above can be encoded in a structured format (YAML with schema validation). A simplified illustration:
risk:
  id: "R-001"
  name: "Privilege escalation via compromised admin endpoint"
  description: "..."
  control_objective: "Ensure privileged access originates only from trusted and managed devices"
control:
  id: "C-001"
  name: "Privileged Access Workstation (PAW)"
  type: "TechnicalControl"
  constraints:
    - id: "CON-001"
      description: "Admin roles require compliant devices"
    - id: "CON-002"
      description: "Access from non-managed devices must be blocked"
implementation_mapping:
  - control_id: "C-001"
    resource_type: "azurerm_windows_virtual_machine"
    tags:
      role: "PAW"
  - control_id: "C-001"
    resource_type: "azurerm_conditional_access_policy"
    parameters:
      grant_controls: ["requireCompliantDevice"]
signal:
  - source: "Entra ID sign-in logs"
  - source: "Conditional Access logs"
  - source: "Defender alerts"
This encoding is not intended for direct human reading. It is the canonical source from which documents, IaC skeletons, and coverage reports are generated.
**Scope Definition for Initial Implementation**
To ensure feasibility and maintain momentum, the initial implementation scope is intentionally limited.
The first version of the system will include only Terraform-manageable components:
Included:
•	Azure resources
•	Azure Policy
•	Management groups
•	RBAC
•	Core security controls
Excluded (modeled but not automated):
•	Conditional Access
•	PIM
•	Entitlement Management
•	Graph API configurations
•	Microsoft 365 security
The following areas are explicitly out of scope for the initial implementation: Microsoft Entra ID advanced capabilities such as Conditional Access, PIM, and Entitlement Management; Microsoft Graph API-dependent configurations; and Microsoft 365 security configurations such as Purview and Defender for Office.
These elements should still be represented in the architecture model, but marked as external_control, manual_implementation_required, or not_yet_automated. This allows the model to remain broader than the first execution layer without forcing early implementation complexity.
The initial implementation will focus on consistency checking (model ↔ Terraform) before adding full IaC generation. Generating a Terraform skeleton from the model is a secondary goal. The primary value proposition is detecting drift and ensuring architectural intent is reflected in implementation. This ordering reduces risk and delivers working validation earlier.
**Relationship with Existing Microsoft Capabilities**
The concept does not attempt to replace existing Microsoft security and governance tools, but rather to integrate and extend them.
Azure Policy already provides enforcement and compliance evaluation. Microsoft Defender for Cloud already provides posture assessment and recommendations. Microsoft Cloud Security Benchmark provides structured mappings of security controls. Regulatory compliance initiatives such as ISO 27001 and NIST already exist as policy sets.
These tools provide control definitions, compliance evaluation, and recommendations. They do not provide architectural intent, decision rationale, traceability from risk to implementation, or a unified model linking architecture to IaC.
The proposed solution therefore introduces a higher-level architecture layer that references existing controls, maps them to requirements and constraints, connects them to implementation through Terraform, and provides traceability across risk, control, constraint, implementation, and validation. Instead of duplicating functionality, the system acts as an orchestrator and model layer above existing tools.
**Integration Strategy**
The initial implementation path is Architecture Model to Terraform as the primary execution layer to Azure Policy and Defender for Cloud as enforcement and validation layers.
A future extension may introduce Microsoft Graph or other APIs for identity and governance domains that are not yet automated. This phased approach enables early validation of the core concept while keeping the initial implementation realistic.
**Strategic Value**
By leveraging existing Microsoft capabilities and focusing on the missing architectural layer, the solution avoids duplication of existing tooling, enhances visibility and traceability, bridges the gap between design and implementation, and creates a path toward a broader multi-cloud architecture model.
Cross-organizational architecture handover. When AaC delivers an architecture to a client, the client receives not only documents but also the canonical model (or a profile-rendered view). The client can continue evolving the architecture in their own tooling, or re-import future changes from AaC. The model becomes a transferable asset, not a static deliverable.
Subcontractor integration. A security specialist receives only the security profile of the model. After completing their work, they return updates (in the same canonical format or a subset). The system merges these updates into the master model without manual re-entry.
Methodological independence. The same architecture can be rendered as TOGAF architecture for an enterprise architect, as CAF architecture for a cloud governance lead, and as Company internal HLD for the delivery team — all from one model. This breaks the current lock-in where choosing a methodology forces a specific document template.
**Non-goals**
•	Not a replacement for Azure Policy or Defender
•	Not a full compliance platform
•	Not a full IaC generator (initially)
•	Not tied to a single vendor or framework
**Conclusion**
This concept proposes a shift from architecture as static documentation to architecture as a living, structured, and executable model.
The initial scope is deliberately constrained to maximize execution success. Existing Microsoft tools are treated as foundational building blocks, while the proposed solution adds the missing architectural intelligence layer that connects intent, control, and implementation.
The long-term value of the system lies not only in traceability to IaC, but also in the ability to preserve one canonical architecture while rendering it through different organizational or methodological views without losing meaning or silently omitting important parts of the architecture.
The long-term ambition is not only to generate documents and validate IaC, but to establish a portable, vendor-neutral, methodology-agnostic format for architectural knowledge. The initial implementation is deliberately constrained to Azure, Terraform, and security domain. But the model architecture — canonical representation, profile-based rendering, coverage control, and two-way consistency — is designed to extend. This proposal is a starting point, not a final specification.
