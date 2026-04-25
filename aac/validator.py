import json
from .model import ArchitectureModel

def get_nested_attr(obj, path):
    """
    Helper to access nested dictionary keys using dot notation (e.g., 'settings.tls_version').
    """
    for key in path.split('.'):
        if isinstance(obj, dict):
            obj = obj.get(key)
        else:
            return None
    return obj

def check_resource_matches_mapping(resource, mapping):
    """
    Checks if a resource from Terraform state matches a single implementation mapping.
    Returns (is_match, error_message).
    """
    # 1. Check resource type
    if resource.get("type") != mapping.resource_type:
        return False, "type mismatch"

    # 2. Check tags (if specified in the model)
    if mapping.tags:
        tags = resource.get("tags", {})
        for key, expected_value in mapping.tags.items():
            if tags.get(key) != expected_value:
                return False, f"tag '{key}' mismatch: expected '{expected_value}', got '{tags.get(key)}'"

    # 3. Check parameters (Recursive validation)
    if mapping.parameters:
        attributes = resource.get("attributes", {})
        for param_path, expected_value in mapping.parameters.items():
            actual_value = get_nested_attr(attributes, param_path)
            if actual_value != expected_value:
                return False, f"param '{param_path}' mismatch: expected {expected_value}, got {actual_value}"

    return True, "ok"

def check_model_against_terraform_state(model: ArchitectureModel, state_path: str) -> bool:
    """
    Validates an architecture model against a Terraform state file.
    Also provides a summary of risk coverage.
    """
    with open(state_path) as f:
        state = json.load(f)

    # Flatten resources from state for easier lookup
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
    covered_control_ids = set()

    print("--- Mapping Validation ---")
    for mapping in model.implementation_mapping:
        found = False
        for res in all_resources:
            matches, msg = check_resource_matches_mapping(res, mapping)
            if matches:
                found = True
                covered_control_ids.add(mapping.control_id)
                print(f"✅ PASS: {mapping.control_id} -> {res['name']} ({mapping.resource_type})")
                break
            
            # If type matches but validation fails, report error and stop searching for this mapping
            if msg != "type mismatch":
                print(f"❌ FAIL: {mapping.control_id} found resource '{res['name']}', but {msg}")
                all_passed = False
                found = True
                break

        if not found:
            print(f"⚠️  MISSING: {mapping.control_id} (no resource of type {mapping.resource_type} found)")
            all_passed = False

    # Risk Coverage Analysis
    print("\n--- Risk Coverage Analysis ---")
    for risk in model.risks:
        # Check if any control associated with this risk (by ID) is covered
        # Note: You can expand this logic if you add a 'controls' list to the Risk dataclass
        is_covered = any(ctrl.id in covered_control_ids for ctrl in model.controls if ctrl.id == risk.id or risk.id in covered_control_ids)
        
        status = "🛡️  COVERED" if is_covered else "🚨 EXPOSED"
        print(f"{status} | Risk '{risk.name}' (ID: {risk.id})")

    return all_passed