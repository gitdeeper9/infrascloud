"""Inter-station Coherence (γ²) - Statistical wave analysis"""

import numpy as np
from typing import Tuple, Optional
from scipy import signal


class InterStationCoherence:
    """
    Inter-station coherence calculator
    
    γ²(ω) = |G₁₂(ω)|² / [G₁₁(ω) · G₂₂(ω)] ∈ [0, 1]
    """
    
    def __init__(self, fs: float = 20.0, nperseg: int = 256):
        """
        Initialize coherence calculator
        
        Parameters
        ----------
        fs : float
            Sampling frequency (Hz)
        nperseg : int
            Length of each segment for coherence estimation
        """
        self.fs = fs
        self.nperseg = nperseg
    
    def compute(self,
               signal1: np.ndarray,
               signal2: np.ndarray,
               frequencies: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute coherence between two signals
        
        Parameters
        ----------
        signal1 : np.ndarray
            First signal
        signal2 : np.ndarray
            Second signal
        frequencies : np.ndarray, optional
            Frequency array (if None, will be computed)
        
        Returns
        -------
        freqs : np.ndarray
            Frequency array
        coherence : np.ndarray
            Coherence γ²(ω)
        """
        # Compute coherence using Welch's method
        freqs, coherence = signal.coherence(
            signal1, signal2,
            fs=self.fs,
            nperseg=self.nperseg,
            noverlap=self.nperseg // 2
        )
        
        return freqs, coherence
    
    def detect_event(self,
                    coherence: np.ndarray,
                    freq_band: Tuple[float, float],
                    threshold: float = 0.6,
                    min_bins: int = 3) -> Tuple[bool, float, int]:
        """
        Detect coherent event based on coherence threshold
        
        Parameters
        ----------
        coherence : np.ndarray
            Coherence array
        freq_band : tuple
            Frequency band of interest (fmin, fmax)
        threshold : float
            Coherence threshold for detection
        min_bins : int
            Minimum number of frequency bins above threshold
        
        Returns
        -------
        detected : bool
            True if event detected
        max_coherence : float
            Maximum coherence in band
        n_above : int
            Number of bins above threshold
        """
        # Find indices in frequency band
        # For now, assume coherence corresponds to full band
        band_coherence = coherence
        
        # Count bins above threshold
        above_threshold = band_coherence >= threshold
        n_above = np.sum(above_threshold)
        
        # Maximum coherence
        max_coherence = np.max(band_coherence) if len(band_coherence) > 0 else 0.0
        
        # Detection condition
        detected = n_above >= min_bins and max_coherence >= threshold
        
        return detected, max_coherence, n_above
    
    def array_coherence(self, signals: np.ndarray) -> np.ndarray:
        """
        Compute average coherence across array
        
        Parameters
        ----------
        signals : np.ndarray
            Array of signals, shape (n_signals, n_samples)
        
        Returns
        -------
        np.ndarray
            Average coherence across all pairs
        """
        n_signals = signals.shape[0]
        coherence_sum = 0.0
        n_pairs = 0
        
        for i in range(n_signals):
            for j in range(i + 1, n_signals):
                freqs, coh = self.compute(signals[i], signals[j])
                coherence_sum += coh
                n_pairs += 1
        
        return coherence_sum / n_pairs if n_pairs > 0 else np.zeros_like(freqs)
