"""Geographic utilities for source localization"""

import numpy as np


def azimuth(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Compute azimuth from point 1 to point 2
    
    Parameters
    ----------
    lat1, lon1 : float
        Coordinates of point 1 (degrees)
    lat2, lon2 : float
        Coordinates of point 2 (degrees)
    
    Returns
    -------
    float
        Azimuth angle (degrees, 0-360)
    """
    # Convert to radians
    lat1_r = np.radians(lat1)
    lat2_r = np.radians(lat2)
    lon1_r = np.radians(lon1)
    lon2_r = np.radians(lon2)
    
    # Compute azimuth
    dlon = lon2_r - lon1_r
    x = np.sin(dlon) * np.cos(lat2_r)
    y = (np.cos(lat1_r) * np.sin(lat2_r) - 
         np.sin(lat1_r) * np.cos(lat2_r) * np.cos(dlon))
    
    az = np.arctan2(x, y)
    az_deg = np.degrees(az)
    
    # Convert to 0-360 range
    return (az_deg + 360) % 360


def great_circle_distance(lat1: float, lon1: float, 
                         lat2: float, lon2: float) -> float:
    """
    Compute great circle distance using Haversine formula
    
    Parameters
    ----------
    lat1, lon1 : float
        Coordinates of point 1 (degrees)
    lat2, lon2 : float
        Coordinates of point 2 (degrees)
    
    Returns
    -------
    float
        Distance (km)
    """
    R = 6371.0  # Earth radius (km)
    
    # Convert to radians
    lat1_r = np.radians(lat1)
    lat2_r = np.radians(lat2)
    dlat = lat2_r - lat1_r
    dlon = np.radians(lon2 - lon1)
    
    # Haversine formula
    a = (np.sin(dlat/2)**2 + 
         np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon/2)**2)
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c


def triangulate(azimuths: np.ndarray, 
               station_coords: np.ndarray) -> tuple:
    """
    Triangulate source position from multiple azimuths
    
    Parameters
    ----------
    azimuths : np.ndarray
        Array of azimuth angles (degrees)
    station_coords : np.ndarray
        Array of (lat, lon) station coordinates
    
    Returns
    -------
    lat : float
        Estimated source latitude
    lon : float
        Estimated source longitude
    uncertainty : float
        Position uncertainty (km)
    """
    # TODO: Implement least squares triangulation
    # For now, return average
    center_lat = np.mean([c[0] for c in station_coords])
    center_lon = np.mean([c[1] for c in station_coords])
    uncertainty = 150.0  # km
    
    return center_lat, center_lon, uncertainty


def geographic_prior(event_type: str, lat: float, lon: float) -> float:
    """
    Compute geographic prior probability for event type
    
    Parameters
    ----------
    event_type : str
        Type of event
    lat : float
        Latitude (degrees)
    lon : float
        Longitude (degrees)
    
    Returns
    -------
    float
        Prior probability
    """
    if event_type == 'tropical_cyclone':
        # Tropical cyclones occur in specific latitude bands
        if -30 <= lat <= 30:
            return 0.9
        else:
            return 0.1
    
    elif event_type == 'volcanic_explosion':
        # Volcanoes occur at plate boundaries
        # Simplified - would need actual volcano database
        return 0.5
    
    elif event_type == 'large_earthquake':
        # Earthquakes at plate boundaries
        return 0.7
    
    else:
        return 0.5
