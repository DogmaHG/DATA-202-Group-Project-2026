import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "Movies_and_TV.csv")

df = pd.read_csv(
    CSV_PATH,
    header=None,
    names=["item_id", "reviewerID", "rating", "timestamp"],
    dtype={"item_id": str, "reviewerID": str, "rating": float, "timestamp": int},
)

df["year"] = pd.to_datetime(df["timestamp"], unit="s").dt.year

print(f"Loaded {len(df):,} reviews")
print(df.head())

yearly = df.groupby("year")["rating"].agg(["mean", "count"]).reset_index()
yearly.columns = ["year", "avg_rating", "review_count"]

r, p = stats.pearsonr(yearly["year"], yearly["avg_rating"])
print("\n[Ratings over Time]")
print(f"Pearson r = {r:.4f}, p-value = {p:.4f}")

fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(yearly["year"], yearly["avg_rating"], color="steelblue", marker="o", label="Avg Rating")
ax1.set_xlabel("Year")
ax1.set_ylabel("Average Rating", color="steelblue")
ax1.set_ylim(1, 5)
ax2 = ax1.twinx()
ax2.bar(yearly["year"], yearly["review_count"], alpha=0.2, color="gray", label="Review Count")
ax2.set_ylabel("Number of Reviews", color="gray")
plt.title(f"Movies & TV — Average Rating Over Time\nPearson r = {r:.4f}, p = {p:.4f}")
fig.tight_layout()
out1 = os.path.join(SCRIPT_DIR, "ratings_over_time.png")
fig.savefig(out1, dpi=150)
plt.close(fig)
print(f"Saved → {out1}")

reviewer_stats = df.groupby("reviewerID").agg(
    review_count=("rating", "count"),
    avg_rating=("rating", "mean"),
).reset_index()

reviewer_stats = reviewer_stats[reviewer_stats["review_count"] >= 5]

r2, p2 = stats.pearsonr(reviewer_stats["review_count"], reviewer_stats["avg_rating"])
print("\n[Reviewer Activity vs Rating Behavior]")
print(f"Pearson r = {r2:.4f}, p-value = {p2:.4f}")

fig2, ax = plt.subplots(figsize=(10, 6))
hb = ax.hexbin(
    reviewer_stats["review_count"],
    reviewer_stats["avg_rating"],
    gridsize=60,
    cmap="YlOrRd",
    mincnt=1,
)
fig2.colorbar(hb, ax=ax, label="Number of Reviewers")
ax.set_xlabel("Number of Reviews Written")
ax.set_ylabel("Average Rating Given")
ax.set_title(f"Reviewer Activity vs. Average Rating\nPearson r = {r2:.4f}, p = {p2:.4f}")
fig2.tight_layout()
out2 = os.path.join(SCRIPT_DIR, "reviewer_activity_vs_rating.png")
fig2.savefig(out2, dpi=150)
plt.close(fig2)
print(f"Saved → {out2}")
