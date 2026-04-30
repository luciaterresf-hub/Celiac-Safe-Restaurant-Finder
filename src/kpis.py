import pandas as pd
import re
from rapidfuzz import fuzz


# patrones gluten
GLUTEN_PATTERNS = [
    r"\bgluten\b",
    r"\bgluten free\b",
    r"\bcross contamination\b",
    r"\bceliac\b",
    r"\bgluten friendly\b"
]

COMBINED_PATTERN = re.compile("|".join(GLUTEN_PATTERNS), flags=re.IGNORECASE)


def gluten_match_info(text):
    if not isinstance(text, str) or not text.strip():
        return False

    if COMBINED_PATTERN.search(text):
        return True

    # fuzzy
    for word in text.split():
        if len(word) >= 5 and fuzz.ratio(word, "gluten") >= 85:
            return True

    return False


# sentimiento simple
POSITIVE = {"good", "great", "amazing", "excellent", "safe", "friendly"}
NEGATIVE = {"bad", "terrible", "unsafe", "sick", "rude"}


def get_sentiment(text):
    words = set(text.split())
    pos = len(words & POSITIVE)
    neg = len(words & NEGATIVE)
    return "positive" if pos >= neg else "negative"


# clasificación final
def classify_reviews(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["gluten_flag"] = df["clean_review_text"].apply(gluten_match_info)
    df["sentiment"] = df["clean_review_text"].apply(get_sentiment)

    def safety(row):
        if not row["gluten_flag"]:
            return None
        if row["sentiment"] == "negative":
            return "unsafe"
        return "safe"

    df["safety"] = df.apply(safety, axis=1)

    return df


def compute_restaurant_ranking(df: pd.DataFrame) -> pd.DataFrame:

    df = classify_reviews(df)

    ranking = (
        df.groupby("title", as_index=False)
        .agg(
            total_reviews=("clean_review_text", "count"),
            safe_reviews=("safety", lambda x: (x == "safe").sum()),
            unsafe_reviews=("safety", lambda x: (x == "unsafe").sum())
        )
    )

    ranking["classified_reviews"] = (
        ranking["safe_reviews"] + ranking["unsafe_reviews"]
    )

    ranking["safety_pct"] = (
        ranking["safe_reviews"] / ranking["classified_reviews"]
    ).fillna(0)

    ranking["ranking_score"] = (
        ranking["safe_reviews"] * 2
        - ranking["unsafe_reviews"] * 3
        + ranking["classified_reviews"] * 0.5
    )

    ranking = ranking.sort_values(
        by=["ranking_score", "safe_reviews"],
        ascending=False
    ).reset_index(drop=True)

    return ranking
