# Changelog

All notable changes to the INFRAS-CLOUD project will be documented in this file.

**DOI:** 10.5281/zenodo.18952438  
**Repository:** github.com/gitdeeper9/infrascloud  
**Web Dashboard:** infrascloud.netlify.app

---

## [1.0.0] - 2026-03-11

### 🚀 Initial Release
- Publication of INFRAS-CLOUD research paper
- Release of complete 8-parameter physics framework
- Open access data from 47 IMS stations (2005-2025)
- 1,847 validated severe weather events
- Interactive web dashboard at infrascloud.netlify.app

### Added

#### Core Physics Engine
- **Microbarom Amplitude (P_ub)**: Ocean-atmosphere coupling energy
  - P_ub = ρ_air · c · ∫∫ F(k, ω/2) · F(-k, ω/2) · G(r, ω) d²k
  - Ocean wave height estimation: ±0.5 m accuracy
  - Storm position tracking: ±150 km at 6,000 km range
  - Microbarom detection at H_s ≥ 1.5 m

- **Stratospheric Ducting Efficiency (D_str)**: Transoceanic propagation
  - D_str = [c_eff(z_strat) - c_eff(z_0)] / c_eff(z_0)
  - Stratospheric wind speed: ±7.8 m/s accuracy (r²=0.91 vs. radiosonde)
  - Sudden stratospheric warming detection
  - Phase velocity inversion: σ_v ≈ ±5-15 m/s

- **Spectral Peak Frequency (f_p)**: Event-type discrimination
  - f_p = c_fluid / (2·L_source) (resonant cavity sources)
  - f_p = Γ / (2π·r²) (vortex acoustic sources)
  - f_p = 1 / T_pulse (impulsive sources)
  - 6-class event classification: 93.1% accuracy

- **Azimuthal Arrival Angle (θ)**: Source localization
  - B(k, ω) = Σᵢ wᵢ · pᵢ(ω) · exp(+i k · rᵢ)
  - Azimuthal accuracy: σ_θ ≈ ±2-5°
  - Mobile source tracking

- **Phase Velocity (v_ph)**: Stratospheric wind structure
  - Effective sound speed profiling
  - Stratospheric temperature inversion
  - Wind speed at 30-50 km altitude

- **Atmospheric Absorption (α_air)**: Thermodynamic profiling
  - α_air = (ω² / 2ρc³) · [4η/3 + ζ + κ(1/C_v - 1/C_p)] ∝ f²
  - Humidity and temperature profiling
  - Frequency-dependent energy loss

- **Inter-station Coherence (γ²)**: Event validation
  - γ²(ω) = |G₁₂(ω)|² / [G₁₁(ω) · G₂₂(ω)] ∈ [0, 1]
  - Detection threshold: γ² ≥ 0.60
  - Noise discrimination

- **Signal-to-Noise Ratio (SNR)**: Source discrimination
  - Natural vs. anthropogenic source classification
  - Array sensitivity characterization

- **Atmospheric Infrasonic Severity Index (AISI)**: Eight-parameter composite
  - AISI = 0.18·P*_ub + 0.14·D*_str + 0.21·f*_p + 0.15·θ* + 0.12·v*_ph + 0.07·α*_air + 0.08·γ²* + 0.05·SNR*
  - Critical threshold: AISI ≥ 0.80 (immediate meteorological alert)
  - Elevated alert: AISI 0.55-0.79 (increased monitoring)
  - Background: AISI < 0.55 (routine)

#### Processing Pipeline
- **InfrasProcessor**: Real-time CWT spectral analysis
  - Morlet wavelet with ω₀ = 6
  - Adaptive time-frequency resolution
  - 60-second latency from acquisition to output

- **BeamFormer**: Multi-station f-k beamforming
  - Dolph-Chebyshev weighting
  - 2D frequency-wavenumber analysis
  - 256-s windows with 75% overlap

- **DuctingAnalyzer**: Stratospheric duct characterization
  - Real-time D_str inversion
  - Stratospheric wind estimation
  - SSW event detection

- **AIEventClassifier**: Physics-informed neural network
  - 8-parameter input → 3 hidden layers (64, 32, 16) → 6-class softmax
  - Trained on 1,847 verified events
  - AUC = 0.97 (cross-validated)

#### Validation Dataset
- **Total Events**: 1,847 (2005-2025)
- **Tropical Cyclones**: 312 (max range 9,400 km)
- **Mesoscale Convective Systems**: 487 (max range 6,200 km)
- **Volcanic Explosions**: 234 (max range 12,000 km)
- **Large Earthquakes**: 198 (Mw 6.5+, max range 8,000 km)
- **Oceanic Microbaroms**: 428 (max range 6,000 km)
- **Tornadoes**: 188 (EF1+, max range 280 km)

#### Case Studies
- **Hurricane Irma (2017)**: 12-day continuous AISI record
  - 9-day precursor before Category 5
  - r² = 0.91 vs. central pressure
  - Position accuracy ±225 km at 3,000 km

- **Hunga Tonga-Hunga Haʻapai (2022)**: Global infrasonic propagation
  - Source energy: 38 ± 4 megatons TNT
  - 47 station pairs for wind field mapping
  - 90-minute global stratospheric snapshot

