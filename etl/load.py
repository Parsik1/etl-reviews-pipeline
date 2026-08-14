import os
import sqlite3
import pandas as pd

DB_PATH = "/opt/airflow/data/processed/reviews.db"


def load_to_sqlite(transformed_path: str, db_path: str = DB_PATH) -> str:
    if not os.path.exists(transformed_path):
        raise FileNotFoundError(f"Transformed file not found: {transformed_path}")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    df = pd.read_parquet(transformed_path)

    conn = sqlite3.connect(db_path)
    try:
        df.to_sql("reviews_clean", conn, if_exists="replace", index=False)

        agg = (
            df.assign(day=df["review_date"].dt.date)
            .groupby(["day", "brand"], as_index=False)
            .agg(
                reviews_cnt=("review_text_clean", "count"),
                avg_rating=("rating", "mean"),
                positive_cnt=("sentiment", lambda s: (s == "positive").sum()),
                negative_cnt=("sentiment", lambda s: (s == "negative").sum()),
                neutral_cnt=("sentiment", lambda s: (s == "neutral").sum()),
            )
        )
        agg.to_sql("reviews_agg_daily", conn, if_exists="replace", index=False)
    finally:
        conn.close()

    return db_path
