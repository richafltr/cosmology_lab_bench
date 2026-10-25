"""Unit tests for the astronomical tool suite."""

import unittest
from cosmology_lab.tools.registry import dispatch_tool, TOOL_REGISTRY, OPENAI_TOOL_SCHEMAS
from cosmology_lab.tools.observation_tools import query_jwst_catalog, list_available_catalogs
from cosmology_lab.tools.expansion_tools import solve_cosmic_expansion
from cosmology_lab.tools.structure_tools import evaluate_mom_z14, evaluate_xlssc122_lensing
from cosmology_lab.tools.spin_tools import analyze_galaxy_spin_parity
from cosmology_lab.tools.comparison_tools import compare_cosmological_models
from cosmology_lab.tools.simulation_tools import export_simulation_state

class TestCosmologyTools(unittest.TestCase):

    def test_schema_coverage(self):
        """Verify all registered tools have corresponding OpenAI schemas."""
        schema_names = {s["function"]["name"] for s in OPENAI_TOOL_SCHEMAS}
        registry_names = set(TOOL_REGISTRY.keys())
        self.assertEqual(schema_names, registry_names)

    def test_query_jwst_catalog(self):
        """Verify catalog queries return real observational parameters."""
        catalogs = list_available_catalogs()
        self.assertIn("xlssc122_lensing", catalogs)
        self.assertIn("mom_z14_spectroscopy", catalogs)
        self.assertIn("jades_galaxy_spins", catalogs)

        data = query_jwst_catalog("xlssc122_lensing")
        self.assertEqual(data["observables"]["redshift_z"], 1.98)
        self.assertEqual(data["observables"]["nfw_parameters"]["c_200_concentration"], 6.3)

    def test_solve_cosmic_expansion(self):
        """Verify Friedmann expansion solver."""
        res = solve_cosmic_expansion(model_type="black_hole", h0=70.0, a_star=0.68)
        self.assertIn("epoch_grid", res)
        self.assertTrue(res["horizon_evaluation"]["condition_satisfied"])

    def test_evaluate_mom_z14(self):
        """Verify MoM-z14 tool."""
        res_lcdm = evaluate_mom_z14(model_type="lcdm")
        self.assertEqual(res_lcdm["galaxy"], "MoM-z14 (Mother of Miracles)")
        self.assertGreater(res_lcdm["evaluation"]["tension_sigma"], 4.0)

        res_bh = evaluate_mom_z14(model_type="black_hole", xi_seed=2.45)
        self.assertLess(res_bh["evaluation"]["tension_sigma"], 1.5)

    def test_evaluate_xlssc122_lensing(self):
        """Verify XLSSC 122 lensing tool."""
        res_lcdm = evaluate_xlssc122_lensing(model_type="lcdm")
        self.assertGreater(res_lcdm["evaluation"]["tension_sigma"], 3.5)

    def test_analyze_galaxy_spin_parity(self):
        """Verify JADES spin parity tool."""
        res = analyze_galaxy_spin_parity(model_type="black_hole", a_star=0.68)
        self.assertEqual(res["observed_cw"], 158)
        self.assertEqual(res["observed_ccw"], 105)

    def test_compare_cosmological_models(self):
        """Verify multi-pillar Bayesian comparison tool."""
        res = compare_cosmological_models(a_star=0.68, xi_seed=2.45)
        stats = res["model_comparison_statistics"]
        self.assertGreater(stats["delta_bic"], 20.0)
        self.assertGreater(stats["ln_bayes_factor_in_favor_of_black_hole"], 10.0)

    def test_export_simulation_state(self):
        """Verify Three.js state compiler exports all 6 epochs."""
        res = export_simulation_state(a_star=0.68, xi_seed=2.45, h0=70.0)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["n_epochs"], 6)

if __name__ == "__main__":
    unittest.main()
