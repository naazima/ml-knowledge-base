# Histogram

**Course:** Foundations Python & Stats
**Type:** technique

## In one sentence
A histogram cuts the range of a numeric variable into equal-width bins and counts how many values land in each, so you can see the full shape of the data: where it piles up, where it thins out, any gaps, and which way it leans.

## When to use it
- Looking at the shape of one numeric column (the first thing to do with a new variable).
- Checking for more than one peak before trusting the mean, the median or a [boxplot](boxplot.md).
- Medium or large datasets, where each bin has enough points to be meaningful.
- **Not** for comparing many groups. Overlaid histograms get messy; use one small histogram per group, or a [boxplot](boxplot.md) per group.
- **Not** for categories (text labels). That is a bar graph.

## How it works (simple)
1. Find the smallest and largest value and split that range into equal-width intervals (bins).
2. Count the observations in each bin.
3. Draw one bar per bin. Bar height is the count by default (`stat="count"`).

Reading the shape:

| What you see | Reading |
|---|---|
| Left and right halves look like mirror images | Roughly symmetric |
| Tall bars on the left, a thin tail to the right | Right-skewed (positive skew) |
| Tall bars on the right, a thin tail to the left | Left-skewed (negative skew) |
| Two separated tall regions with a dip between | Bimodal: maybe two groups mixed together |

A **mode** is a peak, i.e. a tall region of bars. Skew is named after the side the tail points to, same as in the [boxplot](boxplot.md) card.

**The KDE curve** (`kde=True`) is a smooth line laid over the bars. It is estimated from the raw data, not from the bars, so it does not depend on the bin choice. Its smoothness is set by its own bandwidth, which you can scale with `bw_adjust` (bigger is smoother).

### What a boxplot hides
A boxplot only encodes five numbers: the quartiles, the median and the whisker ends. Two very different shapes can give the same box. In the `bore` column the median sits near the middle of the box and the whiskers are about equal, so the boxplot looks like one tidy symmetric group (skew is about 0). The histogram of the same column shows two humps with a dip between them. A boxplot can't show that, because the dip lives inside the box. So use the boxplot for centre, spread and outliers, and the histogram for shape.

## Key parameters / choices
- **`bins`:** the number of bins, or the name of a rule, or explicit edges. Seaborn passes it to `numpy.histogram_bin_edges`.
- **`binwidth`:** the width of each bin instead of the count. According to the seaborn help text it overrides `bins`.
- **`binrange`:** lowest and highest bin edge (defaults to the data extremes).
- **`kde`:** `True` adds the smooth density curve.
- **`bw_adjust`:** controls how smooth the KDE curve is. It is not a histplot argument of its own; pass it with `kde_kws={"bw_adjust": 0.5}`. Smaller values give a wigglier curve, bigger values a smoother one. It has no effect on the bars.
- **`stat`:** `count` (default), `frequency`, `probability`/`proportion`, `percent`, `density`. Use `density` or `probability` when comparing groups of different sizes.
- **`hue`:** splits the data by a category and overlays one histogram per level. Fine for two groups, cluttered for many.

**Seaborn's default bins.** `help(sns.histplot)` (seaborn 0.13.2 in the `.venv`) describes `bins` as a rule name, a number of bins or the bin breaks, "passed to `numpy.histogram_bin_edges`". The help text itself does not give the default value. The function signature does: `bins='auto'`. NumPy's documentation for `'auto'` says it takes the minimum bin width between its `'sturges'` and `'fd'` (Freedman–Diaconis) estimators. On `price` both `'auto'` and `'fd'` give 14 bins.

### How to choose the number of bins
- **Too few bins** blur everything into a couple of blocks. Peaks, gaps and the shape of the tail disappear.
- **Too many bins** leave only a few points in each bin, so the bars turn spiky and the noise looks like structure.
- **A good start:** the Freedman–Diaconis rule. `binwidth = 2 × IQR / n^(1/3)`, then `bins = (max − min) / binwidth`. It uses the IQR, so a few outliers do not stretch it. For `price` this gives about 14 bins.
- **Then check by eye.** Try a few values around the rule's answer. A real feature (a peak, a gap) should survive modest changes in bins. If it vanishes, be careful about reading too much into it.
- Round the width to something readable (e.g. a width of 3000 rather than 2979) when the axis labels matter.

## Common pitfalls
- **The shape depends on the bins.** The same data can look unimodal or bimodal with different bin widths. In `bore`, the default bins show two humps with a dip, but a bin width of 0.2 smooths the dip away. Always try several bin settings before claiming bimodality.
- **Too many bins give spiky bars.** The KDE line is a separate calculation, so it is not affected by the bin count.
- **Overlaid `hue` histograms** hide each other and are hard to compare. Prefer separate subplots.
- **Different group sizes:** with `stat="count"` the biggest group dominates. Switch to `density` for a fair shape comparison.
- **Very small samples:** a histogram of a handful of points mostly shows the bin edges, not the data.
- **Trimmed axes:** limiting `xlim`/`ylim` can cut off the tail and hide skew or outliers.
- A histogram is for continuous or finely-valued numbers. For a column with only a few distinct integer values, use a bar graph (or `discrete=True`).

