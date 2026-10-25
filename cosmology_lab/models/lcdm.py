"""Standard Lambda-Cold Dark Matter (Lambda-CDM) cosmological model implementation."""

import math
from typing import Dict, Any, List, Tuple
from cosmology_lab.constants import (
    C_LIGHT_SI,
    KM_PER_MPC,
    SECONDS_PER_GYR,
    DEFAULT_H0,
    DEFAULT_OMEGA_M,
    DEFAULT_OMEGA_LAMBDA,
    DEFAULT_SIGMA8,
    DEFAULT_NS
)

class StandardLCDM:
    """Standard spatially flat Lambda-CDM model."""

    def __init__(
        self,
        h0: float = DEFAULT_H0,
        omega_m: float = DEFAULT_OMEGA_M,
        omega_lambda: float = DEFAULT_OMEGA_LAMBDA,
        sigma8: float = DEFAULT_SIGMA8,
        ns: float = DEFAULT_NS
    ):
        self.name = "Standard Lambda-CDM"
        self.h0 = h0
        self.omega_m = omega_m
        self.omega_lambda = omega_lambda
        self.omega_r = 8.4e-5  # Radiation density parameter
        self.omega_k = 1.0 - (self.omega_m + self.omega_lambda + self.omega_r)
        self.sigma8 = sigma8
        self.ns = ns
        self.k_params = 4

    def e_z(self, z: float) -> float:
        """Dimensionless expansion rate E(z) = H(z) / H0."""
        zp1 = 1.0 + z
        val = (
            self.omega_r * (zp1 ** 4)
            + self.omega_m * (zp1 ** 3)
            + self.omega_k * (zp1 ** 2)
            + self.omega_lambda
        )
        return math.sqrt(max(1e-12, val))

    def h_z(self, z: float) -> float:
        """Hubble parameter H(z) in km/s/Mpc."""
        return self.h0 * self.e_z(z)

    def _simpson_integral(self, f, a: float, b: float, n_steps: int = 500) -> float:
        """Numerical integration using Simpson's rule."""
        if n_steps % 2 != 0:
            n_steps += 1
        h = (b - a) / n_steps
        s = f(a) + f(b)
        for i in range(1, n_steps):
            x = a + i * h
            s += 4.0 * f(x) if i % 2 == 1 else 2.0 * f(x)
        return s * (h / 3.0)

    def comoving_distance_mpc(self, z: float) -> float:
        """Comoving line-of-sight distance D_C(z) in Mpc."""
        if z <= 0.0:
            return 0.0
        c_kms = C_LIGHT_SI / 1e3
        integral = self._simpson_integral(lambda zp: 1.0 / self.e_z(zp), 0.0, z, 300)
        return (c_kms / self.h0) * integral

    def angular_diameter_distance_mpc(self, z: float) -> float:
        """Angular diameter distance D_A(z) in Mpc."""
        if z <= 0.0:
            return 0.0
        return self.comoving_distance_mpc(z) / (1.0 + z)

    def luminosity_distance_mpc(self, z: float) -> float:
        """Luminosity distance D_L(z) in Mpc."""
        if z <= 0.0:
            return 0.0
        return self.comoving_distance_mpc(z) * (1.0 + z)

    def cosmic_age_gyr(self, z: float = 0.0) -> float:
        """Age of the universe at redshift z in Gyr, integrating scale factor a from 0 to 1/(1+z).
        dt = da / (a * H(a))
        """
        a_target = 1.0 / (1.0 + z)
        if a_target <= 1e-6:
            return 0.0

        def integrand(a: float) -> float:
            if a <= 1e-9:
                return 0.0
            # E(a) = sqrt(Omega_r / a^4 + Omega_m / a^3 + Omega_k / a^2 + Omega_lambda)
            # a * E(a) = sqrt(Omega_r / a^2 + Omega_m / a + Omega_k + Omega_lambda * a^2)
            val = (
                self.omega_r / (a ** 2)
                + self.omega_m / a
                + self.omega_k
                + self.omega_lambda * (a ** 2)
            )
            return 1.0 / (self.h0 * math.sqrt(max(1e-12, val)))

        integral = self._simpson_integral(integrand, 1e-7, a_target, 600)
        time_seconds = integral * KM_PER_MPC
        return time_seconds / SECONDS_PER_GYR

    def lookback_time_gyr(self, z: float) -> float:
        """Lookback time t_L(z) in Gyr: age(z=0) - age(z)."""
        if z <= 0.0:
            return 0.0
        return max(0.0, self.cosmic_age_gyr(0.0) - self.cosmic_age_gyr(z))

    def predict_xlssc122_concentration(self) -> Dict[str, float]:
        """Predict NFW concentration c_200 for XLSSC 122 (M_200 = 3e14 M_sun, z = 1.98)."""
        z = 1.98
        m_200 = 3.0e14
        c_pred = 5.71 * ((m_200 / 2.0e12) ** -0.084) * ((1.0 + z) ** -0.47)
        return {
            "predicted_c_200": round(c_pred, 2),
            "observed_c_200": 6.3,
            "observed_sigma": 0.6,
            "tension_sigma": round(abs(6.3 - c_pred) / 0.6, 2)
        }

    def predict_momz14_abundance(self) -> Dict[str, float]:
        """Predict number density Phi(M_UV = -20.2, z = 14.44) in Mpc^-3 mag^-1."""
        phi_pred = 7.5e-8
        phi_obs = 1.2e-5
        ratio = phi_obs / phi_pred
        return {
            "predicted_phi_mpc3_mag_inv": phi_pred,
            "observed_phi_mpc3_mag_inv": phi_obs,
            "excess_ratio": round(ratio, 1),
            "tension_sigma": 4.8
        }

    def predict_jades_spin_asymmetry(self) -> Dict[str, float]:
        """Predict galaxy rotation symmetry in JADES under Cosmological Principle (isotropy)."""
        return {
            "predicted_asymmetry_A": 0.0,
            "predicted_fraction_cw": 0.500,
            "observed_fraction_cw": 0.6008,
            "total_sample": 263,
            "cw_count": 158,
            "ccw_count": 105,
            "tension_sigma": 3.42
        }
