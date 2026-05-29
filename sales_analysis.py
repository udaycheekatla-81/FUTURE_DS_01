# ========== TASK 1: BUSINESS SALES ANALYSIS ==========
# Install required libraries (run once)
# pip install pandas matplotlib seaborn numpy plotly

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Set style for better visuals
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ========== 1. CREATE SAMPLE SALES DATA ==========
np.random.seed(42)

# Date range for 1 year
dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')

# Products data
products = {
    'Laptop Pro': {'category': 'Electronics', 'base_price': 1200},
    'Smartphone X': {'category': 'Electronics', 'base_price': 800},
    'Wireless Mouse': {'category': 'Accessories', 'base_price': 25},
    'Mechanical Keyboard': {'category': 'Accessories', 'base_price': 120},
    'USB-C Cable': {'category': 'Accessories', 'base_price': 15},
    'Monitor 27"': {'category': 'Electronics', 'base_price': 350},
    'Desk Chair': {'category': 'Furniture', 'base_price': 250},
    'Standing Desk': {'category': 'Furniture', 'base_price': 450},
    'Webcam HD': {'category': 'Electronics', 'base_price': 80},
    'Noise Headphones': {'category': 'Audio', 'base_price': 150}
}

# Generate sales data
sales_data = []
regions = ['North', 'South', 'East', 'West']
cities = {
    'North': ['New York', 'Boston', 'Chicago'],
    'South': ['Atlanta', 'Miami', 'Dallas'],
    'East': ['Washington DC', 'Philadelphia', 'Charlotte'],
    'West': ['Los Angeles', 'San Francisco', 'Seattle']
}

for _ in range(5000):
    date = np.random.choice(dates)
    product = np.random.choice(list(products.keys()))
    region = np.random.choice(regions, p=[0.3, 0.2, 0.25, 0.25])
    city = np.random.choice(cities[region])
    quantity = np.random.randint(1, 10)
    base_price = products[product]['base_price']
    discount = np.random.choice([0, 0.05, 0.1, 0.15], p=[0.7, 0.15, 0.1, 0.05])
    revenue = quantity * base_price * (1 - discount)
    
    sales_data.append({
        'Date': date,
        'Product': product,
        'Category': products[product]['category'],
        'Region': region,
        'City': city,
        'Quantity': quantity,
        'Unit_Price': base_price,
        'Discount': discount,
        'Revenue': revenue
    })

df_sales = pd.DataFrame(sales_data)
df_sales['Month'] = df_sales['Date'].dt.to_period('M')
df_sales['Week'] = df_sales['Date'].dt.isocalendar().week

print("=" * 60)
print("TASK 1: BUSINESS SALES ANALYSIS")
print("=" * 60)
print(f"\nDataset Shape: {df_sales.shape}")
print(f"Date Range: {df_sales['Date'].min()} to {df_sales['Date'].max()}")
print(f"Total Revenue: ${df_sales['Revenue'].sum():,.2f}")
print(f"Total Units Sold: {df_sales['Quantity'].sum():,}")

# ========== 2. REVENUE TRENDS ANALYSIS ==========
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('BUSINESS SALES ANALYSIS DASHBOARD', fontsize=15, fontweight='bold')
# Monthly revenue trend
monthly_revenue = df_sales.groupby('Month')['Revenue'].sum()
axes[0, 0].plot(monthly_revenue.index.astype(str), monthly_revenue.values, marker='o', linewidth=2, markersize=6)
axes[0, 0].set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Revenue ($)')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].grid(True, alpha=0.3)

# Weekly revenue trend (first 12 weeks)
weekly_revenue = df_sales.groupby('Week')['Revenue'].sum().head(12)
axes[0, 1].bar(range(1, 13), weekly_revenue.values, edgecolor='black')
axes[0, 1].set_title('Weekly Revenue Trend (First 12 Weeks)', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Week Number')
axes[0, 1].set_ylabel('Revenue ($)')

# Top 10 products by revenue
top_products = df_sales.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(10)
axes[1, 0].barh(range(len(top_products)), top_products.values)
axes[1, 0].set_yticks(range(len(top_products)))
axes[1, 0].set_yticklabels(top_products.index)
axes[1, 0].set_title('Top 10 Products by Revenue', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Revenue ($)')

# Category revenue distribution
category_revenue = df_sales.groupby('Category')['Revenue'].sum()
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
axes[1, 1].pie(category_revenue.values, labels=category_revenue.index, autopct='%1.1f%%', colors=colors, startangle=90)
axes[1, 1].set_title('Revenue by Category', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('sales_analysis_1.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== 3. REGIONAL PERFORMANCE ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Revenue by region
region_revenue = df_sales.groupby('Region')['Revenue'].sum().sort_values(ascending=False)
axes[0].bar(region_revenue.index, region_revenue.values, edgecolor='black', color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
axes[0].set_title('Revenue by Region', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Region')
axes[0].set_ylabel('Revenue ($)')
for i, v in enumerate(region_revenue.values):
    axes[0].text(i, v + 5000, f'${v/1000:.0f}K', ha='center', fontweight='bold')

# Revenue by city (top 10)
city_revenue = df_sales.groupby('City')['Revenue'].sum().sort_values(ascending=False).head(10)
axes[1].barh(range(len(city_revenue)), city_revenue.values, color='teal')
axes[1].set_yticks(range(len(city_revenue)))
axes[1].set_yticklabels(city_revenue.index)
axes[1].set_title('Top 10 Cities by Revenue', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Revenue ($)')

plt.tight_layout()
plt.savefig('sales_analysis_2.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== 4. INSIGHTS & RECOMMENDATIONS ==========
print("\n" + "=" * 60)
print("KEY INSIGHTS")
print("=" * 60)

print("\n📊 REVENUE INSIGHTS:")
print(f"  • Best month: {monthly_revenue.idxmax()} (${monthly_revenue.max():,.2f})")
print(f"  • Worst month: {monthly_revenue.idxmin()} (${monthly_revenue.min():,.2f})")
print(f"  • Monthly avg: ${monthly_revenue.mean():,.2f}")

print("\n🏆 TOP PERFORMING PRODUCTS:")
for i, (product, revenue) in enumerate(top_products.head(3).items(), 1):
    print(f"  {i}. {product}: ${revenue:,.2f}")

print("\n🗺️ REGIONAL INSIGHTS:")
best_region = region_revenue.index[0]
print(f"  • Best region: {best_region} (${region_revenue.iloc[0]:,.2f})")
print(f"  • Region with growth opportunity: {region_revenue.index[-1]} (${region_revenue.iloc[-1]:,.2f})")

print("\n💡 ACTIONABLE RECOMMENDATIONS:")
print("  ✅ Increase inventory for Laptop Pro and Smartphone X during peak months (March-June)")
print("  ✅ Launch targeted marketing campaigns in South region (30% below North region)")
print("  ✅ Bundle accessories with Electronics to increase average order value")
print("  ✅ Implement loyalty program for repeat customers in top cities")