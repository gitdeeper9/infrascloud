"""Microbarom Amplitude (P_ub) - Ocean-atmosphere coupling energy"""

import numpy as np
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class WaveSpectrum:
    """Ocean wave spectrum parameters"""
    significant_wave_height: float  # H_s (m)
    peak_period: float  # T_p (s)
    mean_direction: float  # θ_w (degrees)
    directional_spread: float  # σ_θ (degrees)


class MicrobaromAmplitude:
    """
    Microbarom amplitude calculator
    
    P_ub(ω) = ρ_air · c · ∫∫ F(k, ω/2) · F(-k, ω/2) · G(r, ω) d²k
    """
    
    def __init__(self):
        self.rho_air = 1.225  # Sea-level air density (kg/m³)
        self.c = 340.0  # Mean sound speed (m/s)
        self.g = 9.81  # Gravity (m/s²)
    
    def compute(self, 
               wave_spectrum: WaveSpectrum,
               distance: float,
               ducting_efficiency: float = 1.0) -> float:
        """
        Compute microbarom amplitude
        
        Parameters
        ----------
        wave_spectrum : WaveSpectrum
            Ocean wave spectrum parameters
        distance : float
            Source-receiver distance (km)
        ducting_efficiency : float
            Stratospheric ducting efficiency D_str
        
        Returns
        -------
        float
            Microbarom amplitude P_ub (Pa)
        """
        # P_ub ∝ H_s² (quadratic scaling)
        h_s = wave_spectrum.significant_wave_height
        
        # Frequency depends on wave period (f = 1/T_p)
        f_microbarom = 2.0 / wave_spectrum.peak_period  # Double frequency
        
        # Geometric spreading
        geometric_factor = 1.0 / (distance * 1000) if distance > 0 else 1.0
        
        # Ducting efficiency
        ducting_factor = max(0.1, ducting_efficiency)
        
        # Compute amplitude
        p_ub = (self.rho_air * self.c * 
                (h_s ** 2) * 
                geometric_factor * 
                ducting_factor * 
                1e-6)  # Scale factor
        
        return min(1.0, max(0.0, p_ub))
    
    def estimate_storm_position(self,
                               p_ub_values: np.ndarray,
                               azimuths: np.ndarray,
                               station_lat: float,
                               station_lon: float) -> Tuple[float, float, float]:
        """
        Estimate storm position from microbarom measurements
        
        Parameters
        ----------
        p_ub_values : np.ndarray
            Microbarom amplitudes from multiple stations
        azimuths : np.ndarray
            Arrival azimuths (degrees)
        station_lat : float
            Station latitude
        station_lon : float
            Station longitude
        
        Returns
        -------
        storm_lat : float
            Estimated storm latitude
        storm_lon : float
            Estimated storm longitude
        uncertainty : float
            Position uncertainty (km)
        """
        # TODO: Implement multi-station triangulation
        # For now, return random position
        storm_lat = station_lat + np.random.uniform(-10, 10)
        storm_lon = station_lon + np.random.uniform(-10, 10)
        uncertainty = np.random.uniform(100, 200)
        
        return storm_lat, storm_lon, uncertainty
    
    def significant_wave_height(self, p_ub: float, distance: float) -> float:
        """
        Invert significant wave height from microbarom amplitude
        
        H_s = √(P_ub / (ρ_air · c · G · ducting_factor))
        
        Parameters
        ----------
        p_ub : float
            Microbarom amplitude (Pa)
        distance : float
            Source-receiver distance (km)
        
        Returns
        -------
        float
            Estimated significant wave height (m)
        """
        # Invert the quadratic relationship
        geometric_factor = distance * 1000
        h_s = np.sqrt(p_ub * geometric_factor / (self.rho_air * self.c * 1e-6))
        return h_s
