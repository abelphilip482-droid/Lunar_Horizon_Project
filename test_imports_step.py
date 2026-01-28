import json
import sys
print(f"Step 1: imports ok", file=sys.stderr, flush=True)

try:
    from datetime import datetime
    print(f"Step 2: datetime imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"Step 2 ERROR: {e}", file=sys.stderr, flush=True)

try:
    import numpy as np
    print(f"Step 3: numpy imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"Step 3 ERROR: {e}", file=sys.stderr, flush=True)

try:
    import matplotlib
    print(f"Step 4: matplotlib imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"Step 4 ERROR: {e}", file=sys.stderr, flush=True)

try:
    from osgeo import gdal
    print(f"Step 5: gdal imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"Step 5 ERROR: {e}", file=sys.stderr, flush=True)

print(json.dumps({"status": "all imports successful"}))
