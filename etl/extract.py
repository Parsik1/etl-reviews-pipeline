import os
import pandas as pd

RAW_CSV_PATH = "/opt/airflow/data/raw/marketplace_reviews.csv"

COLS = ["product_id", "product_name", "brand", "rating", "review_text", "review_date"]


def extract_reviews(raw_path: str = RAW_CSV_PATH) -> str:
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"CSV not found: {raw_path}")

    df = pd.read_csv(raw_path, sep=";", header=None, names=COLS)

    tmp_path = "/opt/airflow/data/processed/extracted.parquet"
    os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
    df.to_parquet(tmp_path, index=False)
    return tmp_path
