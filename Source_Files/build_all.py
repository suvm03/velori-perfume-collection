"""Rebuild all deliverables and verify PDFs/images."""
from pathlib import Path
import subprocess
import sys

here=Path(__file__).resolve().parent
for script in ['build_collection.py','finish_assets.py','verify_deliverables.py']:
    subprocess.run([sys.executable,str(here/script)],check=True)
