import pathlib

DATA_DIR = pathlib.Path.cwd() / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
CACHE_DIR = DATA_DIR / "cache"

ASSETS_DIR = pathlib.Path(__file__).parent / "assets"

[d.mkdir(parents=True, exist_ok=True) for d in {DATA_DIR, UPLOAD_DIR, CACHE_DIR}]
(DATA_DIR / ".gitignore").write_text("*")
