from src.loader import load_restaurant_data
from src.transform import clean_restaurant_data
from src.kpis import compute_restaurant_ranking
from src.config import CLEAN_DATA_PATH, RESTAURANT_RANKING_PATH


def run_pipeline():
    df = load_restaurant_data()

    df_clean = clean_restaurant_data(df)

    ranking = compute_restaurant_ranking(df_clean)

    df_clean.to_csv(CLEAN_DATA_PATH, index=False)
    ranking.to_csv(RESTAURANT_RANKING_PATH, index=False)

    print("Pipeline executed successfully")
    print(f"Clean data saved to: {CLEAN_DATA_PATH}")
    print(f"Ranking saved to: {RESTAURANT_RANKING_PATH}")


if __name__ == "__main__":
    run_pipeline()
