import os
import re
import pandas as pd


def _clean_text(text: str) -> str:
    if pd.isna(text):
        return ""
    t = str(text).lower().strip()
    t = re.sub(r"\s+", " ", t)
    return t


def _sentiment_from_rating(rating: int) -> str:
    if rating <= 2:
        return "negative"
    if rating == 3:
        return "neutral"
    return "positive"


def transform_reviews(extracted_path: str) -> str:
    if not os.path.exists(extracted_path):
        raise FileNotFoundError(f"Extracted file not found: {extracted_path}")

    df = pd.read_parquet(extracted_path)


    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0).astype(int)
    df["review_date"] = pd.to_datetime(df["review_date"], format="%d.%m.%Y", errors="coerce")

    df["review_text_clean"] = df["review_text"].apply(_clean_text)

    df = df[df["review_text_clean"].str.len() > 0]
    df = df[df["review_date"].notna()]

    df = df.drop_duplicates(subset=["product_id", "rating", "review_text_clean", "review_date"])

    df["sentiment"] = df["rating"].apply(_sentiment_from_rating)

    tmp_path = "/opt/airflow/data/processed/transformed.parquet"
    os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
    df.to_parquet(tmp_path, index=False)
    return tmp_path
