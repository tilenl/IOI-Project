# LLC4320 Flask API Server

Flask REST API server for serving LLC4320 ocean data to frontend applications.

This server acts as a gateway to access LLC4320 data directly from OpenVisus servers.
Data is loaded on-demand via API calls - no local data files are required (except
the coordinate file `llc4320_latlon.nc`).

## Setup

1. **Install dependencies** (if not already installed):

   ```bash
   pip install -r ../config/requirements.txt
   ```

2. **Download coordinate file** (required):
   - Download `llc4320_latlon.nc` to the `data/` directory
   - See `notebooks/LLC4320_metadata.ipynb` for download instructions
   - Or contact: aashishpanta0@gmail.com

## Running the Server

### Development Mode

From the project root:

```bash
# default port 5000 is usually not available, so I use 8080
python -m server.app --port 8080
```

Or from the `server/` directory:

```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

### Custom Port and Configuration

You can specify a custom port using command-line arguments:

```bash
# Specify a custom port
python -m server.app --port 8080

# Specify both host and port
python -m server.app --host 127.0.0.1 --port 8080

# Enable debug mode
python -m server.app --port 8080 --debug

# Or use environment variables
PORT=8080 python -m server.app
HOST=127.0.0.1 PORT=8080 python -m server.app
```

**Available options:**

- `--port`: Port number (default: 5000, or PORT environment variable)
- `--host`: Host to bind to (default: 0.0.0.0, or HOST environment variable)
- `--debug`: Enable Flask debug mode (default: False, or FLASK_DEBUG=true)

### Production Mode

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server.app:app
```

## API Endpoints

### Health Check

```
GET /api/health
```

Returns server status.

**Response:**

```json
{
  "status": "healthy",
  "service": "LLC4320 Data API"
}
```

### Metadata

```
GET /api/metadata?field=salinity
```

Get metadata about a dataset field.

**Query Parameters:**

- `field` (str): Field name - 'salinity', 'temperature', 'vertical_velocity', etc. (default: 'salinity')

**Response:**

```json
{
  "field": "salt",
  "dimensions": {
    "x": 17280,
    "y": 12960,
    "z": 90
  },
  "total_timesteps": 10312,
  "data_type": "float32",
  "available_fields": [
    "salinity",
    "temperature",
    "vertical_velocity",
    "salt",
    "theta",
    "w"
  ],
  "field_units": {
    "salinity": "g kg⁻¹",
    "temperature": "°C",
    "vertical_velocity": "m s⁻¹"
  }
}
```

### Data Slice (2D)

```
GET /api/data/slice?field=salinity&timestep=0&depth_level=0&lat_min=-40&lat_max=-10&lon_min=105&lon_max=160&quality=-12&format=array
```

Get a 2D slice of data for a specific timestep and depth level.

**Query Parameters:**

- `field` (str): Field name - 'salinity', 'temperature', 'vertical_velocity', etc. (default: 'salinity')
- `timestep` (int): Timestep index (default: 0)
- `depth_level` (int): Depth level index (default: 0)
- `lat_min` (float): **Required** - Minimum latitude in degrees
- `lat_max` (float): **Required** - Maximum latitude in degrees
- `lon_min` (float): **Required** - Minimum longitude in degrees
- `lon_max` (float): **Required** - Maximum longitude in degrees
- `quality` (int): Data quality level, -12 to 0 (default: -12, lower = faster but lower resolution)
- `format` (str): Response format - `'array'` or `'base64'` (default: `'array'`)

**Response:**

```json
{
  "field": "salinity",
  "timestep": 0,
  "depth_level": 0,
  "data": {
    "format": "array",
    "data": [[...], [...], ...]
  },
  "coordinates": {
    "latitude": [[...], [...], ...],
    "longitude": [[...], [...], ...]
  },
  "shape": [2500, 5500],
  "lat_range": [-40.0, -10.0],
  "lon_range": [105.0, 160.0],
  "quality": -12
}
```

### Timestep Data (3D)

```
GET /api/data/timestep?field=salinity&timestep=0&lat_min=-40&lat_max=-10&lon_min=105&lon_max=160&z_min=0&z_max=1&quality=-12&format=array
```

Get data for a specific timestep across multiple depth levels (3D data: depth, y, x).

**Query Parameters:**

