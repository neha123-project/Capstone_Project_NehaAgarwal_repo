import numpy as np
import pandas as pd

# Task 1 — Load and inspect
customers = pd.read_csv('customers.csv')
print(customers.shape)

products = pd.read_csv('products.csv')
print(products.shape)

orders_df = pd.read_csv('orders.csv')
print(orders_df.shape)

#Task 2 — Standardize payment_method casing

#Standardize the Payment Method
# List the unique entires for payment type

print(orders_df['payment_method'].unique())

# Change the case to upper case for all payment types

orders_df['payment_method'] = orders_df['payment_method'].str.strip().str.upper()
print(orders_df['payment_method'].unique())

# Count the no of different payment types
print(orders_df['payment_method'].value_counts())

#  Task 3 — Remove duplicate orders

# Columns used to identify duplicates
cols = ['customer_id', 'product_id', 'order_date', 'quantity',
        'discount_pct', 'payment_method', 'rating', 'returned']

# Find duplicate rows, keeping the first occurrence
duplicates = orders_df.duplicated(subset=cols, keep='first')

# Print the order_id values of the 5 duplicate rows
print("Dropped order_id:", orders_df[duplicates]['order_id'].tolist())

# Remove duplicates and create a copy
orders_clean = orders_df.drop_duplicates(subset=cols, keep='first').copy()

# Check number of duplicates dropped and final shape
print("Number of duplicates dropped:", duplicates.sum())
print("orders_clean.shape:", orders_clean.shape)

#  Task 4 — Impute missing values

# Count missing values BEFORE filling them
print("Discount rows affected:", orders_clean['discount_pct'].isna().sum())
print("Rating rows affected:", orders_clean['rating'].isna().sum())

# Find and print median rating
median_rating = orders_clean['rating'].median()
print("Median rating:", median_rating)

# Fill missing discount percentages with 0
orders_clean['discount_pct'] = orders_clean['discount_pct'].fillna(0)

# Fill missing ratings with the median
orders_clean['rating'] = orders_clean['rating'].fillna(median_rating)

#saving order_clean
orders_clean.to_csv('orders_clean.csv', index=False)

from google.colab import files
files.download('orders_clean.csv')

# Verify that no missing values remain
print("Missing values after imputation:")
print(orders_clean[['discount_pct', 'rating']].isnull().sum())

#  Task 5 — Merge and reconcile against Part 1

# products = pd.read_csv('products.csv')
# customers = pd.read_csv('customers.csv')

# Merge orders with products and customers
merged = orders_clean.merge(products, on='product_id')
merged = merged.merge(customers, on='customer_id')

# Calculate order value
merged['order_value'] = merged['quantity'] * merged['price'] * (1 - merged['discount_pct'] / 100)

# Print total order value
print("Total order value:", round(merged['order_value'].sum(), 2))
print("Number of cleaned orders:", len(merged))

# Reconciliation note
print("""
Reconciliation: The cleaned total is ₹97,358.30, which is ₹2,501.90 less
than the raw total of ₹99,860.20. This exact difference is due to the
5 duplicate rows removed in Task 3, whose combined order value is ₹2,501.90.
The discount and rating imputation does not change the order value total.
""")

#Task 6 — IQR outlier detection on quantity

# Calculate Q1 and Q3
Q1 = merged['quantity'].quantile(0.25)
Q3 = merged['quantity'].quantile(0.75)

# Calculate IQR
IQR = Q3 - Q1

# Calculate lower and upper limits
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower:", lower)
print("Upper:", upper)

# Flag outliers without removing them
merged['is_outlier'] = (
    (merged['quantity'] < lower) |
    (merged['quantity'] > upper)
)

# Show the outlier rows
outliers = merged[merged['is_outlier']]

print("Number of outliers:", len(outliers))
print(outliers[['order_id', 'quantity']])

# Statistical Summary for orders

print("=== SHAPE ===")
print(orders_clean.shape)

print("\n=== DATA TYPES ===")
print(orders_clean.dtypes)

print("\n=== NUMERIC SUMMARY ===")
print(orders_clean[['quantity','discount_pct','rating','returned']].describe().round(1))

print("\n=== CATEGORICAL COUNTS ===")
for col in [ 'payment_method', 'returned']:
  print(f"\n{col}:")
  print(orders_df[col].value_counts())

# Task 7 — Hypothesis: does COD have a higher return rate?
schema_prompt = """
You are a Data Analyst on Mamaearth's Growth Analytics team. The team suspects that returns are eating into margins on a subset of orders,
but nobody has actually built the pipeline to prove it end-to-end:

DATASET: MAMA Earth's order data
ROWS: 180 orders

COLUMNS:
order_id           object
customer_id        object
product_id         object
order_date         object
quantity            int64
discount_pct      float64
payment_method     object
rating            float64
returned
- order_id (str): unique order identifier
-product_id (str): unique product identifier
- order_date (date): when the order was placed
- customer_id (str): customer code
- payment_method (str): Card / UPI / COD
- quantity (int): number of items purchased
- discount_pct (int): discount applied - 0, 5, 10, 15, or 20%
- rating (int): customer satisfaction rating from 1 to 5
- returned (int): whether the order was returned

SUMMARY STATISTICS:
=== SHAPE ===
(180, 9)

=== DATA TYPES ===
order_id           object
customer_id        object
product_id         object
order_date         object
quantity            int64
discount_pct      float64
payment_method     object
rating            float64
returned            int64


=== NUMERIC SUMMARY ===
       quantity  discount_pct  rating  returned
count     180.0         168.0   165.0     180.0
mean        1.8          18.0     3.0       0.2
std         2.8          10.9     1.5       0.4
min         1.0           0.0     1.0       0.0
25%         1.0          10.0     2.0       0.0
50%         1.0          20.0     3.0       0.0
75%         2.0          30.0     4.0       0.2
max        30.0          30.0     5.0       1.0

=== CATEGORICAL COUNTS ===

payment_method:
payment_method
CARD    70
UPI     55
COD     55
Name: count, dtype: int64

returned:
returned
0    135
1     45
Name: count, dtype: int64

TASK: Generate exactly 3 testable hypotheses about patterns
that might exist in this data. Each hypothesis should:
- Reference specific column names
- State a direction (e.g. \"higher\", \"more likely\", \"lower than\")
- Be something that would matter to the business if confirmed

CONSTRAINTS:
- No hypotheses about data quality or missing values
- Each hypothesis must be different from the others
- Do not explain how to test the hypothesis

FORMAT: Numbered list. Each item: hypothesis in one sentence,
then one sentence on why it would be business-relevant if confirmed.
"""
#print(schema_prompt)

