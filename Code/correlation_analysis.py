import gzip
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


filepath = "/Users/lucapopescu/Desktop/DATA202_Mid_Pres/Movies_and_TV_5.json"

records = []
with open(filepath, 'r') as f:
    for line in f:
        review = json.loads(line)
        records.append({
            "rating":      review.get("overall"),
            "reviewerID":  review.get("reviewerID"),
            "unixTime":    review.get("unixReviewTime"),
            "vote":        review.get("vote"),
            "verified":    review.get("verified"),
        })

df = pd.DataFrame(records)

# Convert timestamp to year
df["year"] = pd.to_datetime(df["unixTime"], unit="s").dt.year

# Clean vote column (it comes in as a string like "2,394")
df["vote"] = df["vote"].astype(str).str.replace(",", "").str.strip()
df["vote"] = pd.to_numeric(df["vote"], errors="coerce").fillna(0)

print(f"Loaded {len(df):,} reviews")
print(df.head())


yearly = df.groupby("year")["rating"].agg(["mean", "count"]).reset_index()
yearly.columns = ["year", "avg_rating", "review_count"]

# Pearson correlation between year and average rating
r, p = stats.pearsonr(yearly["year"], yearly["avg_rating"])
print(f"\n[Ratings over Time]")
print(f"Pearson r = {r:.4f}, p-value = {p:.4f}")

# Plot
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
plt.savefig("ratings_over_time.png", dpi=150)
plt.show()


reviewer_stats = df.groupby("reviewerID").agg(
    review_count=("rating", "count"),
    avg_rating=("rating", "mean")
).reset_index()

# Only keep reviewers with at least 5 reviews (since this is already 5-core data)
reviewer_stats = reviewer_stats[reviewer_stats["review_count"] >= 5]

# Pearson correlation
r2, p2 = stats.pearsonr(reviewer_stats["review_count"], reviewer_stats["avg_rating"])
print(f"\n[Reviewer Activity vs Rating Behavior]")
print(f"Pearson r = {r2:.4f}, p-value = {p2:.4f}")

# Plot
plt.figure(figsize=(10, 6))
plt.hexbin(reviewer_stats["review_count"], reviewer_stats["avg_rating"],
           gridsize=60, cmap="YlOrRd", mincnt=1)
plt.colorbar(label="Number of Reviewers")
plt.xlabel("Number of Reviews Written")
plt.ylabel("Average Rating Given")
plt.title(f"Reviewer Activity vs. Average Rating\nPearson r = {r2:.4f}, p = {p2:.4f}")
plt.tight_layout()
plt.savefig("reviewer_activity_vs_rating.png", dpi=150)
plt.show()