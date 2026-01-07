"""
Script to load LLC4320 salinity data across multiple timesteps and save it locally.

This script loads salinity data from the LLC4320 dataset for a specified region
(latitude/longitude range) and depth range, across multiple timesteps, and saves
the data to the data folder.

Configuration variables (modify before running):
- QUALITY: Data quality/resolution level (-8 recommended for balance)
- NUMBER_OF_TIME_STEPS: Number of timesteps to load (10312 total available)
- LAT_RANGE: Latitude range [min, max] in degrees
- LON_RANGE: Longitude range [min, max] in degrees
- Z_RANGE: Depth level range [min, max] (0-89 available, 90 total levels)
"""

import os
import sys
import numpy as np
import xarray as xr
import openvisuspy as ovp
from pathlib import Path

# ============================================================================
# CONFIGURATION VARIABLES - Modify these before running
# ============================================================================

QUALITY = -12  # Data quality level (-8 recommended for balance)
NUMBER_OF_TIME_STEPS = 10312  # Number of timesteps to load (max: 10312)

# Latitude and longitude range (in degrees)
# Example: Australian region from LLC4320_metadata.ipynb
LAT_RANGE = [-40, -10]  # [min_lat, max_lat]
LON_RANGE = [105, 160]  # [min_lon, max_lon]

# Depth level range (z indices: 0-89, 90 total levels)
# Use [0, 1] for surface only, [0, 10] for first 10 levels, etc.
Z_RANGE = [0, 1]  # [min_z, max_z] - loads depth levels min_z to (max_z-1)

# ============================================================================
# SALINITY DATA URL
# ============================================================================

SALINITY_URL = "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/salt/salt_llc4320_x_y_depth.idx"

# ============================================================================
# PATHS
# ============================================================================

# Get the project root directory (parent of scripts folder)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LATLON_FILE = DATA_DIR / "llc4320_latlon.nc"

# ============================================================================
# FUNCTIONS
# ============================================================================


