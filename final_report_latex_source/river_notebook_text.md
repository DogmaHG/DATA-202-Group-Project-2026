# Extracted from final_review_behavior_analysis.ipynb

(Markdown and outputs in order; figures in this folder are `river_figure_01.png` through `river_figure_05.png`.)

---

## Cell 1 (markdown)

# Review behavior: movies, users, and popularity

This notebook examines **user–movie interactions** in **Movies_and_TV.csv** (same schema as [DatasetDescription.md](../DatasetDescription.md): `item_id`, `user_id`, `rating`, `timestamp`). It focuses on factors that influence **how a movie is reviewed** and **how users review**.

**Questions addressed**

1. Correlation between **how many reviews a movie has** (full dataset) and its **average rating**.
2. Correlation between **movie review count** and **divisiveness** (standard deviation of ratings).
3. Correlation between **how many reviews a user gives** and their **average score** (a proxy for “harshness”).
4. **Heavy users**: compare review behaviour (means, spread, star mix) to lighter users.

**Note:** We load **all rows** from **Movies_and_TV.csv** using chunked reads concatenated into one DataFrame (**no random subsampling**). `**n_reviews`** for each movie/user counts **every matching row** in this file. `**MIN_MOVIE_REVIEWS`** / `**MIN_USER_REVIEWS**` exclude very sparse entities so means and SDs are stable. Full-data analysis uses substantial **RAM** and may take noticeably longer than a subsample.

## Cell 3 (markdown)

## 1. Load full dataset

Read the CSV in chunks of `CHUNK_ROWS` rows and concatenate to one table. Tune `CHUNK_ROWS` if you need to reduce peak memory during the read.

*Output (stdout/stderr):*

```
Loaded rows: 8,765,568
```

*Output (text/plain):*

```
      item_id         user_id  rating   timestamp                  datetime
0  0001527665  A3478QRKQDOPQ2     5.0  1362960000 2013-03-11 00:00:00+00:00
1  0001527665  A2VHSG6TZHU1OB     5.0  1361145600 2013-02-18 00:00:00+00:00
2  0001527665  A23EJWOW1TLENE     5.0  1358380800 2013-01-17 00:00:00+00:00
3  0001527665  A1KM9FNEJ8Q171     5.0  1357776000 2013-01-10 00:00:00+00:00
4  0001527665  A38LY2SSHVHRYB     4.0  1356480000 2012-12-26 00:00:00+00:00
```

*Output: HTML table/display omitted (see notebook for full table).*

## Cell 5 (markdown)

## 2. Movie-level and user-level aggregates

We aggregate ratings **by movie** (`item_id`) and **by user** (`user_id`).

- `**n_reviews*`*: number of review rows in the **full loaded dataset** for that movie or user.
- `**mean_rating`**: average star rating (1–5).
- `**std_rating**`: sample standard deviation of ratings (divisiveness); defined only if there are at least two ratings.

**Filters** (tune as needed):

- `MIN_MOVIE_REVIEWS`: drop movies with fewer than this many reviews **in the file** before correlating count vs mean/std.
- `MIN_USER_REVIEWS`: same for user-level “harshness” analysis.

**About filtered *n*:** With the **full** extract, counts reflect total activity in **Movies_and_TV.csv**. The minimum-review filters still remove users or titles with fewer than the threshold reviews so per-entity means and SDs are not driven by noise; filtered row counts are typically **much larger** than in a random subsample.

*Output (stdout/stderr):*

```
Movies in dataset: 182,032; after n≥5: 89,590
Users in dataset: 3,826,085; after n≥5: 311,221
```

*Output (text/plain):*

```
      item_id  n_reviews  mean_rating  std_rating
0  0001527665         18     4.166667    1.504894
1  0005089549         17     4.823529    0.727607
2  000503860X         27     4.814815    0.483341
3  0005419263         48     4.791667    0.617419
4  0005092663         50     4.400000    1.160577
```

*Output: HTML table/display omitted (see notebook for full table).*

*Output (text/plain):*

```
           user_id  n_reviews  mean_rating  std_rating
0   A3478QRKQDOPQ2         48     3.479167    1.110675
9   A2M1CU2IRZG0K9          7     4.285714    0.755929
11   AFTUJYISOFHY6          5     5.000000    0.000000
21  A3JVF9Y53BEOGC         31     3.806452    1.470133
22  A12VPEOEZS1KTC         42     4.166667    1.057301
```

*Output: HTML table/display omitted (see notebook for full table).*

## Cell 7 (markdown)

## 3. Movie popularity vs average rating

**Question:** Is there a correlation between the number of reviews a movie has and the average review score?

We report **Pearson** on raw counts and on **log1p(n)** (aligned with the log-scaled *x*-axis), **Spearman ρ**, and **Kendall τ**, plus **R²** from the log-scale Pearson. A combined **summary table** appears after all three figures. The **|ρ| strength** label maps |Spearman ρ| to **negligible / weak / moderate / strong** (exploratory bands, same as the printout).

