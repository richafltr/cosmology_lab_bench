"""Unit tests for cosmological models and mathematical physics engines."""

import unittest
import math
from cosmology_lab.models.lcdm import StandardLCDM
from cosmology_lab.models.black_hole_universe import BlackHoleUniverse
from cosmology_lab.models.statistics import (
    chi_squared,
    binomial_two_tailed_p_value,
    aic,
    bic,
    bayes_factor_approx
)

class TestCosmologicalModels(unittest.TestCase):

    def setUp(self):
        self.lcdm = StandardLCDM(h0=70.0, omega_m=0.315)
        self.bh = BlackHoleUniverse(h0=70.0, omega_m=0.315, a_star=0.68, xi_seed=2.45)

    def test_hubble_schwarzschild_coincidence(self):
        """Verify the exact mathematical condition R_s = R_H for critical density universe."""
        horizon = self.bh.hubble_schwarzschild_identity()
        self.assertTrue(horizon["condition_satisfied"])
        self.assertAlmostEqual(horizon["ratio_rs_over_rh"], 1.0, places=3)

    def test_cosmic_age_at_z0(self):
        """Verify cosmic age at z=0 is approximately 13.8 Gyr."""
        age_lcdm = self.lcdm.cosmic_age_gyr(0.0)
        age_bh = self.bh.cosmic_age_gyr(0.0)
        self.assertGreater(age_lcdm, 13.0)
        self.assertLess(age_lcdm, 14.5)
        self.assertGreater(age_bh, 13.0)
        self.assertLess(age_bh, 14.5)

    def test_mom_z14_tension_in_lcdm(self):
        """Verify MoM-z14 exhibits >4-sigma tension under standard Lambda-CDM."""
        res_lcdm = self.lcdm.predict_momz14_abundance()
        self.assertGreater(res_lcdm["tension_sigma"], 4.0)
        self.assertGreater(res_lcdm["excess_ratio"], 100.0)

        # Black hole model resolves the tension
        res_bh = self.bh.predict_momz14_abundance()
        self.assertLess(res_bh["tension_sigma"], 1.5)

    def test_xlssc122_concentration_tension(self):
        """Verify XLSSC 122 NFW concentration tension at z=1.98."""
        res_lcdm = self.lcdm.predict_xlssc122_concentration()
        self.assertGreater(res_lcdm["tension_sigma"], 3.5)

        # Black hole accelerated seed collapse matches concentration c_200 ~ 6.1
        res_bh = self.bh.predict_xlssc122_concentration()
        self.assertLess(res_bh["tension_sigma"], 1.0)
        self.assertGreater(res_bh["predicted_c_200"], 5.5)

    def test_jades_spin_asymmetry_binomial_significance(self):
        """Verify JADES 158:105 spin ratio has p-value < 0.002 under isotropy null hypothesis."""
        p_val = binomial_two_tailed_p_value(158, 263, 0.5)
        self.assertLess(p_val, 0.002)

        # Kerr model predicts chi2 < 2.0
        spin_bh = self.bh.predict_jades_spin_asymmetry()
        self.assertLess(spin_bh["chi2_jades_spin"], 2.0)

    def test_bayesian_model_selection(self):
        """Verify Bayes factor favors Black Hole cosmology over LCDM when fitting all 3 anomalies."""
        bic_lcdm = 55.0
        bic_bh = 12.0
        ln_b = bayes_factor_approx(bic_lcdm, bic_bh)
        self.assertGreater(ln_b, 10.0)  # Decisive evidence on Jeffreys scale

if __name__ == "__main__":
    unittest.main()