# Task 7 — Hypothesis: does COD have a higher return rate?

print("Hypothesis: COD orders have a higher return rate than other payment methods.")

result = merged.groupby('payment_method')['returned'].agg(['count', 'mean'])


result['mean'] = (result['mean'] * 100).round(1).astype(str) + '%'

print(result['mean'])

print("Hypothesis: Confirmed")

#  Task 8 — Multi-level segmentation

return_by_segment = merged.groupby(['payment_method', 'city_tier']).agg(
    total_orders=('order_id', 'count'),
    returned_orders=('returned', 'sum'),
    return_rate=('returned', 'mean')
).round(3)

print(return_by_segment.sort_values('return_rate', ascending=False))

print("Highest-risk segment: COD + Tier-2 cities at 54.5%")

# Task 9 — Correlation analysis
corr = merged[['rating', 'returned', 'discount_pct', 'quantity']].corr()

print(corr.round(2))

print("\nCorrelation strength:")

for col1 in corr.columns:
    for col2 in corr.columns:
        if col1 < col2:
            r = abs(corr.loc[col1, col2])

            if r < 0.2:
                strength = "negligible"
            elif r < 0.4:
               strength = "weak"
            elif r < 0.7:
                strength = "moderate"
            else:
                strength = "strong"

            print(col1, "vs", col2, ":", strength)

print("\nHypothesis: Higher discounts reduce returns")

if abs(corr.loc['discount_pct', 'returned']) < 0.2:
    print("Busted")
else:
    print("Not Busted")

# Task 10 — Outlier-corrected time series

# Convert order_date to datetime
merged['order_date'] = pd.to_datetime(merged['order_date'])

# Create year-month
merged['month'] = merged['order_date'].dt.to_period('M')

# Monthly total including outliers
monthly_total = merged.groupby('month')['order_value'].sum().round(2)

print("Monthly order value including outliers:")
print(monthly_total)

# Monthly total excluding outliers
monthly_clean = merged[merged['is_outlier'] == False].groupby('month')['order_value'].sum().round(2)

print("\nMonthly order value excluding outliers:")
print(monthly_clean)

merged.to_csv('merged.csv', index=False)
print(merged.columns.tolist())

from google.colab import files

files.download('merged.csv')

print("\nJanuary's apparent lead is an artifact of the two bulk orders landing in January: O0011 on 2026-01-28 and O0098 on 2026-01-10.")
print("Once these outlier orders are excluded, March is the genuine peak month.")

#Task 1 — narrator/findings.json

import json

orders_with_price = orders_df.merge(
    products[['product_id', 'price']],
    on='product_id'
)

orders_with_price['order_value'] = (
    orders_with_price['quantity'] *
    orders_with_price['price'] *
    (1 - orders_with_price['discount_pct'].fillna(0) / 100)
)

raw_total = orders_with_price['order_value'].sum()

#print("Raw total:", round(raw_total, 2))

#raw_total = orders_df['order_value'].sum()
cleaned_total = merged['order_value'].sum()

findings = {
    "cleaned_total_revenue_inr": round(cleaned_total, 2),

    "raw_total_revenue_inr": round(raw_total, 2),

    "duplicate_reconciliation_delta_inr": round(
        raw_total - cleaned_total, 2
    ),

    "return_rate_by_payment": {
        "COD": result.loc["COD", "mean"],
        "CARD": result.loc["CARD", "mean"],
        "UPI": result.loc["UPI", "mean"]
    },

    "highest_risk_segment": {
        "payment_method": return_by_segment.sort_values(
            'return_rate', ascending=False
        ).iloc[0].name[0],

        "city_tier": int(
            return_by_segment.sort_values(
                'return_rate', ascending=False
            ).iloc[0].name[1]
        ),

        "return_rate_pct": round(
            return_by_segment.sort_values(
                'return_rate', ascending=False
            ).iloc[0]['return_rate'] * 100, 1
        )
    },

    "true_peak_month": {
        "month": str(monthly_clean.idxmax()),
        "revenue_inr": round(monthly_clean.max(), 2)
    },

"outlier_inflated_month": {
    "month": str(monthly_total.idxmax()),
    "apparent_revenue_inr": round(monthly_total.max(), 2),
    "corrected_revenue_inr": round(
        monthly_clean.loc[monthly_total.idxmax()], 2
    )
}
}

# Download the required data in json format 
with open("findings.json", "w") as f:
    json.dump(findings, f, indent=4)

from google.colab import files

files.download('findings.json')