def extract_data_by_latlon_range(
  db, lat_center, lon_center, lat_range, lon_range, z_range, quality, timestep
):
  """
  Extract data for a specific timestep using latitude/longitude range.

  Parameters:
  -----------
  db : openvisuspy dataset object
      Pre-loaded dataset (loaded once globally)
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

  # Extract lat/lon for the region (only needed once, but return for consistency)
  lat = lat_center[y_min:y_max, x_min:x_max]
  lon = lon_center[y_min:y_max, x_min:x_max]

  # Read data for this timestep
  # Note: time parameter only accepts single value, not range
  try:
    data = db.db.read(
      time=timestep, x=[x_min, x_max], y=[y_min, y_max], z=z_range, quality=quality
    )
    return data, lat, lon
  except Exception as e:
    raise RuntimeError(f"Failed to read data at timestep {timestep}: {e}") from e


def load_salinity_data():
  """
  Main function to load salinity data across multiple timesteps.

  Returns:
  --------
  data : np.ndarray
      Stacked data array with shape (time, z, y, x)
  lat : np.ndarray
      Latitude coordinates for the region
  lon : np.ndarray
      Longitude coordinates for the region
  """
  print("=" * 70)
  print("LLC4320 Salinity Data Loading Script")
  print("=" * 70)
  print("\nConfiguration:")
  print(f"  Quality level: {QUALITY}")
  print(f"  Number of timesteps: {NUMBER_OF_TIME_STEPS}")
  print(f"  Latitude range: {LAT_RANGE}")
  print(f"  Longitude range: {LON_RANGE}")
  print(
    f"  Depth range (z indices): {Z_RANGE} (levels {Z_RANGE[0]} to {Z_RANGE[1] - 1})"
  )
  print(f"  Total depth levels: {Z_RANGE[1] - Z_RANGE[0]}")

  # Check if lat/lon file exists
  if not LATLON_FILE.exists():
    raise FileNotFoundError(
      f"Latitude/longitude file not found: {LATLON_FILE}\n"
      f"Please download llc4320_latlon.nc to the data folder.\n"
      f"See notebooks/LLC4320_metadata.ipynb for download instructions."
    )

  # Load latitude and longitude coordinates
  print(f"\nLoading coordinates from {LATLON_FILE}...")
  ds = xr.open_dataset(LATLON_FILE)
  lat_center = ds["latitude"].values
  lon_center = ds["longitude"].values
  ds.close()
  print(f"  Coordinate arrays loaded: shape {lat_center.shape}")

  # Load dataset once (globally) - this is the key optimization!
  print(f"\nLoading dataset from {SALINITY_URL}...")
  print("  (This is done once and reused for all timesteps)")
  db_salinity = ovp.LoadDataset(SALINITY_URL)
  print("  ✓ Dataset loaded successfully!")

  # Load first timestep to get shape
  print(f"\nLoading first timestep to determine data shape...")
  print("  (This may take a moment for the initial connection...)")
  first_data, lat, lon = extract_data_by_latlon_range(
    db_salinity,
    lat_center,
    lon_center,
    LAT_RANGE,
    LON_RANGE,
    Z_RANGE,
    QUALITY,
    timestep=0,
  )
  print(f"  First timestep shape: {first_data.shape}")
  print(f"  Spatial region shape: {lat.shape}")

  # Determine expected final shape
  expected_shape = (
    NUMBER_OF_TIME_STEPS,
    first_data.shape[0],
    first_data.shape[1],
    first_data.shape[2],
  )
  print(f"\nExpected final data shape: {expected_shape}")
  print(f"  - Time dimension: {NUMBER_OF_TIME_STEPS}")
  print(f"  - Depth dimension: {first_data.shape[0]}")
  print(f"  - Y dimension: {first_data.shape[1]}")
  print(f"  - X dimension: {first_data.shape[2]}")

  # Estimate data size
  data_size_gb = np.prod(expected_shape) * 4 / (1024**3)  # float32 = 4 bytes
  print(f"\nEstimated data size: {data_size_gb:.2f} GB")
  print(f"  (assuming float32, {np.prod(expected_shape):,} total elements)")

  # Load all timesteps
  print(f"\nLoading {NUMBER_OF_TIME_STEPS} timesteps...")
  print("  This may take a while...")

  timesteps = []
  for t in range(NUMBER_OF_TIME_STEPS):
    # Print progress every 100 timesteps or for first few
    if (t + 1) % 100 == 0 or t == 0 or (t + 1) <= 5:
      print(f"  Loading timestep {t + 1}/{NUMBER_OF_TIME_STEPS}...")

    try:
      timestep_data, _, _ = extract_data_by_latlon_range(
        db_salinity,
        lat_center,
        lon_center,
        LAT_RANGE,
        LON_RANGE,
        Z_RANGE,
        QUALITY,
        timestep=t,
      )
      timesteps.append(timestep_data)
      
      if (t + 1) % 100 == 0 or t == 0:
        print(f"  ✓ Timestep {t + 1} loaded (shape: {timestep_data.shape})")
    except Exception as e:
      print(f"\n  ✗ Error loading timestep {t + 1}: {e}")
      import traceback
      traceback.print_exc()
      raise

  # Stack timesteps along time axis
  print(f"\nStacking timesteps...")
  data = np.stack(timesteps, axis=0)

  print(f"\nFinal data shape: {data.shape}")
  print(f"  - Time: {data.shape[0]}")
  print(f"  - Depth: {data.shape[1]}")
  print(f"  - Y: {data.shape[2]}")
  print(f"  - X: {data.shape[3]}")

  return data, lat, lon


def save_data(data, lat, lon):
  """
  Save the loaded data to the data folder.

  Parameters:
  -----------
  data : np.ndarray
      Data array with shape (time, z, y, x)
  lat : np.ndarray
      Latitude coordinates
  lon : np.ndarray
      Longitude coordinates
  """
  # Ensure data directory exists
  DATA_DIR.mkdir(exist_ok=True)

  # Create output filenames
  output_data_file = DATA_DIR / "salinity_data.npy"
  output_lat_file = DATA_DIR / "salinity_lat.npy"
  output_lon_file = DATA_DIR / "salinity_lon.npy"

  print(f"\nSaving data to {DATA_DIR}...")

  # Save data
  print(f"  Saving data array to {output_data_file}...")
  np.save(output_data_file, data)

  # Save coordinates
  print(f"  Saving latitude coordinates to {output_lat_file}...")
  np.save(output_lat_file, lat)

  print(f"  Saving longitude coordinates to {output_lon_file}...")
  np.save(output_lon_file, lon)

  # Report file sizes
  data_size_mb = output_data_file.stat().st_size / (1024**2)
  print(f"\nSaved files:")
  print(f"  {output_data_file.name}: {data_size_mb:.2f} MB")
  print(
    f"  {output_lat_file.name}: {output_lat_file.stat().st_size / (1024**2):.2f} MB"
  )
  print(
    f"  {output_lon_file.name}: {output_lon_file.stat().st_size / (1024**2):.2f} MB"
  )
  print(f"  Total: {data_size_mb:.2f} MB")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
  try:
    # Set up OpenVisus cache
    cache_dir = PROJECT_ROOT / ".visus_cache_can_be_deleted"
    os.environ["VISUS_CACHE"] = str(cache_dir)
    cache_dir.mkdir(exist_ok=True)

    # Load data
    data, lat, lon = load_salinity_data()

    # Save data
    save_data(data, lat, lon)

    print("\n" + "=" * 70)
    print("Data loading completed successfully!")
    print("=" * 70)

  except KeyboardInterrupt:
    print("\n\nScript interrupted by user.")
    sys.exit(1)
  except Exception as e:
    print(f"\n\nError: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
