import json
from pathlib import Path
CATALOG_PATH = Path(__file__).with_name("environmental_sources.json")
def get_source_catalog():
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
