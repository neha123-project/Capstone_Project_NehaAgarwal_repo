# Task 11 — Two visualizations (analysis/visualize.py) -'return_rate_by_payment.png'
# (bar chart: return rate by payment method)

# Generate a matplotlib bar chart using a DataFrame called orders_clean.
# Data:  a bar chart of return rate by (cleaned) payment_method
# Sort bars descending.
# Title: "States the finding (e.g. "COD Returns at 44.4% — 3x Card"
# Colour the Referral bar green (#27AE60), all others grey (#BDC3C7)
# Add data labels above each bar (1 decimal, % sign)
# Remove top and right spines. Figure size: 7x4. tight_layout().
# Save as 'return_rate_by_payment.png', dpi=150, facecolor='white'

# Task 11 — Two visualizations (analysis/visualize.py) -'return_rate_by_payment.png'
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
from google.colab import files

#uploaded = files.upload('orders_clean.csv')
orders_clean = pd.read_csv("orders_clean.csv")


# Calculate return rate by payment method
return_rate = orders_clean.groupby('payment_method')['returned'].mean() * 100

# Sort from highest to lowest
return_rate = return_rate.sort_values(ascending=False)

# Create bar chart
plt.figure(figsize=(7, 4))

bars = plt.bar(
    return_rate.index,
    return_rate.values,
    color=['#27AE60' if x == 'COD' else '#BDC3C7' for x in return_rate.index]
)

# Add data labels
for bar, value in zip(bars, return_rate.values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f'{value:.1f}%',
        ha='center',
        va='bottom'
    )

# Title
plt.title("COD Returns at 44.4% — 3x Card")
plt.ylabel("Return Rate (%)")

# Remove top and right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.tight_layout()

# Save the chart
plt.savefig('return_rate_by_payment.png', dpi=150, facecolor='white')

plt.show()

# Task 11 — Two visualizations (analysis/visualize.py) -'monthly_revenue_trend.png'
# (line chart: outlier corrected monthly revenue)

# Generate a matplotlib line chart using a DataFrame called monthly_clean.
# Data: Take data from monthly_clean excluidng the outliers.
# Reindex in month order: Jan, Feb, Mar, Apr, May, Jun.
# Add circular markers at each point.
# Highlight the revenue peak month with a red marker (colour #E74C3C, size 120, zorder=5).
# Add annotation on Peak Month: "", fontsize=9, colour red.
# Title: "Actual Peak Month should be mentioned"
# X-label: Order Month. Y-label: Order Value (%). Y-axis: 0 to 60.
# Remove top and right spines. Figure size: 8x4. tight_layout().
# Save as 'monthly_revenue_trend.png', dpi=150, facecolor='white'

# Task 11 — Two visualizations (analysis/visualize.py) -'monthly_revenue_trend.png'
import pandas as pd
import matplotlib.pyplot as plt

# Read merged data

merged = pd.read_csv('merged.csv')

# print(merged.columns)

merged['order_date'] = pd.to_datetime(merged['order_date'])

merged['month'] = merged['order_date'].dt.to_period('M')

monthly_clean = (
    merged[merged['is_outlier'] == False]
    .groupby('month')['order_value']
    .sum()
    .round(2)
)

# Reindex in month order
monthly_clean = monthly_clean.reindex([
    '2026-01', '2026-02', '2026-03',
    '2026-04', '2026-05', '2026-06'
])

# Month names
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

# Find peak month
peak_position = monthly_clean.values.argmax()
peak_value = monthly_clean.iloc[peak_position]

# Create line chart
plt.figure(figsize=(8, 4))

plt.plot(
    months,
    monthly_clean.values,
    marker='o'
)

# Highlight peak month
plt.scatter(
    months[peak_position],
    peak_value,
    color='#E74C3C',
    s=120,
    zorder=5
)

# Add annotation to the right of peak
plt.annotate(
    f'Peak Month: Mar — ₹{peak_value:,.2f}',
    (months[peak_position], peak_value),
    xytext=(50, 10),
    textcoords='offset points',
    fontsize=9,
    color='#E74C3C'
)
# Title and labels
plt.title("March Is the Actual Peak Month", pad=15)
plt.xlabel("Order Month")
plt.ylabel("Order Value")

# Remove top and right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.tight_layout()

# Save chart
plt.savefig(
    'monthly_revenue_trend.png',
    dpi=150,
    facecolor='white'
)

plt.show()
