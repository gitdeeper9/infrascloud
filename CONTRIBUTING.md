# 🤝 Contributing to INFRAS-CLOUD

## Atmospheric Infrasound & Severe Weather Acoustic Signatures

**DOI**: 10.5281/zenodo.18952438  
**Repository**: github.com/gitdeeper9/infrascloud  
**Web**: infrascloud.netlify.app

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Contributing to Physics Modules](#contributing-to-physics-modules)
- [Contributing to Signal Processing](#contributing-to-signal-processing)
- [Contributing to Documentation](#contributing-to-documentation)
- [Testing Guidelines](#testing-guidelines)
- [Data Contributions](#data-contributions)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

### Our Pledge
We as members, contributors, and leaders pledge to make participation in the INFRAS-CLOUD community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members
- Acknowledging the global impact of severe weather research
- Promoting open science and reproducible research

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at gitdeeper@gmail.com. All complaints will be reviewed and investigated promptly and fairly.

---

## 🚀 Getting Started

### Prerequisites
```bash
# Install development dependencies
python --version  # 3.9-3.11 required
git --version     # 2.30+ recommended
docker --version  # 20.10+ for containerized development
```

Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/infrascloud.git
cd infrascloud

# Add upstream remote
git remote add upstream https://github.com/gitdeeper9/infrascloud.git
```

Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install --upgrade pip
pip install -e .[dev]
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial setup
python scripts/init_dev.py
```

Development Tools

```bash
# Code formatting
black infrascloud/ tests/
isort infrascloud/ tests/

# Linting
flake8 infrascloud/ tests/ --max-line-length=100
pylint infrascloud/ tests/

# Type checking
mypy infrascloud/ --ignore-missing-imports

# Testing
pytest tests/ -v --cov=infrascloud --numprocesses=auto
```

---

🔄 Development Workflow

Branch Naming Convention

```
feature/        # New features (e.g., feature/beamforming-optimization)
bugfix/         # Bug fixes (e.g., bugfix/wavelet-edge-case)
docs/           # Documentation (e.g., docs/api-refactor)
physics/        # Physics module updates (e.g., physics/microbarom-inversion)
processing/     # Signal processing (e.g., processing/wavelet-parameters)
data/           # Data contributions (e.g., data/new-event-2026)
sensor/         # Sensor integrations (e.g., sensor/mb2005-driver)
```

Development Process

```bash
# 1. Update your main branch
git checkout main
git pull upstream main

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes
# ... code changes ...

# 4. Run tests locally
pytest tests/ -v

# 5. Commit with conventional commit message
git add .
git commit -m "feat: add new beamforming optimization algorithm"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Create Pull Request on GitHub
```

Commit Message Convention

We follow Conventional Commits with scientific context:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:

· feat: New feature
· fix: Bug fix
· docs: Documentation only
· style: Code style (formatting)
· refactor: Code change that neither fixes bug nor adds feature
· perf: Performance improvement
· test: Adding missing tests
· chore: Changes to build process or auxiliary tools
· physics: Changes to physics equations or parameters
· processing: Changes to signal processing algorithms
· data: Data additions or updates

Examples:

```
feat(beamforming): add adaptive Dolph-Chebyshev weighting for improved azimuth resolution
fix(wavelet): resolve edge effects in Morlet CWT at low frequencies (<0.01 Hz)
docs(aisi): update threshold values based on 2025 validation
physics(microbarom): refine P_ub inversion algorithm with Monte Carlo uncertainty
data: add 2025 tropical cyclone events to validation catalogue
```

---

🔬 Contributing to Physics Modules

Core Physics Equations

INFRAS-CLOUD is built on eight governing equations from the research paper:

```python
# infrascloud/physics/microbarom.py
def compute_microbarom_amplitude(wave_spectrum, propagation_greens_function,
                                 air_density=1.225, sound_speed=340):
    """
    Compute Microbarom Amplitude (P_ub)
    
    P_ub(ω) = ρ_air · c · ∫∫ F(k, ω/2) · F(-k, ω/2) · G(r, ω) d²k
    
    Parameters
    ----------
    wave_spectrum : array_like
        Directional ocean wave spectrum F(k, ω/2)
    propagation_greens_function : array_like
        Green's function propagator G(r, ω) encoding atmospheric ducting
    air_density : float, optional
        Sea-level air density ρ_air (kg/m³)
    sound_speed : float, optional
        Mean sound speed c (m/s)
    
    Returns
    -------
    float
        Microbarom amplitude P_ub (Pa)
    
    Notes
    -----
    At typical IMS noise floors, microbaroms are detectable when
    significant wave height H_s ≥ 1.5 m in the source region.
    """
    # Implementation
    pass
```

```python
# infrascloud/physics/ducting.py
def compute_stratospheric_ducting_efficiency(ceff_strat, ceff_surface):
    """
    Compute Stratospheric Ducting Efficiency (D_str)
    
    D_str = [c_eff(z_strat) - c_eff(z_0)] / c_eff(z_0) = Δc_eff / c_0
    
    Parameters
    ----------
    ceff_strat : float
        Effective sound speed at stratospheric altitude (42-48 km)
    ceff_surface : float
        Effective sound speed at surface
    
    Returns
    -------
    float
        Stratospheric ducting efficiency
        D_str > 0: ducted propagation exists
        D_str < 0: no stratospheric duct
    
    Notes
    -----
    Typical values:
    - Summer: D_str = +0.10 to +0.25 (eastward winds 50-80 m/s)
    - Winter: D_str = -0.02 to +0.08
    """
    # Implementation
    pass
```

```python
# infrascloud/physics/aisi.py
def compute_aisi(parameters, weights=None):
    """
    Compute Atmospheric Infrasonic Severity Index (AISI)
    
    AISI = w₁·P*_ub + w₂·D*_str + w₃·f*_p + w₄·θ* + w₅·v*_ph +
           w₆·α*_air + w₇·γ²* + w₈·SNR*
    
    Default weights (PCA-regularized logistic regression):
    w₁=0.18, w₂=0.14, w₃=0.21, w₄=0.15, w₅=0.12, w₆=0.07, w₇=0.08, w₈=0.05
    
    Parameters
    ----------
    parameters : dict
        Dictionary with keys: 'P_ub', 'D_str', 'f_p', 'theta',
                              'v_ph', 'alpha_air', 'gamma2', 'SNR'
    weights : dict, optional
        Custom weights for each parameter
    
    Returns
    -------
    float
        AISI value (0-1)
    
    Thresholds:
    - AISI ≥ 0.80: CRITICAL - immediate meteorological alert
    - AISI 0.55-0.79: ELEVATED - increased monitoring
    - AISI < 0.55: BACKGROUND - routine
    """
    # Implementation
    pass
```

Adding New Physics Models

```python
# infrascloud/physics/new_model.py
"""
Template for contributing new physics models
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class NewModelConfig:
    """Configuration for new physics model"""
    parameter1: float
    parameter2: float
    calibration_factor: Optional[float] = 1.0
    uncertainty_bounds: Tuple[float, float] = (0.0, 1.0)

class NewPhysicsModel:
    """
    New physics model implementation
    
    References
    ----------
    [1] Author et al. (2026) - DOI: 10.xxxx/xxxxx
    [2] INFRAS-CLOUD Research Paper - DOI: 10.5281/zenodo.18952438
    """
    
    def __init__(self, config: Dict):
        self.config = NewModelConfig(**config)
        self.validate_against_ims_data()
    
    def compute(self, input_data: np.ndarray) -> float:
        """
        Compute model output
        
        Parameters
        ----------
        input_data : np.ndarray
            Input data (e.g., pressure time series)
        
        Returns
        -------
        float
            Model output
        """
        # Implement your model here
        result = self.config.parameter1 * np.mean(input_data)
        return result * self.config.calibration_factor
    
    def validate_against_ims_data(self):
        """Validate model against 47 IMS stations dataset"""
        # Load validation data from IMS stations
        # Compare predictions with observations
        # Report validation metrics
        # Ensure r² ≥ 0.90 for acceptance
        pass
    
    def get_references(self) -> list:
        """Return list of academic references"""
        return [
            "Author, A. et al. (2026). Title. Journal, volume, pages.",
            "Baladi, S. (2026). INFRAS-CLOUD Research Paper. DOI: 10.5281/zenodo.18952438"
        ]
    
    def get_uncertainty(self) -> float:
        """Return uncertainty estimate"""
        return self.config.uncertainty_bounds[1] - self.config.uncertainty_bounds[0]
```

---

📡 Contributing to Signal Processing

Wavelet Transform Module

```python
# infrascloud/processing/wavelet.py
"""
Continuous Wavelet Transform (CWT) for infrasonic signal processing

Morlet mother wavelet with ω₀ = 6 provides adaptive time-frequency resolution:
- High time resolution at high frequencies
- High frequency resolution at low frequencies (<0.01 Hz precision)
"""

import numpy as np
from scipy import signal
from typing import Tuple, Optional

class WaveletProcessor:
    """
    CWT-based infrasonic signal processor
    
    Implements the wavelet architecture described in Section 4.3 of the
    INFRAS-CLOUD research paper.
    """
    
    def __init__(self, fs=20, fmin=0.001, fmax=20, omega0=6):
        """
        Initialize wavelet processor
        
        Parameters
        ----------
        fs : float
            Sampling frequency (Hz) - IMS standard: 20 Hz
        fmin : float
            Minimum frequency (Hz) - 0.001 Hz for gravity waves
        fmax : float
            Maximum frequency (Hz) - 20 Hz for infrasound band
        omega0 : float
            Morlet wavelet central frequency (default: 6)
        """
        self.fs = fs
        self.fmin = fmin
        self.fmax = fmax
        self.omega0 = omega0
        self._validate_parameters()
    
    def compute_scalogram(self, pressure_timeseries: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute wavelet scalogram
        
        W(a, b) = (1/√a) · ∫ p(t) · ψ*((t-b)/a) dt
        
        Parameters
        ----------
        pressure_timeseries : np.ndarray
            Pressure data from microbarometer (Pa)
        
        Returns
        -------
        frequencies : np.ndarray
            Frequency array (Hz)
        scalogram : np.ndarray
            Wavelet power spectrum |W(a,b)|²
        """
        # Implementation
        pass
    
    def extract_fp(self, scalogram: np.ndarray, frequencies: np.ndarray,
                   time_window: Tuple[float, float]) -> float:
        """
        Extract spectral peak frequency f_p
        
        Parameters
        ----------
        scalogram : np.ndarray
            Wavelet power spectrum
        frequencies : np.ndarray
            Frequency array
        time_window : tuple
            (start_time, end_time) in seconds
        
        Returns
        -------
        float
            Dominant frequency f_p (Hz)
        """
        # Implementation
        pass
    
    def detect_frequency_chirp(self, scalogram: np.ndarray, 
                               time_axis: np.ndarray) -> Tuple[bool, float]:
        """
        Detect tornado vortex frequency chirp
        
        f_p = Γ/(2πr²) ∝ 1/r²
        
        Parameters
        ----------
        scalogram : np.ndarray
            Wavelet power spectrum
        time_axis : np.ndarray
            Time array (seconds)
        
        Returns
        -------
        chirp_detected : bool
            True if frequency chirp detected
        chirp_rate : float
            Rate of frequency change df_p/dt (Hz/s)
        """
        # Implementation
        pass
    
    def _validate_parameters(self):
        """Validate wavelet parameters"""
        assert 0.001 <= self.fmin <= 0.1, "fmin should be in gravity wave band"
        assert 10 <= self.fmax <= 30, "fmax should cover infrasound band"
        assert 4 <= self.omega0 <= 10, "omega0 typically 6 for Morlet"
```

Beamforming Module

```python
# infrascloud/processing/beamforming.py
"""
Frequency-wavenumber (f-k) beamforming for infrasonic arrays

B(k, ω) = Σᵢ wᵢ · pᵢ(ω) · exp(+i k · rᵢ)
"""

import numpy as np
from typing import Dict, Tuple

class BeamFormer:
    """
    Multi-station f-k beamforming engine
    
    Estimates azimuth θ and phase velocity v_ph with uncertainties
    σ_θ ≈ ±2-5° and σ_v ≈ ±5-15 m/s.
    """
    
    def __init__(self, station_coordinates: np.ndarray,
                 weighting='dolph-chebyshev', window_length=256, overlap=0.75):
        """
        Initialize beamformer
        
        Parameters
        ----------
        station_coordinates : np.ndarray
            Array element positions (x, y) in meters
        weighting : str
            Weighting method ('dolph-chebyshev', 'uniform', 'hamming')
        window_length : int
            Analysis window length in seconds
        overlap : float
            Window overlap fraction (0-1)
        """
        self.stations = station_coordinates
        self.n_stations = len(station_coordinates)
        self.weighting = weighting
        self.window_length = window_length
        self.overlap = overlap
    
    def compute_beam_power(self, pressure_spectra: np.ndarray,
                           frequencies: np.ndarray) -> Dict:
        """
        Compute beam power over (θ, v_ph) space
        
        Parameters
        ----------
        pressure_spectra : np.ndarray
            Complex pressure spectra pᵢ(ω) for each station
        frequencies : np.ndarray
            Frequency array (Hz)
        
        Returns
        -------
        dict
            - 'theta': azimuth angle (degrees)
            - 'v_ph': phase velocity (m/s)
            - 'beam_power': maximum beam power
            - 'theta_uncertainty': σ_θ (degrees)
            - 'v_ph_uncertainty': σ_v (m/s)
        """
        # Implementation
        pass
    
    def compute_coherence(self, station1_spectra: np.ndarray,
                          station2_spectra: np.ndarray,
                          frequencies: np.ndarray) -> np.ndarray:
        """
        Compute inter-station coherence γ²
        
        γ²(ω) = |G₁₂(ω)|² / [G₁₁(ω) · G₂₂(ω)] ∈ [0, 1]
        
        Parameters
        ----------
        station1_spectra : np.ndarray
            Complex pressure spectrum for station 1
        station2_spectra : np.ndarray
            Complex pressure spectrum for station 2
        frequencies : np.ndarray
            Frequency array (Hz)
        
        Returns
        -------
        np.ndarray
            Coherence γ²(ω)
        """
        # Implementation
        pass
    
    def _dolph_chebyshev_weights(self, n_stations: int, sidelobe_level: float = -30):
        """Compute Dolph-Chebyshev weighting coefficients"""
        # Implementation
        pass
```

---

📚 Contributing to Documentation

Documentation Structure

```
docs/
├── api/                    # API documentation
│   ├── physics.md
│   ├── processing.md
│   └── sensors.md
├── tutorials/              # Step-by-step tutorials
│   ├── quickstart.md
│   ├── single-station.md
│   ├── multi-station.md
│   └── case-studies/
│       ├── hurricane-irma.md
│       ├── hunga-tonga.md
│       └── tornado-outbreak.md
├── explanations/           # Conceptual guides
│   ├── microbarom-theory.md
│   ├── stratospheric-ducting.md
│   ├── wavelet-transform.md
│   └── aisi-explained.md
├── theory/                 # Theoretical foundations
│   ├── helmholtz-equation.md
│   ├── beamforming.md
│   └── coherence-analysis.md
├── references/             # Technical references
│   ├── parameters.md
│   ├── equations.md
│   ├── thresholds.md
│   └── sensors-specs.md
└── contributing/           # Contribution guides
    └── style-guide.md
```

Docstring Style (NumPy/Google)

```python
def compute_aisi(parameters: Dict[str, float], weights: Optional[Dict] = None) -> float:
    """
    Calculate Atmospheric Infrasonic Severity Index from eight parameters.
    
    The AISI is a weighted composite of normalized parameter values,
    ranging from 0 (background) to 1 (critical severe weather).
    
    Parameters
    ----------
    parameters : Dict[str, float]
        Dictionary containing the eight INFRAS-CLOUD parameters:
        - P_ub : Microbarom amplitude (Pa)
        - D_str : Stratospheric ducting efficiency (unitless)
        - f_p : Spectral peak frequency (Hz)
        - theta : Azimuthal arrival angle (degrees)
        - v_ph : Phase velocity (m/s)
        - alpha_air : Atmospheric absorption coefficient (dB/km)
        - gamma2 : Inter-station coherence (0-1)
        - SNR : Signal-to-noise ratio (dB)
    
    weights : Optional[Dict]
        Custom weights for each parameter. If None, uses PCA-derived
        weights from the 1,847-event training catalogue:
        w = {'P_ub': 0.18, 'D_str': 0.14, 'f_p': 0.21, 'theta': 0.15,
             'v_ph': 0.12, 'alpha_air': 0.07, 'gamma2': 0.08, 'SNR': 0.05}
    
    Returns
    -------
    float
        Atmospheric Infrasonic Severity Index (0-1)
    
    Examples
    --------
    >>> params = {
    ...     'P_ub': 0.25, 'D_str': 0.18, 'f_p': 0.22, 'theta': 0.15,
    ...     'v_ph': 0.12, 'alpha_air': 0.07, 'gamma2': 0.08, 'SNR': 0.05
    ... }
    >>> aisi = compute_aisi(params)
    >>> print(f"{aisi:.2f}")
    0.84
    
    Notes
    -----
    Reference thresholds:
    - AISI ≥ 0.80: CRITICAL - immediate meteorological alert
    - 0.55 ≤ AISI < 0.80: ELEVATED - increased monitoring
    - AISI < 0.55: BACKGROUND - routine monitoring
    
    References
    ----------
    .. [1] Baladi, S. (2026). INFRAS-CLOUD Research Paper.
           DOI: 10.5281/zenodo.18952438
    """
    pass
```

Building Documentation Locally

```bash
# Install documentation tools
pip install mkdocs mkdocs-material mkdocstrings[python] pymdown-extensions

# Build docs
mkdocs build

# Serve locally
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

---

🧪 Testing Guidelines

Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── physics/
│   │   ├── test_microbarom.py
│   │   ├── test_ducting.py
│   │   ├── test_aisi.py
│   │   └── test_helmholtz.py
│   ├── processing/
│   │   ├── test_wavelet.py
│   │   ├── test_beamforming.py
│   │   └── test_coherence.py
│   └── sensors/
│       ├── test_mb2005.py
│       └── test_paros.py
├── integration/            # Integration tests
│   ├── test_full_pipeline.py
│   ├── test_event_detection.py
│   └── test_beamforming_network.py
├── validation/             # Validation against IMS data
│   ├── test_irma_2017.py
│   ├── test_hunga_tonga_2022.py
│   └── test_outbreak_2011.py
└── conftest.py             # Shared fixtures
```

Writing Tests

```python
# tests/unit/physics/test_microbarom.py
import pytest
import numpy as np
from infrascloud.physics.microbarom import MicrobaromAmplitude, MicrobaromParams

class TestMicrobaromAmplitude:
    """Test suite for microbarom amplitude calculations"""
    
    @pytest.mark.parametrize("wave_height,expected_range", [
        (1.5, (0.01, 0.05)),   # Minimal detection
        (3.0, (0.05, 0.15)),   # Tropical storm
        (6.0, (0.15, 0.35)),   # Hurricane
        (10.0, (0.35, 0.60)),  # Major hurricane
    ])
    def test_pub_range(self, wave_height, expected_range):
        """Test microbarom amplitude range for different wave heights"""
        # Create synthetic wave spectrum
        params = MicrobaromParams(
            wave_height=wave_height,
            wave_period=10.0,
            wind_speed=20.0,
            fetch=500e3
        )
        
        microbarom = MicrobaromAmplitude()
        p_ub = microbarom.compute(params)
        
        assert expected_range[0] <= p_ub <= expected_range[1]
    
    def test_quadratic_scaling(self):
        """Test P_ub ∝ H_s² scaling"""
        params1 = MicrobaromParams(wave_height=2.0)
        params2 = MicrobaromParams(wave_height=4.0)
        
        microbarom = MicrobaromAmplitude()
        p1 = microbarom.compute(params1)
        p2 = microbarom.compute(params2)
        
        # Should be approximately 4x
        ratio = p2 / p1
        assert 3.8 <= ratio <= 4.2
    
    def test_validation_against_irma_2017(self):
        """Test model validation with Hurricane Irma data"""
        # Load IS42 data from September 2017
        # Verify r² ≥ 0.91 against NHC central pressure
        pass

# tests/unit/processing/test_wavelet.py
class TestWaveletProcessor:
    """Test suite for wavelet transform processing"""
    
    def test_frequency_chirp_detection(self):
        """Test detection of tornado vortex frequency chirp"""
        # Generate synthetic chirp signal
        fs = 20
        t = np.arange(0, 600, 1/fs)  # 10 minutes
        f0, f1 = 0.5, 2.0  # Chirp from 0.5 to 2.0 Hz
        chirp = signal.chirp(t, f0, t[-1], f1, method='quadratic')
        
        processor = WaveletProcessor(fs=fs)
        frequencies, scalogram = processor.compute_scalogram(chirp)
        
        chirp_detected, rate = processor.detect_frequency_chirp(scalogram, t)
        
        assert chirp_detected
        assert rate > 0  # Positive chirp rate
    
    def test_fp_extraction(self):
        """Test spectral peak frequency extraction"""
        # Generate 0.2 Hz microbarom signal
        fs = 20
        t = np.arange(0, 3600, 1/fs)  # 1 hour
        signal = np.sin(2 * np.pi * 0.2 * t)
        
        processor = WaveletProcessor(fs=fs)
        frequencies, scalogram = processor.compute_scalogram(signal)
        
        f_p = processor.extract_fp(scalogram, frequencies, (0, 3600))
        
        assert 0.19 <= f_p <= 0.21  # Should detect 0.2 Hz
```

Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=infrascloud --cov-report=html

# Run specific test file
pytest tests/unit/physics/test_microbarom.py -v

# Run tests matching pattern
pytest -k "wavelet"

# Run with parallel execution
pytest -n auto

# Run validation tests only
pytest tests/validation/ -v

# Run slow tests
pytest -m "slow"
```

---

🌪️ Data Contributions

Contributing New Event Data

If you have infrasonic data from severe weather events that could help validate INFRAS-CLOUD:

1. Prepare your data in the required format:

```python
# Required columns for CSV export
# timestamp, station_id, P_ub, D_str, f_p, theta, v_ph, alpha_air, gamma2, SNR, AISI, event_type, event_flag
```

1. Include metadata:

```yaml
event:
  type: "tropical_cyclone"  # or tornado/volcanic/earthquake/microbarom
  name: "Hurricane Name"
  date: "2025-09-15"
  location:
    latitude: XX.XXX
    longitude: YY.YYY
  intensity: "Category 4"  # or EF-scale/VEI/Mw
  verification_source: "NHC best-track"  # independent verification
  verification_doi: "10.xxxx/xxxxx"
  
station:
  id: "ISXX"
  network: "IMS"
  latitude: XX.XXX
  longitude: YY.YYY
  instrumentation: "MB2005"
  
contributor:
  name: "Your Name"
  affiliation: "Your Institution"
  email: "your.email@institution.org"
  orcid: "0000-0000-0000-0000"
  reference: "DOI or citation if published"
```

1. Data format example:

```csv
timestamp,station_id,P_ub,D_str,f_p,theta,v_ph,alpha_air,gamma2,SNR,AISI,event_type,event_flag
2025-09-15T00:00:00Z,IS42,0.12,0.08,0.18,145,335,0.002,0.45,12,0.42,tropical_cyclone,0
2025-09-15T01:00:00Z,IS42,0.14,0.09,0.18,146,334,0.002,0.48,13,0.45,tropical_cyclone,0
...
2025-09-18T00:00:00Z,IS42,0.28,0.15,0.21,158,342,0.003,0.72,18,0.76,tropical_cyclone,0
2025-09-18T12:00:00Z,IS42,0.35,0.18,0.22,162,345,0.003,0.81,22,0.91,tropical_cyclone,1  # Peak intensity
```

1. Submit via pull request to the data/contributions/ directory

---

🔀 Pull Request Process

PR Checklist

· Code follows project style guide
· Tests added/updated and passing
· Documentation updated
· CHANGELOG.md updated
· All CI checks passing
· Reviewed by at least one maintainer
· Physics changes validated against IMS data (if applicable)
· Performance benchmarks meet targets (if applicable)

PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactor
- [ ] Data contribution

## Related Issues
Closes #XXX

## Physics Changes (if applicable)
- [ ] Equations modified
- [ ] Constants updated
- [ ] Validation against IMS data (r² ≥ 0.90)
- [ ] Documentation updated with equations

## Signal Processing Changes (if applicable)
- [ ] Algorithm modified
- [ ] Performance benchmarks
- [ ] Test coverage ≥ 80%
- [ ] Documentation updated

## Data Contribution (if applicable)
- [ ] Data format validated
- [ ] Metadata complete
- [ ] Independent verification source provided
- [ ] License compatible

## Testing Performed
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] IMS data validation
- [ ] Performance benchmarks

## Additional Notes
Any additional information reviewers should know
```

Review Process

1. Automated Checks: CI runs tests, linting, type checking
2. Code Review: At least one maintainer reviews
3. Physics Review: For changes to core equations
4. Documentation Review: For documentation changes
5. Data Validation: For data contributions

---

🌍 Community Guidelines

Communication Channels

· GitHub Issues: Bug reports, feature requests
· GitHub Discussions: Q&A, ideas, community support
· Email: gitdeeper@gmail.com (project lead)
· ORCID: 0009-0003-8903-0029

Recognition

Contributors are recognized in:

· AUTHORS.md
· Release notes
· Academic publications (where applicable)

Research Contributions

If you use INFRAS-CLOUD in your research:

1. Cite the paper: Baladi, S. (2026). INFRAS-CLOUD. DOI: 10.5281/zenodo.18952438
2. Share your data/code when possible
3. Submit a case study to our repository

---

📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to INFRAS-CLOUD! 🌪️

For questions: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
