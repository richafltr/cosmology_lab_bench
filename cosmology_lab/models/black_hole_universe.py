"""Schwarzschild-Kerr Interior and Einstein-Cartan Torsion Bounce Cosmology model."""

import math
from typing import Dict, Any, List, Tuple
from cosmology_lab.constants import (
    C_LIGHT_SI,
    G_NEWTON_SI,
    KM_PER_MPC,
    SECONDS_PER_GYR,
    DEFAULT_H0,
    DEFAULT_OMEGA_M,
    DEFAULT_OMEGA_LAMBDA,
    critical_density_si,
    hubble_radius_si,
    schwarzschild_radius_si
)

class BlackHoleUniverse:
    """Cosmological model where our observable universe is the interior of a Kerr black hole
    formed via an Einstein-Cartan spin-torsion non-singular bounce.
    """

    def __init__(
        self,
        h0: float = DEFAULT_H0,
        omega_m: float = DEFAULT_OMEGA_M,
        omega_lambda: float = DEFAULT_OMEGA_LAMBDA,
        a_star: float = 0.68,
        xi_seed: float = 2.45,
        preferred_axis_ra: float = 168.0,
        preferred_axis_dec: float = -20.5
    ):
        self.name = "Kerr-Einstein-Cartan Black Hole Universe"
        self.h0 = h0
        self.omega_m = omega_m
        self.omega_lambda = omega_lambda
        self.omega_r = 8.4e-5
        self.omega_k = 1.0 - (self.omega_m + self.omega_lambda + self.omega_r)
        self.a_star = max(0.0, min(0.99, a_star))
        self.xi_seed = max(1.0, xi_seed)
        self.preferred_axis_ra = preferred_axis_ra
        self.preferred_axis_dec = preferred_axis_dec
        self.k_params = 6

    def hubble_schwarzschild_identity(self) -> Dict[str, float]:
        """Compute the ratio of Schwarzschild radius R_s to Hubble radius R_H."""
        r_h = hubble_radius_si(self.h0)
        rho_c = critical_density_si(self.h0)
        volume_hubble = (4.0 / 3.0) * math.pi * (r_h ** 3)
        mass_enclosed_kg = volume_hubble * rho_c
        r_s = schwarzschild_radius_si(mass_enclosed_kg)
        ratio = r_s / r_h
        return {
            "hubble_radius_meters": r_h,
            "hubble_radius_gly": r_h / (9.46073e15 * 1e9),
            "enclosed_critical_mass_kg": mass_enclosed_kg,
            "schwarzschild_radius_meters": r_s,
            "ratio_rs_over_rh": round(ratio, 5),
            "condition_satisfied": abs(ratio - 1.0) < 1e-4
        }

    def e_z(self, z: float) -> float:
        """Dimensionless expansion rate E(z) = H(z) / H0."""
        zp1 = 1.0 + z
        omega_rot = 1.2e-5 * (self.a_star ** 2)
        val = (
            (self.omega_r + omega_rot) * (zp1 ** 4)
            + self.omega_m * (zp1 ** 3)
            + self.omega_k * (zp1 ** 2)
            + self.omega_lambda
        )
        return math.sqrt(max(1e-12, val))

    def h_z(self, z: float) -> float:
        """Hubble parameter H(z) in km/s/Mpc."""
        return self.h0 * self.e_z(z)

    def _simpson_integral(self, f, a: float, b: float, n_steps: int = 500) -> float:
        if n_steps % 2 != 0:
            n_steps += 1
        h = (b - a) / n_steps
        s = f(a) + f(b)
        for i in range(1, n_steps):
            x = a + i * h
            s += 4.0 * f(x) if i % 2 == 1 else 2.0 * f(x)
        return s * (h / 3.0)

    def cosmic_age_gyr(self, z: float = 0.0) -> float:
        """Age of the universe at redshift z in Gyr integrating scale factor a."""
        a_target = 1.0 / (1.0 + z)
        if a_target <= 1e-6:
            return 0.0

        omega_rot = 1.2e-5 * (self.a_star ** 2)

        def integrand(a: float) -> float:
            if a <= 1e-9:
                return 0.0
            val = (
                (self.omega_r + omega_rot) / (a ** 2)
                + self.omega_m / a
                + self.omega_k
                + self.omega_lambda * (a ** 2)
            )
            return 1.0 / (self.h0 * math.sqrt(max(1e-12, val)))

        integral = self._simpson_integral(integrand, 1e-7, a_target, 600)
        time_seconds = integral * KM_PER_MPC
        return time_seconds / SECONDS_PER_GYR

    def lookback_time_gyr(self, z: float) -> float:
        """Lookback time in Gyr: age(z=0) - age(z)."""
        if z <= 0.0:
            return 0.0
        return max(0.0, self.cosmic_age_gyr(0.0) - self.cosmic_age_gyr(z))

    def predict_xlssc122_concentration(self) -> Dict[str, float]:
        """Predict NFW concentration c_200 for XLSSC 122 under accelerated seed collapse."""
        c_lcdm = 3.2
        scale_factor = (self.xi_seed ** 0.72)
        c_pred = c_lcdm * scale_factor
        tension = abs(6.3 - c_pred) / 0.6
        return {
            "predicted_c_200": round(c_pred, 2),
            "observed_c_200": 6.3,
            "observed_sigma": 0.6,
            "tension_sigma": round(tension, 2),
            "predicted_z_coll": round(3.6 * (self.xi_seed ** 0.8), 1)
        }

    def predict_momz14_abundance(self) -> Dict[str, float]:
        """Predict UV luminosity function Phi(M_UV = -20.2, z = 14.44) under torsion seed boost."""
        phi_lcdm = 7.5e-8
        boost_exponent = 3.45 * (self.xi_seed - 1.0)
        phi_pred = phi_lcdm * math.exp(min(15.0, boost_exponent))
        phi_obs = 1.2e-5
        log_diff = abs(math.log10(phi_pred) - math.log10(phi_obs))
        tension = log_diff / 0.25
        return {
            "predicted_phi_mpc3_mag_inv": phi_pred,
            "observed_phi_mpc3_mag_inv": phi_obs,
            "boost_factor": round(phi_pred / phi_lcdm, 1),
            "tension_sigma": round(tension, 2)
        }

    def predict_jades_spin_asymmetry(self, z: float = 1.5) -> Dict[str, float]:
        """Predict galaxy spin asymmetry A(z) and overall CW fraction for JADES."""
        gamma = 0.14
        a_bin1 = math.tanh(gamma * self.a_star * ((1.0 + 0.65) ** 0.78))
        a_bin2 = math.tanh(gamma * self.a_star * ((1.0 + 1.48) ** 0.78))
        a_bin3 = math.tanh(gamma * self.a_star * ((1.0 + 2.85) ** 0.78))
        
        a_avg = (72.0 * a_bin1 + 98.0 * a_bin2 + 93.0 * a_bin3) / 263.0
        fraction_cw_pred = 0.5 * (1.0 + a_avg)
        
        cw_pred = 263.0 * fraction_cw_pred
        ccw_pred = 263.0 * (1.0 - fraction_cw_pred)
        
        chi2 = ((158.0 - cw_pred) ** 2) / cw_pred + ((105.0 - ccw_pred) ** 2) / ccw_pred
        
        return {
            "predicted_asymmetry_A_mean": round(a_avg, 4),
            "predicted_fraction_cw": round(fraction_cw_pred, 4),
            "predicted_n_cw": round(cw_pred, 1),
            "predicted_n_ccw": round(ccw_pred, 1),
            "observed_fraction_cw": 0.6008,
            "chi2_jades_spin": round(chi2, 3),
            "tension_sigma": round(math.sqrt(max(0.0, chi2)), 2),
            "binned_asymmetries": {
                "z_0.65": round(a_bin1, 4),
                "z_1.48": round(a_bin2, 4),
                "z_2.85": round(a_bin3, 4)
            }
        }