- `field` (str): Field name - 'salinity', 'temperature', 'vertical_velocity', etc. (default: 'salinity')
- `timestep` (int): Timestep index (default: 0)
- `lat_min` (float): **Required** - Minimum latitude in degrees
- `lat_max` (float): **Required** - Maximum latitude in degrees
- `lon_min` (float): **Required** - Minimum longitude in degrees
- `lon_max` (float): **Required** - Maximum longitude in degrees
- `z_min` (int): Minimum depth level index (default: 0)
- `z_max` (int): Maximum depth level index (default: 1)
- `quality` (int): Data quality level, -12 to 0 (default: -12)
- `format` (str): Response format - `'array'` or `'base64'` (default: `'array'`)

**Response:**

```json
{
  "field": "salinity",
  "timestep": 0,
  "data": {
    "format": "array",
    "data": [[[...]], [[[...]]], ...]
  },
  "coordinates": {
    "latitude": [[...], [...], ...],
    "longitude": [[...], [...], ...]
  },
  "shape": [1, 2500, 5500],
  "lat_range": [-40.0, -10.0],
  "lon_range": [105.0, 160.0],
  "z_range": [0, 1],
  "quality": -12
}
```

## Data Format Options

### Array Format (`format=array`)

- Data is returned as nested JSON arrays (lists)
- Easy to use directly in JavaScript
- Larger payload size for big datasets
- Best for: Small to medium datasets, development

### Base64 Format (`format=base64`)

- Data is base64-encoded binary
- More efficient for large datasets
- Requires decoding on frontend
- Best for: Large datasets, production

**Frontend decoding example (JavaScript):**

```javascript
const base64Data = response.data.data;
const binaryString = atob(base64Data);
const bytes = new Uint8Array(binaryString.length);
for (let i = 0; i < binaryString.length; i++) {
  bytes[i] = binaryString.charCodeAt(i);
}
const floatArray = new Float32Array(bytes.buffer);
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid parameters)
- `404`: Endpoint not found
- `500`: Internal server error

Error responses follow this format:

```json
{
  "error": "Error message description"
}
```

## CORS

CORS is enabled by default, allowing frontend applications to access the API from any origin. For production, consider restricting CORS to specific origins.

## Performance Considerations

- **On-Demand Loading**: Data is loaded directly from OpenVisus servers on each request
- **Dataset Caching**: OpenVisus dataset objects are cached in memory (loaded once per field)
- **Quality Parameter**: Use lower quality values (e.g., -12) for faster loading during development
- **Base64 Encoding**: Use `format=base64` for large datasets to reduce payload size
- **Regional Queries**: Request only the lat/lon region you need to minimize data transfer
- **OpenVisus Cache**: OpenVisus maintains its own cache directory (`.visus_cache_can_be_deleted`)

## Example Frontend Usage

```javascript
// Fetch metadata
const metadata = await fetch(
  "http://localhost:5000/api/metadata?field=salinity",
).then((res) => res.json());

// Fetch a 2D slice for a specific region
const slice = await fetch(
  "http://localhost:5000/api/data/slice?" +
    "field=salinity&" +
    "timestep=0&" +
    "depth_level=0&" +
    "lat_min=-40&lat_max=-10&" +
    "lon_min=105&lon_max=160&" +
    "quality=-12",
).then((res) => res.json());

// Use the data
const salinityData = slice.data.data;
const lat = slice.coordinates.latitude;
const lon = slice.coordinates.longitude;
```

## Available Fields

The API supports three data fields:

- **Salinity** (`field=salinity` or `field=salt`): Ocean salinity in g kg⁻¹
- **Temperature** (`field=temperature` or `field=theta`): Ocean temperature in °C
- **Vertical Velocity** (`field=vertical_velocity` or `field=w`): Vertical velocity in m s⁻¹

## Quality Levels

The `quality` parameter controls data resolution and loading speed:

- **-12**: Fastest, lowest resolution (recommended for development)
- **-8**: Balanced quality/speed
- **-6**: Higher quality, slower
- **0**: Full resolution (slowest, >30GB per timestep)

## Project Structure

```
server/
├── __init__.py          # Package initialization
├── app.py               # Flask application and routes
├── data_service.py      # Data loading and serialization logic
└── README.md            # This file
```
