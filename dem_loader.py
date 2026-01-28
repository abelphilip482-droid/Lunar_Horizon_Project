"""
Helper script to load DEM and make it available for lh.py
"""
import sys
import os
from osgeo import gdal
import numpy as np

def load_dem(dem_path):
    """Load DEM file using GDAL"""
    gdal.UseExceptions()
    
    ds = gdal.Open(dem_path)
    if ds is None:
        raise ValueError(f"Failed to open DEM file: {dem_path}")
    
    # Read the first band
    band = ds.GetRasterBand(1)
    image = band.ReadAsArray().astype(np.float32)
    
    return image, ds

if __name__ == "__main__":
    dem_path = r"C:\Users\Abel Philip\Downloads\WAC_GLD100_E000N1800_064P.IMG"
    
    try:
        image, ds = load_dem(dem_path)
        print(f"Successfully loaded DEM: {image.shape}")
        print(f"Min: {np.nanmin(image)}, Max: {np.nanmax(image)}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
