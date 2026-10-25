"""Tools for integrating Friedmann expansion equations and evaluating horizon conditions."""

from typing import Dict, Any, List
from cosmology_lab.models.lcdm import StandardLCDM
from cosmology_lab.models.black_hole_universe import BlackHoleUniverse

def solve_cosmic_expansion(
    model_type: str = "black_hole",
    h0: float = 70.0,
    omega_m: float = 0.315,
    omega_lambda: float = 0.685,
    a_star: float = 0.68,
    redshifts: List[float] = None
) -> Dict[str, Any]:
    """Solve cosmic expansion dynamics H(z), cosmic age t(z), lookback time, and Schwarzschild-Hubble horizon.
    
    Args:
        model_type: 'lcdm' or 'black_hole'
        h0: Hubble constant (km/s/Mpc)
        omega_m: Matter density parameter
        omega_lambda: Dark energy parameter
        a_star: Dimensionless Kerr spin (for black_hole model)
        redshifts: List of redshifts to evaluate (e.g. [0.0, 1.98, 14.44])
    
    Returns:
        Expansion metrics, cosmic ages, and horizon identity evaluation.
    """
    if redshifts is None:
        redshifts = [0.0, 0.65, 1.48, 1.98, 2.85, 6.0, 14.44, 1100.0]
    
    if model_type.lower() == "lcdm":
        model = StandardLCDM(h0=h0, omega_m=omega_m, omega_lambda=omega_lambda)
        horizon_info = {
            "model": "Standard Lambda-CDM",
            "interpretation": "Infinite expanding flat FLRW metric. Horizon equality R_s = R_H regarded as coincidence."
        }
    else:
        model = BlackHoleUniverse(h0=h0, omega_m=omega_m, omega_lambda=omega_lambda, a_star=a_star)
        horizon_info = model.hubble_schwarzschild_identity()
    
    results = []
    for z in sorted(redshifts):
        results.append({
            "redshift_z": z,
            "h_z_kms_mpc": round(model.h_z(z), 2),
            "lookback_time_gyr": round(model.lookback_time_gyr(z), 3),
            "cosmic_age_gyr": round(model.cosmic_age_gyr(z), 4),
            "comoving_distance_mpc": round(model.comoving_distance_mpc(z), 1) if hasattr(model, "comoving_distance_mpc") else None
        })
    
    total_age = model.cosmic_age_gyr(0.0)
    
    return {
        "model_name": model.name,
        "parameters": {
            "h0": h0,
            "omega_m": omega_m,
            "omega_lambda": omega_lambda,
            "a_star": a_star if model_type.lower() != "lcdm" else None
        },
        "age_of_universe_now_gyr": round(total_age, 3),
        "horizon_evaluation": horizon_info,
        "epoch_grid": results
    }
