# Global Ecology & Biodiversity

## DSM GeoTIFF Processing Script

This Python script automates the process of downloading, clipping, and merging GeoTIFF files using a JSON tile index and a target shapefile. It is designed for users needing to extract specific regions from a larger dataset of GeoTIFF tiles based on area of interest (AOI) boundaries.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage Instructions](#usage-instructions)
- [Script Workflow](#script-workflow)
- [Output Files](#output-files)
- [File Structure](#file-structure)
- [Error Handling](#error-handling)
- [License](#license)

---

## Overview

This script takes two inputs:

1. **A JSON file** containing metadata of GeoTIFF tiles, including URLs and spatial boundaries.
2. **A Shapefile** that defines an area of interest (AOI).

The script identifies tiles intersecting with the AOI, downloads these tiles, clips them to the AOI boundary, and merges them into a single GeoTIFF file.

---

## Requirements

Ensure you have the following Python packages installed:

- **geopandas**: For handling geographic data, including shapefiles.
- **rasterio**: For handling raster data, such as GeoTIFF files.
- **shapely**: For geometric operations.
- **requests**: For downloading files from the web.

## Installation

You can install the required packages using:

**pip**

```bash
pip install geopandas rasterio shapely requests
```

or **conda**

```bash
conda install geopandas rasterio shapely requests
```

## Usage Instructions

- 1. Prepare Input Files:

  JSON File: Place the JSON file containing tile metadata (tile boundaries, URLs, etc.) in data/0_json/DSM/kaartbladindex.json.
  Shapefile: Place the shapefile containing the AOI polygon in data/1_shpfiles/. The shapefile should consist of several files (e.g., .shp, .shx, .dbf) with the main file named AWD_sampling_area.shp.
