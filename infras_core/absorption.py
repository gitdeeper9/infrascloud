"""Atmospheric Absorption Coefficient (α_air) - Thermodynamic profiling"""

import numpy as np
from typing import Optional
from dataclasses import dataclass


@dataclass
class AtmosphericState:
    """Atmospheric state parameters"""
    temperature: float  # Temperature (K)
    pressure: float  # Pressure (Pa)
    humidity: float  # Relative humidity (0-1)
    co2_concentration: float = 400e-6  # CO2 concentration (ppm)


class AtmosphericAbsorption:
    """
    Atmospheric absorption coefficient calculator
    
    α_air = (ω² / 2ρc³) · [4η/3 + ζ + κ(1/C_v - 1/C_p)] ∝ f²
    """
    
    def __init__(self):
        self.R = 287.0  # Specific gas constant (J/(kg·K))
        self.C_p = 1005.0  # Specific heat at constant pressure (J/(kg·K))
        self.C_v = 718.0  # Specific heat at constant volume (J/(kg·K))
        self.gamma = self.C_p / self.C_v  # Adiabatic index
    
    def compute(self, 
               frequency: float,
               state: AtmosphericState,
               distance: float = 1.0) -> float:
        """
        Compute atmospheric absorption coefficient
        
        Parameters
        ----------
        frequency : float
            Frequency (Hz)
        state : AtmosphericState
            Atmospheric state parameters
        distance : float
            Propagation distance (km)
        
        Returns
        -------
        float
            Absorption coefficient α_air (dB/km)
        """
        # ω = 2πf
        omega = 2 * np.pi * frequency
        
        # Air density
        rho = state.pressure / (self.R * state.temperature)
        
        # Sound speed
        c = np.sqrt(self.gamma * self.R * state.temperature)
        
        # Classical absorption terms
        # Dynamic viscosity η (simplified)
        eta = 1.8e-5 * (state.temperature / 293.0) ** 0.7
        
        # Bulk viscosity ζ (approximation)
        zeta = 0.6 * eta
        
        # Thermal conductivity κ
        kappa = 0.026 * (state.temperature / 293.0) ** 0.8
        
        # Molecular absorption (humidity dependent)
        molecular_term = self._molecular_absorption(frequency, state)
        
        # Classical absorption
        classical_term = (omega**2 / (2 * rho * c**3)) * (
            (4*eta/3) + zeta + kappa * (1/self.C_v - 1/self.C_p)
        )
        
        # Total absorption (dB per km)
        alpha = (classical_term + molecular_term) * 1000 * 8.686  # Convert to dB/km
        
        return alpha * distance
    
    def _molecular_absorption(self, frequency: float, state: AtmosphericState) -> float:
        """
        Compute molecular absorption due to oxygen and nitrogen
        
        Based on ISO 9613-1 standard
        """
        # Simplified model - TODO: Implement full ISO 9613-1
        T = state.temperature
        T0 = 293.15
        T01 = 273.16
        
        # Saturation vapor pressure
        psat = 610.94 * np.exp(17.625 * (T - 273.15) / (T - 273.15 + 243.04))
        
        # Molar concentration of water vapor
        h = state.humidity * psat / state.pressure
        
        # Oxygen relaxation frequency
        frO = (state.pressure / 101325) * (24 + 4.04e4 * h * 
              (0.02 + h) / (0.391 + h))
        
        # Nitrogen relaxation frequency
        frN = (state.pressure / 101325) * np.sqrt(T / T0) * (
              9 + 280 * h * np.exp(-4.17 * ((T0 / T)**(1/3) - 1)))
        
        # Molecular absorption coefficient
        alpha_mol = (1.84e-11 * (state.pressure / 101325) * np.sqrt(T / T0) +
                     (T0 / T)**(5/2) * (
                         0.01275 * np.exp(-2239.1 / T) * frO /
                         (frO**2 + frequency**2) +
                         0.1068 * np.exp(-3352 / T) * frN /
                         (frN**2 + frequency**2)
                     ))
        
        return alpha_mol
    
    def temperature_from_absorption(self,
                                   alpha: float,
                                   frequency: float,
                                   pressure: float,
                                   humidity: float) -> float:
        """
        Estimate temperature from absorption measurement
        
        Parameters
        ----------
        alpha : float
            Measured absorption (dB/km)
        frequency : float
            Frequency (Hz)
        pressure : float
            Pressure (Pa)
        humidity : float
            Relative humidity (0-1)
        
        Returns
        -------
        float
            Estimated temperature (K)
        """
        # TODO: Implement temperature inversion
        # For now, return typical value
        return 288.15
