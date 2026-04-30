from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[1]

# Main folders
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ASSETS_DIR = BASE_DIR / "assets"

# Input files
RAW_DATA_PATH = RAW_DATA_DIR / "raw_data.csv"
IMAGES_DATA_PATH = RAW_DATA_DIR / "imagenes.csv"

# Output files
CLEAN_DATA_PATH = PROCESSED_DATA_DIR / "clean_data.csv"
RESTAURANT_RANKING_PATH = PROCESSED_DATA_DIR / "restaurant_ranking.csv"
