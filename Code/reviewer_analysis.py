"""
Reviewer Pattern Analysis — Movies & TV (ratings-only CSV)
CSV format: item, user, rating, timestamp
Place this script in the same directory as Movies_and_TV.csv
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats

CSV_FILE    = "Movies_and_TV.csv"
NEG_THRESH  = 2          # ratings ≤ this count as "negative"
MIN_REVIEWS = 5          # drop reviewers with fewer reviews (too noisy)
TOP_PCT     = [10, 20, 25, 50]   # percentiles to report in concentration table

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_PATH    = os.path.join(SCRIPT_DIR, CSV_FILE)

print("Loading data")
df = pd.read_csv(
    CSV_PATH,
    header=None,
    names=["item", "user", "rating", "timestamp"],
    dtype={"item": str, "user": str, "rating": float, "timestamp": int},
)
print(f"  Total reviews loaded : {len(df):,}")
print(f"  Unique reviewers     : {df['user'].nunique():,}")
print(f"  Unique items         : {df['item'].nunique():,}")


print("\nAggregating per reviewer")
rev = (
    df.groupby("user")
    .agg(
        review_count=("rating", "count"),
        mean_rating=("rating", "mean"),
        std_rating=("rating", "std"),
        neg_count=("rating", lambda x: (x <= NEG_THRESH).sum()),
    )
    .reset_index()
)

rev["std_rating"] = rev["std_rating"].fillna(0)

rev["neg_rate"] = rev["neg_count"] / rev["review_count"]

before = len(rev)
rev = rev[rev["review_count"] >= MIN_REVIEWS].copy()
print(f"  Reviewers with ≥{MIN_REVIEWS} reviews : {len(rev):,}  (dropped {before - len(rev):,})")


print("\n─── Analysis A: Heterogeneity of reviewer mean ratings ───")

mean_of_means = rev["mean_rating"].mean()
std_of_means  = rev["mean_rating"].std()
median_means  = rev["mean_rating"].median()

print(f"  Mean of reviewer means   : {mean_of_means:.4f}")
print(f"  Median of reviewer means : {median_means:.4f}")
print(f"  Std dev of reviewer means: {std_of_means:.4f}")
print(f"  Min reviewer mean        : {rev['mean_rating'].min():.4f}")
print(f"  Max reviewer mean        : {rev['mean_rating'].max():.4f}")

harsh_frac = (rev["mean_rating"] <= NEG_THRESH).mean()
print(f"\n  Fraction of reviewers whose MEAN rating ≤ {NEG_THRESH}★ : {harsh_frac:.2%}")

r_count_mean, p_count_mean = stats.pearsonr(rev["review_count"], rev["mean_rating"])
print(f"\n  Pearson r (review count vs mean rating) : {r_count_mean:.4f}  (p = {p_count_mean:.4e})")

r_count_neg, p_count_neg = stats.pearsonr(rev["review_count"], rev["neg_rate"])
print(f"  Pearson r (review count vs neg rate)    : {r_count_neg:.4f}  (p = {p_count_neg:.4e})")

t_stat, t_p = stats.ttest_1samp(rev["mean_rating"], 3.0)
print(f"\n  One-sample t-test (H0: mean = 3.0) : t = {t_stat:.4f}, p = {t_p:.4e}")


print("\n─── Analysis B: Concentration of negative reviews ───")

total_neg = rev["neg_count"].sum()
print(f"  Total negative reviews (≤{NEG_THRESH}★) : {total_neg:,}")
print(f"  Across {len(rev):,} reviewers with ≥{MIN_REVIEWS} reviews\n")

# Sort by negative count descending
rev_sorted = rev.sort_values("neg_count", ascending=False).reset_index(drop=True)
rev_sorted["cum_neg"]     = rev_sorted["neg_count"].cumsum()
rev_sorted["cum_neg_pct"] = rev_sorted["cum_neg"] / total_neg * 100
rev_sorted["pct_reviewers"] = (rev_sorted.index + 1) / len(rev_sorted) * 100

print(f"  {'Top % reviewers':<22} {'% of negative reviews':>22}")
print(f"  {'─'*44}")
for pct in TOP_PCT:
    idx = int(np.ceil(len(rev_sorted) * pct / 100)) - 1
    cum_neg_pct = rev_sorted.loc[idx, "cum_neg_pct"]
    print(f"  Top {pct:>3}%                   {cum_neg_pct:>18.1f}%")

# Correlation
r_neg_mean, p_neg_mean = stats.pearsonr(rev["neg_rate"], rev["mean_rating"])
print(f"\n  Pearson r (neg rate vs mean rating) : {r_neg_mean:.4f}  (p = {p_neg_mean:.4e})")

# Variance of negative rates across reviewers
neg_rate_var  = rev["neg_rate"].var()
neg_rate_std  = rev["neg_rate"].std()
neg_rate_mean = rev["neg_rate"].mean()
print(f"\n  Mean negative rate across reviewers : {neg_rate_mean:.4f}")
print(f"  Std dev of negative rates           : {neg_rate_std:.4f}")
print(f"  Variance of negative rates          : {neg_rate_var:.6f}")


print("\nGenerating plots")

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.grid":        True,
    "grid.color":       "#e5e5e5",
    "grid.linewidth":   0.6,
    "font.size":        11,
})

fig1, ax = plt.subplots(figsize=(8, 5))
ax.hist(rev["mean_rating"], bins=50, color="#4a6fa5", edgecolor="white", linewidth=0.4)
ax.axvline(mean_of_means, color="#c0392b", linewidth=1.5, linestyle="--",
           label=f"Mean = {mean_of_means:.2f}")
ax.axvline(mean_of_means - std_of_means, color="#e67e22", linewidth=1.2, linestyle=":",
           label=f"±1 SD ({std_of_means:.2f})")
ax.axvline(mean_of_means + std_of_means, color="#e67e22", linewidth=1.2, linestyle=":")
ax.set_xlabel("Reviewer mean rating")
ax.set_ylabel("Number of reviewers")
ax.set_title("Distribution of reviewer mean ratings", fontweight="bold", loc="left")
ax.legend(fontsize=9)
plt.tight_layout()
out1 = os.path.join(SCRIPT_DIR, "plot_mean_ratings.png")
fig1.savefig(out1, dpi=150, bbox_inches="tight")
print(f"  Saved → {out1}")
plt.show()

fig2, ax = plt.subplots(figsize=(8, 5))
ax.hist(rev["neg_rate"], bins=50, color="#7b6fa5", edgecolor="white", linewidth=0.4)
ax.axvline(neg_rate_mean, color="#c0392b", linewidth=1.5, linestyle="--",
           label=f"Mean = {neg_rate_mean:.3f}")
ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
ax.set_xlabel("Negative review rate (share of reviewer's reviews ≤ 2★)")
ax.set_ylabel("Number of reviewers")
ax.set_title("Distribution of reviewer negative rates", fontweight="bold", loc="left")
ax.legend(fontsize=9)
plt.tight_layout()
out2 = os.path.join(SCRIPT_DIR, "plot_negative_rates.png")
fig2.savefig(out2, dpi=150, bbox_inches="tight")
print(f"  Saved → {out2}")
plt.show()

fig3, ax = plt.subplots(figsize=(8, 5))
ax.plot(
    rev_sorted["pct_reviewers"],
    rev_sorted["cum_neg_pct"],
    color="#4a6fa5", linewidth=2, label="Observed"
)
ax.plot([0, 100], [0, 100], color="#aaaaaa", linewidth=1, linestyle="--", label="Perfect equality")

for pct in [10, 25, 50]:
    idx = int(np.ceil(len(rev_sorted) * pct / 100)) - 1
    y_val = rev_sorted.loc[idx, "cum_neg_pct"]
    ax.annotate(
        f"Top {pct}% → {y_val:.0f}%",
        xy=(pct, y_val),
        xytext=(pct + 5, y_val - 10),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color="#555", lw=0.8),
        color="#333",
    )

ax.set_xlabel("Cumulative % of reviewers\n(sorted by most → fewest negative reviews)")
ax.set_ylabel("Cumulative % of all negative reviews")
ax.set_title("Concentration of negative reviews", fontweight="bold", loc="left")
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.legend(fontsize=9)
plt.tight_layout()
out3 = os.path.join(SCRIPT_DIR, "plot_concentration.png")
fig3.savefig(out3, dpi=150, bbox_inches="tight")
print(f"  Saved → {out3}")
plt.show()

print("\nDone.")