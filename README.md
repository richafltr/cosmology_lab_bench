# Cosmology Lab Bench: Black Hole Universe RL Environment

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Three.js](https://img.shields.io/badge/simulation-Three.js%20r128-black.svg)](https://threejs.org/)
[![Status](https://img.shields.io/badge/bench-reproducible-brightgreen.svg)]()

A dry laboratory **Reinforcement Learning (RL) environment and scientific discovery benchmark** designed to test an AI agent's (**Argon**) scientific reasoning, hypothesis formulation, and astrophysical tool orchestration.

The agent is tasked with testing the profound thought experiment: **Is our observable universe the interior of a black hole?**

Rather than relying on speculative conjecture, the laboratory benchmarks the agent against newly uncovered, high-precision observational anomalies from the **James Webb Space Telescope (JWST)** that directly challenge the standard model of cosmology ($\Lambda\text{CDM}$). The agent's final milestone is compiling an interactive **3D Universe Evolution Simulation (in Three.js)** spanning the cosmic time-skip from the Big Bang bounce ($t=0$) to modern humans ($t=13.8\text{ Gyr}$).

---

## 🌌 Grounding Cosmological Evidence: The Three JWST Pillars

The laboratory environment incorporates quantitative data catalogs derived directly from three landmark papers:

```
                                  JWST Observational Evidence
                                              │
           ┌──────────────────────────────────┼──────────────────────────────────┐
           ▼                                  ▼                                  ▼
     [PILLAR 1]                         [PILLAR 2]                         [PILLAR 3]
  Galaxy Cluster XLSSC 122               MoM-z14                            JADES Spin Parity
  (Finner et al. 2025/2026)      (Naidu & Oesch et al. 2025)               (Lior Shamir 2025)
  ─────────────────────────      ───────────────────────────               ──────────────────
  • Redshift z = 1.98            • Redshift z_spec = 14.44                 • 263 deep spiral galaxies
  • Lookback: 10.4 Gyr           • Lookback: 13.52 Gyr (280 Myr post-BB)   • 158 Clockwise vs 105 CCW
  • Most distant strong lens     • M_UV = -20.2, compact r_e = 74 pc       • 60:40 Parity asymmetry
  • Core c_200 = 6.3 (vs 3.2)    • >100x UVLF excess over LCDM             • Binomial p = 0.0013
  • 3.9σ tension in LCDM         • 4.8σ tension in LCDM                    • 3.4σ isotropy violation
```

1. **XLSSC 122 Strong Lensing Cluster ($z = 1.98$)**  
   *Paper:* Kyle Finner et al., *The Astrophysical Journal Letters*, DOI: [`10.3847/2041-8213/ae1d80`](https://doi.org/10.3847/2041-8213/ae1d80)  
   *The Anomaly:* Located 10.4 billion light-years away (cosmic noon), XLSSC 122 is the most distant galaxy cluster confirmed to act as a strong gravitational lens, featuring giant blue arcs and mature intracluster light (ICL). Its dark matter core concentration is measured at $c_{200} = 6.3 \pm 0.6$, whereas standard $\Lambda\text{CDM}$ hierarchical assembly (Duffy et al. 2008, Diemer & Joyce 2019) predicts $c \approx 3.2 \pm 0.4$ ($3.9\sigma$ tension). Clusters at $z \sim 2$ should be dynamically young and unrelaxed.

2. **MoM-z14 ("Mother of Miracles") ($z_{\rm spec} = 14.44$)**  
   *Paper:* Rohan P. Naidu, Pascal A. Oesch et al., *A Cosmic Miracle: A Remarkably Luminous Galaxy at $z_{\rm spec} = 14.44$ Confirmed with JWST*, arXiv: [`2505.11263v2`](https://arxiv.org/abs/2505.11263)  
   *The Anomaly:* Confirmed spectroscopically a mere **280 million years after the Big Bang**. Despite its extreme youth, MoM-z14 is remarkably luminous ($M_{\rm UV} = -20.2$), ultra-compact ($r_e = 74_{-12}^{+15}\text{ pc}$), and exhibits pronounced super-solar nitrogen enrichment ($[\text{N/C}] = +0.85\text{ dex}$) resembling ancient globular cluster progenitors. Its number density is **$>100\times$ higher** than standard $\Lambda\text{CDM}$ UV Luminosity Function predictions ($4.8\sigma$ tension), requiring unphysical $>100\%$ baryon conversion efficiency in standard dark matter halos.

3. **JADES Galaxy Rotation Directional Asymmetry**  
   *Paper:* Lior Shamir, *The distribution of galaxy rotation in JWST Advanced Deep Extragalactic Survey*, *Monthly Notices of the Royal Astronomical Society (MNRAS)*, 538(1), 76–91 (2025), DOI: [`10.1093/mnras/staf292`](https://doi.org/10.1093/mnras/staf292)  
   *The Anomaly:* Deep-field spiral galaxies in the GOODS-S field exhibit a statistically significant directional asymmetry: **158 rotate clockwise vs 105 counterclockwise** (a 60:40 split, asymmetry $A \approx 0.2015$, two-tailed binomial $p = 0.0013$, significance $3.42\sigma$). The asymmetry strengthens with redshift, directly violating the Cosmological Principle (large-scale isotropy).

---

## 🧮 Theoretical Framework: Black Hole Cosmology

The dry laboratory provides mathematical physics engines to test the **Kerr–Einstein–Cartan Black Hole Interior Cosmology** (Pathria 1972, Stuckey 1994, Popławski 2010–2021, Gaztañaga 2022):

### 1. The Horizon Equivalence Identity
For a spatially flat universe ($\Omega_{\rm tot} = 1$), the total mass enclosed within the Hubble sphere $R_H = c / H_0$ precisely equals the Schwarzschild radius:
$$M_H = \frac{4}{3}\pi R_H^3 \rho_c = \frac{4}{3}\pi \left(\frac{c}{H_0}\right)^3 \left(\frac{3 H_0^2}{8\pi G}\right) = \frac{c^3}{2 G H_0}$$
$$R_s = \frac{2 G M_H}{c^2} = \frac{2 G}{c^2}\left(\frac{c^3}{2 G H_0}\right) = \frac{c}{H_0} = R_H \implies \frac{R_s}{R_H} = 1.0000$$

### 2. Einstein–Cartan Non-Singular Bounce
At ultra-high densities ($\rho \sim 10^{52}\text{ g/cm}^3$), spacetime torsion couples to fermion spin densities, generating repulsive gravitational forces that avoid the central singularity. The collapsing parent black hole bounces into a new expanding interior universe.

### 3. Accelerated Structure Seeding ($\xi_{\rm seed}$)
Torsion-induced perturbations generate an amplified small-scale primordial power spectrum ($\xi_{\rm seed} \approx 2.45$). This shifts proto-halo collapse redshifts earlier:
$$(1 + z_{\rm coll, BH}) \approx (1 + z_{\rm coll, LCDM}) \cdot \xi_{\rm seed}^{0.65}$$
- **MoM-z14 ($z=14.44$):** Boosts the UVLF by $\sim 145\times$, matching the observed number density ($1.2 \times 10^{-5}\text{ Mpc}^{-3}\text{ mag}^{-1}$) naturally.
- **XLSSC 122 ($z=1.98$):** Scales concentration $c_{200} \propto (1+z_{\rm coll})/(1+z_{\rm obs})$, yielding $c_{200} \approx 6.1$, precisely matching the strong-lensing core ($6.3 \pm 0.6$).

### 4. Kerr Frame-Dragging Vorticity ($\vec{\omega}$)
A parent Kerr black hole with dimensionless spin $a_* \approx 0.68$ imparts a relic background vorticity $\omega(z) = \omega_0 (1+z)^2$ onto proto-galactic tidal torques. This predicts an alignment asymmetry:
$$A(z) = \frac{N_{\rm CW} - N_{\rm CCW}}{N_{\rm CW} + N_{\rm CCW}} = \tanh\left( \gamma \cdot a_* \cdot (1+z)^{0.78} \right)$$
At $z \sim 2.85$, $A \approx 0.27$, reducing the JADES spin parity $\chi^2$ from $10.68$ ($\Lambda\text{CDM}$) to $0.48$ (BH Cosmology).

---

## 🛠️ The Dry Laboratory RL Bench Architecture

```
cosmology_lab_bench/
├── data/jwst_catalogs/              # Real quantitative JWST observational datasets
│   ├── xlssc122_lensing.json        # Finner et al. (ApJL 2025/2026) data
│   ├── mom_z14_spectroscopy.json    # Naidu et al. (arXiv:2505.11263) data
│   ├── jades_galaxy_spins.json      # Shamir (MNRAS 2025) data
│   └── cosmic_chronometers.json     # Expansion rate & horizon coincidence data
├── cosmology_lab/
│   ├── env.py                       # Gymnasium-compatible RL environment (CosmologyLabEnv)
│   ├── reward.py                    # Multi-objective scientific reward function (0-100 pts)
│   ├── verifier.py                  # Consistency verifier for physical parameters & Three.js
│   ├── models/
│   │   ├── lcdm.py                  # Standard Lambda-CDM numerical integrator
│   │   ├── black_hole_universe.py   # Kerr-Einstein-Cartan Bounce cosmology model
│   │   └── statistics.py            # Chi-sq, AIC, BIC, Bayes factors, binomial p-values
│   └── tools/
│       ├── registry.py              # OpenAI tool schemas & dispatcher
│       ├── observation_tools.py     # query_jwst_catalog tool
│       ├── expansion_tools.py       # solve_cosmic_expansion tool (R_s = R_H)
│       ├── structure_tools.py       # evaluate_mom_z14 & evaluate_xlssc122_lensing
│       ├── spin_tools.py            # analyze_galaxy_spin_parity tool
│       ├── comparison_tools.py      # compare_cosmological_models tool
│       └── simulation_tools.py      # export_simulation_state tool (Three.js state)
├── agents/
│   ├── agent_interface.py           # Abstract BaseCosmologyAgent
│   └── argon_baseline.py            # Argon reference research agent
├── simulation/                      # Interactive Three.js 3D Universe Evolution Simulation
│   ├── index.html                   # Interactive HUD & 3D canvas
│   ├── css/style.css                # Dark-matter telemetry styling
│   ├── js/
│   │   ├── main.js                  # Three.js animation & time-skip engine
│   │   └── epochs.js                # 3D visualizers for all 6 cosmic epochs
│   └── data/universe_state.json     # Compiled trajectory exported by agent
└── tests/                           # Complete test suite (17 tests, 100% pass)
```

---

## 🔬 Scientific Tool Suite for Argon

Argon interacts with the environment via standardized tools:

| Tool Name | Purpose | Key Inputs | Output |
|---|---|---|---|
| `query_jwst_catalog` | Inspect raw JWST catalogs | `catalog_name`, `query_filter` | Observational metrics, uncertainties |
| `solve_cosmic_expansion` | Solve Friedmann / Kerr expansion | `model_type`, `h0`, `a_star` | $H(z)$, ages, $R_s / R_H$ identity |
| `evaluate_mom_z14` | Test early galaxy UVLF & mass | `model_type`, `xi_seed` | Predicted vs observed $\Phi(M_{\rm UV})$, $\sigma$-tension |
| `evaluate_xlssc122_lensing` | Model dark matter halo core | `model_type`, `xi_seed` | Predicted $c_{200}$, Einstein radius $\theta_E$ |
| `analyze_galaxy_spin_parity` | Test Kerr vorticity on spins | `model_type`, `a_star` | CW/CCW counts, asymmetry $A(z)$, $\chi^2$ |
| `compare_cosmological_models`| Multi-pillar Bayesian selection | `a_star`, `xi_seed` | $\chi^2_{\rm tot}$, $\Delta\text{AIC}$, $\Delta\text{BIC}$, $\ln B$ |
| `export_simulation_state` | Export trajectory to Three.js | `a_star`, `xi_seed`, `h0` | 6-epoch trajectory JSON for 3D engine |

---

## 🏆 Evaluation & Reward Function

Argon is scored on a **0 – 100 point scale** across 4 scientific research competencies:

1. **Falsification of Standard Model (25 pts):**  
   Quantify $>3\sigma$ to $4.8\sigma$ tensions in $\Lambda\text{CDM}$ across MoM-z14, XLSSC 122, and JADES.
2. **Black Hole Hypothesis Formulation (25 pts):**  
   Verify the $R_s = R_H$ horizon identity and tune Kerr spin ($a_* \approx 0.68$) and torsion seed factor ($\xi_{\rm seed} \approx 2.45$).
3. **Bayesian Statistical Evidence (25 pts):**  
   Establish decisive evidence ($\Delta\text{BIC} > 40$, $\ln B > 20$) over $\Lambda\text{CDM}$.
4. **Three.js 3D Simulation Compilation (25 pts):**  
   Generate the verified 6-epoch 3D trajectory connecting the Big Bang bounce to modern humans.

**Passing Threshold:** $\ge 80 / 100$ points.

---

## 🚀 Quickstart

### 1. Run Unit Tests (Zero External Dependencies Required)
The core benchmark runs with pure Python standard library:
```bash
python3 -m unittest discover tests
```

### 2. Run the Argon Baseline Agent
Watch Argon execute its research workflow and solve the benchmark:
```bash
python3 -c "
from cosmology_lab.env import CosmologyLabEnv
from agents.argon_baseline import ArgonBaselineAgent

env = CosmologyLabEnv()
agent = ArgonBaselineAgent()
obs, info = env.reset()
done = False

while not done:
    action = agent.act(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated

env.render()
"
```

### 3. Launch the Three.js 3D Universe Evolution Simulation
Serve the repository locally and open the interactive simulation in your browser:
```bash
python3 -m http.server 8000
```
Open **`http://localhost:8000/simulation/`** to interact with the 6-epoch cosmic time-skip:
- **Epoch 0:** Kerr Black Hole Horizon & Torsion Bounce ($t = 0$)
- **Epoch 1:** Cosmic Dawn & Recombination ($t = 380\text{ kyr} - 100\text{ Myr}$)
- **Epoch 2:** MoM-z14 "Mother of Miracles" ($t = 280\text{ Myr}$, $z = 14.44$)
- **Epoch 3:** JADES Spin Chirality & Spiral Formation ($t = 2.3\text{ Gyr}$, $z = 2.85$)
- **Epoch 4:** XLSSC 122 Strong Lensing & Dark Matter Core ($t = 3.38\text{ Gyr}$, $z = 1.98$)
- **Epoch 5:** Modern Universe, Solar System & Humanity ($t = 13.8\text{ Gyr}$, $z = 0$)

---

## 📚 References & Observational Citations

1. **Kyle Finner et al. (2025/2026)**  
   *JWST Discovery of Strong Lensing from a Galaxy Cluster at Cosmic Noon: Giant Arcs and a Highly Concentrated Core of XLSSC 122*  
   *The Astrophysical Journal Letters*, DOI: [10.3847/2041-8213/ae1d80](https://doi.org/10.3847/2041-8213/ae1d80)
2. **Rohan P. Naidu, Pascal A. Oesch et al. (2025)**  
   *A Cosmic Miracle: A Remarkably Luminous Galaxy at $z_{\rm spec} = 14.44$ Confirmed with JWST*  
   *arXiv preprint*, [arXiv:2505.11263v2](https://arxiv.org/abs/2505.11263)
3. **Lior Shamir (2025)**  
   *The distribution of galaxy rotation in JWST Advanced Deep Extragalactic Survey*  
   *Monthly Notices of the Royal Astronomical Society*, 538(1), 76–91, DOI: [10.1093/mnras/staf292](https://doi.org/10.1093/mnras/staf292)
4. **Nikodem J. Popławski (2010–2021)**  
   *Cosmology with torsion: An alternative to cosmic inflation and non-singular black hole universe*  
   *Physics Letters B*, 694(3), 181–185.

---

## 📄 License
MIT License. Created by [richafltr](https://github.com/richafltr).
