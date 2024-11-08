import glob
import json
import os

import geopandas as gpd
import rasterio
import requests
from rasterio.mask import mask
from rasterio.merge import merge
from shapely.geometry import shape

# Step 0: Define paths and create directories 
json_path = 'data/0_json/DTM/kaartbladindex.json'
shapefile_path = 'data/1_shpfiles/AWD_sampling_area.shp'
download_dir = 'data/2_downloaded_geotiff/DTM'
output_clipped_dir = 'data/3_clipped/DTM'
output_merged_dir = 'data/4_merged/DTM'

os.makedirs(download_dir, exist_ok=True)
os.makedirs(output_clipped_dir, exist_ok=True)
os.makedirs(output_merged_dir, exist_ok=True)

# Step 1: Load the shapefile and JSON data
sampling_area = gpd.read_file(shapefile_path)
with open(json_path) as f:
    data = json.load(f)

# Step 2: Convert JSON features to a GeoDataFrame
tiles = []
for feature in data['features']:
    polygon = shape(feature['geometry'])
    properties = feature['properties']
    tiles.append({'geometry': polygon, 'properties': properties})
tiles_gdf = gpd.GeoDataFrame(tiles)

# Ensure CRS matches between GeoDataFrames
tiles_gdf.set_crs(epsg=28992, inplace=True)
sampling_area = sampling_area.to_crs(tiles_gdf.crs)

# Step 3: Find intersecting tiles
intersections = tiles_gdf[tiles_gdf.intersects(sampling_area.unary_union)]
intersecting_urls = intersections['properties'].apply(lambda x: x['url']).tolist()

# Step 4: Download each intersecting GeoTIFF
for url in intersecting_urls:
    file_name = os.path.join(download_dir, url.split('/')[-1])
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Saved {file_name}")
    else:
        print(f"Failed to download {url}")

# Step 5: Clip each downloaded GeoTIFF to the shapefile boundary
clipped_rasters = []
for tif_path in glob.glob(os.path.join(download_dir, '*.tif')):
    with rasterio.open(tif_path) as src:
        out_image, out_transform = mask(src, sampling_area.geometry, crop=True)
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })
        
        clipped_path = os.path.join(output_clipped_dir, f"clipped_{os.path.basename(tif_path)}")
        with rasterio.open(clipped_path, "w", **out_meta) as dest:
            dest.write(out_image)
        clipped_rasters.append(clipped_path)

# Step 6: Merge all clipped GeoTIFFs into one file
src_files_to_mosaic = [rasterio.open(fp) for fp in clipped_rasters]
mosaic, out_trans = merge(src_files_to_mosaic)
out_meta = src_files_to_mosaic[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans,
    "crs": src_files_to_mosaic[0].crs
})

# Save the merged file
merged_output_path = os.path.join(output_merged_dir, "merged_clipped.tif")
with rasterio.open(merged_output_path, "w", **out_meta) as dest:
    dest.write(mosaic)

# Close all opened files
for src in src_files_to_mosaic:
    src.close()

print(f"Merged file saved to {merged_output_path}")
