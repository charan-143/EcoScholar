import json
from pathlib import Path
DATASET_PATH=Path(__file__).with_name("environmental_datasets.json")
def get_dataset_catalog():
    return json.loads(DATASET_PATH.read_text(encoding="utf-8"))
