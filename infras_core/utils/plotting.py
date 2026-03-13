"""Plotting utilities for visualization"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Tuple


def plot_scalogram(times: np.ndarray,
                  frequencies: np.ndarray,
                  scalogram: np.ndarray,
                  title: str = "Wavelet Scalogram",
                  figsize: Tuple[int, int] = (10, 6),
                  save_path: Optional[str] = None):
    """
    Plot wavelet scalogram
    
    Parameters
    ----------
    times : np.ndarray
        Time array (s)
    frequencies : np.ndarray
        Frequency array (Hz)
    scalogram : np.ndarray
        Wavelet power spectrum
    title : str
        Plot title
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    im = ax.pcolormesh(times, frequencies, scalogram,
                       shading='gouraud', cmap='viridis')
    
    ax.set_yscale('log')
    ax.set_ylim(frequencies.min(), frequencies.max())
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title(title)
    
    plt.colorbar(im, ax=ax, label='Power')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_beam_map(theta: np.ndarray,
                 vph: np.ndarray,
                 beam_power: np.ndarray,
                 title: str = "Beamforming Power Map",
                 figsize: Tuple[int, int] = (8, 6),
                 save_path: Optional[str] = None):
    """
    Plot beamforming power map
    
    Parameters
    ----------
    theta : np.ndarray
        Azimuth angles (degrees)
    vph : np.ndarray
        Phase velocities (m/s)
    beam_power : np.ndarray
        Beam power for each (theta, vph)
    title : str
        Plot title
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    Theta, Vph = np.meshgrid(theta, vph)
    im = ax.pcolormesh(Theta, Vph, beam_power.T,
                       shading='gouraud', cmap='hot')
    
    ax.set_xlabel('Azimuth θ (degrees)')
    ax.set_ylabel('Phase Velocity v_ph (m/s)')
    ax.set_title(title)
    
    plt.colorbar(im, ax=ax, label='Beam Power')
    
    # Mark maximum
    max_idx = np.unravel_index(np.argmax(beam_power), beam_power.shape)
    ax.plot(theta[max_idx[1]], vph[max_idx[0]], 'b*', markersize=15,
            label=f'Peak: θ={theta[max_idx[1]]:.1f}°, v={vph[max_idx[0]]:.1f} m/s')
    ax.legend()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_aisi_timeseries(times: np.ndarray,
                        aisi_values: np.ndarray,
                        events: Optional[list] = None,
                        title: str = "AISI Timeseries",
                        figsize: Tuple[int, int] = (12, 6),
                        save_path: Optional[str] = None):
    """
    Plot AISI timeseries with thresholds
    
    Parameters
    ----------
    times : np.ndarray
        Time array
    aisi_values : np.ndarray
        AISI values
    events : list, optional
        List of event times to mark
    title : str
        Plot title
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(times, aisi_values, 'b-', linewidth=1.5, label='AISI')
    
    # Threshold lines
    ax.axhline(y=0.80, color='r', linestyle='--', label='Critical (0.80)')
    ax.axhline(y=0.55, color='orange', linestyle='--', label='Elevated (0.55)')
    
    # Fill regions
    ax.fill_between(times, 0.80, 1.0, alpha=0.2, color='red')
    ax.fill_between(times, 0.55, 0.80, alpha=0.2, color='orange')
    
    # Mark events
    if events:
        for event_time in events:
            ax.axvline(x=event_time, color='green', linestyle=':', alpha=0.7)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('AISI')
    ax.set_title(title)
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_station_map(stations: dict,
                    source: Optional[tuple] = None,
                    title: str = "Station Map",
                    figsize: Tuple[int, int] = (10, 8),
                    save_path: Optional[str] = None):
    """
    Plot station locations on map
    
    Parameters
    ----------
    stations : dict
        Dictionary with station coordinates
    source : tuple, optional
        (lat, lon) of source
    title : str
        Plot title
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot stations
    for name, (lat, lon) in stations.items():
        ax.plot(lon, lat, '^', markersize=10, color='blue')
        ax.text(lon + 0.5, lat + 0.5, name, fontsize=8)
    
    # Plot source
    if source:
        ax.plot(source[1], source[0], '*', markersize=15, color='red',
                label='Source')
    
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
