"""Tools for querying and inspecting JWST observational catalogs."""

import json
import os
from typing import Dict, Any, List

CATALOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "jwst_catalogs")

def list_available_catalogs() -> List[str]:
    """List all available astronomical datasets in the laboratory bench."""
    return [
        "xlssc122_lensing",
        "mom_z14_spectroscopy",
        "jades_galaxy_spins",
        "cosmic_chronometers"
    ]

def query_jwst_catalog(catalog_name: str, query_filter: str = "") -> Dict[str, Any]:
    """Query a specific JWST observation dataset.
    
    Args:
        catalog_name: One of 'xlssc122_lensing', 'mom_z14_spectroscopy', 'jades_galaxy_spins', 'cosmic_chronometers'
        query_filter: Optional section filter like 'observables', 'lcdm_predictions', 'sample_summary'
    
    Returns:
        JSON dataset content or filtered sub-tree.
    """
    valid_names = list_available_catalogs()
    if catalog_name not in valid_names:
        return {
            "error": f"Unknown catalog '{catalog_name}'. Available: {valid_names}"
        }
    
    filepath = os.path.join(CATALOG_DIR, f"{catalog_name}.json")
    if not os.path.exists(filepath):
        return {"error": f"Catalog file not found at {filepath}"}
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if query_filter and query_filter in data:
        return {query_filter: data[query_filter]}
    
    return data
