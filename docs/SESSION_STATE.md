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
│   └── data_access_analysis.md   # Data access and streamlines analysis
│
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
- **Frontend**: Simple HTML/JavaScript test interface for API validation
- **Environment Management**: Virtual environment (`.venv`) with strict dependency versioning
- **Critical Constraint**: Do NOT run `OpenVisus configure` commands after installation (invalidates signatures, causes kernel crashes)

## Recent Changes

- **Coordinates Endpoint Removed**: Removed `/api/coordinates` endpoint to prevent performance issues (150MB+ data size). Coordinates remain available within data slice responses
- **Frontend Optimized**: Removed large data array displays from frontend to prevent lag. Only summary statistics shown
- **API Architecture Complete**: Flask REST API with endpoints for metadata, data slices, and timestep data. Supports salinity, temperature, and vertical velocity fields

## Blockers

None currently.

## Next Step

**Research hosting options**: Investigate how to host the Flask server on the internet and whether Flask's built-in server is suitable for production deployment.


