# LLC4320 Frontend Test Page

Simple HTML test page for testing the Flask API endpoints and verifying data is being sent correctly.

## Usage

1. **Start the Flask server**:
   ```bash
   python -m server.app
   ```
   The server will start on `http://localhost:5000`

2. **Open the HTML file**:
   - Option 1: Open `index.html` directly in your browser (file:// protocol)
   - Option 2: Use a simple HTTP server:
     ```bash
     # Python 3
     python -m http.server 8000
     # Then open http://localhost:8000/frontend/index.html
     ```
   - Option 3: The Flask server can be configured to serve static files (see below)

3. **Test the API**:
   - The page will automatically test the health endpoint on load
   - Use the form to configure parameters and fetch data
   - View the results, statistics, and data previews

## Features

- **Metadata Testing**: Fetch and display dataset metadata
- **Data Slice Testing**: Fetch 2D data slices with configurable parameters
- **Coordinate Testing**: Fetch latitude/longitude coordinates
- **Statistics**: Automatically calculates min, max, mean for array data
- **Data Preview**: Shows preview of data arrays (first 10×10 for arrays)
- **Error Handling**: Clear error messages if API calls fail
- **Loading Indicators**: Visual feedback during API calls

## Default Test Parameters

The form is pre-filled with reasonable defaults:
- **Field**: Salinity
- **Timestep**: 0
- **Depth Level**: 0
- **Quality**: -12 (fast loading)
- **Region**: Australian region (lat: -40 to -10, lon: 105 to 160)

## Notes

- The page uses vanilla JavaScript (no frameworks required)
- CORS must be enabled on the Flask server (already configured)
- Large data arrays are truncated in the preview for performance
- Base64 format option available for testing binary data transfer

