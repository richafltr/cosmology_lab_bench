"""End-to-end integration test: Argon research agent solving the cosmology bench."""

import unittest
from cosmology_lab.env import CosmologyLabEnv
from agents.argon_baseline import ArgonBaselineAgent
from cosmology_lab.verifier import ScientificVerifier

class TestArgonBaselineAgent(unittest.TestCase):

    def test_argon_agent_solves_benchmark(self):
        """Verify that the Argon baseline agent systematically investigates all 3 JWST anomalies,
        falsifies standard Lambda-CDM, establishes Bayesian evidence for Black Hole Cosmology,
        exports the 3D Three.js universe simulation, and passes the benchmark.
        """
        env = CosmologyLabEnv(max_steps=20)
        agent = ArgonBaselineAgent()
        verifier = ScientificVerifier()

        obs, info = env.reset()
        done = False
        step_count = 0

        while not done and step_count < 20:
            action = agent.act(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            step_count += 1

        final_eval = env.evaluate_submission()
        
        # Verify agent achieved passing score (>= 80 / 100)
        self.assertGreaterEqual(final_eval["total_score"], 80.0)
        self.assertTrue(final_eval["passed_benchmark"])

        # Verify all subscores
        subscores = final_eval["subscores"]
        self.assertGreaterEqual(subscores["falsification_standard_model"], 20.0)
        self.assertGreaterEqual(subscores["black_hole_hypothesis_formulation"], 20.0)
        self.assertGreaterEqual(subscores["bayesian_statistical_evidence"], 20.0)
        self.assertGreaterEqual(subscores["threejs_simulation_export"], 20.0)

        # Verify Three.js artifacts
        sim_check = verifier.verify_threejs_simulation_artifacts()
        self.assertTrue(sim_check["all_passed"])

if __name__ == "__main__":
    unittest.main()
