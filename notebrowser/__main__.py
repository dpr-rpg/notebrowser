"""Generate static site from GM notes."""
import os
from pathlib import Path
from sys import argv

from notebrowser.building import make

base_dir = Path(f"{os.getcwd()}") / Path(argv[1])
assert base_dir.exists()
assert base_dir.is_dir()
make(base_dir)
