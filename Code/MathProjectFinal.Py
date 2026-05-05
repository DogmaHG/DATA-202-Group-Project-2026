import os
import pandas as pd
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "Movies_and_TV.csv")

cols = ["user_id", "item_id", "rating", "timestamp"]

df = pd.read_csv(CSV_PATH, names=cols, header=None)

print(df.head())

print(df.isnull().sum())

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
print(df.head())

df["month"] = df["timestamp"].dt.month
df["month_name"] = df["timestamp"].dt.month_name()

seasonal_data = df.groupby("month")["rating"].mean()
month_labels = df.groupby("month")["month_name"].first()

plt.figure(figsize=(10, 5))
plt.plot(month_labels, seasonal_data, marker="o", color="b", linestyle="-")

plt.title("Average Movie/TV Ratings by Month")
plt.xlabel("Month")
plt.ylabel("Average Rating")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

out_png = os.path.join(SCRIPT_DIR, "average_rating_by_month.png")
plt.savefig(out_png, dpi=150, bbox_inches="tight")
print(f"Saved figure → {out_png}")

print("Average Rating per Month:")
print(df.groupby("month_name")["rating"].mean().sort_values(ascending=False))