## How to evaluate it
A histogram is descriptive, so there is no score. Check it against other views:
- `df[col].skew()` puts a number on the lean (positive means a right tail).
- `df[col].describe()` gives the same centre and spread as a [boxplot](boxplot.md).
- Re-draw with a few different `bins` or `binwidth` values. Features that persist are likely real.
- If you suspect two groups, split the data by a category (e.g. `hue` or subplots) and see if the humps separate.

## Minimal example
Run from the project root, in the `.venv`. The CSV is read in place from `materials/` (private, never copied).

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Run from the project root. The file is private, so we only read it in place.
df = pd.read_csv("materials/foundations-python-stats/Automobile.csv")

# --- 1. Rule-of-thumb bin width (Freedman-Diaconis) for price ---
price = df["price"]
iqr = price.quantile(0.75) - price.quantile(0.25)
binwidth = 2 * iqr / len(price) ** (1 / 3)
n_bins = round((price.max() - price.min()) / binwidth)
print(f"price: IQR={iqr:.0f}, binwidth={binwidth:.0f}, bins={n_bins}, skew={price.skew():.2f}")

# --- 2. Same data, three bin choices ---
fig, axes = plt.subplots(1, 3, figsize=(14, 3.5), sharex=True)
for ax, bins, label in zip(axes, [4, n_bins, 60], ["too few", "rule of thumb", "too many"]):
    sns.histplot(data=df, x="price", bins=bins, ax=ax)
    ax.set_title(f"{label}: bins={bins}")
plt.tight_layout()
plt.show()

# --- 3. What a boxplot hides: bore ---
bore = df["bore"]
print(f"bore: median={bore.median():.2f}, skew={bore.skew():.2f}")

fig, (top, bottom) = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
sns.boxplot(data=df, x="bore", ax=top)
top.set_title("Boxplot of bore: looks like one symmetric group")
sns.histplot(data=df, x="bore", kde=True, ax=bottom)  # default bins ("auto")
bottom.set_title("Histogram of bore: two humps with a dip between")
plt.tight_layout()
plt.show()
```

Output on the course dataset (201 rows): `price` has IQR = 8725, a rule-of-thumb bin width of about 2979 and 14 bins, with skew = 1.81 (right-skewed). With 4 bins the right tail is just a block, with 60 bins the bars get spiky, and 14 bins show the pile-up on the left and the long tail clearly. For `bore`, the median is 3.31 and skew is −0.02, so the boxplot looks symmetric, but the histogram (10 default bins, counts 35, 39, 28, 27, 42, 17 across the middle) shows a peak near 3.2, a dip near 3.4 and a second peak near 3.6.

To make the KDE line smoother or wigglier, add `kde_kws={"bw_adjust": 2}` or `{"bw_adjust": 0.5}` to the `histplot` call. The bars stay the same.

## My work
No notebooks linked yet. `notebooks/` is empty. Add a link here when one of my own notebooks uses a histogram.

## Quick quiz
1. What does the height of a bar in a default seaborn histogram represent?
2. Why is it risky to use too few bins, and what goes wrong with too many?
3. A boxplot of a column looks symmetric. What can a histogram of the same column reveal that the boxplot hides?

<details>
<summary>Answers</summary>

1. The number of observations (the count) that fall inside that bin's interval. Other `stat` options rescale it (e.g. `density`, `probability`).
2. Too few bins blur out peaks, gaps and the shape of the tails. Too many leave only a few points per bin, so the bars become spiky and noise looks like structure. A good start is the Freedman–Diaconis rule, `2 × IQR / n^(1/3)`, followed by trying nearby values.
3. Multiple peaks (bimodality), clusters or gaps. A box only shows quartiles, so two humps with a dip between can still look like one ordinary box. Check by trying several bin widths.

</details>

## Open questions
- ~~What is the course's bin-width formula `2 × IQR / n^(1/3)`?~~ **Resolved:** it is the Freedman–Diaconis rule.
- Is the second hump in `bore` a real subgroup (for example, a different engine family) or just an effect of the bin choice? It appears with the default bins but not with a bin width of 0.2. I have not investigated which cars sit in each hump.
- The course notebook adds `kde=True` with a huge `bins` value and says the KDE flattens. I have not reproduced that. From the seaborn docs the KDE is computed from the data, not from the bins, so I have left that claim out until I can check what the course plot really did.
