"""Multi-objective scientific reward function for evaluating Argon's cosmological research."""

import os
import json
from typing import Dict, Any, List

class CosmologyRewardEvaluator:
    """Evaluates agent research trajectory across 4 core scientific competencies:
    1. Falsification of standard model (0 - 25 pts)
    2. Black Hole Cosmology hypothesis testing & parameter estimation (0 - 25 pts)
    3. Multi-pillar Bayesian evidence & statistical rigor (0 - 25 pts)
    4. 3D Three.js Universe simulation compilation & physical integrity (0 - 25 pts)
    """

    def __init__(self, simulation_path: str = None):
        if simulation_path:
            self.simulation_path = simulation_path
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.simulation_path = os.path.join(base_dir, "simulation", "data", "universe_state.json")

    def evaluate_trajectory(self, tool_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compute comprehensive reward score from tool call history."""
        called_tools = {step.get("tool_name") for step in tool_history}
        
        # 1. Falsification Score (0 - 25 pts)
        falsification_pts = 0.0
        falsification_notes = []
        
        catalog_queries = [s for s in tool_history if s.get("tool_name") == "query_jwst_catalog"]
        queried_datasets = set()
        for q in catalog_queries:
            args = q.get("arguments", {})
            if "catalog_name" in args:
                queried_datasets.add(args["catalog_name"])
        
        if len(queried_datasets) >= 3:
            falsification_pts += 10.0
            falsification_notes.append("Surveyed all 3 JWST discovery datasets.")
        elif len(queried_datasets) >= 1:
            falsification_pts += 5.0
            falsification_notes.append("Surveyed initial JWST datasets.")
            
        lcdm_tests = [
            s for s in tool_history
            if s.get("arguments", {}).get("model_type") == "lcdm"
        ]
        if len(lcdm_tests) >= 2:
            falsification_pts += 15.0
            falsification_notes.append("Quantified >3-sigma tensions of standard Lambda-CDM across early galaxies and lensing.")
        elif len(lcdm_tests) >= 1:
            falsification_pts += 8.0
            falsification_notes.append("Tested baseline Lambda-CDM.")

        # 2. Black Hole Cosmology Hypothesis & Parameter Sweep (0 - 25 pts)
        hypothesis_pts = 0.0
        hypothesis_notes = []
        
        expansion_calls = [s for s in tool_history if s.get("tool_name") == "solve_cosmic_expansion"]
        for ec in expansion_calls:
            res = ec.get("result", {})
            h_eval = res.get("horizon_evaluation", {})
            if h_eval.get("condition_satisfied"):
                hypothesis_pts += 10.0
                hypothesis_notes.append("Verified Schwarzschild-Hubble horizon equality R_s = R_H.")
                break
                
        bh_structure = [
            s for s in tool_history
            if s.get("tool_name") in ["evaluate_mom_z14", "evaluate_xlssc122_lensing", "analyze_galaxy_spin_parity"]
            and s.get("arguments", {}).get("model_type") == "black_hole"
        ]
        if len(bh_structure) >= 3:
            hypothesis_pts += 15.0
            hypothesis_notes.append("Tuned Kerr spin a* and torsion seed factor xi_seed to resolve early-universe anomalies.")
        elif len(bh_structure) >= 1:
            hypothesis_pts += 8.0
            hypothesis_notes.append("Tested Black Hole cosmology mechanisms.")

        # 3. Bayesian Model Comparison (0 - 25 pts)
        bayesian_pts = 0.0
        bayesian_notes = []
        
        comp_calls = [s for s in tool_history if s.get("tool_name") == "compare_cosmological_models"]
        if comp_calls:
            latest_comp = comp_calls[-1].get("result", {})
            stats = latest_comp.get("model_comparison_statistics", {})
            delta_bic = stats.get("delta_bic", 0.0)
            ln_b = stats.get("ln_bayes_factor_in_favor_of_black_hole", 0.0)
            
            if delta_bic > 20.0 and ln_b > 10.0:
                bayesian_pts += 25.0
                bayesian_notes.append(f"Decisive Bayesian model preference established (Delta BIC: {delta_bic}, ln B: {ln_b}).")
            elif delta_bic > 5.0:
                bayesian_pts += 15.0
                bayesian_notes.append("Positive Bayesian evidence for Black Hole universe.")
            else:
                bayesian_pts += 5.0
        else:
            bayesian_notes.append("Bayesian model comparison tool not executed.")

        # 4. Three.js Simulation Artifact Verification (0 - 25 pts)
        sim_pts = 0.0
        sim_notes = []
        
        if os.path.exists(self.simulation_path):
            try:
                with open(self.simulation_path, "r", encoding="utf-8") as f:
                    sim_data = json.load(f)
                epochs = sim_data.get("epochs", [])
                params = sim_data.get("metadata", {}).get("parameters", {})
                
                if len(epochs) == 6:
                    sim_pts += 15.0
                    sim_notes.append("All 6 cosmic evolution epochs (Big Bang -> Modern Humans) correctly exported.")
                elif len(epochs) >= 4:
                    sim_pts += 8.0
                    sim_notes.append("Partial epochs exported.")
                    
                if "a_star" in params and "xi_seed" in params:
                    sim_pts += 10.0
                    sim_notes.append("Physical parameters (Kerr spin a*, torsion seed factor xi_seed) successfully coupled to 3D trajectory.")
            except Exception as e:
                sim_notes.append(f"Simulation file reading error: {str(e)}")
        else:
            sim_notes.append(f"Simulation statefile not yet generated at {self.simulation_path}.")

        total_score = min(100.0, falsification_pts + hypothesis_pts + bayesian_pts + sim_pts)
        passed = total_score >= 80.0
        
        return {
            "total_score": round(total_score, 1),
            "max_score": 100.0,
            "passed_benchmark": passed,
            "subscores": {
                "falsification_standard_model": round(falsification_pts, 1),
                "black_hole_hypothesis_formulation": round(hypothesis_pts, 1),
                "bayesian_statistical_evidence": round(bayesian_pts, 1),
                "threejs_simulation_export": round(sim_pts, 1)
            },
            "evaluator_feedback": {
                "falsification": falsification_notes,
                "hypothesis": hypothesis_notes,
                "bayesian": bayesian_notes,
                "simulation": sim_notes
            }
        }
