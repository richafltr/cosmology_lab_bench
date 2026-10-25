"""Physical and cosmological constants in SI and astrophysical units."""

import math

# Fundamental physical constants (SI)
C_LIGHT_SI = 299792458.0              # Speed of light in vacuum (m / s)
G_NEWTON_SI = 6.67430e-11             # Gravitational constant (m^3 / kg / s^2)
H_PLANCK_SI = 6.62607015e-34          # Planck constant (J * s)
H_BAR_SI = H_PLANCK_SI / (2.0 * math.pi)
K_BOLTZMANN_SI = 1.380649e-23         # Boltzmann constant (J / K)

# Astronomical distance and mass units
METERS_PER_PC = 3.085677581491367e16  # 1 parsec in meters
METERS_PER_KPC = 1e3 * METERS_PER_PC
METERS_PER_MPC = 1e6 * METERS_PER_PC
KM_PER_MPC = METERS_PER_MPC / 1e3
METERS_PER_LY = 9.4607304725808e15    # 1 light year in meters
SECONDS_PER_YEAR = 31557600.0         # 1 Julian year (365.25 days) in seconds
SECONDS_PER_GYR = 1e9 * SECONDS_PER_YEAR
KG_PER_SOLAR_MASS = 1.98847e30        # Solar mass M_sun in kg

# Standard Planck 2018 baseline parameters
DEFAULT_H0 = 67.4                     # Hubble constant (km / s / Mpc)
DEFAULT_OMEGA_M = 0.315               # Matter density parameter
DEFAULT_OMEGA_LAMBDA = 0.685          # Dark energy / cosmological constant parameter
DEFAULT_OMEGA_B = 0.049               # Baryon density parameter
DEFAULT_SIGMA8 = 0.811                # Primordial fluctuation amplitude
DEFAULT_NS = 0.965                    # Scalar spectral index

def h0_to_si(h0_kms_mpc: float) -> float:
    """Convert H0 from km/s/Mpc to s^-1."""
    return (h0_kms_mpc * 1e3) / METERS_PER_MPC

def critical_density_si(h0_kms_mpc: float) -> float:
    """Compute cosmic critical density rho_c = 3 H0^2 / (8 pi G) in kg / m^3."""
    h_si = h0_to_si(h0_kms_mpc)
    return (3.0 * (h_si ** 2)) / (8.0 * math.pi * G_NEWTON_SI)

def hubble_radius_si(h0_kms_mpc: float) -> float:
    """Compute the Hubble horizon radius R_H = c / H0 in meters."""
    return C_LIGHT_SI / h0_to_si(h0_kms_mpc)

def schwarzschild_radius_si(mass_kg: float) -> float:
    """Compute Schwarzschild radius R_s = 2 G M / c^2 in meters."""
    return (2.0 * G_NEWTON_SI * mass_kg) / (C_LIGHT_SI ** 2)