*Output (stdout/stderr):*

```
Movie review count vs mean rating — correlation strength
  n movies: 89,590
  Pearson r (raw count vs mean):     +0.0403  (p=1.88e-33)  [negligible]
  Pearson r (log1p count vs mean):   +0.0981  (p=2.39e-190)  matches log-x axis; R²=0.0096
  Spearman rho (rank):             +0.0672  (p=2.74e-90)  [negligible]
  Kendall tau:                     +0.0471  (p=3.10e-96)
```

**[Figure 1: saved as `river_figure_01.png`]**

## Cell 9 (markdown)

**How to read:** A positive correlation suggests **more-reviewed movies in this dataset** also tend to have **higher** average stars (or the reverse if negative). Association does not imply causation (e.g. popular titles may differ by genre/quality; selection and visibility mix exposure and taste).

## Cell 10 (markdown)

**Interpretation.** Use your printed **Spearman ρ** (and **p-value**) together with the strength label. **Near-zero** ρ means popularity (review count) and average stars are **essentially unrelated** in this dataset—mass-market visibility does not line up with higher or lower mean ratings here. A **positive** ρ suggests titles that appear more often (higher review volume) also carry **higher** average scores (possibly mainstream/family-friendly skew, or survivor bias in what gets reviewed heavily). A **negative** ρ would suggest **more-reviewed** movies tend to be rated **lower** on average (e.g. debate-heavy or controversial picks drawing volume). Keep in mind **noise**, **genre mix**, and that correlation is **not** causal.

## Cell 11 (markdown)

## 4. Movie popularity vs divisiveness (rating SD)

**Question:** Is there a correlation between the number of reviews and how divisive a movie is (standard deviation of ratings)?

We use movies with **at least two** ratings so `std_rating` is defined, and keep `n_reviews ≥ MIN_MOVIE_REVIEWS` for comparability with section 3.

*Output (stdout/stderr):*

```
Movie review count vs rating SD (divisiveness) — correlation strength
  n movies: 89,590
  Pearson r (raw count vs SD):     -0.0124  (p=2.17e-04)  [negligible]
  Pearson r (log1p count vs SD):   -0.0034  (p=3.05e-01)  matches log-x axis; R²=0.0000
  Spearman rho (rank):             -0.0310  (p=1.62e-20)  [negligible]
  Kendall tau:                     -0.0269  (p=1.06e-32)
```

**[Figure 2: saved as `river_figure_02.png`]**

## Cell 13 (markdown)

**How to read:** Higher SD means **more spread** across 1–5 stars (more disagreement). Near-zero SD means almost everyone gave the same star value.

## Cell 14 (markdown)

**Interpretation.** Link **Spearman ρ** to whether disagreement grows or shrinks with exposure in this dataset. **Positive** ρ means movies with **more** reviews tend to have **higher** rating SD (**more divisive**—wider spread across 1–5★). **Negative** ρ means heavy-volume titles show **more consensus** (lower SD). **Near-zero** ρ implies divisiveness is **not** systematically tied to how often the movie appears in this dataset. Remember SD also depends on **how many stars actually vary** (two ratings both at 5★ have SD 0); interpret alongside **n** and the scatter cloud shape.

## Cell 15 (markdown)

## 5. User activity vs average score (“harshness”)

**Question:** Is there a correlation between the number of reviews a user gives and how harshly they score films?

We operationalize **harshness** as **lower mean_rating** for that user (on the 1–5 scale), among users with at least `MIN_USER_REVIEWS` ratings so the mean is stable.

*Output (stdout/stderr):*

```
User review count vs mean rating (harshness proxy) — correlation strength
  n users: 311,221
  Pearson r (raw count vs mean):     -0.0234  (p=5.17e-39)  [negligible]
  Pearson r (log1p count vs mean):   -0.0207  (p=7.79e-31)  matches log-x axis; R²=0.0004
  Spearman rho (rank):             -0.0574  (p=2.82e-225)  [negligible]
  Kendall tau:                     -0.0408  (p=1.42e-218)
```

*Output (stdout/stderr):*

```
/var/folders/qq/w0x7mqq17y3_vgq8xckwfb980000gp/T/ipykernel_89951/3863865306.py:22: UserWarning: Glyph 8658 (\N{RIGHTWARDS DOUBLE ARROW}) missing from font(s) Arial.
  plt.tight_layout()
/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages/IPython/core/pylabtools.py:170: UserWarning: Glyph 8658 (\N{RIGHTWARDS DOUBLE ARROW}) missing from font(s) Arial.
  fig.canvas.print_figure(bytes_io, **kw)
```

**[Figure 3: saved as `river_figure_03.png`]**

