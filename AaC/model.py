from dataclasses import dataclass
from typing import List, Dict, Any
import yaml

@dataclass
class Risk:
    id: str
    name: str
    control_objective: str

@dataclass
class Control:
    id: str
    name: str
    control_type: str  # "TechnicalControl"
    constraints: List[Dict[str, str]]

@dataclass
class ImplementationMapping:
    control_id: str
    resource_type: str
    tags: Dict[str, str]
    parameters: Dict[str, Any]

@dataclass
class ArchitectureModel:
    risks: List[Risk]
    controls: List[Control]
    implementation_mapping: List[ImplementationMapping]

def load_model(path: str) -> ArchitectureModel:
    with open(path) as f:
        data = yaml.safe_load(f)
    # YAML ti dataclass (simplified)
    risks = [Risk(**r) for r in data.get("risks", [])]
    controls = [Control(**c) for c in data.get("controls", [])]
    mappings = [ImplementationMapping(**m) for m in data.get("implementation_mapping", [])]
    return ArchitectureModel(risks, controls, mappings)
