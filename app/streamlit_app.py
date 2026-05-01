import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.config import (
    RESTAURANT_RANKING_PATH,
    CLEAN_DATA_PATH,
    IMAGES_DATA_PATH
)

import math
import html
import time
import json
import re
import unicodedata
import urllib.parse
import urllib.request
import io
from pathlib import Path
import streamlit as st
import pandas as pd
import folium
from folium.features import DivIcon
from folium.plugins import AntPath
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from branca.element import MacroElement, Template
from PIL import Image, ImageOps

st.set_page_config(layout="wide")

# -------------------------
# STYLE
# -------------------------
st.markdown("""
<style>
/* SIDEBAR */
section[data-testid="stSidebar"] {
    width: 380px !important;
    min-width: 380px !important;
    max-width: 380px !important;
}
section[data-testid="stSidebar"] > div {
    width: 380px !important;
    min-width: 380px !important;
    max-width: 380px !important;
}
section[data-testid="stSidebar"] * {
    font-size: 17px !important;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 0.5rem !important;
}

/* REMOVE TOP SPACE */
[data-testid="stAppViewContainer"] {
    overflow-x: hidden;
    padding-top: 0px !important;
}

/* CARDS */
.card {
    padding: 16px;
    border-radius: 14px;
    background-color: white;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    margin-bottom: 12px;
    font-size: 16px;
    border: 2px solid transparent;
    transition: all 0.15s ease;
}
.card.active {
    background-color: #fff1ed;
    border: 2px solid #ff3b1f;
    box-shadow: 0 6px 18px rgba(255,59,31,0.12);
}

/* REVIEW SIDEBAR RIGHT */
.review-panel {
    position: sticky;
    top: 20px;
}

.review-card {
    background: white;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    border: 1px solid #f3f4f6;
}

.review-text {
    font-size: 18.5px;
    line-height: 1.75;
    color: #111827;
}

/* IMAGE GALLERY */
.photo-collage-box {
    background: white;
    border-radius: 18px;
    padding: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    margin-top: 8px;
}

.photo-collage {
    column-count: 3;
    column-gap: 12px;
}

.photo-tile {
    break-inside: avoid;
    margin-bottom: 12px;
    border-radius: 16px;
    overflow: hidden;
    background: #f8fafc;
}

.photo-tile img {
    width: 100%;
    height: auto;
    display: block;
    object-fit: cover;
}

@media (max-width: 1100px) {
    .photo-collage {
        column-count: 2;
    }
}

@media (max-width: 700px) {
    .photo-collage {
        column-count: 1;
    }
}

/* MAP TOOLTIP */
.leaflet-tooltip {
    display: none !important;
}

/* POPUP LINKS */
.popup-link {
    text-decoration: none;
    color: #111827;
    cursor: pointer;
}
.popup-link:hover {
    color: #ff3b1f;
}

/* COVER */
.cover-wrap {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle at top, #fff1ed 0%, #fff7f3 35%, #ffffff 75%);
    padding: 30px 20px;
}

.cover-box {
    text-align: center;
    animation: fadeIn 1.2s ease forwards;
}

.cover-line {
    display: block;
    opacity: 0;
    transform: translateY(30px);
    animation: riseUp 0.9s ease forwards;
}

.cover-line.big {
    font-size: 96px;
    font-weight: 900;
    line-height: 0.9;
    color: #ff3b1f;
    letter-spacing: 2px;
    animation-delay: 0.15s;
}

.cover-line.small {
    font-size: 44px;
    font-weight: 800;
    color: #111827;
    margin-top: 40px;
    letter-spacing: 6px;
    animation-delay: 0.6s;
}

.cover-sub {
    margin-top: 70px;
    margin-bottom: 28px;
    font-size: 20px;
    color: #6b7280;
    opacity: 0;
    transform: translateY(20px);
    animation: riseUp 0.9s ease forwards;
    animation-delay: 1s;
    animation-fill-mode: forwards;
}

.cover-fake-button {
    display: inline-block;
    padding: 14px 28px;
    border-radius: 999px;
    background: #ff3b1f;
    color: white;
    font-size: 18px;
    font-weight: 700;
    box-shadow: 0 8px 24px rgba(255,59,31,0.22);
    border: none;
    cursor: pointer;
}

div[data-testid="stButton"] > button {
    border-radius: 999px;
    font-weight: 700;
    min-height: 44px;
}

/* CATEGORY PILLS */
.category-pill-label {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.3px;
    color: #6b7280;
    margin-bottom: 8px;
    text-transform: uppercase;
}

div[data-testid="stButton"] > button[kind="secondary"] {
    border-radius: 999px !important;
    border: 1px solid #f3d6cf !important;
    background: #fffaf8 !important;
    color: #7c2d12 !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    min-height: 42px !important;
    padding: 0 14px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
    border: 1px solid #ffb7a8 !important;
    background: #fff1ed !important;
    color: #ff3b1f !important;
}

div[data-testid="stButton"] > button[kind="primary"] {
    border-radius: 999px !important;
    border: 1px solid #ff3b1f !important;
    background: #ff3b1f !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    min-height: 42px !important;
    padding: 0 14px !important;
    box-shadow: 0 8px 20px rgba(255,59,31,0.18) !important;
}

/* TRANSITION */
.transition-overlay {
    position: fixed;
    inset: 0;
    z-index: 99999;
    background:
        radial-gradient(circle at center, #fff4ef 0%, #fff9f7 45%, #ffffff 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    animation: overlayReveal 1.35s ease forwards;
}

.transition-overlay::before {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    border-radius: 999px;
    background: rgba(255, 59, 31, 0.08);
    filter: blur(2px);
    animation: softHalo 1.1s ease-out forwards;
}

.transition-overlay::after {
    content: "";
    position: absolute;
    width: 320px;
    height: 320px;
    border-radius: 999px;
    border: 1.5px solid rgba(255, 59, 31, 0.10);
    animation: softRing 1.15s ease-out forwards;
}

.transition-logo-wrap {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
    z-index: 2;
    animation: logoEntrance 1.05s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    transform-origin: center center;
}

.wheat-badge {
    width: 138px;
    height: 138px;
    border-radius: 999px;
    background: linear-gradient(180deg, #ff7258 0%, #ff4b2b 55%, #ff3b1f 100%);
    position: relative;
    box-shadow:
        0 18px 40px rgba(255,59,31,0.20),
        0 0 0 10px rgba(255,59,31,0.05);
    animation: badgeFloat 1s ease-out forwards;
}

.wheat-stem {
    position: absolute;
    left: 50%;
    top: 26px;
    width: 4px;
    height: 86px;
    background: white;
    transform: translateX(-50%);
    border-radius: 999px;
    animation: stemGrow 0.34s ease-out 0.18s both;
}

.wheat-leaf-l1,
.wheat-leaf-l2,
.wheat-leaf-l3,
.wheat-leaf-r1,
.wheat-leaf-r2,
.wheat-leaf-r3 {
    position: absolute;
    width: 24px;
    height: 10px;
    background: white;
    border-radius: 999px;
    opacity: 0;
}

.wheat-leaf-l1 { left: 52px; top: 38px; transform: rotate(-55deg) scale(0.6); animation: leafPop 0.18s ease-out 0.28s forwards; }
.wheat-leaf-l2 { left: 47px; top: 53px; transform: rotate(-55deg) scale(0.6); animation: leafPop 0.18s ease-out 0.36s forwards; }
.wheat-leaf-l3 { left: 42px; top: 68px; transform: rotate(-55deg) scale(0.6); animation: leafPop 0.18s ease-out 0.44s forwards; }
.wheat-leaf-r1 { right: 52px; top: 38px; transform: rotate(55deg) scale(0.6); animation: leafPop 0.18s ease-out 0.28s forwards; }
.wheat-leaf-r2 { right: 47px; top: 53px; transform: rotate(55deg) scale(0.6); animation: leafPop 0.18s ease-out 0.36s forwards; }
.wheat-leaf-r3 { right: 42px; top: 68px; transform: rotate(55deg) scale(0.6); animation: leafPop 0.18s ease-out 0.44s forwards; }

.wheat-slash {
    position: absolute;
    left: 34px;
    top: 73px;
    width: 72px;
    height: 5px;
    background: white;
    border-radius: 999px;
    transform: rotate(-38deg) scaleX(0.2);
    transform-origin: center;
    opacity: 0;
    animation: slashDraw 0.22s ease-out 0.56s forwards;
}

.transition-text {
    font-size: 15px;
    font-weight: 900;
    color: #111827;
    letter-spacing: 4px;
    opacity: 0;
    transform: translateY(8px);
    animation: textFadeUp 0.34s ease-out 0.5s forwards;
}

@keyframes riseUp {
    from { opacity: 0; transform: translateY(30px); letter-spacing: 12px; }
    to { opacity: 1; transform: translateY(0); letter-spacing: normal; }
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes softHalo { 0% { opacity: 0; transform: scale(0.7); } 100% { opacity: 1; transform: scale(1.08); } }
@keyframes softRing { 0% { opacity: 0; transform: scale(0.82); } 100% { opacity: 1; transform: scale(1.02); } }
@keyframes logoEntrance {
    0% { opacity: 0; transform: translateY(18px) scale(0.92); filter: blur(6px); }
    45% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    78% { opacity: 1; transform: translateY(-2px) scale(1.02); }
    100% { opacity: 0; transform: translateY(-6px) scale(1.06); }
}
@keyframes badgeFloat { 0% { transform: scale(0.9); } 100% { transform: scale(1); } }
@keyframes stemGrow { 0% { opacity: 0; height: 0; } 100% { opacity: 1; height: 86px; } }
@keyframes leafPop { 0% { opacity: 0; transform: scale(0.6); } 100% { opacity: 1; } }
@keyframes slashDraw { 0% { opacity: 0; transform: rotate(-38deg) scaleX(0.2); } 100% { opacity: 1; transform: rotate(-38deg) scaleX(1); } }
@keyframes textFadeUp { 0% { opacity: 0; transform: translateY(8px); } 100% { opacity: 0.95; transform: translateY(0); } }
@keyframes overlayReveal {
    0% { opacity: 0; }
    8% { opacity: 1; }
    82% { opacity: 1; }
    100% { opacity: 0; visibility: hidden; }
}
@keyframes blink {
    50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HELPERS
# -------------------------
def normalize_text(value):
    if pd.isna(value):
        return ""
    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("utf-8")
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value

def highlight_keywords(text):
    if not text:
        return ""

    escaped_text = html.escape(str(text))
    keyword_pattern = re.compile(
        r"\bgluten free\b|\bgluten-free\b|\bgluten\b|\bgf\b|\bceliac\b|\bcoeliac\b",
        flags=re.IGNORECASE
    )

    return keyword_pattern.sub(lambda match: f"<b>{match.group(0)}</b>", escaped_text)

def get_query_param_value(key):
    value = st.query_params.get(key)
    if isinstance(value, list):
        return value[0] if value else None
    return value

def find_category_column(df):
    possible_cols = [
        "categoryName",
        "category_name",
        "category",
        "CategoryName",
        "Category",
        "categoryname"
    ]
    for col in possible_cols:
        if col in df.columns:
            return col

    normalized = {str(col).strip().lower(): col for col in df.columns}
    for key in ["categoryname", "category_name", "category"]:
        if key in normalized:
            return normalized[key]

    return None



def get_project_root():
    app_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    if (app_dir / "data").exists() or (app_dir / "assets").exists():
        return app_dir
    if (app_dir.parent / "data").exists() or (app_dir.parent / "assets").exists():
        return app_dir.parent
    return app_dir

def candidate_file_paths(*relative_parts):
    project_root = get_project_root()
    app_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    rel_path = Path(*relative_parts)

    candidates = [
        project_root / rel_path,
        app_dir / rel_path,
        Path.cwd() / rel_path,
        Path("/mnt/data") / rel_path.name,
    ]

    unique = []
    seen = set()
    for path in candidates:
        key = str(path)
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique



@st.cache_data
def load_data():
    df = pd.read_csv(RESTAURANT_RANKING_PATH)

    df.columns = df.columns.str.strip()

    # The CSV uses lat + lng. Keep lng, and create lon as an alias
    # because the rest of the app uses lon in several places.
    if "lng" in df.columns:
        df["lng"] = (
            df["lng"]
            .astype(str)
            .str.strip()
            .str.replace(",", ".", regex=False)
        )
        df["lng"] = pd.to_numeric(df["lng"], errors="coerce")
        df["lon"] = df["lng"]

    if "lat" in df.columns:
        df["lat"] = (
            df["lat"]
            .astype(str)
            .str.strip()
            .str.replace(",", ".", regex=False)
        )
        df["lat"] = pd.to_numeric(df["lat"], errors="coerce")

    if "title" in df.columns:
        df = df.rename(columns={"title": "restaurant_name"})

    if "safety_pct" in df.columns:
        df = df.rename(columns={"safety_pct": "safety_percent"})

    if "ranking_score" in df.columns:
        df = df.rename(columns={"ranking_score": "ranking"})

    required_defaults = {
        "restaurant_name": "",
        "address": "",
        "categoryName": "Other",
        "price": "",
        "menu": "",
        "safe_reviews": 0,
        "unsafe_reviews": 0,
        "ranking": 0,
        "safety_percent": 0,
        "safety_label": "unsafe",
        "lat": None,
        "lon": None,
    }

    for col, default in required_defaults.items():
        if col not in df.columns:
            df[col] = default

    df = df.dropna(subset=["lat", "lon"]).copy()

    df["price_tier"] = df["price"].fillna("").astype(str)
    df["price_display"] = df["price_tier"]

    df = df.reset_index(drop=True)
    df["row_id"] = df.index.astype(str)
    df["restaurant_name_norm"] = df["restaurant_name"].apply(normalize_text)

    return df

@st.cache_data
def load_reviews():
    try:
        df = pd.read_csv(CLEAN_DATA_PATH)
    except Exception:
        return pd.DataFrame(columns=[
            "restaurant_title", "text", "restaurant_title_norm", "title_norm", "text_norm"
        ])

    if df.empty:
        return pd.DataFrame(columns=[
            "restaurant_title", "text", "restaurant_title_norm", "title_norm", "text_norm"
        ])

    df = df.rename(columns={
        "title": "restaurant_title",
        "raw_review_text": "text"
    })

    if "restaurant_title" not in df.columns:
        df["restaurant_title"] = ""

    if "text" not in df.columns:
        df["text"] = ""

    df["restaurant_title"] = df["restaurant_title"].fillna("").astype(str)
    df["text"] = df["text"].fillna("").astype(str)

    df["restaurant_title_norm"] = df["restaurant_title"].apply(normalize_text)
    df["title_norm"] = df["restaurant_title_norm"]
    df["text_norm"] = df["text"].apply(normalize_text)

    return df.drop_duplicates(subset=["restaurant_title", "text"])

@st.cache_data
def load_images():
    try:
        img_df = pd.read_csv(IMAGES_DATA_PATH)
    except Exception:
        return pd.DataFrame(columns=["title", "title_norm"])

    if img_df.empty:
        return pd.DataFrame(columns=["title", "title_norm"])

    if "title" not in img_df.columns:
        return pd.DataFrame(columns=["title", "title_norm"])

    img_df["title"] = img_df["title"].fillna("").astype(str)
    img_df["title_norm"] = img_df["title"].apply(normalize_text)

    # limpiar URLs vacías o inválidas
    image_cols = [
        col for col in img_df.columns
        if "image" in col.lower() or "url" in col.lower()
    ]

    for col in image_cols:
        img_df[col] = img_df[col].fillna("").astype(str).str.strip()
        img_df[col] = img_df[col].replace(
            ["nan", "None", "none", "null", "NaN"],
            ""
        )

    return img_df


def get_reviews_for_restaurant(restaurant_name, reviews_df, max_reviews=12):
    name_norm = normalize_text(restaurant_name)

    if reviews_df.empty or not name_norm:
        return pd.DataFrame(columns=reviews_df.columns)

    restaurant_reviews = reviews_df[
        reviews_df["title_norm"] == name_norm
    ].copy()

    if restaurant_reviews.empty:
        restaurant_reviews = reviews_df[
            reviews_df["title_norm"].str.contains(name_norm, na=False, regex=False)
            | reviews_df["title_norm"].apply(lambda x: name_norm in x if isinstance(x, str) else False)
        ].copy()

    if restaurant_reviews.empty:
        return pd.DataFrame(columns=reviews_df.columns)

    gluten_pattern = (
        r"\bgluten\b|"
        r"\bgluten free\b|"
        r"\bgluten-free\b|"
        r"\bglutenfree\b|"
        r"\bgf\b|"
        r"\bceliac\b|"
        r"\bcoeliac\b|"
        r"\bcoeliac disease\b|"
        r"\bceliac disease\b"
    )

    restaurant_reviews = restaurant_reviews[
        restaurant_reviews["text_norm"].str.contains(
            gluten_pattern,
            na=False,
            regex=True
        )
    ].copy()

    return restaurant_reviews.head(max_reviews)

@st.cache_data(show_spinner=False)
def get_image_hash(url, timeout=6, hash_size=8):
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read()

        image = Image.open(io.BytesIO(data))
        image = ImageOps.exif_transpose(image).convert("L")
        image = image.resize((hash_size, hash_size), Image.Resampling.LANCZOS)

        pixels = list(image.getdata())
        avg = sum(pixels) / len(pixels)
        return "".join("1" if px >= avg else "0" for px in pixels)
    except Exception:
        return None


def hamming_distance(hash_a, hash_b):
    if not hash_a or not hash_b or len(hash_a) != len(hash_b):
        return 999
    return sum(ch1 != ch2 for ch1, ch2 in zip(hash_a, hash_b))


def _collect_distinct_image_urls(matched_rows, max_images=8, visual_dup_threshold=8):
    image_cols = [
        col for col in matched_rows.columns
        if (
            col == "imageUrl"
            or col.startswith("imageUrls/")
            or (col.startswith("images/") and col.endswith("/imageUrl"))
        )
    ]

    urls = []

    for _, row in matched_rows.iterrows():
        for col in image_cols:
            value = row.get(col)

            if pd.isna(value):
                continue

            url = str(value).strip()

            if not url:
                continue

            if not url.startswith("http"):
                continue

            urls.append(url)

    clean_urls = []
    seen = set()

    for url in urls:
        key = url.split("?")[0].rstrip("/").lower()
        if key not in seen:
            seen.add(key)
            clean_urls.append(url)

        if len(clean_urls) >= max_images:
            break

    return clean_urls


def get_images_for_restaurant(restaurant_name, images_df, max_images=8):
    name_norm = normalize_text(restaurant_name)

    if not name_norm or images_df.empty:
        return []

    matched = images_df[images_df["title_norm"] == name_norm].copy()

    if matched.empty:
        matched = images_df[
            images_df["title_norm"].str.contains(name_norm, na=False, regex=False)
        ].copy()

    if matched.empty:
        return []

    return _collect_distinct_image_urls(matched, max_images=max_images)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_route(lat1, lon1, lat2, lon2, mode="driving"):
    mode = "foot" if str(mode).lower() in ["foot", "walking", "walk"] else "driving"
    url = (
        f"https://router.project-osrm.org/route/v1/{mode}/"
        f"{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
    )

    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        routes = data.get("routes", [])
        if not routes:
            return None, None, None

        route = routes[0]
        coords = route.get("geometry", {}).get("coordinates", [])
        if not coords:
            return None, None, None

        latlon_coords = [(coord[1], coord[0]) for coord in coords]
        distance_km = route.get("distance", 0) / 1000
        duration_min = route.get("duration", 0) / 60
        return latlon_coords, distance_km, duration_min
    except Exception:
        return None, None, None

def build_restaurant_url(row_id):
    return f"/?restaurant={urllib.parse.quote(str(row_id))}"


def get_menu_url(row):
    menu_value = row.get("menu", "")

    if pd.isna(menu_value):
        return None

    menu_value = str(menu_value).strip()
    if not menu_value or menu_value.lower() in {"nan", "none", "null"}:
        return None

    if not re.match(r"^https?://", menu_value, flags=re.IGNORECASE):
        menu_value = f"https://{menu_value}"

    return menu_value

def safe_rate_percent(value):
    if pd.notnull(value):
        try:
            value = float(value)
            if 0 <= value <= 1:
                value *= 100
            return f"{value:.2f}%"
        except Exception:
            return "N/A"
    return "N/A"


def get_safety_badge_color(value):
    try:
        if pd.isnull(value):
            return "#9ca3af"
        value = float(value)
        if 0 <= value <= 1:
            value *= 100
        if value >= 80:
            return "#22c55e"
        elif value >= 50:
            return "#facc15"
        return "#ef4444"
    except Exception:
        return "#9ca3af"


def render_safety_badge_html(value):
    badge_color = get_safety_badge_color(value)
    badge_text = html.escape(safe_rate_percent(value))
    return f"""
    <style>
    @keyframes safetyBadgeShine {{
        0% {{
            transform: translateX(-130%) translateY(-10%) rotate(25deg);
        }}
        100% {{
            transform: translateX(130%) translateY(-10%) rotate(25deg);
        }}
    }}
    </style>
    <div style="display:flex; justify-content:center; align-items:center; padding-top:6px;">
        <div style="
            position:relative;
            width:170px;
            height:170px;
            min-width:170px;
            border-radius:999px;
            background:{badge_color};
            color:white;
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            box-shadow:0 12px 30px rgba(0,0,0,0.12);
            text-align:center;
            padding:16px;
            box-sizing:border-box;
            overflow:hidden;
            isolation:isolate;
        ">
            <div style="
                position:absolute;
                top:-35%;
                left:-60%;
                width:70%;
                height:170%;
                background:linear-gradient(
                    120deg,
                    rgba(255,255,255,0) 0%,
                    rgba(255,255,255,0.12) 35%,
                    rgba(255,255,255,0.55) 50%,
                    rgba(255,255,255,0.12) 65%,
                    rgba(255,255,255,0) 100%
                );
                filter:blur(2px);
                animation:safetyBadgeShine 3.8s ease-in-out infinite;
                pointer-events:none;
                z-index:1;
            "></div>
            <div style="
                position:absolute;
                inset:6px;
                border-radius:999px;
                border:1.5px solid rgba(255,255,255,0.28);
                pointer-events:none;
                z-index:1;
            "></div>
            <div style="position:relative; z-index:2; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div style="font-size:18px; font-weight:800; letter-spacing:0.5px; line-height:1.1; margin-bottom:10px; opacity:0.95;">SAFETY RATE</div>
                <div style="font-size:40px; font-weight:900; line-height:1;">{badge_text}</div>
            </div>
        </div>
    </div>
    """

def get_popup_images_for_restaurant(restaurant_name, images_df, max_images=3):
    name_norm = normalize_text(restaurant_name)

    if not name_norm or images_df is None or images_df.empty:
        return []

    matched = images_df[images_df["title_norm"] == name_norm].copy()

    if matched.empty:
        matched = images_df[
            images_df["title_norm"].str.contains(name_norm, na=False, regex=False)
        ].copy()

    if matched.empty:
        return []

    return _collect_distinct_image_urls(matched, max_images=max_images)


def build_popup_html(row, images_df=None):
    name = html.escape(str(row.get("restaurant_name", "")))
    category = html.escape(str(row.get("categoryName", row.get("category", ""))))
    price = html.escape(str(row.get("price_tier", "") or row.get("price", "")))
    restaurant_url = build_restaurant_url(row["row_id"])

    safe_rate_raw = row.get("safety_percent", None)
    if pd.notnull(safe_rate_raw):
        try:
            safe_rate_value = float(safe_rate_raw)
            if 0 <= safe_rate_value <= 1:
                safe_rate_value *= 100
            safe_rate_pct = f"{safe_rate_value:.2f}%"
        except Exception:
            safe_rate_pct = "N/A"
    else:
        safe_rate_pct = "N/A"

    preview_html = ""
    if images_df is not None:
        preview_images = get_popup_images_for_restaurant(
            row.get("restaurant_name", ""),
            images_df,
            max_images=3,
        )

        if preview_images:
            imgs_html = ""
            for img_url in preview_images:
                safe_url = html.escape(str(img_url), quote=True)
                imgs_html += f"""
                <img
                    src="{safe_url}"
                    style="
                        width:32%;
                        height:78px;
                        object-fit:cover;
                        border-radius:10px;
                        display:block;
                        flex:0 0 auto;
                        background:#f3f4f6;
                    "
                >
                """

            preview_html = f"""
            <div style="
                display:flex;
                gap:6px;
                margin-bottom:10px;
            ">
                {imgs_html}
            </div>
            """

    return f"""
    <div style="
        min-width:260px;
        max-width:320px;
        padding:12px 14px;
        border-radius:14px;
        background:#ffffff;
        font-family: Arial, sans-serif;
    ">
        {preview_html}

        <div style="
            font-size:17px;
            font-weight:800;
            color:#111827;
            line-height:1.25;
            margin-bottom:6px;
        ">
            <a
                href="{restaurant_url}"
                target="_blank"
                rel="noopener noreferrer"
                class="popup-link"
            >
                {name}
            </a>
        </div>

        <div style="font-size:12px; color:#374151; line-height:1.6;">
            <div><b>Category:</b> {category}</div>
            <div><b>Price:</b> {price}</div>
            <div><b>Safety:</b> {safe_rate_pct}</div>
        </div>
    </div>
    """

def build_hover_text(row):

    name = str(row.get("restaurant_name", ""))
    address = str(row.get("address", ""))
    category = str(row.get("categoryName", row.get("category", "")))
    price = str(row.get("price_tier", "") or row.get("price", ""))
    safe_rate = safe_rate_percent(row.get("safety_percent"))

    distance_text = ""
    if pd.notnull(row.get("distance_km")):
        distance_text = f"\n{row['distance_km']:.2f} km"

    text = f"{name}\n{address}\n{category}\nSafe rate: {safe_rate}{distance_text}"
    return html.escape(text, quote=True)

def normalize_safety_label(value):
    if pd.isna(value):
        return "unsafe"

    value = str(value).strip().lower()

    if value == "safe":
        return "safe"
    elif value == "unsafe":
        return "unsafe"
    elif value in ["partly safe", "partly_safe", "partlysafe"]:
        return "partly safe"

    return "unsafe"

def get_marker_style(row, active=False):
    label = normalize_safety_label(row.get("safety_label", "unsafe"))

    if label == "safe":
        return {"bg": "#22c55e", "text": "GF", "show_text": True, "strikethrough": False}
    elif label == "unsafe":
        return {"bg": "#ef4444", "text": "GF", "show_text": True, "strikethrough": True}
    else:
        return {"bg": "#facc15", "text": "GF", "show_text": True, "strikethrough": False}


def marker_html(active=False, hover_text="", bg="#ff3b1f", text="GF", show_text=True, strikethrough=False):
    size = 30 if active else 24
    shadow = "0 0 0 10px rgba(255,59,31,0.16)" if active else "0 6px 16px rgba(255,59,31,0.18)"
    font_size = "12px" if active else "11px"
    content = text if show_text else " "

    slash_html = ""
    if strikethrough:
        slash_width = int(size * 0.95)
        slash_html = f"""
        <div style="
            position:absolute;
            width:{slash_width}px;
            height:3px;
            background:white;
            border-radius:999px;
            top:50%;
            left:50%;
            transform:translate(-50%, -50%) rotate(-45deg);
            box-shadow:0 0 2px rgba(0,0,0,0.15);
            pointer-events:none;
            z-index:2;
        "></div>
        """

    return f"""
    <div
        title="{hover_text}"
        style="
            position:relative;
            width:{size}px;
            height:{size}px;
            border-radius:999px;
            background:{bg};
            color:white;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:{font_size};
            font-weight:900;
            border:3px solid white;
            box-shadow:{shadow};
            font-family:Arial,sans-serif;
            cursor:pointer;
            overflow:hidden;
        ">
        <span style="position:relative; z-index:1;">{content}</span>
        {slash_html}
    </div>
    """

def add_sequential_gf_animation(map_obj, rows):
    marker_data = []

    for _, row in rows.iterrows():
        hover_text = build_hover_text(row)
        style = get_marker_style(row, active=False)

        marker_data.append({
            "lat": float(row["lat"]),
            "lon": float(row["lon"]),
            "popup": build_popup_html(row, images_df),
            "tooltip": str(row["row_id"]),
            "hover_text": hover_text,
            "icon_html": marker_html(
                active=False,
                hover_text=hover_text,
                bg=style["bg"],
                text=style["text"],
                show_text=style["show_text"],
                strikethrough=style["strikethrough"]
            )
        })

    marker_data_json = json.dumps(marker_data)

    template = Template(f"""
    {{% macro script(this, kwargs) %}}
    const map = {{this._parent.get_name()}};
    const markerData = {marker_data_json};

    function addMarkerSequentially(item, index) {{
        setTimeout(() => {{
            const marker = L.marker([item.lat, item.lon], {{
                icon: L.divIcon({{
                    className: '',
                    html: item.icon_html,
                    iconSize: [24, 24],
                    iconAnchor: [12, 12],
                    popupAnchor: [0, -12]
                }})
            }}).addTo(map);

            marker.bindPopup(item.popup, {{ maxWidth: 320 }});

            const el = marker.getElement();
            if (el) {{
                el.style.opacity = '0';
                el.style.transform = 'scale(0.2)';
                el.style.transition = 'opacity 0.28s ease, transform 0.32s ease';

                requestAnimationFrame(() => {{
                    el.style.opacity = '1';
                    el.style.transform = 'scale(1)';
                }});
            }}
        }}, 180 + index * 140);
    }}

    map.whenReady(() => {{
        markerData.forEach((item, index) => {{
            addMarkerSequentially(item, index);
        }});
    }});
    {{% endmacro %}}
    """)

    macro = MacroElement()
    macro._template = template
    map_obj.get_root().add_child(macro)

# -------------------------
# SESSION STATE
# -------------------------
if "user_location" not in st.session_state:
    st.session_state.user_location = None

if "geo_error" not in st.session_state:
    st.session_state.geo_error = None

if "selected_id" not in st.session_state:
    st.session_state.selected_id = None

if "last_search" not in st.session_state:
    st.session_state.last_search = None


if "last_location_key" not in st.session_state:
    st.session_state.last_location_key = None

if "last_price" not in st.session_state:
    st.session_state.last_price = "All"

if "last_price_filter" not in st.session_state:
    st.session_state.last_price_filter = "All"

if "filtered_df_cached" not in st.session_state:
    st.session_state.filtered_df_cached = None

if "show_map" not in st.session_state:
    st.session_state.show_map = False

if get_query_param_value("restaurant") is not None:
    st.session_state.show_map = True

if "map_transition" not in st.session_state:
    st.session_state.map_transition = False

if "pins_animated" not in st.session_state:
    st.session_state.pins_animated = False

if "last_category" not in st.session_state:
    st.session_state.last_category = "All"

if "selected_category_label" not in st.session_state:
    st.session_state.selected_category_label = "All"

if "route_target" not in st.session_state:
    st.session_state.route_target = None

if "route_mode" not in st.session_state:
    st.session_state.route_mode = "driving"

if "route_summary" not in st.session_state:
    st.session_state.route_summary = None


# -------------------------
# GEOLOCATION
# -------------------------
if st.session_state.user_location is None and st.session_state.geo_error is None:
    loc = get_geolocation()

    if loc:
        if "error" in loc:
            st.session_state.geo_error = loc["error"]
        elif "coords" in loc:
            coords = loc["coords"]
            lat = coords.get("latitude")
            lon = coords.get("longitude")

            if lat is not None and lon is not None:
                st.session_state.user_location = {
                    "latitude": lat,
                    "longitude": lon
                }
                st.rerun()

location = st.session_state.user_location

# -------------------------
# DATA
# -------------------------
df = load_data()
reviews_df = load_reviews()
images_df = load_images()

# -------------------------
# COVER PAGE
# -------------------------
if not st.session_state.show_map and not st.session_state.map_transition:

    def set_cover_background():
        import base64
        candidate_paths = (
            candidate_file_paths("assets", "skyline.png")
            + candidate_file_paths("skyline.png")
            + candidate_file_paths("data", "skyline.png")
        )

        skyline_path = next((path for path in candidate_paths if path.exists()), None)
        if skyline_path is None:
            return

        with open(skyline_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .cover-wrap {{
            position: relative;
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        .cover-wrap::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: rgba(255,255,255,0.65);
        }}

        .cover-box {{
            position: relative;
            z-index: 2;
        }}
        </style>
        """, unsafe_allow_html=True)

    set_cover_background()

    st.markdown("""
    <div class="cover-wrap">
        <div class="cover-box">
            <span class="cover-line big">GLUTEN FREE</span>
            <span class="cover-line small">MELBOURNE</span>
            <div class="cover-sub">
                Find gluten-free restaurants near you
            </div>
            <form action="" method="get">
                <button name="go_map" value="1" class="cover-fake-button">
                    Explore map
                </button>
            </form>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if get_query_param_value("go_map") == "1":
        st.session_state.map_transition = True
        st.session_state.pins_animated = False
        st.query_params.clear()
        st.rerun()

    st.stop()

# -------------------------
# TRANSITION
# -------------------------
if st.session_state.map_transition:
    st.markdown("""
    <div class="transition-overlay">
        <div class="transition-logo-wrap">
            <div class="wheat-badge">
                <div class="wheat-stem"></div>
                <div class="wheat-leaf-l1"></div>
                <div class="wheat-leaf-l2"></div>
                <div class="wheat-leaf-l3"></div>
                <div class="wheat-leaf-r1"></div>
                <div class="wheat-leaf-r2"></div>
                <div class="wheat-leaf-r3"></div>
                <div class="wheat-slash"></div>
            </div>
            <div class="transition-text">GLUTEN FREE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(1.2)
    st.session_state.map_transition = False
    st.session_state.show_map = True
    st.rerun()

# -------------------------
# RESTAURANT PAGE
# -------------------------
restaurant_page = get_query_param_value("restaurant")

if restaurant_page is not None:
    restaurant_page = str(restaurant_page)
    selected_restaurant = df[df["row_id"].astype(str) == restaurant_page]

    if not selected_restaurant.empty:
        r = selected_restaurant.iloc[0]

        restaurant_reviews = get_reviews_for_restaurant(
            r.get("restaurant_name", ""),
            reviews_df,
            max_reviews=12
        )

        restaurant_images = get_images_for_restaurant(
            r.get("restaurant_name", ""),
            images_df,
            max_images=6
        )

        col_title, col_actions = st.columns([5, 2])

        with col_title:
            st.markdown(f"""
            <h1 style="
                font-weight: 900;
                color: #ff3b1f;
                line-height: 1.05;
                margin-bottom: 10px;
                margin-top: 40px;
                font-size: 56px;
            ">
                {html.escape(str(r.get("restaurant_name", "")))}
            </h1>
            """, unsafe_allow_html=True)

        with col_actions:
            st.markdown("<div style='margin-top:55px'></div>", unsafe_allow_html=True)
            if st.button("← Back", use_container_width=True):
                st.query_params.clear()
                st.rerun()

        col1, col2 = st.columns([2.2, 1])

        with col1:
            st.markdown('<h2 style="font-size:32px; margin-bottom:12px;">Information</h2>', unsafe_allow_html=True)

            info_col, badge_col = st.columns([3.2, 1.5], vertical_alignment="center")

            with info_col:
                st.markdown(f"""
                <div style="line-height:1.5; font-size:21px; margin-top:0;">
                    <p style="margin:0 0 8px 0;"><b>Address:</b> {html.escape(str(r.get('address', 'N/A')))}</p>
                    <p style="margin:0 0 8px 0;"><b>Category:</b> {html.escape(str(r.get('categoryName', 'N/A')))}</p>
                    <p style="margin:0 0 8px 0;"><b>Price:</b> {html.escape(str(r.get('price_tier', '') or r.get('price', 'N/A')))}</p>
                    <p style="margin:0 0 8px 0;"><b>Rank:</b> {html.escape(str(r.get('ranking', 'N/A')))}</p>
                    <p style="margin:0 0 8px 0;"><b>Safe reviews:</b> {html.escape(str(r.get('safe_reviews', 'N/A')))}</p>
                    <p style="margin:0 0 8px 0;"><b>Unsafe reviews:</b> {html.escape(str(r.get('unsafe_reviews', 'N/A')))}</p>
                    <p style="margin:0 0 8px 0;"><b>Safe rate:</b> {safe_rate_percent(r.get('safety_percent'))}</p>
                </div>
                """, unsafe_allow_html=True)

                menu_url = get_menu_url(r)
                if menu_url:
                    st.markdown('<div style="margin-top:14px;"></div>', unsafe_allow_html=True)
                    st.link_button("View menu", menu_url, use_container_width=False)

            with badge_col:
                st.markdown(render_safety_badge_html(r.get('safety_percent')), unsafe_allow_html=True)

            if restaurant_images:
                st.subheader("Photos")

                collage_html = '<div class="photo-collage-box"><div class="photo-collage">'
                for img_url in restaurant_images:
                    safe_url = html.escape(str(img_url), quote=True)
                    collage_html += f'<div class="photo-tile"><img src="{safe_url}" loading="lazy"></div>'
                collage_html += '</div></div>'

                st.markdown(collage_html, unsafe_allow_html=True)
            else:
                st.info("No photos found for this restaurant.")

            if pd.notnull(r.get("lat")) and pd.notnull(r.get("lon")):
                st.subheader("Directions")

                if location:
                    dir_col1, dir_col2, dir_col3 = st.columns(3)

                    with dir_col1:
                        if st.button("🚗", use_container_width=True, key=f"restaurant_drive_{restaurant_page}"):
                            st.session_state.route_target = {
                                "lat": float(r["lat"]),
                                "lon": float(r["lon"]),
                                "name": str(r.get("restaurant_name", "")),
                            }
                            st.session_state.route_mode = "driving"
                            st.session_state.route_summary = None
                            st.rerun()

                    with dir_col2:
                        if st.button("🚶", use_container_width=True, key=f"restaurant_walk_{restaurant_page}"):
                            st.session_state.route_target = {
                                "lat": float(r["lat"]),
                                "lon": float(r["lon"]),
                                "name": str(r.get("restaurant_name", "")),
                            }
                            st.session_state.route_mode = "foot"
                            st.session_state.route_summary = None
                            st.rerun()

                    with dir_col3:
                        if st.button("✖️", use_container_width=True, key=f"restaurant_clear_{restaurant_page}"):
                            st.session_state.route_target = None
                            st.session_state.route_summary = None
                            st.rerun()
                else:
                    st.info("Enable location to get directions.")

                restaurant_map = folium.Map(
                    location=[r["lat"], r["lon"]],
                    zoom_start=14,
                    tiles="CartoDB positron"
                )

                style = get_marker_style(r, active=True)

                folium.Marker(
                    location=[r["lat"], r["lon"]],
                    popup=folium.Popup(build_popup_html(r, images_df), max_width=340),
                    icon=DivIcon(
                        icon_size=(30, 30),
                        icon_anchor=(15, 15),
                        html=marker_html(
                            active=True,
                            hover_text=build_hover_text(r),
                            bg=style["bg"],
                            text=style["text"],
                            show_text=style["show_text"],
                            strikethrough=style["strikethrough"]
                        )
                    )
                ).add_to(restaurant_map)

                if location:
                    folium.Circle(
                        location=[location["latitude"], location["longitude"]],
                        radius=60,
                        color=None,
                        fill=True,
                        fill_color="#007aff",
                        fill_opacity=0.18
                    ).add_to(restaurant_map)

                    folium.CircleMarker(
                        location=[location["latitude"], location["longitude"]],
                        radius=7,
                        color="#ffffff",
                        weight=2,
                        fill=True,
                        fill_color="#007aff",
                        fill_opacity=1
                    ).add_to(restaurant_map)

                    target = st.session_state.route_target
                    if target is not None:
                        target_matches_current = (
                            abs(float(target["lat"]) - float(r["lat"])) < 0.000001
                            and abs(float(target["lon"]) - float(r["lon"])) < 0.000001
                        )

                        if target_matches_current:
                            route_coords, route_distance_km, route_duration_min = get_route(
                                location["latitude"],
                                location["longitude"],
                                float(target["lat"]),
                                float(target["lon"]),
                                st.session_state.route_mode,
                            )

                            if route_coords and route_distance_km is not None:
                                if st.session_state.route_mode == "foot":
                                    route_duration_min = (route_distance_km / 4.5) * 60
                                else:
                                    route_duration_min = (route_distance_km / 22) * 60

                                AntPath(
                                    locations=route_coords,
                                    color="#007aff",
                                    pulse_color="#7fb7ff",
                                    weight=6,
                                    delay=800,
                                    dash_array=[16, 24]
                                ).add_to(restaurant_map)
                                restaurant_map.fit_bounds(route_coords, padding=(30, 30))

                                st.session_state.route_summary = {
                                    "distance_km": route_distance_km,
                                    "duration_min": route_duration_min,
                                    "mode": st.session_state.route_mode,
                                    "name": target.get("name", "Destination"),
                                }
                            else:
                                st.session_state.route_summary = {
                                    "error": "Route unavailable",
                                    "mode": st.session_state.route_mode,
                                    "name": target.get("name", "Destination"),
                                }

                route_summary = st.session_state.route_summary
                if route_summary and route_summary.get("name") == str(r.get("restaurant_name", "")):
                    if route_summary.get("error"):
                        st.warning("Route unavailable right now.")
                    else:
                        mode_label = "Drive" if route_summary.get("mode") == "driving" else "Walk"
                        st.info(
                            f"{mode_label} route: {route_summary['distance_km']:.2f} km · {route_summary['duration_min']:.0f} min"
                        )

                st_folium(
                    restaurant_map,
                    height=500,
                    use_container_width=True,
                    key=f"restaurant_map_{restaurant_page}_{st.session_state.route_mode}_{'route' if st.session_state.route_target else 'noroute'}"
                )

        with col2:
            st.markdown('<div class="review-panel">', unsafe_allow_html=True)
            st.markdown('<h2 style="font-size:32px; margin-bottom:12px;">Gluten mentions in reviews</h2>', unsafe_allow_html=True)

            if restaurant_reviews.empty:
                st.info("No gluten-related reviews found.")
            else:
                st.markdown(f"<div style='font-size:18px; color:#6b7280; margin-bottom:12px;'>{len(restaurant_reviews)} gluten review(s) found</div>", unsafe_allow_html=True)

                for _, review_row in restaurant_reviews.iterrows():
                    full_text = str(review_row.get("text", ""))

                    review_placeholder = st.empty()
                    typed_text = ""

                    for char in full_text:
                        typed_text += char
                        review_placeholder.markdown(f"""
                        <div class="review-card">
                            <div class="review-text">
                                {highlight_keywords(typed_text)}
                                <span style="animation: blink 1s step-end infinite;">|</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.003)

                    time.sleep(0.08)

            st.markdown('</div>', unsafe_allow_html=True)

        st.stop()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("Restaurants")
search = st.sidebar.text_input("Search by name")

category_map = {
    "All": None,
    "Japanese": "Japanese restaurant",
    "Greek": "Greek restaurant",
    "Italian": "Italian restaurant",
    "Mexican": "Mexican restaurant",
    "Cafe": "Cafe",
    "Bagel": "Bagel shop",
    "Ice Cream": "Ice cream shop",
    "Bakery": "Bakery",
    "Healthy": "Health food restaurant",
    "Other": "OTHER"
}

category_icons = {
    "All": "✧",
    "Japanese": "🍣",
    "Greek": "🇬🇷",
    "Italian": "🍝",
    "Mexican": "🌮",
    "Cafe": "☕",
    "Bagel": "🥯",
    "Ice Cream": "🍦",
    "Bakery": "🥐",
    "Healthy": "🌿",
    "Other": "🍽"
}

st.sidebar.markdown('<div class="category-pill-label">Category</div>', unsafe_allow_html=True)

pill_rows = [
    ["All", "Japanese"],
    ["Greek", "Italian"],
    ["Mexican", "Cafe"],
    ["Bagel", "Ice Cream"],
    ["Bakery", "Healthy"],
    ["Other"]
]

for row in pill_rows:
    cols = st.sidebar.columns(len(row))
    for i, label in enumerate(row):
        with cols[i]:
            is_selected = st.session_state.selected_category_label == label
            button_type = "primary" if is_selected else "secondary"
            display_label = f"{category_icons.get(label, '')} {label}"

            if st.button(
                display_label,
                key=f"cat_{label}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.selected_category_label = label
                st.session_state.filtered_df_cached = None
                st.session_state.pins_animated = False
                st.rerun()

selected_category_label = st.session_state.selected_category_label

st.sidebar.markdown('<div class="category-pill-label" style="margin-top:12px;">Price</div>', unsafe_allow_html=True)

price_options = ["All", r"\$", r"\$\$", r"\$\$\$"]

price_cols = st.sidebar.columns(len(price_options))
selected_price_value = st.session_state.get("last_price", "All")

price_value_map = {
    "All": "All",
    r"\$": "$",
    r"\$\$": "$$",
    r"\$\$\$": "$$$"
}

selected_price_real = price_value_map.get(selected_price_value, selected_price_value)


for i, price in enumerate(price_options):
    with price_cols[i]:
        is_selected = selected_price_value == price
        button_type = "primary" if is_selected else "secondary"

        if st.button(
            price,
            key=f"price_{price}",
            use_container_width=True,
            type=button_type
        ):
            st.session_state.last_price = price
            st.session_state.filtered_df_cached = None
            st.session_state.pins_animated = False
            st.rerun()

selected_price_value = st.session_state.get("last_price", "All")

price_value_map = {
    "All": "All",
    r"\$": "$",
    r"\$\$": "$$",
    r"\$\$\$": "$$$"
}

selected_price_real = price_value_map.get(selected_price_value, selected_price_value)


# -------------------------
# FILTERING
# -------------------------
location_key = None
if location:
    location_key = (
        round(location["latitude"], 5),
        round(location["longitude"], 5)
    )

selected_category_value = category_map[selected_category_label]
category_col = find_category_column(df) or "categoryName"

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["restaurant_name"].fillna("").str.contains(search, case=False, na=False, regex=False)
    ].copy()

if selected_category_value is not None:
    if selected_category_label == "Other":
        known_categories = {
            value for key, value in category_map.items()
            if key not in ["All", "Other"] and value is not None
        }
        if category_col in filtered_df.columns:
            filtered_df = filtered_df[
                ~filtered_df[category_col].fillna("").isin(known_categories)
            ].copy()
        else:
            filtered_df = df.iloc[0:0].copy()
    else:
        if category_col in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df[category_col].fillna("") == selected_category_value
            ].copy()
        else:
            filtered_df = df.iloc[0:0].copy()

if selected_price_real != "All":
    if "price_tier" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["price_tier"].fillna("") == selected_price_real
        ].copy()
    else:
        filtered_df = df.iloc[0:0].copy()

if filtered_df.empty:
    filtered_df = df.iloc[0:0].copy()

if location and "lat" in filtered_df.columns and "lon" in filtered_df.columns:
    user_lat = location["latitude"]
    user_lon = location["longitude"]

    if not filtered_df.empty:
        filtered_df["distance_km"] = filtered_df.apply(
            lambda row: haversine(user_lat, user_lon, row["lat"], row["lon"]),
            axis=1
        )
        filtered_df = filtered_df.sort_values("distance_km", ascending=True)
    else:
        filtered_df["distance_km"] = pd.Series(index=filtered_df.index, dtype=float)
else:
    filtered_df["distance_km"] = pd.Series(index=filtered_df.index, dtype=float)

st.session_state.filtered_df_cached = filtered_df.copy()
st.session_state.last_search = search
st.session_state.last_location_key = location_key
st.session_state.last_category = selected_category_label
st.session_state.last_price_filter = selected_price_value



# -------------------------
# TITLE + COVER BUTTON
# -------------------------
col_title_1, col_title_2 = st.columns([5, 1])
with col_title_1:
    st.markdown("""
    <h1 style="
        font-weight: 900;
        color: #ff3b1f;
        line-height: 1.05;
        margin-bottom: 20px;
    ">
        <div style="font-size: 80px;">GLUTEN FREE</div>
        <div style="font-size: 40px;">MELBOURNE</div>
    </h1>
    """, unsafe_allow_html=True)

with col_title_2:
    if st.button("Cover", use_container_width=True):
        st.session_state.show_map = False
        st.session_state.map_transition = False
        st.session_state.pins_animated = False
        st.query_params.clear()
        st.rerun()

# -------------------------
# MAP CENTER
# -------------------------
CBD_MELBOURNE = (-37.8136, 144.9631)
center_lat = CBD_MELBOURNE[0]
center_lon = CBD_MELBOURNE[1]

# -------------------------
# CREATE MAP
# -------------------------
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=15,
    tiles="CartoDB positron"
)

# -------------------------
# RESTAURANT PINS
# -------------------------
# IMPORTANTE: usamos lon, no lng, porque load_data() crea lon desde lng
# y el resto de la app/rutas trabajan con lon.
visible_rows = filtered_df.dropna(subset=["lat", "lon"]).head(80).copy()

# Limpieza extra por si alguna coordenada llega como texto
visible_rows["lat"] = pd.to_numeric(
    visible_rows["lat"].astype(str).str.strip().str.replace(",", ".", regex=False),
    errors="coerce"
)
visible_rows["lon"] = pd.to_numeric(
    visible_rows["lon"].astype(str).str.strip().str.replace(",", ".", regex=False),
    errors="coerce"
)
visible_rows = visible_rows.dropna(subset=["lat", "lon"]).copy()

for _, row in visible_rows.iterrows():
    popup_html = build_popup_html(row, images_df)
    hover_text = build_hover_text(row)
    row_id = str(row["row_id"])
    is_active = row_id == str(st.session_state.selected_id)
    style = get_marker_style(row, active=is_active)

    folium.Marker(
        location=[float(row["lat"]), float(row["lon"])],
        tooltip=row_id,
        popup=folium.Popup(popup_html, max_width=320),
        icon=DivIcon(
            icon_size=(30, 30) if is_active else (24, 24),
            icon_anchor=(15, 15) if is_active else (12, 12),
            html=marker_html(
                active=is_active,
                hover_text=hover_text,
                bg=style["bg"],
                text=style["text"],
                show_text=style["show_text"],
                strikethrough=style["strikethrough"]
            )
        )
    ).add_to(m)

# Ajusta el mapa a los pines solo si no hay ubicación de usuario.
# Así no rompe las rutas ni el centrado cuando hay geolocalización.
if location is None and not visible_rows.empty:
    m.fit_bounds(visible_rows[["lat", "lon"]].values.tolist(), padding=(30, 30))

# -------------------------
# USER LOCATION
# -------------------------
if location:
    folium.Circle(
        location=[location["latitude"], location["longitude"]],
        radius=60,
        color=None,
        fill=True,
        fill_color="#007aff",
        fill_opacity=0.18
    ).add_to(m)

    folium.CircleMarker(
        location=[location["latitude"], location["longitude"]],
        radius=7,
        color="#ffffff",
        weight=2,
        fill=True,
        fill_color="#007aff",
        fill_opacity=1
    ).add_to(m)

# -------------------------
# MAP
# -------------------------
map_state_key = f"main_map_pins_v3_{normalize_text(search)}_{selected_category_label}_{selected_price_value}_{len(filtered_df)}_{len(visible_rows)}"

st_folium(
    m,
    height=700,
    use_container_width=True,
    return_on_hover=True,
    key=map_state_key
)

# -------------------------
# RESULTS
# -------------------------
st.sidebar.header("Results")

for _, row in filtered_df.head(20).iterrows():
    distance_text = ""
    if pd.notnull(row["distance_km"]):
        distance_text = f"<br><small><b>{row['distance_km']:.2f} km</b></small>"

    category_text = html.escape(str(row.get(category_col, "")))
    price_text = html.escape(str(row.get("price_tier", "") or row.get("price", "")))
    active_class = "card active" if str(row["row_id"]) == str(st.session_state.selected_id) else "card"

    st.sidebar.markdown(f"""
    <div class="{active_class}">
        <b>{html.escape(str(row.get('restaurant_name', '')))}</b><br>
        <small>{html.escape(str(row.get('address', '')))}</small><br>
        <small>{category_text}</small><br>
        <small>{price_text}</small>
        {distance_text}
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# GEOLOCATION ERROR
# -------------------------
if st.session_state.geo_error:
    st.warning(f"Could not get location: {st.session_state.geo_error}")
