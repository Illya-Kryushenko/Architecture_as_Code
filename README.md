# Architecture as Code (AaC)
Structured architecture models linked to CAF, Zero Trust, and Infrastructure as Code

## Overview

This repository captures the initial concept of transforming architecture from static documentation into a structured, traceable, and partially executable model.

The current starting point is Microsoft Cloud Adoption Framework (CAF) and Zero Trust guidance. The core idea is to transform architectural guidance into machine-readable templates that can be linked to architecture models, Infrastructure as Code, validation, and drift detection.

The initial focus is Security Architecture, where the structure is stronger and the relationships between risk, control, and implementation are clearer.

## Problem

Modern cloud environments have a structural gap between:

- architectural intent
- architectural guidance
- implementation in IaC
- deployed reality

Architecture documents explain intent, but become outdated.
IaC accurately describes implementation, but does not explain why the system is built this way.

As a result, organizations struggle with:

- architectural drift
- weak traceability
- poor alignment between decisions and implementation
- manual and inconsistent validation of architecture

## Core Idea

The proposed model introduces an architecture layer that sits above IaC and connects:

- guidance
- constraints
- requirements
- architecture decisions
- implementation mappings
- validation rules

The long-term direction is to move from architecture as static text to architecture as a living, structured, and verifiable model.

## Initial Direction

The first practical scope is:

- CAF and Zero Trust as executable templates
- Security Architecture as the first implementation domain
- human-readable architecture documents generated from a structured model
- support for both canonical architecture data and human commentary
- validation against IaC and deployed state (working prototype: resource existence check)

## Guiding Principles

- The architecture model is the primary source of truth
- Human-readable documents are generated views of the model
- Structured content defines architecture
- Commentary explains architecture
- Commentary must not replace canonical architectural facts

## Specification

The AaC model specification is in [`docs/architecture-model.md`](docs/architecture-model.md).

- [Example architecture model](examples/basic-model.yaml) – defines the structure of the architecture model
- [Example model](examples/basic-model.yaml) – illustrates risks, controls, and implementation mappings
- [Terraform state example](examples/example.tfstate) – used for validation

The specification is versioned and open to change based on community feedback.

## Call to Action

We invite everyone to:

1. **Try the prototype** – clone, run against your Terraform state
2. **Open issues** – what works, what doesn't, what's missing
3. **Propose changes** to the model schema (`/specification/v1/`)
4. **Contribute code** – validator, Terraform parser, document generator, Azure API integration
5. **Adopt AaC** in your projects (even as an experiment)

This project aims to become an **Open Standard** for Architecture as Code, not a vendor-specific tool. We want to build a community around it.

All contributions are welcome: docs, examples, code, use cases.

## Repository Scope

This repository currently contains:

- concept notes
- initial ADRs
- evolving structure for an Architecture as Code model
- **working prototype** (validator)
- **minimal specification** v1 (JSON schema)

## Status

**Working prototype** – the validator can:
- Parse an AaC model (YAML)
- Parse a Terraform state file (JSON)
- Check that resources defined in the model exist in the state
- Output PASS/FAIL for each control

See [`examples/basic-model.yaml`](examples/basic-model.yaml) and run:
```bash
PYTHONPATH=. python -m aac.cli --model examples/basic-model.yaml --state examples/example.tfstate
```

## Scope (Initial Version)

This project focuses on architecture modeling and Terraform-based implementation.

Out of scope for the initial version:
- Identity governance (PIM, Conditional Access)
- Microsoft Graph-based configurations
- Full Microsoft 365 security integration

These areas are modeled but not automated.

- Supports multiple representation profiles (future capability)
- Includes architecture coverage validation (planned)

## Contributing

We follow the **Open Standard** model, not a single-vendor roadmap.

To contribute:
1. Open an issue to discuss the change
2. Fork the repository
3. Submit a pull request

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details (coming soon).
