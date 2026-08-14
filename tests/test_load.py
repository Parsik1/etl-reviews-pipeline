import sqlite3
import pandas as pd

from etl.load import load_to_sqlite

def test_load_to_sqlite_like_original(tmp_path):
    df = pd.DataFrame([
        {
            "product_id": 101,
            "product_name": "Samsung Galaxy A55",
            "brand": "Samsung",
            "rating": 3,
            "review_text": "Средне, есть недостатки по звуку.",
            "review_date": "2024-04-17",
            "review_text_clean": "средне, есть недостатки по звуку.",
            "sentiment": "neutral",
        },
        {
            "product_id": 102,
            "product_name": "Xiaomi Redmi Note 13",
            "brand": "Xiaomi",
            "rating": 2,
            "review_text": "Много бесполезных приложений в системе.",
            "review_date": "2024-09-08",
            "review_text_clean": "много бесполезных приложений в системе.",
            "sentiment": "negative",
        },
        {
            "product_id": 103,
            "product_name": "Apple iPhone 15",
            "brand": "Apple",
            "rating": 5,
            "review_text": "Очень доволен качеством, всё работает отлично.",
            "review_date": "2024-08-21",
            "review_text_clean": "очень доволен качеством, всё работает отлично.",
            "sentiment": "positive",
        },
        {
            "product_id": 101,
            "product_name": "Samsung Galaxy A55",
            "brand": "Samsung",
            "rating": 2,
            "review_text": "Памяти маловато для фото и видео.",
            "review_date": "2024-07-25",
            "review_text_clean": "памяти маловато для фото и видео.",
            "sentiment": "negative",
        },
        {
            "product_id": 102,
            "product_name": "Xiaomi Redmi Note 13",
            "brand": "Xiaomi",
            "rating": 2,
            "review_text": "Производительность на высоте.",
            "review_date": "2024-07-31",
            "review_text_clean": "производительность на высоте.",
            "sentiment": "negative",
        },
    ])

    df["review_date"] = pd.to_datetime(df["review_date"])

    transformed_path = tmp_path / "transformed.parquet"
    df.to_parquet(transformed_path, index=False)

    db_path = tmp_path / "reviews_test.db"
    returned_db_path = load_to_sqlite(str(transformed_path), str(db_path))

    assert str(returned_db_path).endswith(".db")
    assert db_path.exists()

    conn = sqlite3.connect(str(db_path))
    try:
        tables = pd.read_sql(
            "SELECT name FROM sqlite_master WHERE type='table'",
            conn
        )["name"].tolist()

        assert "reviews_clean" in tables
        assert "reviews_agg_daily" in tables

        reviews_clean = pd.read_sql("SELECT * FROM reviews_clean", conn)
        assert len(reviews_clean) == 5

        agg = pd.read_sql("SELECT * FROM reviews_agg_daily", conn)
        assert int(agg["reviews_cnt"].sum()) == 5

        by_brand = reviews_clean.groupby("brand").size().to_dict()
        assert by_brand["Samsung"] == 2
        assert by_brand["Xiaomi"] == 2
        assert by_brand["Apple"] == 1
    finally:
        conn.close()
