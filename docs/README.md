# LLC4320 Ocean Data Visualization Project

This project provides tools and examples for working with the ECCO LLC4320 ocean dataset, a high-resolution global ocean simulation dataset. The dataset contains information about salinity levels, temperature, circulation patterns, and other oceanographic variables.

## Getting Started

### Installation

**Before proceeding, please follow the installation instructions in [`installation.md`](installation.md).** The installation guide contains detailed steps for setting up the required Python environment (Python 3.10) and installing all necessary dependencies, including the OpenVisus framework which is essential for accessing the LLC4320 data.

### Verification

After successfully completing the installation steps, verify your setup by running the [`ieee_scivis_llc4320.ipynb`](ieee_scivis_llc4320.ipynb) notebook. This notebook demonstrates how to read and visualize LLC4320 data ~~from the OSDF/Pelican cloud storage~~ using direct HTTPS access with the OpenVisus framework. If all cells execute successfully, your installation is complete and working correctly.

### Additional Examples

Once you've verified your installation, explore the [`LLC4320_metadata.ipynb`](LLC4320_metadata.ipynb) notebook for additional examples and different ways to work with the dataset, including extracting latitude and longitude information and other metadata operations.

## Dataset Information

- **Data Source**: [MITgcm LLC4320 Pre-SWOT JPL L4 ACC SMST v1.0](https://podaac.jpl.nasa.gov/dataset/MITgcm_LLC4320_Pre-SWOT_JPL_L4_ACC_SMST_v1.0)
- **Dataset Documentation**: [ECCO LLC4320 Data Overview](https://sciviscontest2026.github.io/data/home)
- **Visualization Reference**: [Beautiful Streamlines for Visualizing 2D Vector Fields](https://www.allnans.com/jekyll/update/2018/04/04/beautiful-streamlines.html)

## Project Structure

```
.
├── .markdown_data/              # Images and assets used in markdown files (especially installation.md)
├── installation.md              # Detailed installation guide (read this first!)
├── README.md                    # This file - project introduction and overview
├── requirements.txt             # Python package dependencies (used in installation.md)
├── .gitignore                   # Git ignore file for excluding local files (.venv, .cursor, cache, data files)
├── ieee_scivis_llc4320.ipynb   # Main demo notebook - verify installation by running this
├── LLC4320_metadata.ipynb      # Additional demo notebook - more examples of dataset usage
└── IOI_Project_proposal.pdf    # Original project proposal with visualization goals
```

### File Descriptions

- **`.markdown_data/`**: Contains images and visual assets referenced in the markdown documentation files, particularly those used in `installation.md`.

- **`installation.md`** and **`README.md`**: These markdown files serve as introductory documentation for the project. Start with `installation.md` for setup instructions, then refer to `README.md` for project overview and usage.

- **`requirements.txt`**: Lists all Python package dependencies required for this project. This file is referenced and used during the installation process described in `installation.md`.

- **`.gitignore`**: Git ignore file that excludes local development files from version control, including `.venv` (virtual environment), `.cursor` (editor files), `.visus_cache_can_be_deleted` (OpenVisus cache directory), and `llc4320_latlon.nc` (large data file).

- **`ieee_scivis_llc4320.ipynb`**: The primary demonstration notebook. After completing installation, run this notebook to verify that everything is set up correctly. It shows how to access and visualize LLC4320 ocean data.

- **`LLC4320_metadata.ipynb`**: A secondary demo notebook providing additional examples of how to work with the LLC4320 dataset, including metadata extraction and other data manipulation techniques. **Note**: This notebook requires the `llc4320_latlon.nc` file, which is not tracked in git due to its size. See download instructions below.

- **`llc4320_latlon.nc`**: A NetCDF file containing latitude and longitude coordinate information for the LLC4320 dataset, used in the metadata notebook examples. This file is excluded from version control (see `.gitignore`) and must be downloaded separately. Download link is provided in the `LLC4320_metadata.ipynb` notebook, or contact aashishpanta0@gmail.com for access.

- **`IOI_Project_proposal.pdf`**: Contains the original project proposal and idea describing what we are trying to visualize for our final project.

## Requirements

- Python 3.10 (3.10.16 tested) - **Important**: Later versions are not supported due to OpenVisus library compatibility
- All other dependencies are listed in `requirements.txt`

## Notes

- The OpenVisus framework is critical for accessing the LLC4320 data via direct HTTPS access
- Each field in the dataset is >400TB in size
- Do not run `OpenVisus configure` commands after installation, as this can invalidate library signatures and cause kernel crashes

## License

[Add your license information here]

## Contact

For questions or issues related to accessing the `llc4320_latlon.nc` file, please contact: aashishpanta0@gmail.com
