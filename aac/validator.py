import json
from .model import ArchitectureModel

def check_model_against_terraform_state(model: ArchitectureModel, state_path: str) -> bool:
    with open(state_path) as f:
        state = json.load(f)

    resources = {}
    for resource in state.get("resources", []):
        for instance in resource.get("instances", []):
            resource_type = resource["type"]
            resources[resource_type] = resources.get(resource_type, 0) + 1

    all_passed = True
    for mapping in model.implementation_mapping:
        expected_type = mapping.resource_type
        if expected_type not in resources:
            print(f"FAIL: {mapping.control_id} expects {expected_type}, but none found.")
            all_passed = False
        else:
            print(f"PASS: {mapping.control_id} -> {expected_type} found.")

    return all_passed