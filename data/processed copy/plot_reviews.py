import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "reviews.db"
OUT_DIR = BASE_DIR / "plots"
OUT_DIR.mkdir(exist_ok=True)

# 1) загрузка данных
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM reviews_agg_daily", conn)
conn.close()

# df: reviews_agg_daily
df["day"] = pd.to_datetime(df["day"])
df = df.sort_values(["day", "brand"])

# 1) Средний рейтинг по брендам за весь период (взвешенный по кол-ву отзывов)
overall = (df.groupby("brand")
             .apply(lambda x: pd.Series({
                 "reviews_cnt": x["reviews_cnt"].sum(),
                 "avg_rating_weighted": np.average(x["avg_rating"], weights=x["reviews_cnt"])
             }))
             .reset_index())

plt.figure(figsize=(8, 4))
sns.barplot(data=overall.sort_values("avg_rating_weighted", ascending=False),
            x="brand", y="avg_rating_weighted")
plt.title("Средний рейтинг по брендам (взвешенный)")
plt.xlabel("Бренд")
plt.ylabel("Средний рейтинг")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/overall_avg_rating_by_brand.png", dpi=200)
plt.close()

# 2) Количество отзывов по месяцам (по брендам)
monthly = (df.assign(month=df["day"].dt.to_period("M").dt.to_timestamp())
             .groupby(["month", "brand"], as_index=False)
             .agg(reviews_cnt=("reviews_cnt", "sum"),
                  avg_rating=("avg_rating", lambda s: np.average(s, weights=df.loc[s.index, "reviews_cnt"]))))

pivot_m = monthly.pivot_table(index="month", columns="brand", values="reviews_cnt", fill_value=0)
ax = pivot_m.plot(kind="bar", stacked=True, figsize=(12, 5))
ax.set_title("Количество отзывов по месяцам (по брендам)")
ax.set_xlabel("Месяц")
ax.set_ylabel("Количество отзывов")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/monthly_reviews_cnt_stacked.png", dpi=200)
plt.close()

# 3) Доля тональности по брендам (100% stacked, за весь период)
senti = (df.groupby("brand", as_index=False)[["positive_cnt","neutral_cnt","negative_cnt"]].sum())
senti["total"] = senti[["positive_cnt","neutral_cnt","negative_cnt"]].sum(axis=1)
for col in ["positive_cnt","neutral_cnt","negative_cnt"]:
    senti[col] = senti[col] / senti["total"]

plt.figure(figsize=(8, 4))
bottom = np.zeros(len(senti))
for col, label in [("positive_cnt","positive"), ("neutral_cnt","neutral"), ("negative_cnt","negative")]:
    plt.bar(senti["brand"], senti[col], bottom=bottom, label=label)
    bottom += senti[col].values

plt.title("Доля тональности по брендам (за весь период)")
plt.xlabel("Бренд")
plt.ylabel("Доля")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/sentiment_share_by_brand.png", dpi=200)
plt.close()
