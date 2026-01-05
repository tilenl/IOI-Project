# Project Structure Plans

This document presents two alternative organizational structures for the LLC4320 Ocean Data Visualization Project. Both plans aim to improve readability and maintainability while reflecting the scientific visualization nature of the project.

## Current State Analysis

**Project Type**: Scientific visualization / Data analysis project for oceanographic data  
**Key Components**:
- Documentation (README, installation guide, session state)
- Jupyter notebooks (demo and metadata examples)
- Configuration files (requirements, gitignore)
- Data files (large NetCDF files, excluded from git)
- Reference materials (project proposal PDF)
- Assets (markdown images)

**Current Issue**: All files are in the root directory, making it harder to navigate as the project grows.

---

## Plan 1: Scientific Project Structure (Organized by Function)

**Philosophy**: Organize files by their functional purpose, following common scientific computing project conventions.

### Structure:
```
.
├── docs/                          # Documentation
│   ├── README.md                  # Main project overview
│   ├── installation.md            # Setup instructions
│   ├── SESSION_STATE.md           # Development session tracking
│   └── .markdown_data/            # Images for markdown docs
│
├── notebooks/                     # Jupyter notebooks
│   ├── ieee_scivis_llc4320.ipynb # Main demo/verification notebook
│   └── LLC4320_metadata.ipynb    # Metadata examples
│
├── data/                          # Data files (gitignored)
│   └── llc4320_latlon.nc         # Coordinate data
│
├── config/                        # Configuration files
│   ├── requirements.txt           # Python dependencies
│   └── .gitignore                # Git ignore rules
│
├── references/                    # External references
│   └── IOI_Project_proposal.pdf  # Original project proposal
│
├── TODO.md                        # Task tracking (root for visibility)
└── .venv/                         # Virtual environment (gitignored)
```

### Advantages:
- ✅ Clear separation of concerns
- ✅ Easy to find files by type
- ✅ Scales well as project grows
- ✅ Follows scientific computing conventions
- ✅ Keeps root directory clean

### Disadvantages:
- ❌ Requires updating paths in documentation
- ❌ Slightly deeper file paths
- ❌ More directories to navigate

### Migration Notes:
- Update README.md paths to reflect new structure
- Update installation.md references
- Move `.markdown_data/` into `docs/`
- Update `.gitignore` to reflect new data location

---

## Plan 2: Flat Structure with Minimal Organization (Keep It Simple)

**Philosophy**: Keep most files at root for easy access, only organize notebooks and data that are clearly distinct.

### Structure:
```
.
├── README.md                      # Main project overview
├── installation.md                # Setup instructions
├── SESSION_STATE.md               # Development session tracking
├── TODO.md                        # Task tracking
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
│
├── notebooks/                     # Jupyter notebooks
│   ├── ieee_scivis_llc4320.ipynb # Main demo/verification notebook
│   └── LLC4320_metadata.ipynb    # Metadata examples
│
├── data/                          # Data files (gitignored)
│   └── llc4320_latlon.nc         # Coordinate data
│
├── references/                    # External references
│   └── IOI_Project_proposal.pdf  # Original project proposal
│
├── .markdown_data/                # Images for markdown docs (root level)
└── .venv/                         # Virtual environment (gitignored)
```

### Advantages:
- ✅ Minimal changes required
- ✅ Documentation stays easily accessible at root
- ✅ Configuration files remain at root (standard practice)
- ✅ Less path updating needed
- ✅ Familiar structure for small projects

### Disadvantages:
- ❌ Root directory still has many files
- ❌ Less organized than Plan 1
- ❌ May become cluttered as project grows

### Migration Notes:
- Only need to move notebooks and data
- Minimal documentation updates
- Keep most references at root level

---

## Recommendation

**For a research/visualization project of this size**: **Plan 2** is recommended because:
1. The project is currently small and focused
2. Documentation at root makes onboarding easier
3. Configuration files at root follow Python conventions
4. Minimal disruption to existing workflows
5. Can always migrate to Plan 1 later if the project grows significantly

**For a larger or multi-person project**: **Plan 1** would be better for long-term maintainability and scalability.

---

## Implementation Considerations

### Common to Both Plans:
- Both separate notebooks from documentation (good practice)
- Both isolate data files (important for git management)
- Both keep TODO.md at root for visibility
- Both maintain `.gitignore` appropriately

### Path Updates Required:
- **Plan 1**: Update all documentation references, notebook paths in README
- **Plan 2**: Update notebook paths in README, minimal other changes

### Next Steps After Choosing:
1. Create new directory structure
2. Move files according to chosen plan
3. Update all path references in documentation
4. Update `.gitignore` if data location changes
5. Test that notebooks still work with new paths
6. Update SESSION_STATE.md with chosen structure

