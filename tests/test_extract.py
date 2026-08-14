import pandas as pd
import etl.extract as ex

def test_extract_reviews_like_original(tmp_path, monkeypatch):
    lines = [
        "101;Samsung Galaxy A55;Samsung;3;Средне, есть недостатки по звуку.;17.04.2024",
        "102;Xiaomi Redmi Note 13;Xiaomi;2;Много бесполезных приложений в системе.;08.09.2024",
        "103;Apple iPhone 15;Apple;5;Очень доволен качеством, всё работает отлично.;21.08.2024",
        "101;Samsung Galaxy A55;Samsung;2;Памяти маловато для фото и видео.;25.07.2024",
        "102;Xiaomi Redmi Note 13;Xiaomi;2;Производительность на высоте.;31.07.2024",
    ]

    csv_path = tmp_path / "marketplace_reviews.csv"
    csv_path.write_text("\n".join(lines), encoding="utf-8")

    original_to_parquet = pd.DataFrame.to_parquet

    out_file = tmp_path / "extracted.parquet"
    def fake_to_parquet(self, path, index=False, **kwargs):
        return original_to_parquet(self, out_file, index=index, **kwargs)

    monkeypatch.setattr(pd.DataFrame, "to_parquet", fake_to_parquet)
    ex.extract_reviews(raw_path=str(csv_path))

    assert out_file.exists()
    df = pd.read_parquet(out_file)

    assert len(df) == 5
    assert set(ex.COLS) <= set(df.columns)
    assert df.loc[0, "product_id"] == 101
