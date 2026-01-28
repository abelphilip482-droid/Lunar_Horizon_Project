import sys
sys.path.insert(0, r"C:\Users\Abel Philip\OneDrive\Documents")

try:
    print("Attempting to import lh.py...")
    import lh
    print("SUCCESS: lh.py imported")
except Exception as e:
    print(f"ERROR importing lh.py: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
