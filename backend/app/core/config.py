import yaml
import os
from pathlib import Path

# Get the project root directory
# current file is in backend/app/core/config.py
# root is backend/../.. -> d:\Watone\Pixiv_Novel_Download
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_PATH = BASE_DIR / "configs" / "config.yaml"

def load_config():
    if not CONFIG_PATH.exists():
        return {
            "app_name": "Pixiv Novel Downloader",
            "debug": True,
            "proxy": {},
            "auth": {}
        }
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

app_config = load_config()

# Update with default values if missing
if "app_name" not in app_config:
    app_config["app_name"] = "Pixiv Novel Downloader"
if "proxy" not in app_config:
    app_config["proxy"] = {}
if "auth" not in app_config:
    app_config["auth"] = {}
