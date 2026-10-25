"""Gymnasium-compatible Reinforcement Learning Environment for Argon Cosmological Research."""

import json
from typing import Dict, Any, List, Tuple, Optional
from cosmology_lab.tools.registry import dispatch_tool, OPENAI_TOOL_SCHEMAS, TOOL_REGISTRY
from cosmology_lab.reward import CosmologyRewardEvaluator

class CosmologyLabEnv:
    """Astrophysical Dry Laboratory RL Environment.
    
    Argon (or any RL agent) is dropped into this environment to investigate whether
    our universe is inside a black hole, starting from recent JWST observational anomalies.
    
    Argon interacts by querying observational catalogs, testing mathematical models,
    fitting parameters (Kerr spin a*, torsion seed factor xi_seed), comparing Bayesian
    evidence against standard Lambda-CDM, and compiling a 3D Three.js universe evolution simulation.
    """

    def __init__(self, max_steps: int = 25):
        self.max_steps = max_steps
        self.reward_evaluator = CosmologyRewardEvaluator()
        self.current_step = 0
        self.tool_history: List[Dict[str, Any]] = []
        self.hypotheses_tested: List[str] = []
        self.done = False

    def reset(self, seed: Optional[int] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Reset the environment to the initial laboratory state."""
        self.current_step = 0
        self.tool_history = []
        self.hypotheses_tested = []
        self.done = False
        
        initial_obs = {
            "mission": "Astrophysical Investigation: Is our Universe the Interior of a Black Hole?",
            "observational_context": (
                "Recent JWST observations reveal multiple cosmological anomalies that directly challenge "
                "standard Lambda-CDM: (1) XLSSC 122 at z=1.98 with a hyper-concentrated dark matter core (c200=6.3); "
                "(2) MoM-z14 at z=14.44 (280 Myr post-Big Bang) with extreme UV luminosity (M_UV=-20.2) and nitrogen enrichment; "
                "(3) JADES GOODS-S spiral galaxy spin distribution showing a 60:40 parity asymmetry (158 CW vs 105 CCW). "
                "Your objective is to conduct rigorous astrophysical research using your laboratory tools, determine if "
                "a Kerr-Einstein-Cartan Black Hole Bounce model explains these phenomena, and compile a 3D simulation of "
                "the universe's evolution from the Big Bang to modern humans."
            ),
            "available_tools": [s["function"]["name"] for s in OPENAI_TOOL_SCHEMAS],
            "step": 0,
            "max_steps": self.max_steps
        }
        info = {
            "status": "ready",
            "tool_schemas": OPENAI_TOOL_SCHEMAS
        }
        return initial_obs, info

    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, bool, Dict[str, Any]]:
        """Execute one tool action in the laboratory bench.
        
        Action formats supported:
        1. {"tool_name": "query_jwst_catalog", "arguments": {"catalog_name": "xlssc122_lensing"}}
        2. {"name": "query_jwst_catalog", "parameters": {...}}  (OpenAI tool call format)
        """
        self.current_step += 1
        
        tool_name = action.get("tool_name") or action.get("name")
        arguments = action.get("arguments") or action.get("parameters") or {}
        
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except Exception:
                arguments = {}
                
        # Execute tool
        result = dispatch_tool(tool_name, arguments)
        
        step_record = {
            "step": self.current_step,
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result
        }
        self.tool_history.append(step_record)
        
        # Track hypotheses
        if "model_type" in arguments:
            m_type = arguments["model_type"]
            if m_type not in self.hypotheses_tested:
                self.hypotheses_tested.append(m_type)
        
        # Calculate intermediate reward
        eval_result = self.reward_evaluator.evaluate_trajectory(self.tool_history)
        step_reward = eval_result["total_score"]
        
        # Termination conditions
        terminated = False
        truncated = False
        
        # Successful completion if agent reached >= 80% and exported the simulation
        if eval_result["passed_benchmark"] and any(s["tool_name"] == "export_simulation_state" for s in self.tool_history):
            terminated = True
            
        if self.current_step >= self.max_steps:
            truncated = True
            
        self.done = terminated or truncated
        
        obs = {
            "step": self.current_step,
            "latest_tool": tool_name,
            "result": result,
            "current_score": eval_result["total_score"],
            "done": self.done
        }
        
        info = {
            "evaluation": eval_result,
            "hypotheses_tested": self.hypotheses_tested,
            "steps_remaining": max(0, self.max_steps - self.current_step)
        }
        
        return obs, step_reward, terminated, truncated, info

    def evaluate_submission(self) -> Dict[str, Any]:
        """Final grading of agent research trajectory."""
        return self.reward_evaluator.evaluate_trajectory(self.tool_history)

    def render(self, mode: str = "human") -> str:
        """Render text summary of laboratory status."""
        eval_result = self.reward_evaluator.evaluate_trajectory(self.tool_history)
        lines = [
            "=" * 60,
            f"COSMOLOGY LAB BENCH — STEP {self.current_step}/{self.max_steps}",
            f"Total Research Score: {eval_result['total_score']} / 100.0 (Passed: {eval_result['passed_benchmark']})",
            "-" * 60,
            f"  * Falsification of Standard Model:     {eval_result['subscores']['falsification_standard_model']} / 25",
            f"  * Black Hole Hypothesis Formulation:    {eval_result['subscores']['black_hole_hypothesis_formulation']} / 25",
            f"  * Bayesian Model Evidence:             {eval_result['subscores']['bayesian_statistical_evidence']} / 25",
            f"  * Three.js 3D Simulation Export:       {eval_result['subscores']['threejs_simulation_export']} / 25",
            "-" * 60,
            f"Tools Called: {[s['tool_name'] for s in self.tool_history]}",
            "=" * 60
        ]
        output = "\n".join(lines)
        if mode == "human":
            print(output)
        return output
