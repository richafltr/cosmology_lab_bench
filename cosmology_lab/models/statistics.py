"""Statistical utilities for cosmological model evaluation and hypothesis testing."""

import math
from typing import List, Tuple, Dict, Any

def chi_squared(observed: List[float], expected: List[float], uncertainties: List[float]) -> float:
    """Compute total chi-squared: sum((obs - exp)^2 / sigma^2)."""
    if len(observed) != len(expected) or len(observed) != len(uncertainties):
        raise ValueError("Array length mismatch in chi_squared")
    
    total = 0.0
    for obs, exp, unc in zip(observed, expected, uncertainties):
        if unc <= 0:
            unc = 1e-6
        total += ((obs - exp) / unc) ** 2
    return total

def reduced_chi_squared(chi2_val: float, n_points: int, k_params: int) -> float:
    """Compute reduced chi-squared: chi2 / dof."""
    dof = max(1, n_points - k_params)
    return chi2_val / dof

def aic(chi2_val: float, k_params: int) -> float:
    """Akaike Information Criterion: AIC = chi2 + 2*k."""
    return chi2_val + 2.0 * k_params

def bic(chi2_val: float, k_params: int, n_points: int) -> float:
    """Bayesian Information Criterion: BIC = chi2 + k * ln(n)."""
    n_safe = max(2, n_points)
    return chi2_val + k_params * math.log(n_safe)

def bayes_factor_approx(bic_model_a: float, bic_model_b: float) -> float:
    """Log Bayes factor ln(B_ba) ~ 0.5 * (BIC_a - BIC_b).
    Positive value indicates evidence in favor of model b over model a.
    """
    return 0.5 * (bic_model_a - bic_model_b)

def binomial_two_tailed_p_value(k_success: int, n_trials: int, p_null: float = 0.5) -> float:
    """Exact two-tailed binomial p-value using standard combinatorial summation."""
    if n_trials <= 0:
        return 1.0
    
    def log_comb(n: int, r: int) -> float:
        if r < 0 or r > n:
            return float("-inf")
        return math.lgamma(n + 1) - math.lgamma(r + 1) - math.lgamma(n - r + 1)

    # Probability of exactly i successes
    def prob(i: int) -> float:
        return math.exp(log_comb(n_trials, i) + i * math.log(p_null) + (n_trials - i) * math.log(1.0 - p_null))

    target_prob = prob(k_success)
    p_val = 0.0
    for i in range(n_trials + 1):
        pi = prob(i)
        if pi <= target_prob * (1.0 + 1e-12):
            p_val += pi
    return min(1.0, max(0.0, p_val))

def p_value_to_sigma(p_val: float) -> float:
    """Convert two-tailed p-value to equivalent Gaussian standard deviation sigma."""
    if p_val <= 1e-16:
        return 8.2
    if p_val >= 1.0:
        return 0.0
    # Rational approximation of inverse error function
    q = 1.0 - p_val / 2.0
    t = math.sqrt(-2.0 * math.log(1.0 - q))
    c0 = 2.515517
    c1 = 0.802853
    c2 = 0.010328
    d1 = 1.432788
    d2 = 0.189269
    d3 = 0.001308
    z = t - ((c2 * t + c1) * t + c0) / (((d3 * t + d2) * t + d1) * t + 1.0)
    return max(0.0, z)
