from osgeo import gdal
dem_path = r"C:\Users\Abel Philip\Downloads\WAC_GLD100_E000N1800_064P.IMG"
ds = gdal.Open(dem_path)
print("DEM loaded:", ds is not None)
if ds:
    band = ds.GetRasterBand(1)
    print("Band shape would be:", band.XSize, "x", band.YSize)
    ds = None
