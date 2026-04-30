import pandas as pd
from src.config import RAW_DATA_PATH, IMAGES_DATA_PATH


def load_restaurant_data() -> pd.DataFrame:
    """Load raw restaurant data."""
    return pd.read_csv(RAW_DATA_PATH)


def load_images_data() -> pd.DataFrame:
    """Load restaurant image data."""
    return pd.read_csv(IMAGES_DATA_PATH)
