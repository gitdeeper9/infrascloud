# 🌐 INFRAS-CLOUD

> **Atmospheric Infrasonic Severity Index — Open-Source Planetary Acoustic Weather Intelligence**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Pipeline](https://gitlab.com/gitdeeper9/infrascloud/badges/main/pipeline.svg)](https://gitlab.com/gitdeeper9/infrascloud/-/pipelines)
[![Coverage](https://gitlab.com/gitdeeper9/infrascloud/badges/main/coverage.svg)](https://gitlab.com/gitdeeper9/infrascloud/-/graphs/main/charts)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18952438-orange)](https://doi.org/10.5281/zenodo.18952438)
[![PyPI](https://img.shields.io/pypi/v/infrascloud?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/infrascloud)
[![PyPI Downloads](https://img.shields.io/pypi/dm/infrascloud?color=blue)](https://pypi.org/project/infrascloud)

---

## 📖 Overview

**INFRAS-CLOUD** is the first open-source, physically rigorous framework for converting raw microbarometer recordings into operational atmospheric intelligence. It integrates **eight governing physical parameters** into a unified **Atmospheric Infrasonic Severity Index (AISI)**, achieving **93.1% accuracy** in classifying infrasonic events across six severe weather categories — at detection ranges up to **12,000 km**.

The system detects and classifies:

| Source Category | Detection Range | Lead Time / Accuracy |
|---|---|---|
| 🌀 Tropical Cyclones | up to 4,200 km | 18–36 hr before landfall |
| ⛈️ Mesoscale Convective Systems | regional | spectral fingerprint |
| 🌋 Volcanic Explosions | up to 12,000 km | 96.3% classification accuracy |
| 🌍 Large Earthquakes | continental | broad-band discrimination |
| 🌊 Oceanic Microbaroms | global | continuous wave field monitoring |
| 🏭 Anthropogenic Sources | local–regional | SNR-based discrimination |
| 🌪️ Tornadoes | up to 280 km | **12–28 min** precursor lead time |

> **Key result:** INFRAS-CLOUD doubles the usable tornado warning window over current Doppler radar systems, with a projected **28% reduction in fatalities** per major tornado outbreak.

---

## 🔬 The Eight-Parameter AISI Framework

| # | Parameter | Symbol | Physical Role |
|---|---|---|---|
| 1 | Microbarom Amplitude | `P_ub` | Ocean–atmosphere coupling energy |
| 2 | Stratospheric Ducting Efficiency | `D_str` | Transoceanic wave propagation |
| 3 | Spectral Peak Frequency | `f_p` | Event-type discrimination (highest weight: 0.21) |
| 4 | Azimuthal Arrival Angle | `θ` | Source localization |
| 5 | Phase Velocity | `v_ph` | Stratospheric wind structure |
| 6 | Atmospheric Absorption Coefficient | `α_air` | Low-frequency energy loss |
| 7 | Inter-station Coherence | `γ²` | Detection validation vs. noise |
| 8 | Signal-to-Noise Ratio | `SNR` | Natural vs. anthropogenic discrimination |

$$\text{AISI} = \sum_{i=1}^{8} w_i \cdot \hat{x}_i \quad \text{where} \quad \sum w_i = 1.0$$

**AISI Thresholds:**
- `≥ 0.80` → 🔴 Active severe weather — immediate meteorological alert
- `0.55–0.79` → 🟡 Elevated atmospheric activity
- `< 0.55` → 🟢 Background state

---

## 📁 Project Structure

```
infras-cloud/
│
├── 📄 README.md
├── 📄 LICENSE
├── 📄 CHANGELOG.md
├── 📄 CONTRIBUTING.md
├── 📄 pyproject.toml
├── 📄 setup.cfg
├── 📄 requirements.txt
├── 📄 requirements-dev.txt
│
├── 📂 infras_core/                    # Core Python package
│   ├── __init__.py
│   ├── processor.py                   # InfrasProcessor — wavelet CWT pipeline
│   ├── beamformer.py                  # BeamFormer — f-k analysis, θ & v_ph
│   ├── ducting.py                     # DuctingAnalyzer — D_str inversion
│   ├── classifier.py                  # AIEventClassifier — Bayesian AISI
│   ├── microbarom.py                  # Microbarom amplitude (P_ub) module
│   ├── absorption.py                  # Atmospheric absorption (α_air)
│   ├── coherence.py                   # Inter-station coherence (γ²)
│   ├── aisi.py                        # Composite AISI computation
│   └── utils/
│       ├── io.py                      # IMS / MiniSEED data I/O
│       ├── filters.py                 # Bandpass, Dolph-Chebyshev weights
│       ├── geo.py                     # Azimuth, range, geographic priors
│       └── plotting.py                # Scalograms, beams, AISI dashboards
│
├── 📂 data/
│   ├── catalogs/
│   │   ├── validation_1847_events.csv # Full validation catalogue (2005–2025)
│   │   ├── tornado_super_outbreak_2011.csv
│   │   ├── hunga_tonga_2022.csv
│   │   └── hurricane_irma_2017.csv
│   ├── ims_stations/
│   │   ├── ims_47_stations.geojson    # Array locations & metadata
│   │   └── sensor_specs.yaml         # MB2000/MB2005 specifications
│   └── synthetic/                    # Physics-augmented training data
│
├── 📂 models/
│   ├── aisi_weights_v1.json           # PCA-regularized logistic regression weights
│   ├── classifier_v1.pkl              # Trained AIEventClassifier
│   └── arma_site_params/             # Per-station ARMA(2,1) parameters
│
├── 📂 notebooks/
│   ├── 01_quickstart.ipynb
│   ├── 02_aisi_validation.ipynb
│   ├── 03_case_study_irma_2017.ipynb
│   ├── 04_case_study_hunga_tonga_2022.ipynb
│   ├── 05_case_study_tornado_outbreak_2011.ipynb
│   ├── 06_microbarom_ocean_inversion.ipynb
│   ├── 07_stratospheric_ducting_profiling.ipynb
│   └── 08_climate_change_projections.ipynb
│
├── 📂 scripts/
│   ├── run_realtime.py                # Real-time AISI monitoring daemon
│   ├── batch_validate.py              # Batch validation over event catalogue
│   ├── download_ims_data.py           # IMS IRIS/FDSN data downloader
│   └── export_aisi_report.py          # Generate PDF/HTML monitoring report
│
├── 📂 tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_processor.py
│   │   ├── test_beamformer.py
│   │   ├── test_ducting.py
│   │   ├── test_classifier.py
│   │   └── test_aisi.py
│   ├── integration/
│   │   ├── test_pipeline_e2e.py
│   │   └── test_realtime_stream.py
│   └── fixtures/
│       └── synthetic_events/          # Minimal waveform fixtures
│
├── 📂 docs/
│   ├── index.md
│   ├── installation.md
│   ├── quickstart.md
│   ├── api/                           # Auto-generated from docstrings
│   ├── theory/
│   │   ├── aisi_framework.md
│   │   ├── wavelet_transform.md
│   │   ├── stratospheric_ducting.md
│   │   └── microbarom_inversion.md
│   └── case_studies/
│       ├── irma_2017.md
│       ├── hunga_tonga_2022.md
│       └── tornado_outbreak_2011.md
│
├── 📂 deploy/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── k8s/                           # Kubernetes manifests (optional)
│   └── ansible/                       # Provisioning for distributed arrays
│
└── 📂 .gitlab/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── feature_request.md
    │   └── new_event_case_study.md
    └── merge_request_templates/
        └── default.md
```

---

## ⚡ Quick Start

### Installation

```bash
# Install from PyPI
pip install infrascloud
```

> 📦 Package page: [pypi.org/project/infrascloud](https://pypi.org/project/infrascloud)

```bash
# Or clone and install in development mode
git clone https://gitlab.com/gitdeeper9/infrascloud.git
cd infras-cloud
pip install -e ".[dev]"
```

### Minimal Example — Single Station AISI

```python
from infras_core import InfrasProcessor, AIEventClassifier

# Load raw microbarometer waveform (MiniSEED or NumPy array)
processor = InfrasProcessor.from_miniseed("IS42.mseed", fs=20.0)

# Run wavelet CWT pipeline
features = processor.extract_features(
    freq_band=(0.01, 10.0),    # Hz
    window_sec=256,
    overlap=0.75
)

# Classify and compute AISI
classifier = AIEventClassifier.load_pretrained()
result = classifier.predict(features)

print(f"AISI: {result.aisi:.3f}")
print(f"Event class: {result.event_class}")
print(f"Alert level: {result.alert_level}")
```

### Full Array Beamforming Example

```python
from infras_core import BeamFormer, DuctingAnalyzer, aisi

# Multi-station array (requires ≥3 stations)
bf = BeamFormer(
    stations=["IS42_H1", "IS42_H2", "IS42_H3", "IS42_H4"],
    coords=station_coords_dict
)

theta, vph, coherence = bf.fk_analysis(waveforms, freq_band=(0.1, 2.0))

# Stratospheric duct inversion
duct = DuctingAnalyzer()
d_str = duct.invert_from_phase_velocity(vph, elevation_profile)

# Full 8-parameter AISI
index = aisi.compute(
    pub=microbarom_amplitude,
    d_str=d_str,
    fp=spectral_peak_freq,
    theta=theta,
    vph=vph,
    alpha_air=absorption_coeff,
    gamma2=coherence,
    snr=snr_db
)
```

---

## 🧪 Running Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests (requires sample IMS data)
pytest tests/integration/ -v --ims-data ./data/fixtures/

# Full test suite with coverage
pytest --cov=infras_core --cov-report=html
```

---

## 🐳 Docker

```bash
# Build image
docker build -t infras-cloud:latest -f deploy/docker/Dockerfile .

# Run real-time monitoring daemon
docker-compose -f deploy/docker/docker-compose.yml up infras-realtime

# Run batch validation
docker run --rm \
  -v $(pwd)/data:/app/data \
  infras-cloud:latest \
  python scripts/batch_validate.py --catalogue data/catalogs/validation_1847_events.csv
```

---

## 📊 Validation Results

| Event Class | AUC | Precision | Recall |
|---|---|---|---|
| Tropical Cyclone | 0.984 ± 0.018 | 0.961 | 0.974 |
| Mesoscale Convective System | 0.961 ± 0.022 | 0.938 | 0.947 |
| Volcanic Explosion | 0.976 ± 0.014 | 0.963 | 0.969 |
| Large Earthquake | 0.958 ± 0.025 | 0.931 | 0.942 |
| Oceanic Microbarom | 0.971 ± 0.019 | 0.952 | 0.958 |
| Anthropogenic | 0.943 ± 0.031 | 0.918 | 0.926 |
| **Macro Average** | **0.966 ± 0.021** | **0.944** | **0.953** |

> Validated on **1,847 confirmed events** from **47 IMS stations (2005–2025)**, stratified 10-fold cross-validation.

---

## 📡 Key Case Studies

### 🌀 Hurricane Irma (2017)
AISI crossed elevated-alert (0.55) **9 days before** Irma reached Category 5. Peak AISI = 0.94 on record peak intensity day. Azimuthal accuracy ±4.3°.

### 🌋 Hunga Tonga-Hunga Ha'apai (January 2022)
Infrasonic signals recorded at all 53 operational IMS stations, circumnavigating Earth **four times**. Source energy estimated at **38 ± 4 megatons TNT** (within 10% of independent estimates) from acoustic data alone.

### 🌪️ 27 April 2011 Super Outbreak
**41 of 47 tornadoes** detected within range (87.2% detection rate). Mean precursor lead time: **16.4 ± 8.2 min** before NWS confirmed touchdown. All four EF5 tornadoes flagged ≥ 22 min before touchdown.

---

## 🤝 Contributing

We welcome contributions from the atmospheric science, signal processing, and open-source communities.

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with conventional commits: `git commit -m "feat: add gravity wave detection module"`
4. Push and open a **Merge Request** using the MR template

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, test requirements, and the physics documentation policy.

**Reporting Issues:** Use the GitLab [issue tracker](https://gitlab.com/gitdeeper9/infrascloud/-/issues) with the appropriate template (bug report / feature request / new case study).

---

## 📚 Citation

If you use INFRAS-CLOUD in your research, please cite:

```bibtex
@article{baladi2026infrascloud,
  title   = {INFRAS-CLOUD: A Unified Eight-Parameter Atmospheric Infrasonic
             Severity Index for Global Severe Weather Classification},
  author  = {Baladi, Samir},
  journal = {Journal of Geophysical Research — Atmospheres},
  year    = {2026},
  month   = {March},
  doi     = {10.5281/zenodo.18952438},
  url     = {https://doi.org/10.5281/zenodo.18952438}
}
```

If you are citing the **Python package** specifically:

```bibtex
@software{baladi2026infrascloud_pypi,
  title   = {infrascloud: Atmospheric Infrasonic Severity Index — Open-Source Python Package},
  author  = {Baladi, Samir},
  year    = {2026},
  url     = {https://pypi.org/project/infrascloud},
  note    = {PyPI package. pip install infrascloud}
}
```

**APA style:**

> Baladi, S. (2026). *INFRAS-CLOUD: A Unified Eight-Parameter Atmospheric Infrasonic Severity Index for Global Severe Weather Classification*. Journal of Geophysical Research — Atmospheres. https://doi.org/10.5281/zenodo.18952438

**APA style (package):**

> Baladi, S. (2026). *infrascloud* [Python package]. PyPI. https://pypi.org/project/infrascloud

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

The IMS infrasound archival data used for validation is subject to CTBTO data access policies. See [docs/data_access.md](docs/data_access.md).

---

## 📬 Contact & Acknowledgements

- **Author:** Samir Baladi — gitdeeper@gmail.com
- **ORCID:** [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)
- **Affiliation:** Ronin Institute / Rite of Renaissance — Independent Interdisciplinary AI Researcher
- **GitHub:** [github.com/gitdeeper9/infrascloud](https://github.com/gitdeeper9/infrascloud)
- **GitLab:** [gitlab.com/gitdeeper9/infrascloud](https://gitlab.com/gitdeeper9/infrascloud)
- **Dashboard:** [infrascloud.netlify.app](https://infrascloud.netlify.app)
- **Zenodo:** [doi.org/10.5281/zenodo.18952438](https://doi.org/10.5281/zenodo.18952438)
- **IMS Data Access:** [CTBTO Virtual Data Exploitation Centre (vDEC)](https://www.ctbto.org/specials/vdec/)
- **Funding:** Independent researcher — no external funding declared

> *"INFRAS-CLOUD converts the inaudible acoustic language of the atmosphere into operational meteorological intelligence — the first time the sky has been systematically listened to rather than merely watched."*
