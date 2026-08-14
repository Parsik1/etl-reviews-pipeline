import pandas as pd
import etl.transform as tr
def test_transform_reviews_like_original(tmp_path, monkeypatch):
    
    df_in = pd.DataFrame([
        {"product_id": 101, "product_name": "Samsung Galaxy A55", "brand": "Samsung", "rating": 3,
         "review_text": "Средне, есть недостатки по звуку.", "review_date": "17.04.2024"},
        {"product_id": 102, "product_name": "Xiaomi Redmi Note 13", "brand": "Xiaomi", "rating": 2,
         "review_text": "Много бесполезных приложений в системе.", "review_date": "08.09.2024"},
        {"product_id": 103, "product_name": "Apple iPhone 15", "brand": "Apple", "rating": 5,
         "review_text": "Очень доволен качеством, всё работает отлично.", "review_date": "21.08.2024"},
        {"product_id": 101, "product_name": "Samsung Galaxy A55", "brand": "Samsung", "rating": 2,
         "review_text": "Памяти маловато для фото и видео.", "review_date": "25.07.2024"},
        {"product_id": 102, "product_name": "Xiaomi Redmi Note 13", "brand": "Xiaomi", "rating": 2,
         "review_text": "Производительность на высоте.", "review_date": "31.07.2024"},
    ])
    extracted = tmp_path / "extracted.parquet"
    df_in.to_parquet(extracted, index=False)

    assert extracted.exists()

    original_to_parquet = pd.DataFrame.to_parquet
    out_file = tmp_path / "transformed.parquet"

    def fake_to_parquet(self, path, index=False, **kwargs):
        return original_to_parquet(self, out_file, index=index, **kwargs)

    with monkeypatch.context() as m:
        m.setattr(pd.DataFrame, "to_parquet", fake_to_parquet)
        tr.transform_reviews(str(extracted))

    assert out_file.exists()
    df_out = pd.read_parquet(out_file)

    assert len(df_out) > 0
    assert "review_text_clean" in df_out.columns
    assert "sentiment" in df_out.columns
    assert pd.api.types.is_datetime64_any_dtype(df_out["review_date"])
