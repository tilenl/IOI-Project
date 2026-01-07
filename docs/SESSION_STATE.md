# Session State

## Project Overview

**LLC4320 Ocean Data Visualization Project** - A Python-based project for working with the ECCO LLC4320 high-resolution global ocean simulation dataset. The project provides tools and examples for accessing, processing, and visualizing oceanographic data including salinity, temperature, and circulation patterns.

## Current State

- **Project Type**: Scientific visualization / Data analysis
- **Language**: Python 3.10 (3.10.16 tested)
- **Key Dependencies**: OpenVisus 2.2.141, openvisuspy 1.0.71, xarray, numpy, matplotlib, bokeh, panel
- **Data Source**: MITgcm LLC4320 Pre-SWOT JPL L4 ACC SMST v1.0 (each field >400TB)
- **Access Method**: Direct HTTPS access via OpenVisus framework

## Project Map

**Directory Structure Overview** - This section provides the "big picture" of the file system and guides where to place new files.

### Current Structure (Plan 1: Scientific Project Structure)

```
.
├── docs/                          # Documentation files
│   ├── README.md                  # Main project overview
│   ├── installation.md             # Setup instructions
│   ├── SESSION_STATE.md            # This file - development session tracking
│   ├── PROJECT_STRUCTURE_PLANS.md # Structure planning document
│   └── .markdown_data/             # Images/assets for markdown docs
│
├── notebooks/                     # Jupyter notebooks
│   ├── ieee_scivis_llc4320.ipynb  # Main demo/verification notebook
│   └── LLC4320_metadata.ipynb     # Metadata examples notebook
│
├── server/                        # Flask API server
│   ├── app.py                    # Flask application and routes
│   ├── data_service.py           # Data loading from OpenVisus servers
│   ├── README.md                 # API documentation
│   └── __init__.py               # Package initialization
│
├── frontend/                      # Frontend test interface
│   ├── index.html                # HTML test page for API testing
│   └── README.md                 # Frontend usage instructions
│
├── scripts/                       # Python scripts for data processing
│   └── loading_data.py           # Script for loading and saving LLC4320 data
│
├── data/                          # Data files (gitignored)
│   └── llc4320_latlon.nc        # Coordinate data file
│
├── config/                        # Configuration files
│   └── requirements.txt          # Python dependencies (includes Flask)
│
├── references/                    # External references
│   └── IOI_Project_proposal.pdf  # Project proposal PDF
│
├── analysis/                      # Analysis and research documents
│   ├── data_access_analysis.md   # Data access and streamlines analysis
│   └── flask_hosting_analysis.md # Flask hosting and deployment options
│
├── Dockerfile                     # Docker container definition for production deployment
├── docker-compose.yml             # Docker Compose configuration for local development
├── docker-entrypoint.sh           # Entrypoint script for Docker container
├── gunicorn_config.py             # Gunicorn production server configuration
├── .dockerignore                  # Docker ignore file (excludes files from build)
├── TODO.md                        # Task tracking (root for visibility)
└── .gitignore                     # Git ignore rules (root - required by Git)
```

### File Placement Guidelines

- **Documentation** → `docs/` (markdown files, guides; assets → `docs/.markdown_data/`)
- **Server/API** → `server/` (Flask application, data services, API routes)
- **Frontend** → `frontend/` (HTML, CSS, JavaScript for web interface)
- **Analysis** → `analysis/` (research documents, findings, processing pipelines)
- **Jupyter Notebooks** → `notebooks/` (all `.ipynb` files)
- **Python Scripts** → `scripts/` (reusable data processing scripts)
- **Data Files** → `data/` (all gitignored: NetCDF, HDF5, cache files)
- **Configuration** → `config/` (dependencies, settings; `.gitignore` must stay at root)
- **References** → `references/` (PDFs, papers, proposals)
- **Root**: `TODO.md`, `.gitignore`, `.venv/`, `.cursor/` (all gitignored except TODO.md)

## Architectural Decisions

- **Python Version**: Locked to 3.10 due to OpenVisus compatibility constraints
- **Data Access**: Using OpenVisus framework for direct HTTPS access (no OSDF/Pelican cloud storage)
- **API Architecture**: Flask REST API acts as gateway to OpenVisus servers - data loaded on-demand, not cached locally
- **Frontend**: HTML/JavaScript interface with Plotly.js for interactive data visualization (heatmaps with geographic coordinates)
- **Visualization**: Plotly.js for client-side rendering; iterative coordinate processing to avoid stack overflow on large arrays
- **Environment Management**: Virtual environment (`.venv`) with strict dependency versioning
- **Production Server**: Gunicorn WSGI server (Flask's built-in server is development-only)
- **Containerization**: Docker setup with multi-stage optimization, health checks, and production-ready Gunicorn configuration
- **Critical Constraint**: Do NOT run `OpenVisus configure` commands after installation (invalidates signatures, causes kernel crashes)

## Recent Changes

- **Frontend Visualization Complete**: Added interactive data visualization to `frontend/index.html` using Plotly.js. Implemented heatmap visualization for 2D data slices with geographic coordinates, colorbar with field units, and hover tooltips. Supports both array and base64 data formats. Fixed stack overflow error in coordinate processing by replacing `.flat()` and spread operators with iterative min/max functions for large coordinate arrays
- **Docker Setup Complete**: Created complete Docker containerization setup including Dockerfile (Python 3.10, Gunicorn), docker-compose.yml for local testing, docker-entrypoint.sh for environment variable handling, gunicorn_config.py for production configuration, and comprehensive deployment documentation (`docs/DOCKER_DEPLOYMENT.md`). Added Gunicorn to requirements.txt. Created `config/requirements-docker.txt` with OpenVisus 2.2.135 (Linux-compatible version) since 2.2.141 is not available on PyPI for Linux

## Blockers

None currently.

## Next Step

**Test frontend visualization**: Verify the interactive heatmap visualization works correctly with real data from the Flask API. Test with different fields (salinity, temperature, vertical_velocity) and various coordinate ranges to ensure proper rendering.