- **Super Outbreak (2011)**: 218 tornadoes
  - Detection rate: 87.2% (41/47 within range)
  - Mean lead time: 16.4 ± 8.2 minutes
  - All EF5: AISI > 0.80 at 22+ minutes

- **Superstorm Sandy (2012)**: Microbarom monitoring
  - 7-day precursor before landfall
  - P_ub: 2.8× above background
  - Extratropical transition identified 12 hours early

- **Kilauea 2018**: Volcanic infrasound
  - Deep harmonic tremor: 11-day precursor
  - 1:2:3 harmonic series (0.07, 0.14, 0.21 Hz)
  - Magmatic column length: 2,400 m

- **North Atlantic Gravity Waves (2020)**: First published field measurement
  - v_ph = 285 m/s at θ = 287°
  - γ² = 0.73 across 2,200 km separation
  - ±9 m/s vs. ECMWF ERA5

#### Performance Metrics
| Metric | Value | Target |
|--------|-------|--------|
| 6-class Event Classification | 93.1% | ≥90% |
| Tropical Cyclone Detection Range | 4,200 km | ≥4,000 km |
| Tornado Precursor Lead Time | 12-28 min | ≥10 min |
| Volcanic Event Energy (r²) | 0.944 | ≥0.90 |
| Stratospheric Wind Accuracy | ±7.8 m/s | ±10 m/s |
| Ocean Storm Position | ±147 km | ±200 km |
| False Detection Rate | 3.2% | ≤5% |

#### Sensor Integration
- MB2005 microbarometer (CEA/DAM France)
  - Frequency response: 0.005-27 Hz
  - Dynamic range: 120 dB
  - Noise floor: < 10⁻³ Pa/√Hz

- Paroscientific 6000-16B-IS
  - Frequency: 0.001-5 Hz
  - Resolution: 0.001 Pa
  - Dynamic range: 140 dB

- Nanometrics Centaur digitizer
  - 24-bit resolution
  - GPS timing: ±100 ns
  - MiniSEED output

- Vaisala WXT536 weather station
  - Temperature, humidity, pressure, wind
  - Required for α_air correction

#### Deployment Options
- Single-station deployment
- Multi-station network (3+ stations)
- Global IMS network integration
- Real-time processing with 60-second latency
- Docker containers for all services
- Netlify web dashboard
- PyPI package: `pip install infrascloud`

#### Documentation
- Complete API reference
- Installation guide (INSTALL.md)
- Deployment guide (DEPLOY.md)
- Contributing guidelines (CONTRIBUTING.md)
- Code of conduct (CODE_OF_CONDUCT.md)
- Jupyter notebooks for all case studies
- Sensor calibration protocols

---

## [0.9.0] - 2026-02-15

### ⚠️ Pre-release Candidate

### Added
- Beta version of all core modules
- Validation against 30 IMS stations
- Preliminary AISI weight determination
- Basic sensor drivers
- Initial documentation

### Changed
- Refined microbarom inversion algorithms
- Updated wavelet transform parameters
- Improved beamforming resolution

### Fixed
- Array synchronization issues
- Spectral decomposition artifacts
- Coherence calculation edge cases

---

## [0.8.0] - 2026-01-20

### 🧪 Alpha Release

### Added
- Prototype physics modules
- Test deployments at 10 IMS stations
- Basic data collection pipeline
- Preliminary AISI formulation
- Initial case study implementations

---

## [0.5.0] - 2025-09-15

### 🏗️ Development Milestone

### Added
- Microbarom amplitude module
- Basic beamforming implementation
- Spectral analysis tools
- Data ingestion from IMS archive

---

## [0.1.0] - 2025-06-01

### 🎯 Project Initiation

### Added
- Project concept and framework design
- Initial 8-parameter selection
- Literature review compilation
- Research proposal development
- IMS data access agreements

---

## 🔮 Future Releases

### [1.1.0] - Planned Q3 2026
- Additional validation events (2025-2026)
- Machine learning emulators for fast inversion
- Real-time satellite data integration
- Mobile app for field operators
- Extended tornado detection range (<50 km arrays)

### [1.2.0] - Planned Q1 2027
- ISS Infrasound Monitoring (ISIM) payload integration
- Space-based atmospheric acoustic observatory
- Global real-time AISI maps
- Automated alert system with NOAA/ECMWF integration

### [2.0.0] - Planned 2028
- 100+ station global network
- AI-powered precursor prediction
- Climate change acoustic monitoring
- Operational weather service integration

---

## 📊 Version History

| Version | Date | Status | DOI |
|---------|------|--------|-----|
| 1.0.0 | 2026-03-11 | Stable Release | 10.5281/zenodo.18952438 |
| 0.9.0 | 2026-02-15 | Release Candidate | 10.5281/zenodo.18852438 |
| 0.8.0 | 2026-01-20 | Alpha | 10.5281/zenodo.18752438 |
| 0.5.0 | 2025-09-15 | Development | - |
| 0.1.0 | 2025-06-01 | Concept | - |

---

For questions or contributions: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
