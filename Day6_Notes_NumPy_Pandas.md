# Day 6 Notes — NumPy & Pandas Foundations

---

## 1. NumPy Arrays

**What it is:** NumPy's core object is the `ndarray` (n-dimensional array) — a fast, memory-efficient, fixed-type container for numerical data. Unlike Python lists, all elements share the same dtype, which lets NumPy use compiled C code under the hood instead of looping in Python.

**Creating arrays**
```python
import numpy as np

a = np.array([1, 2, 3])              # 1D array
b = np.array([[1, 2], [3, 4]])       # 2D array
c = np.zeros((3, 4))                 # 3x4 array of zeros
d = np.ones((2, 2))
e = np.arange(0, 10, 2)              # [0,2,4,6,8]
f = np.linspace(0, 1, 5)             # 5 evenly spaced values between 0 and 1
g = np.random.rand(3, 3)             # random floats 0-1
```

**Key attributes**
| Attribute | Meaning |
|---|---|
| `a.shape` | dimensions, e.g. (3,4) |
| `a.ndim` | number of dimensions |
| `a.dtype` | data type of elements |
| `a.size` | total number of elements |

**Indexing & slicing**
```python
a[0]          # first element
a[-1]         # last element
a[1:4]        # slice
b[0, 1]       # row 0, col 1
b[:, 0]       # all rows, column 0
b[1, :]       # row 1, all columns
```

**Why use NumPy instead of lists?**
- Vectorized operations (no explicit Python loops → much faster)
- Less memory (fixed dtype vs Python object overhead)
- Foundation for Pandas, scikit-learn, TensorFlow, etc.

**Common operations**
```python
a.reshape(3, 1)      # change shape without changing data
a.flatten()           # collapse to 1D
np.concatenate([a, a])
a.sum(), a.mean(), a.std(), a.max(), a.min()
a.sum(axis=0)         # column-wise sum (2D)
a.sum(axis=1)         # row-wise sum
```

---

## 2. Broadcasting

**What it is:** Broadcasting is NumPy's rule set for performing arithmetic between arrays of *different but compatible* shapes, without actually copying data to match shapes.

**The rule (compared dimension by dimension, from the right):**
1. If dimensions are equal → OK.
2. If one of them is 1 → it gets "stretched" to match the other.
3. If neither is true → error (shapes are incompatible).

**Examples**
```python
a = np.array([1, 2, 3])        # shape (3,)
b = 2
a * b                          # scalar broadcasts to every element → [2,4,6]

c = np.array([[1,2,3],[4,5,6]])  # shape (2,3)
d = np.array([10,20,30])         # shape (3,)
c + d                             # d is broadcast across each row
# [[11,22,33],
#  [14,25,36]]

e = np.array([[1],[2]])        # shape (2,1)
c + e                           # e is broadcast across each column
```

**Why it matters:** Broadcasting avoids writing manual loops to apply an operation across rows/columns — this is the mechanism behind almost every efficient NumPy/Pandas computation (normalizing data, adding a bias vector, scaling features, etc.).

**Common pitfall:** shapes like (3,) and (4,) are NOT broadcastable — always check `.shape` when you get a `ValueError: operands could not be broadcast together`.

---

## 3. Pandas DataFrame

**What it is:** A `DataFrame` is a 2D labeled data structure (rows + named columns) — think of it as a spreadsheet/SQL table in Python, built on top of NumPy.

**Creating a DataFrame**
```python
import pandas as pd

data = {
    "Name": ["Asha", "Ravi", "Meena"],
    "Age": [25, 30, 22],
    "City": ["Bengaluru", "Delhi", "Mumbai"]
}
df = pd.DataFrame(data)
```

**Key components**
- `df.index` — row labels
- `df.columns` — column labels
- `df.values` — underlying NumPy array

**Inspecting data**
```python
df.head()        # first 5 rows
df.tail(3)        # last 3 rows
df.shape          # (rows, columns)
df.info()         # dtypes, non-null counts, memory usage
df.describe()     # summary stats for numeric columns
df.dtypes
df.columns
```

