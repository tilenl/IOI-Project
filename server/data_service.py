"""
Data service layer for loading and serving LLC4320 data from OpenVisus servers.

This module handles data loading directly from OpenVisus endpoints, caching,
and serialization for the Flask API.
"""

import numpy as np
import xarray as xr
import openvisuspy as ovp
from pathlib import Path
import base64
import os
from typing import Dict, Any, Optional, Tuple

# Field URLs for OpenVisus access
FIELD_URLS = {
    "salinity": "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/salt/salt_llc4320_x_y_depth.idx",
    "temperature": "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/theta/theta_llc4320_x_y_depth.idx",
    "vertical_velocity": "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/w/w_llc4320_x_y_depth.idx",
    "salt": "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/salt/salt_llc4320_x_y_depth.idx",
    "theta": "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/theta/theta_llc4320_x_y_depth.idx",
    "w": "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/w/w_llc4320_x_y_depth.idx",
}


class DataService:
    """
    Service class for managing LLC4320 data access via OpenVisus.
    
    Handles loading data directly from OpenVisus servers and provides methods
    for retrieving data slices in various formats. Dataset objects are cached
    for performance.
    """
    
    def __init__(self, data_dir: Optional[Path] = None, cache_dir: Optional[Path] = None):
        """
        Initialize the data service.
        
        Parameters:
        -----------
        data_dir : Path, optional
            Directory containing coordinate data (llc4320_latlon.nc).
            Defaults to project data/ directory.
        cache_dir : Path, optional
            Directory for OpenVisus cache. Defaults to project root.
        """
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        
        # Coordinate file path
        self.latlon_file = self.data_dir / "llc4320_latlon.nc"
        print(f"PATH to llc4320_latlon.nc file: {self.latlon_file}")
        
        # Set up OpenVisus cache
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / ".visus_cache_can_be_deleted"
        os.environ["VISUS_CACHE"] = str(cache_dir)
        cache_dir.mkdir(exist_ok=True)
        
        # Cache for loaded datasets (field_name -> dataset object)
        self._datasets = {}
        
        # Cache for coordinates (loaded once)
        self._lat_center = None
        self._lon_center = None
    
    def _load_coordinates(self):
        """Load latitude/longitude coordinates from NetCDF file."""
        if self._lat_center is None or self._lon_center is None:
            if not self.latlon_file.exists():
                raise FileNotFoundError(
                    f"Coordinate file not found: {self.latlon_file}\n"
                    "Please download llc4320_latlon.nc to the data folder.\n"
                    "See notebooks/LLC4320_metadata.ipynb for download instructions."
                )
            print(f"Loading coordinates from {self.latlon_file}...")
            ds = xr.open_dataset(self.latlon_file)
            print(f"Coordinates loaded from {self.latlon_file} successfully!")
            self._lat_center = ds["latitude"].values
            self._lon_center = ds["longitude"].values
            ds.close()
    
    def _get_dataset(self, field: str):
        """
        Get or load OpenVisus dataset for a field.
        
        Parameters:
        -----------
        field : str
            Field name (salinity, temperature, vertical_velocity, salt, theta, w)
        
        Returns:
        --------
        openvisuspy dataset object
        """
        # Normalize field name
        field_lower = field.lower()
        if field_lower not in FIELD_URLS:
            raise ValueError(
                f"Unknown field: {field}. Available fields: {list(FIELD_URLS.keys())}"
            )
        
        # Return cached dataset if available
        if field_lower in self._datasets:
            return self._datasets[field_lower]
        
        # Load dataset from server
        url = FIELD_URLS[field_lower]
        print(f"Loading dataset for field '{field}' from {url}...")
        dataset = ovp.LoadDataset(url)
        self._datasets[field_lower] = dataset
        print("  Dataset loaded successfully!")
        
        return dataset
    
    def _extract_data_by_latlon_range(
        self,
        db,
        lat_center: np.ndarray,
        lon_center: np.ndarray,
        lat_range: list,
        lon_range: list,
        z_range: list,
        quality: int,
        timestep: int
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Extract data for a specific timestep using latitude/longitude range.
        
        Parameters:
        -----------
        db : openvisuspy dataset object
            Pre-loaded dataset
        lat_center : np.ndarray
            Latitude coordinate array
        lon_center : np.ndarray
            Longitude coordinate array
        lat_range : list
            [min_lat, max_lat] in degrees
        lon_range : list
            [min_lon, max_lon] in degrees
        z_range : list
            [min_z, max_z] depth level indices
        quality : int
            Data quality level
        timestep : int
            Timestep index
        
        Returns:
        --------
        data : np.ndarray
            Extracted data array
        lat : np.ndarray
            Latitude coordinates for the region
        lon : np.ndarray
            Longitude coordinates for the region
        """
        # Create mask for lat/lon range
        mask = (
            (lat_center >= lat_range[0])
            & (lat_center <= lat_range[1])
            & (lon_center >= lon_range[0])
            & (lon_center <= lon_range[1])
        )
        
        y_indices, x_indices = np.where(mask)
        
        if len(x_indices) == 0 or len(y_indices) == 0:
            raise ValueError("No data found in the given lat/lon range.")
        
        x_min = int(x_indices.min())
        x_max = int(x_indices.max()) + 1
        y_min = int(y_indices.min())
        y_max = int(y_indices.max()) + 1
        
        # Extract lat/lon for the region
        lat = lat_center[y_min:y_max, x_min:x_max]
        lon = lon_center[y_min:y_max, x_min:x_max]
        
        # Read data for this timestep
        try:
            data = db.db.read(
                time=timestep,
                x=[x_min, x_max],
                y=[y_min, y_max],
                z=z_range,
                quality=quality
            )
            return data, lat, lon
        except Exception as e:
            raise RuntimeError(f"Failed to read data at timestep {timestep}: {e}") from e
    
    def get_metadata(self, field: str = "salinity") -> Dict[str, Any]:
        """
        Get metadata about a dataset field.
        
        Parameters:
        -----------
        field : str
            Field name (salinity, temperature, vertical_velocity, etc.)
        
        Returns:
        --------
        dict : Metadata dictionary with dataset information.
        """
        db = self._get_dataset(field)
        
        # Get dataset dimensions and timesteps
        logic_box = db.getLogicBox()
        timesteps = db.getTimesteps()
        field_info = db.getField()
        
        return {
            "field": field_info.name if hasattr(field_info, 'name') else field,
            "dimensions": {
                "x": int(logic_box[1][0]) if len(logic_box) > 1 and len(logic_box[1]) > 0 else None,
                "y": int(logic_box[1][1]) if len(logic_box) > 1 and len(logic_box[1]) > 1 else None,
                "z": int(logic_box[1][2]) if len(logic_box) > 1 and len(logic_box[1]) > 2 else None,
            },
            "total_timesteps": len(timesteps),
            "data_type": "float32",
            "available_fields": list(FIELD_URLS.keys()),
            "field_units": {
                "salinity": "g kg⁻¹",
                "salt": "g kg⁻¹",
                "temperature": "°C",
                "theta": "°C",
                "vertical_velocity": "m s⁻¹",
                "w": "m s⁻¹"
            }
        }
    
    def get_data_slice(
        self,
        field: str,
        timestep: int,
        depth_level: int,
        lat_range: list,
        lon_range: list,
        quality: int = -12,
        format_type: str = "array"
    ) -> Dict[str, Any]:
        """
        Get a 2D slice of data for a specific timestep and depth level.
        
        Parameters:
        -----------
        field : str
            Field name (salinity, temperature, vertical_velocity, etc.)
        timestep : int
            Timestep index
        depth_level : int
            Depth level index
        lat_range : list
            [min_lat, max_lat] in degrees
        lon_range : list
            [min_lon, max_lon] in degrees
        quality : int
            Data quality level (default: -12 for faster loading)
        format_type : str
            Response format: 'array' (nested lists) or 'base64' (base64-encoded)
        
        Returns:
        --------
        dict : Dictionary with data array and coordinates
        """
        self._load_coordinates()
        db = self._get_dataset(field)
        
        # Extract data for the specified region
        z_range = [depth_level, depth_level + 1]
        data, lat, lon = self._extract_data_by_latlon_range(
            db, self._lat_center, self._lon_center,
            lat_range, lon_range, z_range, quality, timestep
        )
        
        # Extract 2D slice (remove depth dimension if it's 1)
        if len(data.shape) == 4:
            data_slice = data[0, 0, :, :]  # (time, z, y, x) -> (y, x)
        elif len(data.shape) == 3:
            data_slice = data[0, :, :]  # (z, y, x) -> (y, x)
        else:
            data_slice = data
        
        # Serialize data based on format
        if format_type == "base64":
            # Convert to base64 for more efficient transfer
            data_bytes = data_slice.astype(np.float32).tobytes()
            data_b64 = base64.b64encode(data_bytes).decode('utf-8')
            data_serialized = {
                "format": "base64",
                "dtype": "float32",
                "shape": list(data_slice.shape),
                "data": data_b64
            }
        else:
            # Convert to nested lists (JSON-serializable)
            data_serialized = {
                "format": "array",
                "data": data_slice.tolist()
            }
        
        return {
            "field": field,
            "timestep": timestep,
            "depth_level": depth_level,
            "data": data_serialized,
            "coordinates": {
                "latitude": lat.tolist(),
                "longitude": lon.tolist()
            },
            "shape": list(data_slice.shape),
            "lat_range": lat_range,
            "lon_range": lon_range,
            "quality": quality
        }
    
    def get_timestep_data(
        self,
        field: str,
        timestep: int,
        lat_range: list,
        lon_range: list,
        z_range: list = [0, 1],
        quality: int = -12,
        format_type: str = "array"
    ) -> Dict[str, Any]:
        """
        Get data for a specific timestep across multiple depth levels (3D data: depth, y, x).
        
        Parameters:
        -----------
        field : str
            Field name (salinity, temperature, vertical_velocity, etc.)
        timestep : int
            Timestep index
        lat_range : list
            [min_lat, max_lat] in degrees
        lon_range : list
            [min_lon, max_lon] in degrees
        z_range : list
            [min_z, max_z] depth level indices (default: [0, 1] for surface only)
        quality : int
            Data quality level (default: -12 for faster loading)
        format_type : str
            Response format: 'array' or 'base64'
        
        Returns:
        --------
        dict : Dictionary with 3D data array and coordinates
        """
        self._load_coordinates()
        db = self._get_dataset(field)
        
        # Extract data for the specified region
        data, lat, lon = self._extract_data_by_latlon_range(
            db, self._lat_center, self._lon_center,
            lat_range, lon_range, z_range, quality, timestep
        )
        
        # Remove time dimension if present (should be single timestep)
        if len(data.shape) == 4:
            timestep_data = data[0, :, :, :]  # (time, z, y, x) -> (z, y, x)
        else:
            timestep_data = data
        
        # Serialize data
        if format_type == "base64":
            data_bytes = timestep_data.astype(np.float32).tobytes()
            data_b64 = base64.b64encode(data_bytes).decode('utf-8')
            data_serialized = {
                "format": "base64",
                "dtype": "float32",
                "shape": list(timestep_data.shape),
                "data": data_b64
            }
        else:
            data_serialized = {
                "format": "array",
                "data": timestep_data.tolist()
            }
        
        return {
            "field": field,
            "timestep": timestep,
            "data": data_serialized,
            "coordinates": {
                "latitude": lat.tolist(),
                "longitude": lon.tolist()
            },
            "shape": list(timestep_data.shape),
            "lat_range": lat_range,
            "lon_range": lon_range,
            "z_range": z_range,
            "quality": quality
        }
    