## Cell 17 (markdown)

### Note — correlation coefficients for each metric

Sections **3–5** print **Pearson *r*** (raw and log1p count where relevant), **Spearman ρ**, **Kendall τ**, and *p*-values for each scatter analysis. Section **6** adds **Pearson *r*** between star rating and the heavy-user indicator—that equals the **point-biserial** correlation for a 0/1 predictor.

A **single consolidated table** of all correlation coefficients appears **after section 6** (run sections **2→6** in order, then run that cell). **Pearson (log1p *n*)** matches the log-scaled *x*-axis on the scatter plots. **R²** is the squared Pearson *r* on log count. **Spearman** / **Kendall** summarize monotonic (rank) association.

## Cell 19 (markdown)

**How to read:** If correlation is **negative**, users who write **more** reviews in this dataset tend to give **lower** averages (appear harsher). Positive correlation ⇒ heavier reviewers rate higher on average. Self-selection and profile heterogeneity (genre tastes, early vs late adopters) can drive patterns.

## Cell 20 (markdown)

**Interpretation.** Connect **Spearman ρ** to how **activity** relates to **mean strictness** (lower mean ⇒ harsher, on 1–5). A **negative** ρ means users with **more** reviews in the dataset give **lower** average scores—often read as more **critical** or **selective** heavy reviewers, or a **cohort effect** (long-tenure users vs casual one-offs). A **positive** ρ means busier raters are **less** harsh on average. **Near-zero** ρ says average score does not systematically move with how many reviews a user has in the file, so “harshness” and volume look **independent** in this dataset. This is still **not** proof of user “type”—self-selection, item mix, and time period all confound the link.

## Cell 21 (markdown)

## 6. Heavy users: review behaviour

**Question:** Can we examine heavy users for certain review behaviour?

We label **heavy** users as those at or above the **90th percentile** of `n_reviews` among users with at least `MIN_USER_REVIEWS` reviews (change `HEAVY_QUANTILE` to explore). We compare **mean rating**, **SD of ratings**, and the **share of low (1–2★) vs high (4–5★)** reviews to **non-heavy** users.

*Output (stdout/stderr):*

```
Heavy-user threshold: n_reviews ≥ 19 (quantile 0.90)
Heavy users (in dataset): 32,905
```

*Output (text/plain):*

```
       group  share_of_all_reviews  mean_rating  share_low_1_2  share_high_4_5
0      heavy              0.164255     4.155325       0.110123        0.768691
1  non-heavy              0.835745     4.248279       0.120325        0.803038
```

*Output: HTML table/display omitted (see notebook for full table).*

*Output (stdout/stderr):*

```
Within-user rating SD (users with n≥MIN_USER_REVIEWS):
  Heavy:    mean SD=0.8600, n_users=32,905
  Non-heavy: mean SD=0.7965, n_users=278,316
  Mann–Whitney U (heavy vs non-heavy user SD): p=2.29e-132

Correlation coefficients — star rating vs heavy-user indicator:
  Pearson r (point-biserial): -0.0282  (p=0.00e+00)  [negligible]
  Spearman rho:               -0.0575  (p=0.00e+00)  [negligible]
  Kendall tau:                -0.0541  (p=0.00e+00)
```

**[Figure 4: saved as `river_figure_04.png`]**

*Output (text/plain):*

```
<IPython.core.display.Markdown object>
```

*Output (text/plain):*

```
<IPython.core.display.Markdown object>
```

*Output (text/plain):*

```
       Group  n_users  min (data)      Q1  median      Q3  max (data)     IQR  \
0  Non-heavy   278316         1.0  3.8333  4.4167  4.8571         5.0  1.0238   
1      Heavy    32905         1.0  3.8400  4.3421  4.7662         5.0  0.9262   

   whisker_low  whisker_high  
0       2.2976           5.0  
1       2.4506           5.0
```

*Output: HTML table/display omitted (see notebook for full table).*

**[Figure 5: saved as `river_figure_05.png`]**

## Cell 24 (markdown)

## Correlation coefficients — all analyzed metrics

Each row is one **bivariate relationship**. **Pearson *r*** measures linear association (for review counts, both raw and log1p(*n*) where applicable). **Spearman ρ** and **Kendall τ** measure monotonic (rank) association. For the heavy-user row, **Pearson *r*** is the **point-biserial** correlation between a 0/1 indicator and star rating; log-scale columns are not applicable (shown as —).

*Output (stdout/stderr):*

```
Correlation coefficients for each analyzed metric (Pearson r, Spearman ρ, Kendall τ):
```

*Output (text/plain):*

