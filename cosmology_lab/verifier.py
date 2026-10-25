"""Scientific verification suite for cosmological parameters and Three.js 3D simulation artifacts."""

import os
import json
from typing import Dict, Any, List

class ScientificVerifier:
    """Verifies that research conclusions and simulation artifacts satisfy astrophysical constraints."""

    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.simulation_json_path = os.path.join(self.workspace_root, "simulation", "data", "universe_state.json")
        self.simulation_html_path = os.path.join(self.workspace_root, "simulation", "index.html")

    def verify_black_hole_cosmology_consistency(self, a_star: float, xi_seed: float, h0: float = 70.0) -> Dict[str, Any]:
        """Verify that parameters stay within physical and observational bounds."""
        checks = []
        
        # 1. Kerr spin physical bound: 0.0 <= a_star < 1.0 (extremal limit)
        kerr_valid = 0.0 <= a_star < 1.0
        checks.append({
            "check": "kerr_spin_physical_bound",
            "condition": "0.0 <= a_star < 1.0",
            "passed": kerr_valid,
            "value": a_star
        })
        
        # 2. Primordial seed boost factor: 1.0 <= xi_seed <= 5.0
        seed_valid = 1.0 <= xi_seed <= 5.0
        checks.append({
            "check": "seed_enhancement_bound",
            "condition": "1.0 <= xi_seed <= 5.0",
            "passed": seed_valid,
            "value": xi_seed
        })
        
        # 3. Hubble constant realistic range: 60.0 <= H0 <= 80.0
        h0_valid = 60.0 <= h0 <= 80.0
        checks.append({
            "check": "hubble_constant_bound",
            "condition": "60.0 <= H0 <= 80.0",
            "passed": h0_valid,
            "value": h0
        })
        
        all_passed = all(c["passed"] for c in checks)
        return {
            "all_passed": all_passed,
            "checks": checks
        }

    def verify_threejs_simulation_artifacts(self) -> Dict[str, Any]:
        """Verify that Three.js simulation HTML, JavaScript, and data state are present and valid."""
        checks = []
        
        # 1. HTML file exists
        html_exists = os.path.exists(self.simulation_html_path)
        checks.append({
            "artifact": "simulation/index.html",
            "passed": html_exists
        })
        
        # 2. universe_state.json exists and contains 6 epochs
        json_valid = False
        epoch_count = 0
        if os.path.exists(self.simulation_json_path):
            try:
                with open(self.simulation_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                epochs = data.get("epochs", [])
                epoch_count = len(epochs)
                json_valid = (epoch_count == 6)
            except Exception:
                json_valid = False
                
        checks.append({
            "artifact": "simulation/data/universe_state.json",
            "epochs_found": epoch_count,
            "expected_epochs": 6,
            "passed": json_valid
        })
        
        # 3. Check specific epoch milestones: MoM-z14, XLSSC 122, JADES, Modern Humans
        milestones_found = []
        if json_valid:
            epoch_names = [e["name"].lower() for e in data.get("epochs", [])]
            for target in ["bounce", "mom-z14", "jades", "xlssc 122", "modern"]:
                if any(target in name for name in epoch_names):
                    milestones_found.append(target)
                    
        milestones_passed = len(milestones_found) >= 4
        checks.append({
            "milestone_verification": milestones_found,
            "passed": milestones_passed
        })
        
        all_passed = all(c["passed"] for c in checks)
        return {
            "all_passed": all_passed,
            "checks": checks
        }
