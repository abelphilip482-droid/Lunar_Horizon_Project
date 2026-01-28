#!/usr/bin/env python
"""
Lunar Calculator - Full implementation with lh.py logic and proper 4-panel plots
"""
import sys
import json
import base64
from io import BytesIO
from datetime import datetime, timedelta

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    
    # Get parameters from command line
    try:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        start_date = sys.argv[3]
        end_date = sys.argv[4]
    except (IndexError, ValueError) as e:
        print(json.dumps({"error": f"Invalid parameters: {e}"}))
        sys.exit(1)

    try:
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from osgeo import gdal
        from astropy.coordinates import get_sun
        from astropy.time import Time
        import astropy.units as u
        from lunarsky import MoonLocation, LunarTopo
        
        # ===============================
        # CONSTANTS
        # ===============================
        MILES_2_METERS = 1609.344
        RADIUS_METERS = 1.5 * MILES_2_METERS
        MOON_RADIUS = 1737400.0  # meters
        
        dem_path = r"C:\Users\Abel Philip\Downloads\WAC_GLD100_E000N1800_064P.IMG"
        
        # Load DEM
        gdal.UseExceptions()
        ds = gdal.Open(dem_path)
        if ds is None:
            raise RuntimeError(f"Failed to open DEM: {dem_path}")
        
        band = ds.GetRasterBand(1)
        image = band.ReadAsArray().astype(np.float32)
        
        H, W = image.shape
        deg_per_px_lon = 360.0 / W
        deg_per_px_lat = 180.0 / H
        meters_per_deg_lat = np.pi * MOON_RADIUS / 180.0
        
        # ===============================
        # COORD CONVERSION
        # ===============================
        def coord2pix(lon, lat):
            row = (H / 2.0) - (lat * H / 180.0)
            col = lon * W / 360.0
            return int(round(col)), int(round(row))
        
        # ===============================
        # EXTRACTION FUNCTION
        # ===============================
        def extract_radius_projection_aware(lon0, lat0):
            cx, cy = coord2pix(lon0, lat0)
            
            meters_per_deg_lon = meters_per_deg_lat * max(
                np.cos(np.deg2rad(lat0)), 0.05
            )
            
            px_x = meters_per_deg_lon * deg_per_px_lon
            px_y = meters_per_deg_lat * deg_per_px_lat
            half_diag = 0.5 * np.sqrt(px_x**2 + px_y**2)
            
            rx = int(np.ceil((RADIUS_METERS + half_diag) / px_x))
            ry = int(np.ceil((RADIUS_METERS + half_diag) / px_y))
            
            start_y = max(0, cy - ry)
            end_y   = min(H, cy + ry + 1)
            
            x_indices = (np.arange(cx - rx, cx + rx + 1) % W)
            
            stamp = image[start_y:end_y][:, x_indices]
            cx_l = rx
            cy_l = cy - start_y
            
            h, w = stamp.shape
            dist_map = np.zeros((h, w))
            mask = np.zeros((h, w), dtype=bool)
            
            for y in range(h):
                for x in range(w):
                    dx = (x - cx_l) * px_x
                    dy = (y - cy_l) * px_y
                    d = np.sqrt(dx**2 + dy**2)
                    dist_map[y, x] = d
                    mask[y, x] = d <= (RADIUS_METERS + half_diag)
            
            extracted = np.where(mask, stamp, np.nan)
            return extracted, dist_map, cx_l, cy_l
        
        # ===============================
        # RADIAL HORIZON SCAN
        # ===============================
        def radial_horizon_scan(extracted, dist_map, cx, cy):
            center_elev = extracted[cy, cx]
            dist_to_max = np.full(360, np.nan)
            horizon_angle = np.full(360, np.nan)
            
            for az in range(360):
                theta = np.deg2rad(az)
                max_elev = -np.inf
                step = 1
                
                while True:
                    x = int(round(cx + step * np.sin(theta)))
                    y = int(round(cy - step * np.cos(theta)))
                    
                    if x < 0 or y < 0 or x >= extracted.shape[1] or y >= extracted.shape[0]:
                        break
                    
                    d = dist_map[y, x]
                    if d > RADIUS_METERS:
                        break
                    
                    elev = extracted[y, x]
                    if not np.isnan(elev) and elev > max_elev:
                        max_elev = elev
                        dist_to_max[az] = d
                    
                    step += 1
                
                if max_elev > -np.inf and dist_to_max[az] > 0:
                    horizon_angle[az] = np.degrees(
                        np.arctan((max_elev - center_elev) / dist_to_max[az])
                    )
            
            delta_h = (np.tan(np.deg2rad(horizon_angle)) * dist_to_max)
            return delta_h, dist_to_max, horizon_angle
        
        # ===============================
        # SUN POSITION FUNCTION
        # ===============================
        def compute_sun_path(lon, lat, center_elev):
            moon_loc = MoonLocation(
                lon=lon * u.deg,
                lat=lat * u.deg,
                height=center_elev * u.m
            )
            
            start_time = datetime.strptime(start_date, '%Y-%m-%d')
            stop_time = datetime.strptime(end_date, '%Y-%m-%d')
            increment = timedelta(days=1)
            
            sun_alt, sun_az = [], []
            t = start_time
            
            while t <= stop_time:
                frame = LunarTopo(obstime=Time(t), location=moon_loc)
                sun = get_sun(Time(t)).transform_to(frame)
                sun_alt.append(sun.alt.deg)
                sun_az.append(sun.az.deg % 360)
                t += increment
            
            return np.array(sun_az), np.array(sun_alt)
        
        # ===============================
        # PROCESSING
        # ===============================
        title = f"Location: Lat {latitude}°, Lon {longitude}°"
        
        extracted, dist_map, cx, cy = extract_radius_projection_aware(longitude, latitude)
        
        delta_h, dist_to_max, horizon_angle = radial_horizon_scan(
            extracted, dist_map, cx, cy
        )
        
        sun_az, sun_alt = compute_sun_path(longitude, latitude, extracted[cy, cx])
        
        horizon_angle = np.maximum(horizon_angle, 0.0)
        
        sun_visible = sun_alt > horizon_angle[np.floor(sun_az).astype(int) % 360]
        sunlight_hours = np.sum(sun_visible) * 24.0
        
        # ===============================
        # PLOTTING (4 PANELS)
        # ===============================
        fig, axes = plt.subplots(4, 1, figsize=(10, 14), constrained_layout=True)
        
        # ---- Row 1: DEM
        im = axes[0].imshow(extracted, cmap="jet")
        axes[0].plot(cx, cy, "rx", markersize=8)
        axes[0].contour(dist_map, levels=[RADIUS_METERS], colors="k")
        axes[0].set_title(title)
        axes[0].axis("off")
        
        cbar = fig.colorbar(
            im,
            ax=axes[0],
            orientation="vertical",
            fraction=0.046,
            pad=0.04
        )
        cbar.set_label("Elevation (m)")
        
        # ---- Row 2: ΔH
        axes[1].plot(delta_h)
        axes[1].set_title("ΔH vs Azimuth")
        axes[1].set_xlabel("Azimuth (deg)")
        axes[1].set_ylabel("Elevation Difference (m)")
        axes[1].grid(True)
        
        # ---- Row 3: Distance
        axes[2].plot(dist_to_max)
        axes[2].set_title("Distance to Horizon")
        axes[2].set_xlabel("Azimuth (deg)")
        axes[2].set_ylabel("Distance (m)")
        axes[2].grid(True)
        
        # ---- Row 4: Horizon + Sun
        axes[3].plot(horizon_angle, label="Terrain horizon", linewidth=2)
        axes[3].scatter(sun_az, sun_alt, s=10, c="orange", label="Sun path", zorder=3)
        axes[3].axhline(0, linestyle="--", color="k")
        axes[3].set_title("Sun vs Terrain Horizon Angle")
        axes[3].set_xlabel("Azimuth (deg)")
        axes[3].set_ylabel("Angle (deg)")
        axes[3].legend()
        axes[3].grid(True)
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='PNG', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close('all')
        
        # Return success
        output = {
            "success": True,
            "message": "Calculation completed successfully",
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "sunlight_hours": float(sunlight_hours),
            "graph": img_base64
        }
        
        print(json.dumps(output))
        
    except Exception as e:
        import traceback
        print(json.dumps({
            "error": f"Calculation error: {str(e)}",
            "traceback": traceback.format_exc()[:500]
        }))
        sys.exit(1)
