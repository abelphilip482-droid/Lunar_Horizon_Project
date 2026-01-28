#!/usr/bin/env python
"""Debug script to test calculator logic"""
import subprocess
import tempfile
import os
import json

# Test parameters
latitude = 67
longitude = 5
start_date = "2025-01-11"
end_date = "2025-02-11"

script_path = r"C:\Users\Abel Philip\OneDrive\Documents\lh.py"
dem_path = r"C:\Users\Abel Philip\Downloads\WAC_GLD100_E000N1800_064P.IMG"

# Read lh.py script
with open(script_path, 'r') as f:
    code = f.read()

# Add DEM pre-loading code that runs BEFORE lh.py code
dem_loading_code = f"""
import sys
import os
from osgeo import gdal
import numpy as np

# Load DEM first, before any lh.py code
dem_path = r"{dem_path}"
gdal.UseExceptions()
ds = gdal.Open(dem_path)
if ds is None:
    raise RuntimeError(f"Failed to open DEM: {{dem_path}}")
band = ds.GetRasterBand(1)
image = band.ReadAsArray().astype(np.float32)
nodata = band.GetNoDataValue()
print(f"[DEBUG] DEM loaded: shape={{image.shape}}", file=sys.stderr)

"""

# Comment out duplicate GDAL loading in lh.py
code = code.replace("from osgeo import gdal", "# from osgeo import gdal (pre-loaded above)")
lines = code.split('\n')
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('ds = gdal.Open') or stripped.startswith('band = ds.GetRasterBand') or stripped.startswith('image = band.ReadAsArray'):
        lines[i] = '# ' + line
code = '\n'.join(lines)

# Prepend DEM loading code
code = dem_loading_code + code

# Replace the hardcoded values
code = code.replace("lon = 5", f"lon = {longitude}")
code = code.replace("lat = 67", f"lat = {latitude}")

# Handle date replacements with regex for flexibility
import re
code = re.sub(r"start_time\s*=\s*datetime\([^)]+\)", f"start_time = datetime.strptime('{start_date}', '%Y-%m-%d')", code)
code = re.sub(r"stop_time\s*=\s*datetime\([^)]+\)", f"stop_time = datetime.strptime('{end_date}', '%Y-%m-%d')", code)

# Write to temp file and execute
temp_fd, temp_path = tempfile.mkstemp(suffix='.py')
try:
    with os.fdopen(temp_fd, 'w') as f:
        f.write(code)
    
    print(f"[INFO] Temp script written to: {temp_path}")
    python_exe = r'C:\Users\Abel Philip\.conda\envs\lunar\python.exe'
    print(f"[INFO] Running with: {python_exe}")
    
    result = subprocess.run(
        [r"C:\Users\Abel Philip\.conda\envs\lunar\python.exe", temp_path],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    print(f"[INFO] Return code: {result.returncode}")
    print(f"[INFO] STDOUT:\n{result.stdout}")
    print(f"[INFO] STDERR:\n{result.stderr}")
    
finally:
    try:
        os.unlink(temp_path)
    except:
        pass
