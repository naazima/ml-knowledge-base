# Boxplot

**Course:** Foundations Python & Stats
**Type:** technique

## In one sentence
A boxplot squeezes a numeric variable into a box, a middle line and two whiskers so you can see its centre, spread, outliers and rough skew at a glance, and line up several groups side by side.

## When to use it
- A quick check of spread and outliers for one numeric column.
- Comparing a numeric variable across categories (e.g. price for each body style), where a row of histograms would be cluttered.
- Spotting skew before deciding whether the mean is a fair summary.
- **Not** when you need the shape of the distribution (peaks, clusters). Use a histogram for that.

## How it works (simple)
Sort the data and cut it into quarters:

- **Box:** runs from Q1 (25th percentile) to Q3 (75th percentile). So the box holds the middle 50% of the data. Its width is the IQR = Q3 − Q1.
- **Line inside the box:** the median (50th percentile).
- **Whiskers:** extend from the box out to the furthest data points that are still within about 1.5 × IQR of the box edge.
- **Dots beyond the whiskers:** outliers, i.e. points further out than that rule allows.

**Reading skew** (look at where the median sits in the box and which whisker is longer):

| What you see | Reading |
|---|---|
| Median close to Q1, longer whisker on the right | Right-skewed (positive skew): most values are low, a tail of high ones |
| Median close to Q3, longer whisker on the left | Left-skewed (negative skew): most values are high, a tail of low ones |
| Median roughly centred, whiskers about equal | Roughly symmetric |

The skew is named after the side the tail points to, not where the bulk of the data is. In the `price` column the box is squashed to the left and the tail stretches right, so it is right-skewed.

## Key parameters / choices
- **Orientation:** `x=` for a horizontal box (easier to read skew left to right), `y=` for vertical.
- **Grouping:** give the numeric column to one axis and a categorical column to the other to get one box per category.
- **Whisker length:** seaborn's `whis` argument. Its default is 1.5 (× IQR). Raising it pushes more points inside the whiskers and shows fewer outliers.
- **Presentation:** `color`, `order` (to sort the categories sensibly), and a title/axis labels so the units are clear.

## Common pitfalls
- **Whisker ends are not always the min and max.** If there are outliers, they lie beyond the whisker. The whisker stops at the last point inside the 1.5 × IQR limit.
- **Hidden shape:** two humps (bimodal data) can produce an ordinary-looking box. Always confirm with a histogram when it matters.
- **Skew from a boxplot is a rough guide.** Back it up with a number such as `Series.skew()`.
- **Small groups:** a box drawn from a handful of points looks more solid than it is. Check the group sizes (`value_counts()`).
- An "outlier" here is just a point outside the whisker rule. It is not automatically an error or something to delete.

## How to evaluate it
A boxplot is descriptive, so there is no score. Instead check that it agrees with other views:
- `df[col].describe()` gives the same five numbers (min, Q1, median, Q3, max) to compare against the picture.
- `df[col].skew()` puts a number on the skew (positive means right-skewed).
- A histogram of the same column confirms the shape and any clusters.

## Minimal example
Run from the project root, in the `.venv`. The CSV is read in place from `materials/` (private, never copied).

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Run from the project root. The file is private, so we only read it in place.
df = pd.read_csv("materials/foundations-python-stats/Automobile.csv")

# Numbers behind the picture
print(df["price"].describe()[["min", "25%", "50%", "75%", "max"]])
print("skew of price:", round(df["price"].skew(), 2))  # > 0 means right-skewed

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 1) One variable: horizontal box, so the skew reads left-to-right
sns.boxplot(data=df, x="price", ax=axes[0])
axes[0].set_title("Price (median near Q1, long right whisker)")

# 2) Compare groups: one box per body style
sns.boxplot(data=df, x="body_style", y="price", ax=axes[1])
axes[1].set_title("Price by body style")

plt.tight_layout()
plt.show()
```

Output on the course dataset: Q1 = 7775, median = 10295, Q3 = 16500, max = 45400, skew = 1.81. The median sits nearer Q1 than Q3 and the skew is positive, so `price` is right-skewed.

## My work
No notebooks linked yet. `notebooks/` is empty. Add a link here when one of my own notebooks uses a boxplot.

## Quick quiz
1. What do the two edges of the box and the line inside it represent?
2. In a horizontal boxplot the median sits close to the left edge of the box and the right whisker is much longer. Is the data left- or right-skewed?
3. Name one thing a histogram can show that a boxplot can hide.

<details>
<summary>Answers</summary>

1. The edges are Q1 (25th percentile) and Q3 (75th percentile), so the box holds the middle 50% of the data. The inside line is the median.
2. Right-skewed (positive skew). Most values are low and a tail stretches to the high end.
3. Multiple peaks / clusters (bimodality). A boxplot of such data can look like an ordinary single box.

</details>

## Open questions
- ~~The course diagram labels the whisker ends "Minimum" and "Maximum". Are they the true data min and max?~~ **Resolved:** the whisker ends are the furthest points within 1.5 × IQR of the box (seaborn's default, `whis=1.5`). The diagram's "Minimum/Maximum" label is a simplification.
- How exactly does the course want "closer to the left/right" judged? It reads like an eyeball rule, so I have treated it as one and paired it with `.skew()`.
