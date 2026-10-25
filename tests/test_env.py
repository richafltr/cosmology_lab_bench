"""Tests for the Gymnasium-compatible RL environment and verifier."""

import unittest
from cosmology_lab.env import CosmologyLabEnv
from cosmology_lab.verifier import ScientificVerifier

class TestCosmologyLabEnv(unittest.TestCase):

    def setUp(self):
        self.env = CosmologyLabEnv(max_steps=20)
        self.verifier = ScientificVerifier()

    def test_env_lifecycle(self):
        """Verify reset and step actions."""
        obs, info = self.env.reset()
        self.assertIn("mission", obs)
        self.assertEqual(obs["step"], 0)

        action = {
            "tool_name": "query_jwst_catalog",
            "arguments": {"catalog_name": "mom_z14_spectroscopy"}
        }
        next_obs, reward, terminated, truncated, next_info = self.env.step(action)
        self.assertEqual(next_obs["step"], 1)
        self.assertFalse(terminated)

    def test_scientific_verifier(self):
        """Verify physical parameter bounds checks."""
        res = self.verifier.verify_black_hole_cosmology_consistency(a_star=0.68, xi_seed=2.45, h0=70.0)
        self.assertTrue(res["all_passed"])

        bad_res = self.verifier.verify_black_hole_cosmology_consistency(a_star=1.5, xi_seed=2.45)
        self.assertFalse(bad_res["all_passed"])

if __name__ == "__main__":
    unittest.main()