**Selecting data**
```python
df["Age"]                     # single column (Series)
df[["Name", "Age"]]           # multiple columns (DataFrame)
df.loc[0]                     # row by label
df.iloc[0]                    # row by integer position
df.loc[0, "Name"]             # specific cell by label
df.iloc[0:2, 0:2]             # slice by position
```

**Adding / modifying columns**
```python
df["Age_in_5_years"] = df["Age"] + 5
df.rename(columns={"City": "Location"}, inplace=True)
df.drop("Age_in_5_years", axis=1, inplace=True)
```

---

## 4. Reading CSV / Excel / JSON

Pandas' I/O functions all follow a similar pattern: `pd.read_<format>()` to load, `.to_<format>()` to save.

**CSV**
```python
df = pd.read_csv("data.csv")
df = pd.read_csv("data.csv", sep=";", header=0, index_col=0)
df.to_csv("output.csv", index=False)
```

**Excel** (needs `openpyxl` installed)
```python
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df.to_excel("output.xlsx", index=False)
```

**JSON**
```python
df = pd.read_json("data.json")
df.to_json("output.json", orient="records")
```

**Useful parameters across readers**
| Parameter | Purpose |
|---|---|
| `sep` / `delimiter` | column separator (CSV) |
| `header` | which row is the header |
| `index_col` | which column to use as row index |
| `usecols` | load only specific columns |
| `dtype` | force column data types on load |
| `na_values` | custom strings to treat as NaN |
| `nrows` | limit number of rows read (useful for big files) |

---

## 5. Filtering

**What it is:** Selecting rows that meet certain conditions — the Pandas equivalent of a SQL `WHERE` clause.

**Boolean masking**
```python
df[df["Age"] > 25]
df[df["City"] == "Delhi"]
```

**Multiple conditions** (use `&`, `|`, `~` — NOT `and`/`or`, and wrap each condition in parentheses)
```python
df[(df["Age"] > 20) & (df["City"] == "Mumbai")]
df[(df["Age"] < 25) | (df["City"] == "Delhi")]
df[~(df["City"] == "Delhi")]           # negation
```

**`isin()` for multiple values**
```python
df[df["City"].isin(["Delhi", "Mumbai"])]
```

**String filtering**
```python
df[df["Name"].str.startswith("A")]
df[df["Name"].str.contains("a", case=False)]
```

**`query()` method (alternative syntax)**
```python
df.query("Age > 25 and City == 'Delhi'")
```

---

## 6. GroupBy

**What it is:** GroupBy implements the "split–apply–combine" pattern: split data into groups based on a key, apply a function to each group, then combine results.

```python
df.groupby("City")["Age"].mean()
df.groupby("City").agg({"Age": "mean", "Name": "count"})
df.groupby("City").size()                      # count rows per group
df.groupby(["City", "Gender"]).mean()           # multiple keys
```

**Common aggregation functions:** `mean()`, `sum()`, `count()`, `min()`, `max()`, `std()`, `median()`, `first()`, `last()`

**Custom aggregation**
```python
df.groupby("City").agg(
    avg_age=("Age", "mean"),
    total=("Age", "count")
)
```

**`transform()` vs `agg()`**
- `agg()` returns one row per group (collapsed).
- `transform()` returns a result the same shape as the original data (useful for adding a group-level stat back onto every row).
```python
df["city_avg_age"] = df.groupby("City")["Age"].transform("mean")
```

---

## 7. Missing Value Handling

**Detecting missing values**
```python
df.isnull().sum()          # count of NaNs per column
df.isnull().mean() * 100   # percentage missing per column
df[df["Age"].isnull()]     # rows where Age is missing
```

**Strategy 1 — Drop**
```python
df.dropna()                       # drop rows with ANY missing value
df.dropna(axis=1)                 # drop columns with any missing value
df.dropna(thresh=3)                # keep rows with at least 3 non-null values
df.dropna(subset=["Age"])          # drop rows only if Age is missing
```

