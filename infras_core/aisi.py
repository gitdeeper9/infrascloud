"""Atmospheric Infrasonic Severity Index (AISI) - Composite index"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AISIParameters:
    """All eight AISI parameters"""
    P_ub: float  # Microbarom amplitude (Pa)
    D_str: float  # Stratospheric ducting efficiency
    f_p: float  # Spectral peak frequency (Hz)
    theta: float  # Azimuthal arrival angle (degrees)
    v_ph: float  # Phase velocity (m/s)
    alpha_air: float  # Atmospheric absorption (dB/km)
    gamma2: float  # Inter-station coherence
    SNR: float  # Signal-to-noise ratio (dB)


@dataclass
class AISIResult:
    """AISI calculation result"""
    value: float
    alert_level: str
    parameters: Dict[str, float]
    weights: Dict[str, float]
    uncertainty: float


class AISI:
    """
    Atmospheric Infrasonic Severity Index
    
    AISI = w₁·P*_ub + w₂·D*_str + w₃·f*_p + w₄·θ* + w₅·v*_ph +
           w₆·α*_air + w₇·γ²* + w₈·SNR*
    
    Default weights (PCA-regularized logistic regression on 1,847-event catalogue):
    w₁=0.18, w₂=0.14, w₃=0.21, w₄=0.15, w₅=0.12, w₆=0.07, w₇=0.08, w₈=0.05
    """
    
    # Default weights from the research paper
    DEFAULT_WEIGHTS = {
        'P_ub': 0.18,
        'D_str': 0.14,
        'f_p': 0.21,
        'theta': 0.15,
        'v_ph': 0.12,
        'alpha_air': 0.07,
        'gamma2': 0.08,
        'SNR': 0.05
    }
    
    # Parameter normalization ranges
    PARAM_RANGES = {
        'P_ub': (0.0, 1.0),  # Pa
        'D_str': (-0.1, 0.3),  # unitless
        'f_p': (0.01, 10.0),  # Hz
        'theta': (0.0, 360.0),  # degrees
        'v_ph': (300.0, 360.0),  # m/s
        'alpha_air': (0.0, 0.01),  # dB/km
        'gamma2': (0.0, 1.0),  # unitless
        'SNR': (0.0, 30.0)  # dB
    }
    
    # Alert thresholds
    CRITICAL_THRESHOLD = 0.80
    ELEVATED_THRESHOLD = 0.55
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize AISI calculator
        
        Parameters
        ----------
        weights : dict, optional
            Custom weights for each parameter
        """
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        self._validate_weights()
    
    def _validate_weights(self):
        """Validate that weights sum to 1.0"""
        total = sum(self.weights.values())
        if not np.isclose(total, 1.0, rtol=1e-3):
            raise ValueError(f"Weights must sum to 1.0, got {total}")
    
    def compute(self, params: AISIParameters) -> AISIResult:
        """
        Compute AISI from eight parameters
        
        Parameters
        ----------
        params : AISIParameters
            All eight AISI parameters
        
        Returns
        -------
        AISIResult
            AISI calculation result
        """
        # Convert to dictionary for easier handling
        param_dict = {
            'P_ub': params.P_ub,
            'D_str': params.D_str,
            'f_p': params.f_p,
            'theta': params.theta,
            'v_ph': params.v_ph,
            'alpha_air': params.alpha_air,
            'gamma2': params.gamma2,
            'SNR': params.SNR
        }
        
        # Normalize each parameter
        normalized = {}
        for name, value in param_dict.items():
            normalized[name] = self._normalize_parameter(name, value)
        
        # Compute weighted sum
        aisi_value = 0.0
        for name, weight in self.weights.items():
            aisi_value += weight * normalized[name]
        
        # Ensure [0, 1] range
        aisi_value = np.clip(aisi_value, 0.0, 1.0)
        
        # Determine alert level
        alert_level = self._get_alert_level(aisi_value)
        
        # Estimate uncertainty based on parameter variability
        uncertainty = self._estimate_uncertainty(normalized)
        
        return AISIResult(
            value=aisi_value,
            alert_level=alert_level,
            parameters=param_dict,
            weights=self.weights,
            uncertainty=uncertainty
        )
    
    def _normalize_parameter(self, name: str, value: float) -> float:
        """Normalize parameter to [0, 1] range"""
        if name not in self.PARAM_RANGES:
            return value
        
        min_val, max_val = self.PARAM_RANGES[name]
        
        # Special handling for theta (circular)
        if name == 'theta':
            # Normalize angle to [0, 1]
            return value / 360.0
        
        # Clamp to range
        value = np.clip(value, min_val, max_val)
        
        # Linear normalization
        normalized = (value - min_val) / (max_val - min_val)
        
        return normalized
    
    def _get_alert_level(self, aisi: float) -> str:
        """Get alert level based on AISI value"""
        if aisi >= self.CRITICAL_THRESHOLD:
            return "CRITICAL"
        elif aisi >= self.ELEVATED_THRESHOLD:
            return "ELEVATED"
        else:
            return "BACKGROUND"
    
    def _estimate_uncertainty(self, normalized_params: Dict[str, float]) -> float:
        """Estimate AISI uncertainty based on parameter variability"""
        # Simple uncertainty model: standard deviation of normalized parameters
        values = list(normalized_params.values())
        return float(np.std(values))
    
    @classmethod
    def from_json(cls, json_file: str) -> 'AISI':
        """Load AISI configuration from JSON file"""
        import json
        with open(json_file, 'r') as f:
            data = json.load(f)
        return cls(weights=data.get('weights'))
    
    def compute_batch(self, params_list: list) -> list:
        """Compute AISI for multiple parameter sets"""
        return [self.compute(p) for p in params_list]
