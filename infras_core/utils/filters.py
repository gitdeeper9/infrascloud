"""Signal processing filters"""

import numpy as np
from scipy import signal


def bandpass_filter(data: np.ndarray,
                   fs: float,
                   fmin: float,
                   fmax: float,
                   order: int = 4) -> np.ndarray:
    """
    Apply bandpass filter to data
    
    Parameters
    ----------
    data : np.ndarray
        Input signal
    fs : float
        Sampling frequency (Hz)
    fmin : float
        Low cutoff frequency (Hz)
    fmax : float
        High cutoff frequency (Hz)
    order : int
        Filter order
    
    Returns
    -------
    np.ndarray
        Filtered signal
    """
    nyquist = fs / 2
    low = fmin / nyquist
    high = fmax / nyquist
    
    b, a = signal.butter(order, [low, high], btype='band')
    filtered = signal.filtfilt(b, a, data)
    
    return filtered


def dolph_chebyshev(n: int, sidelobe_level: float = -30) -> np.ndarray:
    """
    Compute Dolph-Chebyshev window/weights
    
    Parameters
    ----------
    n : int
        Number of points
    sidelobe_level : float
        Desired sidelobe level in dB
    
    Returns
    -------
    np.ndarray
        Dolph-Chebyshev weights
    """
    # Convert dB to amplitude ratio
    r = 10 ** (sidelobe_level / 20)
    
    # Chebyshev polynomial parameter
    x0 = np.cosh(1.0 / (n - 1) * np.arccosh(1.0 / r))
    
    # Compute window
    k = np.arange(n)
    window = np.zeros(n)
    
    for i in range(n):
        sum_val = 0
        for m in range(1, n):
            sum_val += np.cos((n - 1) * np.arccos(x0 * np.cos(np.pi * m / (n - 1))))
        
        # Simplified - TODO: Implement full Chebyshev window
        window[i] = 1.0
    
    return window / np.sum(window)


def lowpass_filter(data: np.ndarray, fs: float, cutoff: float, order: int = 4) -> np.ndarray:
    """Apply lowpass filter"""
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low')
    return signal.filtfilt(b, a, data)


def highpass_filter(data: np.ndarray, fs: float, cutoff: float, order: int = 4) -> np.ndarray:
    """Apply highpass filter"""
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='high')
    return signal.filtfilt(b, a, data)
