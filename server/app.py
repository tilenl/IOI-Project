"""
Flask API server for serving LLC4320 ocean data to the frontend.

This server provides RESTful endpoints to access LLC4320 data directly from
OpenVisus servers, enabling the frontend to retrieve data for visualization.
"""

import sys
import os
import argparse
from pathlib import Path

# Add scripts directory to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from server.data_service import DataService

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize data service
data_service = DataService()


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "LLC4320 Data API"})


@app.route("/api/metadata", methods=["GET"])
def get_metadata():
    """
    Get metadata about a dataset field.
    
    Query parameters:
        field (str): Field name - 'salinity', 'temperature', 'vertical_velocity', etc. (default: 'salinity')
    
    Returns:
        JSON with dataset dimensions, timesteps, and field information.
    """
    try:
        field = request.args.get("field", "salinity")
        metadata = data_service.get_metadata(field=field)
        return jsonify(metadata)
    except ValueError as e:
        return jsonify({"error": f"Invalid parameter: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/data/slice", methods=["GET"])
def get_data_slice():
    """
    Get a 2D slice of data for a specific timestep and depth level.
    
    Query parameters:
        field (str): Field name - 'salinity', 'temperature', 'vertical_velocity', etc. (default: 'salinity')
        timestep (int): Timestep index (default: 0)
        depth_level (int): Depth level index (default: 0)
        lat_min (float): Minimum latitude in degrees (required)
        lat_max (float): Maximum latitude in degrees (required)
        lon_min (float): Minimum longitude in degrees (required)
        lon_max (float): Maximum longitude in degrees (required)
        quality (int): Data quality level, -12 to 0 (default: -12)
        format (str): Response format - 'array' or 'base64' (default: 'array')
    
    Returns:
        JSON with data array and coordinates for the slice.
    """
    try:
        # Parse query parameters
        field = request.args.get("field", "salinity")
        timestep = int(request.args.get("timestep", 0))
        depth_level = int(request.args.get("depth_level", 0))
        quality = int(request.args.get("quality", -12))
        format_type = request.args.get("format", "array")
        
        # Parse lat/lon ranges (required)
        lat_min = float(request.args.get("lat_min"))
        lat_max = float(request.args.get("lat_max"))
        lon_min = float(request.args.get("lon_min"))
        lon_max = float(request.args.get("lon_max"))
        
        lat_range = [lat_min, lat_max]
        lon_range = [lon_min, lon_max]
        
        # Get data slice
        result = data_service.get_data_slice(
            field=field,
            timestep=timestep,
            depth_level=depth_level,
            lat_range=lat_range,
            lon_range=lon_range,
            quality=quality,
            format_type=format_type
        )
        
        return jsonify(result)
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid parameter: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/data/timestep", methods=["GET"])
def get_timestep_data():
    """
    Get data for a specific timestep across multiple depth levels (3D data).
    
    Query parameters:
        field (str): Field name - 'salinity', 'temperature', 'vertical_velocity', etc. (default: 'salinity')
        timestep (int): Timestep index (default: 0)
        lat_min (float): Minimum latitude in degrees (required)
        lat_max (float): Maximum latitude in degrees (required)
        lon_min (float): Minimum longitude in degrees (required)
        lon_max (float): Maximum longitude in degrees (required)
        z_min (int): Minimum depth level index (default: 0)
        z_max (int): Maximum depth level index (default: 1)
        quality (int): Data quality level, -12 to 0 (default: -12)
        format (str): Response format - 'array' or 'base64' (default: 'array')
    
    Returns:
        JSON with 3D data array (depth, y, x) and coordinates.
    """
    try:
        # Parse query parameters
        field = request.args.get("field", "salinity")
        timestep = int(request.args.get("timestep", 0))
        z_min = int(request.args.get("z_min", 0))
        z_max = int(request.args.get("z_max", 1))
        quality = int(request.args.get("quality", -12))
        format_type = request.args.get("format", "array")
        
        # Parse lat/lon ranges (required)
        lat_min = float(request.args.get("lat_min"))
        lat_max = float(request.args.get("lat_max"))
        lon_min = float(request.args.get("lon_min"))
        lon_max = float(request.args.get("lon_max"))
        
        lat_range = [lat_min, lat_max]
        lon_range = [lon_min, lon_max]
        z_range = [z_min, z_max]
        
        result = data_service.get_timestep_data(
            field=field,
            timestep=timestep,
            lat_range=lat_range,
            lon_range=lon_range,
            z_range=z_range,
            quality=quality,
            format_type=format_type
        )
        
        return jsonify(result)
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid parameter: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/coordinates", methods=["GET"])
def get_coordinates():
    """
    Get latitude and longitude coordinates.
    
    Query parameters (all optional):
        lat_min (float): Minimum latitude in degrees. If provided, returns only coordinates in range.
        lat_max (float): Maximum latitude in degrees
        lon_min (float): Minimum longitude in degrees
        lon_max (float): Maximum longitude in degrees
    
    Returns:
        JSON with lat and lon arrays. If ranges provided, returns coordinates for that region only.
    """
    try:
        # Parse optional lat/lon ranges
        lat_min = request.args.get("lat_min")
        lat_max = request.args.get("lat_max")
        lon_min = request.args.get("lon_min")
        lon_max = request.args.get("lon_max")
        
        lat_range = None
        lon_range = None
        
        if lat_min is not None and lat_max is not None:
            lat_range = [float(lat_min), float(lat_max)]
        if lon_min is not None and lon_max is not None:
            lon_range = [float(lon_min), float(lon_max)]
        
        coordinates = data_service.get_coordinates(
            lat_range=lat_range,
            lon_range=lon_range
        )
        return jsonify(coordinates)
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid parameter: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


@app.route("/", methods=["GET"])
def serve_frontend():
    """Serve the frontend test page."""
    frontend_dir = PROJECT_ROOT / "frontend"
    return send_from_directory(str(frontend_dir), "index.html")


@app.route("/<path:path>", methods=["GET"])
def serve_static(path):
    """Serve static files from frontend directory."""
    frontend_dir = PROJECT_ROOT / "frontend"
    return send_from_directory(str(frontend_dir), path)


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="LLC4320 Flask API Server")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", 5000)),
        help="Port to run the server on (default: 5000 or PORT env var)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.environ.get("HOST", "0.0.0.0"),
        help="Host to bind to (default: 0.0.0.0 or HOST env var)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.environ.get("FLASK_DEBUG", "False").lower() == "true",
        help="Enable debug mode"
    )
    args = parser.parse_args()
    
    # Development server configuration
    print(f"Starting LLC4320 API server on http://{args.host}:{args.port}")
    print(f"Debug mode: {args.debug}")
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )

