# Global Ecology & Biodiversity

## DSM GeoTIFF Processing Script

This Python script automates the process of downloading, clipping, and merging GeoTIFF files, i.e. Digital Terrain Model (DTM) and Digital Surface Model (DSM), using a JSON tile index and a target shapefile. It is designed for users needing to extract specific regions from a larger dataset of GeoTIFF tiles based on area of interest (AOI) boundaries.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage Instructions](#usage-instructions)
- [Script Workflow](#script-workflow)
- [Output Files](#output-files)
- [License](#license)
- [Contact](#contact)

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

### 1. Prepare Input Files

**JSON File**: Place the JSON file containing tile metadata (tile boundaries, URLs, etc.) in `data/0_json/DSM/kaartbladindex.json`. An example for the JSON file is the `kaartbladindex.json` file on this [WEBSITE](https://service.pdok.nl/rws/ahn/atom/dsm_05m.xml).

**Shapefile**: Place the shapefile containing the AOI polygon in `data/1_shpfiles/`. The shapefile should consist of several files (e.g., .shp, .shx, .dbf) with the main file has `*.shp` extension, i.e. `AWD_sampling_area.shp`.

### 2. Run the script

Execute the script using the command below. Ensure you are in the same directory as dsm.py or provide the full path to it:

```bash
    python dsm.py
```

### 3. Directory Structure and Results:

Downloaded, clipped, and merged GeoTIFF files will be saved in designated folders (`data/2_downloaded_geotiff/DSM`, `data/3_clipped/DSM`, and `data/4_merged/DSM`).

## Script workflow

The script operates in six main steps:

### Step 1: Load and Prepare Data

JSON File: Parses the JSON to extract tile metadata, such as bounding boxes and download URLs.
Shapefile: Reads the AOI from the shapefile, ensuring its Coordinate Reference System (CRS) matches that of the tiles.

### Step 2: Convert JSON Tiles to a GeoDataFrame

Converts the tile information from the JSON file to a GeoDataFrame, allowing spatial operations.

### Step 3: Identify Intersecting Tiles

Uses spatial queries to identify tiles in the JSON file that intersect with the AOI defined in the shapefile.

### Step 4: Download Intersecting Tiles

Downloads each intersecting tile as a GeoTIFF file using the URLs in the JSON file, saving them in `data/2_downloaded_geotiff/DSM`.

### Step 5: Clip Tiles to AOI

Clips each downloaded GeoTIFF to the AOI boundary, ensuring each raster covers only the specified region.
Clipped rasters are saved in `data/3_clipped/DSM`.

### Step 6: Merge Clipped GeoTIFFs

Merges all clipped GeoTIFFs into a single output file, saved as merged_clipped.tif in `data/4_merged/DSM`.

## Output files

After running the script, you should have:

### 1. Downloaded GeoTIFF Files:

1. Stored in `data/2_downloaded_geotiff/DSM`. These are the original tiles before clipping.
2. Clipped GeoTIFF Files: Saved in `data/3_clipped/DSM`. These files are clipped to the AOI boundaries.

### 2. Merged GeoTIFF File:

A single, combined GeoTIFF file named `merged_clipped.tif` in `data/4_merged/DSM`, representing the AOI as one continuous raster.

The `data` folder of this workflow is shared [HERE](https://surfdrive.surf.nl/files/index.php/s/KWOSUgGYteT6nHO).

## License

[Apache-2.0 license](https://www.apache.org/licenses/LICENSE-2.0)

## Contact

For any suggestions and bug reports, please contact:

Jinhu Wang

jinhu.wang (at) hotmail (dot) com
