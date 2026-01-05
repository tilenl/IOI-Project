# Session State

## Project Overview

**LLC4320 Ocean Data Visualization Project** - A Python-based project for working with the ECCO LLC4320 high-resolution global ocean simulation dataset. The project provides tools and examples for accessing, processing, and visualizing oceanographic data including salinity, temperature, and circulation patterns.

## Current State

- **Project Type**: Scientific visualization / Data analysis
- **Language**: Python 3.10 (3.10.16 tested)
- **Key Dependencies**: OpenVisus 2.2.141, openvisuspy 1.0.71, xarray, numpy, matplotlib, bokeh, panel
- **Data Source**: MITgcm LLC4320 Pre-SWOT JPL L4 ACC SMST v1.0 (each field >400TB)
- **Access Method**: Direct HTTPS access via OpenVisus framework

## Project Structure

Current files:
- `README.md` - Project introduction and overview
- `installation.md` - Detailed setup instructions for Python 3.10 environment
- `requirements.txt` - Python dependencies with version constraints
- `ieee_scivis_llc4320.ipynb` - Main demo notebook (verification notebook)
- `LLC4320_metadata.ipynb` - Additional examples and metadata extraction
- `llc4320_latlon.nc` - NetCDF coordinate file (excluded from git, large file)
- `IOI_Project_proposal.pdf` - Original project proposal
- `.gitignore` - Excludes `.venv`, `.cursor`, cache, and data files

## Architectural Decisions

- **Python Version**: Locked to 3.10 due to OpenVisus compatibility constraints
- **Data Access**: Using OpenVisus framework for direct HTTPS access (no OSDF/Pelican cloud storage)
- **Environment Management**: Virtual environment (`.venv`) with strict dependency versioning
- **Critical Constraint**: Do NOT run `OpenVisus configure` commands after installation (invalidates signatures, causes kernel crashes)

## Recent Changes

- Initial project setup with documentation and notebooks
- Installation guide created with Python 3.10 setup instructions
- Requirements file established with version-locked OpenVisus packages

## Blockers

None currently.

## Next Step

**Plan the structure of the project**: Reason and come up with 2 plans of how to tidy the files to get a functional and readable environment. Create a plan a structure that reflects what this project is.

