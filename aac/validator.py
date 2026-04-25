import json
from .model import ArchitectureModel

def check_resource_matches_mapping(resource, mapping):
    """
    Checks if a resource from Terraform state matches a single implementation mapping.
    Returns (is_match, error_message).
    """
    # 1. Check resource type
    if resource.get("type") != mapping.resource_type:
        return False, f"resource type mismatch: expected '{mapping.resource_type}', got '{resource.get('type')}'"

    # 2. Check tags (if specified in the model)
    if mapping.tags:
        tags = resource.get("tags", {})
        for key, expected_value in mapping.tags.items():
            actual_value = tags.get(key)
            if actual_value != expected_value:
                return False, f"tag '{key}' expected '{expected_value}', got '{actual_value}'"

    # 3. Check parameters (if specified in the model) — placeholder for future logic
    if mapping.parameters:
        # TODO: recursive parameter validation
        pass

    return True, "ok"

def check_model_against_terraform_state(model: ArchitectureModel, state_path: str) -> bool:
    """
    Validates an architecture model against a Terraform state file.
    Returns True if all requirements are met, False otherwise.
    """
    with open(state_path) as f:
        state = json.load(f)

    # Collect all resources from the state into a flat list
    all_resources = []
    for resource in state.get("resources", []):
        for instance in resource.get("instances", []):
            all_resources.append({
                "type": resource["type"],
                "name": resource.get("name", ""),
                "attributes": instance.get("attributes", {}),
                "tags": instance.get("attributes", {}).get("tags", {})
            })

    all_passed = True

    # Check each implementation mapping against available resources
    for mapping in model.implementation_mapping:
        found = False
        for res in all_resources:
            matches, msg = check_resource_matches_mapping(res, mapping)
            if matches:
                found = True
                print(f"PASS: {mapping.control_id} -> {mapping.resource_type} found")
                break
            # If type doesn't match, skip silently — keep looking
            if "resource type mismatch" in msg:
                continue
            # Type matched but tag/parameter validation failed
            print(f"FAIL: {mapping.control_id} -> {mapping.resource_type} exists but {msg}")
            all_passed = False
            found = True  # We found a resource of the correct type, but it failed the checks
            break

        if not found:
            print(f"FAIL: {mapping.control_id} expects {mapping.resource_type}, but none found")
            all_passed = False

    return all_passed