"""DuctingAnalyzer - Stratospheric duct characterization"""

import numpy as np
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class AtmosphereProfile:
    """Atmospheric profile data"""
    altitude: np.ndarray  # Altitude (km)
    temperature: np.ndarray  # Temperature (K)
    pressure: np.ndarray  # Pressure (Pa)
    wind_u: np.ndarray  # Zonal wind (m/s)
    wind_v: np.ndarray  # Meridional wind (m/s)


class DuctingAnalyzer:
    """
    Stratospheric duct characterization and inversion
    
    D_str = [c_eff(z_strat) - c_eff(z_0)] / c_eff(z_0) = Δc_eff / c_0
    """
    
    def __init__(self):
        self.gamma = 1.4  # Adiabatic index of air
        self.R = 287.0  # Specific gas constant (J/(kg·K))
    
    def effective_sound_speed(self, 
                              temperature: float,
                              wind_vector: Tuple[float, float],
                              direction: float) -> float:
        """
        Compute effective sound speed
        
        c_eff(z, θ) = √(γ R T(z)) + u(z) · n̂
        
        Parameters
        ----------
        temperature : float
            Temperature at altitude (K)
        wind_vector : tuple
            (u, v) wind components (m/s)
        direction : float
            Propagation direction (degrees)
        
        Returns
        -------
        float
            Effective sound speed (m/s)
        """
        # Convert direction to radians
        theta_rad = np.radians(direction)
        
        # Compute acoustic speed
        c_acoustic = np.sqrt(self.gamma * self.R * temperature)
        
        # Compute wind projection
        u, v = wind_vector
        n_hat = np.array([np.sin(theta_rad), np.cos(theta_rad)])
        wind_projection = u * n_hat[0] + v * n_hat[1]
        
        return c_acoustic + wind_projection
    
    def invert_from_phase_velocity(self,
                                  vph: float,
                                  elevation_profile: AtmosphereProfile,
                                  direction: float = 0.0) -> float:
        """
        Invert stratospheric ducting efficiency from phase velocity
        
        Parameters
        ----------
        vph : float
            Observed phase velocity (m/s)
        elevation_profile : AtmosphereProfile
            Atmospheric profile data
        direction : float
            Propagation direction (degrees)
        
        Returns
        -------
        float
            Stratospheric ducting efficiency D_str
        """
        # Find altitude of maximum effective sound speed
        c_eff_profile = []
        for i, alt in enumerate(elevation_profile.altitude):
            wind = (elevation_profile.wind_u[i], 
                   elevation_profile.wind_v[i])
            c_eff = self.effective_sound_speed(
                elevation_profile.temperature[i],
                wind,
                direction
            )
            c_eff_profile.append(c_eff)
        
        c_eff_profile = np.array(c_eff_profile)
        z_strat_idx = np.argmax(c_eff_profile)
        
        # Get surface and stratospheric values
        c_eff_surface = c_eff_profile[0]
        c_eff_strat = c_eff_profile[z_strat_idx]
        
        # Compute ducting efficiency
        d_str = (c_eff_strat - c_eff_surface) / c_eff_surface
        
        return d_str
    
    def detect_ssw_event(self, 
                        d_str_timeseries: np.ndarray,
                        threshold: float = -0.05) -> Tuple[bool, int]:
        """
        Detect sudden stratospheric warming event from D_str timeseries
        
        Parameters
        ----------
        d_str_timeseries : np.ndarray
            Time series of D_str values
        threshold : float
            Threshold for SSW detection
        
        Returns
        -------
        detected : bool
            True if SSW detected
        onset_idx : int
            Index of SSW onset
        """
        # Look for rapid negative shift
        diff = np.diff(d_str_timeseries)
        negative_shifts = np.where(diff < threshold)[0]
        
        if len(negative_shifts) > 0:
            return True, negative_shifts[0]
        
        return False, -1
