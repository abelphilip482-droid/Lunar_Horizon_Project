#!/usr/bin/env python
import sys
print("Step 1: Python started", file=sys.stderr, flush=True)

try:
    from osgeo import gdal
    print("Step 2: GDAL imported", file=sys.stderr, flush=True)
    
    dem_path = r"C:\Users\Abel Philip\Downloads\WAC_GLD100_E000N1800_064P.IMG"
    print(f"Step 3: Opening DEM at {dem_path}", file=sys.stderr, flush=True)
    
    gdal.UseExceptions()
    print("Step 4: GDAL exceptions enabled", file=sys.stderr, flush=True)
    
    ds = gdal.Open(dem_path)
    print(f"Step 5: DEM opened: {ds is not None}", file=sys.stderr, flush=True)
    
    if ds:
        band = ds.GetRasterBand(1)
        print(f"Step 6: Band retrieved", file=sys.stderr, flush=True)
        
        # Try to read just the metadata, not the full array
        xsize = band.XSize
        ysize = band.YSize
        print(f"Step 7: Band size: {xsize}x{ysize}", file=sys.stderr, flush=True)
        
        # Try to read a small portion
        print("Step 8: Reading small portion...", file=sys.stderr, flush=True)
        data = band.ReadBlock(0, 0)
        print(f"Step 9: Block read successful", file=sys.stderr, flush=True)
        
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)

print("Script completed", file=sys.stderr, flush=True)
