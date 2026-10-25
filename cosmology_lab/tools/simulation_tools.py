"""Tools for exporting validated cosmological parameters and trajectory keyframes to Three.js."""

import json
import os
from typing import Dict, Any, List

DEFAULT_OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "simulation",
    "data",
    "universe_state.json"
)

def export_simulation_state(
    a_star: float = 0.68,
    xi_seed: float = 2.45,
    h0: float = 70.0,
    output_path: str = DEFAULT_OUTPUT_PATH
) -> Dict[str, Any]:
    """Compile and export the complete 6-epoch cosmological trajectory for the Three.js 3D simulation.
    
    Args:
        a_star: Parent Kerr black hole spin parameter
        xi_seed: Primordial torsion seed boost factor
        h0: Hubble constant (km/s/Mpc)
        output_path: Target JSON filepath for Three.js engine
    
    Returns:
        Compilation status, file path, and summary of exported keyframes.
    """
    state = {
        "metadata": {
            "title": "Cosmological Evolution: From Black Hole Bounce to Modern Humans",
            "benchmark": "CosmologyLabBench - Argon Laboratory RL Environment",
            "model_type": "Kerr-Einstein-Cartan Black Hole Universe",
            "parameters": {
                "h0": h0,
                "a_star": a_star,
                "xi_seed": xi_seed,
                "ratio_rs_over_rh": 1.000,
                "omega_tot": 1.0
            }
        },
        "epochs": [
            {
                "id": 0,
                "name": "Kerr Black Hole Interior & Torsion Bounce",
                "redshift_z": 1e9,
                "cosmic_time_gyr": 0.0,
                "time_display": "t = 0 s (Singularity Averted by Torsion)",
                "description": "The universe originates not from an infinite mathematical singularity, but from an Einstein-Cartan spin-torsion bounce inside a parent rotating Kerr black hole. Relic frame-dragging vorticity establishes the cosmic spin axis.",
                "visual_theme": "singularity_bounce",
                "color_palette": ["#ff2200", "#ffaa00", "#ffffff"],
                "particle_vorticity": a_star * 2.5,
                "boundary_radius_gly": 13.97,
                "key_physics": {
                    "torsion_density_scale": "rho_EC ~ 10^52 g/cm^3",
                    "repulsive_spin_coupling": True,
                    "parent_bh_spin": a_star
                }
            },
            {
                "id": 1,
                "name": "Cosmic Dawn & Recombination",
                "redshift_z": 1100.0,
                "cosmic_time_gyr": 0.00038,
                "time_display": "t = 380,000 yr (CMB) to 100 Myr",
                "description": "Protons and electrons combine to form neutral hydrogen, releasing the Cosmic Microwave Background. Neutral fog envelops the cosmos until the first Pop III stars ignite the cosmic dawn.",
                "visual_theme": "cosmic_dawn",
                "color_palette": ["#ff8844", "#331100", "#112244"],
                "particle_vorticity": a_star * 1.8,
                "key_physics": {
                    "temperature_kelvin": 3000.0,
                    "first_stars": "Population III metal-free hypergiants"
                }
            },
            {
                "id": 2,
                "name": "MoM-z14: Mother of Miracles",
                "redshift_z": 14.44,
                "cosmic_time_gyr": 0.280,
                "time_display": "t = 280 Myr post-Big Bang (z = 14.44)",
                "description": "JWST discovery of MoM-z14: An ultra-compact (re = 74 pc), fiercely luminous (M_UV = -20.2) galaxy enriched in nitrogen. Seeded by accelerated torsion fluctuations, defying standard gradual Lambda-CDM assembly.",
                "visual_theme": "mom_z14_galaxy",
                "color_palette": ["#4488ff", "#00ffff", "#ffffff"],
                "particle_vorticity": a_star * 1.4,
                "key_physics": {
                    "radius_pc": 74.0,
                    "absolute_mag_m_uv": -20.2,
                    "stellar_mass_solar": 1.0e8,
                    "uvlf_excess_factor": 160.0
                }
            },
            {
                "id": 3,
                "name": "JADES Era & Galaxy Spin Alignment",
                "redshift_z": 2.85,
                "cosmic_time_gyr": 2.3,
                "time_display": "t = 2.3 Gyr (z ~ 2.85, JADES GOODS-S)",
                "description": "Spiral galaxies condense along cosmic filaments. Frame-dragging vorticity from the parent Kerr black hole biases tidal torques, creating a 60:40 clockwise spin asymmetry (158 CW vs 105 CCW).",
                "visual_theme": "jades_spirals",
                "color_palette": ["#8855ff", "#aa77ff", "#ffffff"],
                "particle_vorticity": a_star * 1.0,
                "key_physics": {
                    "cw_count": 158,
                    "ccw_count": 105,
                    "asymmetry_A": 0.2015,
                    "binomial_p_value": 0.00062
                }
            },
            {
                "id": 4,
                "name": "XLSSC 122: Strong Gravitational Lensing",
                "redshift_z": 1.98,
                "cosmic_time_gyr": 3.38,
                "time_display": "t = 3.38 Gyr (Cosmic Noon, z = 1.98)",
                "description": "XLSSC 122: The most distant strong-lensing galaxy cluster known. Its hyper-concentrated dark matter core (c_200 = 6.3) creates giant blue arcs and mature intracluster light, confirming accelerated early structure growth.",
                "visual_theme": "xlssc122_lensing",
                "color_palette": ["#00aaff", "#ffffff", "#ffaa33"],
                "particle_vorticity": a_star * 0.7,
                "key_physics": {
                    "m_200_solar": 3.0e14,
                    "c_200_concentration": 6.3,
                    "einstein_radius_arcsec": 4.1,
                    "giant_arcs": 3
                }
            },
            {
                "id": 5,
                "name": "Modern Universe, Solar System & Humanity",
                "redshift_z": 0.0,
                "cosmic_time_gyr": 13.8,
                "time_display": "t = 13.8 Gyr (Present Day, z = 0)",
                "description": "The cosmic web expands towards the Hubble horizon (R_H = R_s). In an unassuming spiral arm of the Milky Way, the Solar System and Earth harbor intelligent life capable of deciphering their own black hole origin.",
                "visual_theme": "modern_universe_earth",
                "color_palette": ["#2266ff", "#22bb66", "#ffffff"],
                "particle_vorticity": a_star * 0.3,
                "key_physics": {
                    "hubble_radius_gly": 13.97,
                    "milky_way_mass_solar": 1.5e12,
                    "earth_age_gyr": 4.54,
                    "human_civilization": True
                }
            }
        ]
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    
    return {
        "status": "success",
        "output_path": output_path,
        "n_epochs": len(state["epochs"]),
        "parameters_injected": state["metadata"]["parameters"]
    }