```
                                              metric        n  \
0                  Movie: review count ↔ mean rating    89590   
1     Movie: review count ↔ rating SD (divisiveness)    89590   
2  User: review count ↔ mean rating (harshness pr...   311221   
3       Review-level: star rating ↔ heavy-user (0/1)  8765568   

   Pearson r (raw n or point-biserial)  Pearson r (log1p n)  R² (log Pearson)  \
0                               0.0403               0.0981            0.0096   
1                              -0.0124              -0.0034            0.0000   
2                              -0.0234              -0.0207            0.0004   
3                              -0.0282                  NaN               NaN   

   Spearman ρ  Kendall τ  p (Pearson raw / point-biserial)  p (Pearson log1p)  \
0      0.0672     0.0471                            0.0000             0.0000   
1     -0.0310    -0.0269                            0.0002             0.3049   
2     -0.0574    -0.0408                            0.0000             0.0000   
3     -0.0575    -0.0541                            0.0000                NaN   

   p (Spearman)  p (Kendall) |r| strength (Pearson raw) |ρ| strength  
0           0.0          0.0                 negligible   negligible  
1           0.0          0.0                 negligible   negligible  
2           0.0          0.0                 negligible   negligible  
3           0.0          0.0                 negligible   negligible
```

*Output: HTML table/display omitted (see notebook for full table).*

## Cell 26 (markdown)

## 7. Short synthesis

- **Correlation coefficients:** Use the consolidated table above for **Pearson *r*** (raw or log1p count where applicable), **Spearman ρ**, **Kendall τ**, and *p*-values for each analysis—including **point-biserial *r*** for rating vs heavy-user status.
- **Movie count vs mean / SD:** Summarize the signs of the correlations you obtained and whether *p*-values suggest statistical significance **in this dataset** (this McAuley extract).
- **User count vs mean:** A trend links **volume** to **average strictness** within this Amazon Movies & TV extract; causal claims need richer modeling.
- **Heavy users:** Compare boxplot overlap and star-mix bars—large overlaps imply **similar** behaviour despite activity differences; systematic shifts support **different** behaviour among heavy reviewers.

## Cell 27 (markdown)

## 8. Conclusion — analysis by research check

After running all cells, tie each research question to the printed correlations, *p*-values, plots, and tables using the definitions above.

### Check 1 — Movie review count vs mean rating

**Question:** Is popularity (review volume) associated with average star rating?

**Concluding analysis:** Compare **Spearman ρ** and **Pearson *r* on log1p(*n*)** (aligned with the log-scaled scatter) to judge direction and strength. If ρ is near zero and non-significant, conclude that **mean rating is essentially unrelated to how often the movie is reviewed** in this extract, once sparse titles are filtered out. If ρ is positive (negative), conclude that **more-reviewed movies tend toward higher (lower) average scores**—but stress **association, not causation** (genre, quality, and era confound visibility). Note that **Pearson on raw *n*** can look weaker than the plot because counts are skewed and the chart uses **log *n***.

### Check 2 — Movie review count vs divisiveness (rating SD)

**Question:** Are heavily reviewed movies more or less “divisive” (spread across 1–5★)?

**Concluding analysis:** Interpret **Spearman ρ** between review count and **within-movie rating SD**. A **positive** ρ supports **more disagreement** among popular titles; **negative** ρ supports **more consensus**. Near-zero ρ ⇒ **divisiveness does not systematically track popularity** here. Tie your wording to whether *p* passes your chosen significance bar and whether the **log-*x*** scatter shows any visible gradient versus wide overlap.

### Check 3 — User review count vs mean rating (“harshness”)

**Question:** Do users who write more reviews rate films lower on average?

**Concluding analysis:** Focus on the **sign** of ρ / Pearson(log): **negative** ⇒ users with **more reviews in the file** tend to give **lower** mean scores (read as “stricter” or more critical **on average**); **positive** ⇒ the opposite; **near zero** ⇒ **volume and harshness look unrelated** among users meeting `MIN_USER_REVIEWS`. Acknowledge confounds (different tastes, items reviewed, time period).

### Check 4 — Heavy users vs others

**Question:** Do heavy reviewers show distinct behaviour?

**Concluding analysis:** Integrate (i) the **group summary table** (means, low/high star shares), (ii) **within-user SD** comparison and Mann–Whitney *p* if printed, (iii) **box-plot summary statistics**, (iv) **star-mix bars**, and (v) **point-biserial *r*** between rating and the heavy-user indicator. Conclude whether heavy users are **materially different** or **largely overlapping** with non-heavy users on mean rating and spread. If overlaps are large and effect sizes small, say behaviour is **similar** despite higher activity; if means or mixes diverge consistently, say heavy users show **detectably different** rating patterns **in this dataset**.

### Closing remark

Together, these checks describe **structure in the McAuley Movies & TV reviews file**, not universal truths about Amazon or movies generally. Prefer language that matches **your printed coefficients and visual evidence**, and note limitations (**single domain extract**, **minimum-review filters**, **correlation ≠ causation**).