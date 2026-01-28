#!/usr/bin/env python
"""Test simple DEM loading and parameter replacement"""
import sys
import os
from osgeo import gdal
import numpy as np

dem_path = r"C:\Users\Abel Philip\Downloads\WAC_GLD100_E000N1800_064P.IMG"

print("[1] Testing DEM load...", file=sys.stderr)
gdal.UseExceptions()
ds = gdal.Open(dem_path)
if ds is None:
    print("ERROR: Failed to open DEM", file=sys.stderr)
    sys.exit(1)

print("[2] DEM opened successfully", file=sys.stderr)
band = ds.GetRasterBand(1)
image = band.ReadAsArray().astype(np.float32)
print(f"[3] DEM loaded: shape={image.shape}", file=sys.stderr)

# Now test reading lh.py
lh_path = r"C:\Users\Abel Philip\OneDrive\Documents\lh.py"
print(f"[4] Reading {lh_path}...", file=sys.stderr)

with open(lh_path, 'r') as f:
    code = f.read()

print(f"[5] Read {len(code)} chars from lh.py", file=sys.stderr)
print(f"[6] First 500 chars:\n{code[:500]}", file=sys.stderr)

# Try basic parameter replacement
code2 = code.replace("lon = 5", "lon = 5")  # No-op
code2 = code2.replace("lat = 67", "lat = 67")  # No-op
print(f"[7] Parameter replacement successful", file=sys.stderr)

print("SUCCESS: All tests passed")
