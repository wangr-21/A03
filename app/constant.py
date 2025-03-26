import pathlib

DATA_DIR = pathlib.Path.cwd() / "data"
UPLOAD_DIR = DATA_DIR / "uploads" / "homeworks"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

ASSETS_DIR = pathlib.Path(__file__).parent / "assets"
