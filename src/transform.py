import pandas as pd
import re
import unicodedata


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text.lower().strip()

    # quitar acentos
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    # limpiar símbolos
    text = re.sub(r"[^\\w\\s]", " ", text)

    # espacios
    text = re.sub(r"\\s+", " ", text).strip()

    return text


def clean_restaurant_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # unificar texto
    df["raw_review_text"] = (
        df["textTranslated"]
        .replace("", pd.NA)
        .combine_first(df["text"])
    )

    # columnas clave
    cols = [
        "title", "raw_review_text", "address",
        "categoryName", "price", "menu", "placeId"
    ]

    df = df[cols].copy()

    # limpiar strings
    for col in cols:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # texto limpio
    df["clean_review_text"] = df["raw_review_text"].apply(normalize_text)

    # eliminar inválidos
    df = df[
        (df["placeId"] != "") &
        (df["clean_review_text"] != "")
    ].copy()

    # duplicados
    df = df.drop_duplicates(subset=["placeId", "clean_review_text"])

    return df
