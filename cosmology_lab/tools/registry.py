"""Tool registry providing OpenAI-compatible JSON schemas and dispatcher for Argon."""

from typing import Dict, Any, List, Callable
from cosmology_lab.tools.observation_tools import query_jwst_catalog, list_available_catalogs
from cosmology_lab.tools.expansion_tools import solve_cosmic_expansion
from cosmology_lab.tools.structure_tools import evaluate_mom_z14, evaluate_xlssc122_lensing
from cosmology_lab.tools.spin_tools import analyze_galaxy_spin_parity
from cosmology_lab.tools.comparison_tools import compare_cosmological_models
from cosmology_lab.tools.simulation_tools import export_simulation_state

TOOL_REGISTRY: Dict[str, Callable] = {
    "query_jwst_catalog": query_jwst_catalog,
    "solve_cosmic_expansion": solve_cosmic_expansion,
    "evaluate_mom_z14": evaluate_mom_z14,
    "evaluate_xlssc122_lensing": evaluate_xlssc122_lensing,
    "analyze_galaxy_spin_parity": analyze_galaxy_spin_parity,
    "compare_cosmological_models": compare_cosmological_models,
    "export_simulation_state": export_simulation_state
}

OPENAI_TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "query_jwst_catalog",
            "description": "Inspect real observational data from JWST and cosmological surveys (XLSSC 122 lensing, MoM-z14 spectroscopy, JADES galaxy spins, or cosmic chronometers).",
            "parameters": {
                "type": "object",
                "properties": {
                    "catalog_name": {
                        "type": "string",
                        "enum": ["xlssc122_lensing", "mom_z14_spectroscopy", "jades_galaxy_spins", "cosmic_chronometers"],
                        "description": "The name of the astronomical dataset to query."
                    },
                    "query_filter": {
                        "type": "string",
                        "description": "Optional key to extract a specific sub-dictionary."
                    }
                },
                "required": ["catalog_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "solve_cosmic_expansion",
            "description": "Integrate cosmic expansion equations, calculate age of the universe, and test the Hubble-Schwarzschild horizon identity (R_s = R_H).",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_type": {
                        "type": "string",
                        "enum": ["lcdm", "black_hole"],
                        "description": "Cosmological model to integrate."
                    },
                    "h0": {"type": "number", "description": "Hubble constant in km/s/Mpc (default: 70.0)"},
                    "a_star": {"type": "number", "description": "Dimensionless Kerr spin parameter in [0, 1) (default: 0.68)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_mom_z14",
            "description": "Evaluate UV luminosity function and early structure formation tension for galaxy MoM-z14 at z=14.44 (280 Myr post-Big Bang).",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_type": {"type": "string", "enum": ["lcdm", "black_hole"]},
                    "xi_seed": {"type": "number", "description": "Primordial seed density boost factor (default: 2.45)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_xlssc122_lensing",
            "description": "Evaluate strong gravitational lensing and dark matter concentration c_200 for cluster XLSSC 122 at z=1.98.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_type": {"type": "string", "enum": ["lcdm", "black_hole"]},
                    "xi_seed": {"type": "number", "description": "Primordial seed density boost factor (default: 2.45)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_galaxy_spin_parity",
            "description": "Analyze spiral galaxy spin distribution (clockwise vs counterclockwise) in JADES deep-field data and test Kerr frame-dragging vorticity hypothesis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_type": {"type": "string", "enum": ["lcdm", "black_hole"]},
                    "a_star": {"type": "number", "description": "Parent black hole spin parameter in [0, 1) (default: 0.68)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_cosmological_models",
            "description": "Execute comprehensive Bayesian model comparison (chi2, AIC, BIC, Bayes factor) across all 3 JWST discovery pillars.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a_star": {"type": "number", "description": "Parent black hole spin (default: 0.68)"},
                    "xi_seed": {"type": "number", "description": "Primordial seed boost factor (default: 2.45)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "export_simulation_state",
            "description": "Compile verified cosmological parameters and 6-epoch trajectory into the Three.js 3D universe evolution simulation engine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a_star": {"type": "number", "description": "Kerr spin parameter"},
                    "xi_seed": {"type": "number", "description": "Primordial seed boost"},
                    "h0": {"type": "number", "description": "Hubble constant"}
                }
            }
        }
    }
]

def dispatch_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a tool call by name with keyword arguments."""
    if tool_name not in TOOL_REGISTRY:
        return {"error": f"Tool '{tool_name}' not found. Available: {list(TOOL_REGISTRY.keys())}"}
    try:
        handler = TOOL_REGISTRY[tool_name]
        return handler(**arguments)
    except Exception as e:
        return {"error": f"Execution error in tool '{tool_name}': {str(e)}"}
