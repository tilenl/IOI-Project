# LLC4320 Data Access and Streamlines Processing Analysis

## Executive Summary

This document analyzes how data is accessed from the LLC4320 dataset endpoints and outlines the requirements and approach for processing this data to create beautiful streamline visualizations as described in the [Beautiful Streamlines paper](https://www.allnans.com/jekyll/update/2018/04/04/beautiful-streamlines.html).

**Key Finding**: Only three fields are available: temperature (`theta`), salinity (`salt`), and vertical velocity (`w`). **Horizontal velocity components (u, v) are NOT available**, which presents a challenge for traditional 2D streamline visualization.

---

## 1. Data Access Method

### 1.1 Access Framework
- **Framework**: OpenVisus (via `openvisuspy` Python library)
- **Access Method**: Direct HTTPS access (not OSDF/Pelican, which returns empty content)
- **Base URLs**: 
  - Climate1: `https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/`
  - Climate2: `https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate2/llc4320/idx/`

### 1.2 Data Structure
The LLC4320 dataset uses a **4-dimensional structure**:
- **Time**: Multiple timesteps (each timestep >30GB)
- **Z (Depth)**: 90 vertical levels (depth layers)
- **Y**: 12,960 grid points (latitude-like dimension)
- **X**: 17,280 grid points (longitude-like dimension)

**Data Shape**: `(time, z, y, x)` when loaded via `db.db.read()`, but actual field shape is `(17280, 12960, 90)` = `(X, Y, Depth)`

### 1.3 Coordinate System
- **Array-based indexing**: Data accessed using `x`, `y`, `z` array indices
- **Geographic coordinates**: Latitude/longitude mapping available via `llc4320_latlon.nc` NetCDF file
- **Coordinate extraction**: Functions exist to convert between array indices and lat/lon ranges

---

## 2. Available Data Fields

### 2.1 Confirmed Available Fields

Based on the dataset metadata, **only three fields are available**:

| Field | Variable Name | Unit | Standard Name | Shape | Dimensions |
|-------|--------------|------|---------------|-------|------------|
| **Temperature** | `theta` | °C | Temperature | `(17280, 12960, 90)` | Latitude, Longitude, Depth |
| **Salinity** | `salt` | g kg⁻¹ | Salinity | `(17280, 12960, 90)` | Latitude, Longitude, Depth |
| **Vertical Velocity** | `w` | m s⁻¹ | Vertical velocity | `(17280, 12960, 90)` | Latitude, Longitude, Depth |

**All fields are `float32` data type.**

### 2.2 Field Access Pattern

All fields follow the same access pattern:
```
https://[server]/nasa/nsdf/[climate]/llc4320/idx/[field]/[field]_llc4320_x_y_depth.idx
```

**Available endpoints**:
- Temperature: `https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/theta/theta_llc4320_x_y_depth.idx`
- Salinity: `https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/salt/salt_llc4320_x_y_depth.idx`
- Vertical Velocity: `https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/w/w_llc4320_x_y_depth.idx`

### 2.3 Data Loading Example

```python
import openvisuspy as ovp

# Load dataset
temperature_url = "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/theta/theta_llc4320_x_y_depth.idx"
db = ovp.LoadDataset(temperature_url)

# Read data with parameters:
# - time: timestep index (default: 0)
# - z: depth range [min, max] (default: all levels)
# - x: x-range [min, max] (default: all)
# - y: y-range [min, max] (default: all)
# - quality: resolution/quality level (default: full resolution, -12 for lower quality)
data = db.db.read(time=0, z=[0, 1], x=[500, 2500], y=[8500, 11000], quality=-6)
```

---

## 3. Streamlines Visualization Challenge

### 3.1 Traditional Streamlines Requirements

For 2D streamline visualization, we typically need:

1. **Horizontal Velocity Components**:
   - **U (zonal velocity)**: East-west component of horizontal velocity
   - **V (meridional velocity)**: North-south component of horizontal velocity

2. **Coordinate Information**:
   - **Latitude/Longitude**: For geographic mapping
   - **Grid spacing**: For proper streamline density and spacing

3. **Optional but Useful**:
   - **Scalar field overlay**: Temperature or salinity for color-coding streamlines
   - **Depth level selection**: For visualizing flow at specific ocean depths

### 3.2 Critical Limitation

**⚠️ Important Finding**: The dataset **does NOT contain horizontal velocity components (u, v)**. Only vertical velocity (w) is available.

This means:
- **Traditional 2D streamlines cannot be created directly** from the available data
- Alternative visualization approaches must be considered
- The beautiful streamlines paper's techniques may need to be adapted or alternative methods explored

### 3.3 Alternative Visualization Approaches

Since horizontal velocity is not available, consider these alternatives:

#### Option 1: Vertical Velocity Streamlines
- Visualize **vertical motion patterns** using the `w` field
- Create streamlines showing upwelling/downwelling regions
- Less conventional but could reveal interesting vertical circulation patterns

#### Option 2: Gradient-Based Flow Visualization
- Use **temperature or salinity gradients** to infer flow direction
- Compute gradients: `∇theta` or `∇salt` to create pseudo-velocity fields
- Visualize as streamlines based on gradient directions
- **Note**: This is an approximation and may not represent actual flow

#### Option 3: Scalar Field Visualization with Motion Indicators
- Focus on **temperature/salinity visualization** with motion cues
- Use color, contours, and other techniques from the beautiful streamlines paper
- Add visual indicators of vertical motion (w) as overlay
- Create rich visualizations without traditional streamlines

#### Option 4: 3D Volume Visualization
- Use vertical velocity (w) in a **3D context**
- Create volume renderings showing vertical motion through depth
- Combine with temperature/salinity for multi-variable visualization

---

## 4. Data Processing Pipeline

### 4.1 Loading Available Fields

```python
import openvisuspy as ovp
import numpy as np
import xarray as xr

# Load vertical velocity
w_url = "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/w/w_llc4320_x_y_depth.idx"
db_w = ovp.LoadDataset(w_url)

# Load temperature (for overlay)
theta_url = "https://nsdf-climate1-origin.nationalresearchplatform.org:50098/nasa/nsdf/climate1/llc4320/idx/theta/theta_llc4320_x_y_depth.idx"
db_theta = ovp.LoadDataset(theta_url)

# Select region and depth level
x_range = [500, 2500]
y_range = [8500, 11000]
z_level = [0, 1]  # Surface level
time = 0

w_data = db_w.db.read(time=time, z=z_level, x=x_range, y=y_range, quality=-6)[0, 0, :, :]
theta_data = db_theta.db.read(time=time, z=z_level, x=x_range, y=y_range, quality=-6)[0, 0, :, :]
```

### 4.2 Loading Geographic Coordinates

```python
# Load lat/lon coordinates
ds = xr.open_dataset('./data/llc4320_latlon.nc')
lat_center = ds["latitude"].values
lon_center = ds["longitude"].values

# Extract coordinates for selected region
lat_sub = lat_center[y_range[0]:y_range[1], x_range[0]:x_range[1]]
lon_sub = lon_center[y_range[0]:y_range[1], x_range[0]:x_range[1]]
```

### 4.3 Gradient-Based Pseudo-Velocity (Alternative Approach)

If attempting gradient-based visualization:

```python
# Compute gradients from temperature field
from scipy import ndimage

# Compute spatial gradients (approximate flow direction)
grad_y, grad_x = np.gradient(theta_data)

# Normalize to create unit vectors
magnitude = np.sqrt(grad_x**2 + grad_y**2)
u_pseudo = -grad_x / (magnitude + 1e-10)  # Negative for proper direction
v_pseudo = -grad_y / (magnitude + 1e-10)

# Use u_pseudo, v_pseudo for streamline visualization
# WARNING: This is NOT actual velocity, just gradient-based approximation
```

### 4.4 Data Quality Considerations

- **Quality Parameter**: Use `quality=-6` to `-12` for faster loading during development
- **Full Resolution**: Use `quality=0` (default) for final visualizations (much slower, >30GB per timestep)
- **Memory Management**: Each timestep is >30GB, so select regions carefully
- **Caching**: OpenVisus uses local cache (set via `VISUS_CACHE` environment variable)

---

## 5. Implementation Recommendations

### 5.1 Recommended Approach

Given the data limitations, I recommend:

1. **Start with Vertical Velocity Visualization**:
   - Create visualizations of vertical motion (w) patterns
   - Use techniques from beautiful streamlines paper for rendering quality
   - Overlay with temperature/salinity for context

2. **Explore Gradient-Based Visualization**:
   - Test gradient-based pseudo-velocity approach
   - Document limitations clearly (not actual flow)
   - Compare with known oceanographic patterns for validation

3. **Focus on Multi-Variable Visualization**:
   - Combine temperature, salinity, and vertical velocity
   - Use advanced rendering techniques from the streamlines paper
   - Create rich, informative visualizations despite missing horizontal velocity

### 5.2 Streamlines Library Options

- **Matplotlib**: `matplotlib.pyplot.streamplot()` - For gradient-based pseudo-streamlines
- **Plotly**: `plotly.graph_objects.Streamtube` - For 3D vertical velocity visualization
- **Bokeh**: Custom implementation with `bokeh.plotting.figure.line()` - Interactive visualizations
- **Custom LIC**: Implement Line Integral Convolution from the beautiful streamlines paper for vertical velocity patterns

### 5.3 Next Steps

1. **Create test notebook**: `notebooks/vertical_velocity_visualization.ipynb` to explore w field visualization
2. **Test gradient approach**: Create `notebooks/gradient_based_flow.ipynb` to test pseudo-velocity method
3. **Implement advanced rendering**: Apply beautiful streamlines techniques to available data
4. **Document limitations**: Clearly communicate what can and cannot be visualized

---

## 6. Key Findings Summary

✅ **What We Know**:
- Data access method (OpenVisus via HTTPS)
- Data structure (4D: time, z, y, x; field shape: 17280 × 12960 × 90)
- Available fields: **Only 3 fields** - temperature (theta), salinity (salt), vertical velocity (w)
- Coordinate system (array indices + lat/lon mapping)
- Data loading parameters (time, z, x, y, quality)

❌ **What Is NOT Available**:
- **Horizontal velocity components (u, v)** - Required for traditional 2D streamlines
- Other velocity or flow fields

📋 **What We Need to Implement**:
- Alternative visualization approaches (vertical velocity, gradient-based, multi-variable)
- Coordinate grid preparation
- Advanced rendering techniques adapted from beautiful streamlines paper
- Clear documentation of data limitations and visualization approaches

---

## 7. References

- **Visualization Challenge**: [IEEE SciVis Contest 2026 - ECCO LLC4320 Data](https://sciviscontest2026.github.io/data/home)
- **Dataset**: [MITgcm LLC4320 Pre-SWOT JPL L4 ACC SMST v1.0](https://podaac.jpl.nasa.gov/dataset/MITgcm_LLC4320_Pre-SWOT_JPL_L4_ACC_SMST_v1.0)
- **Dataset Documentation**: [ECCO LLC4320 Data Overview](https://sciviscontest2026.github.io/data/home)
- **Streamlines Paper**: [Beautiful Streamlines for Visualizing 2D Vector Fields](https://www.allnans.com/jekyll/update/2018/04/04/beautiful-streamlines.html)
- **Contact**: For dataset questions, contact aashishpanta0@gmail.com

---

**Document Created**: Analysis of LLC4320 data access and streamlines processing requirements  
**Based on**: `notebooks/ieee_scivis_llc4320.ipynb`, `notebooks/LLC4320_metadata.ipynb`, and dataset metadata  
**Last Updated**: Reflects confirmed available fields (theta, salt, w only)