**Strategy 2 — Fill/Impute**
```python
df["Age"].fillna(df["Age"].mean(), inplace=True)     # mean imputation
df["Age"].fillna(df["Age"].median(), inplace=True)   # median (robust to outliers)
df["City"].fillna(df["City"].mode()[0], inplace=True) # mode for categorical
df.fillna(method="ffill")          # forward fill (carry last valid value forward)
df.fillna(method="bfill")          # backward fill
df.fillna(0)                        # fill with a constant
```

**Choosing a strategy:**
- Numeric + roughly symmetric → mean
- Numeric + skewed/outliers present → median
- Categorical → mode, or a new category like `"Unknown"`
- Time-series data → forward/backward fill
- If a column is mostly missing (e.g., >60-70%) — consider dropping the column entirely rather than imputing.

---

## 8. Data Preprocessing

Preprocessing is the umbrella step of getting raw data into a clean, consistent, model-ready shape. Typical checklist:

1. **Handle missing values** (see above)
2. **Remove duplicates**
   ```python
   df.duplicated().sum()
   df.drop_duplicates(inplace=True)
   ```
3. **Fix data types**
   ```python
   df["Age"] = df["Age"].astype(int)
   df["Date"] = pd.to_datetime(df["Date"])
   ```
4. **Handle outliers** (e.g., using IQR method)
   ```python
   Q1 = df["Age"].quantile(0.25)
   Q3 = df["Age"].quantile(0.75)
   IQR = Q3 - Q1
   lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
   df = df[(df["Age"] >= lower) & (df["Age"] <= upper)]
   ```
5. **Standardize text/categorical data** (fix casing, whitespace, typos)
   ```python
   df["City"] = df["City"].str.strip().str.title()
   ```
6. **Encode categorical variables** (for ML)
   ```python
   pd.get_dummies(df, columns=["City"])          # one-hot encoding
   df["City"].map({"Delhi": 0, "Mumbai": 1})     # label encoding
   ```
7. **Scale/normalize numeric features** (often via scikit-learn's `StandardScaler` / `MinMaxScaler`)

---

## 9. Feature Engineering Basics

**What it is:** Creating new, more informative columns (features) from existing raw data to help downstream analysis or models perform better.

**Common techniques**
```python
# Extract parts of a date
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["DayOfWeek"] = df["Date"].dt.dayofweek

# Binning a continuous variable
df["Age_Group"] = pd.cut(df["Age"], bins=[0,18,35,60,100],
                          labels=["Teen","Young Adult","Adult","Senior"])

# Combining columns
df["Full_Address"] = df["City"] + ", " + df["State"]

# Ratio/derived features
df["Price_per_sqft"] = df["Price"] / df["Area"]

# Flag/indicator features
df["Is_Metro"] = df["City"].isin(["Delhi","Mumbai","Bengaluru"]).astype(int)
```

**Why it matters:** Raw data rarely captures patterns directly usable by a model — good feature engineering (dates → seasonality, text → keywords, numbers → ratios/bins) often improves model performance more than switching algorithms.

---

## Quick-Reference Summary Table

| Topic | Core Idea | Key Functions |
|---|---|---|
| NumPy Arrays | Fast, typed containers for numeric data | `np.array`, `.shape`, `.reshape` |
| Broadcasting | Apply ops across mismatched shapes | automatic in `+ - * /` |
| DataFrame | Labeled 2D table | `pd.DataFrame`, `.loc`, `.iloc` |
| Reading Files | Load external data | `pd.read_csv/excel/json` |
| Filtering | Row selection by condition | boolean masks, `.query()` |
| GroupBy | Split-apply-combine | `.groupby().agg()` |
| Missing Values | Detect & handle NaNs | `.isnull()`, `.dropna()`, `.fillna()` |
| Preprocessing | Clean raw → model-ready data | dedupe, dtype fix, outliers |
| Feature Engineering | Create new predictive columns | date parts, binning, ratios |
