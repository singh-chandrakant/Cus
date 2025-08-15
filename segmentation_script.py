
# segmentation_script.py
# Author: Chandrakant Singh
# Date: 2025-08-15
# Description: Customer segmentation using RFM and KMeans clustering

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ========================
# 1. Load Dataset
# ========================
df = pd.read_csv("ecommerce_customers.csv", parse_dates=["LastPurchaseDate"])

# ========================
# 2. Data Cleaning
# ========================
df.drop_duplicates(subset=["CustomerID"], inplace=True)
df.dropna(subset=["TotalSpend", "TotalOrders", "AvgOrderValue", "LastPurchaseDate"], inplace=True)

# ========================
# 3. Feature Engineering - RFM
# ========================
today = pd.to_datetime("2025-08-15")
df["Recency"] = (today - df["LastPurchaseDate"]).dt.days
df["Frequency"] = df["TotalOrders"]
df["Monetary"] = df["TotalSpend"]

# ========================
# 4. Scaling
# ========================
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(df[["Recency", "Frequency", "Monetary"]])

# ========================
# 5. KMeans Clustering
# ========================
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Segment"] = kmeans.fit_predict(rfm_scaled)

# ========================
# 6. Map Segments to Tiers
# ========================
segment_order = df.groupby("Segment")["Monetary"].mean().sort_values(ascending=False).index
tier_labels = {
    segment_order[0]: "High Value",
    segment_order[1]: "Medium Value",
    segment_order[2]: "Low Value"
}
df["Tier"] = df["Segment"].map(tier_labels)

# ========================
# 7. Save Output
# ========================
df.to_csv("customer_segments.csv", index=False)
print("Segmentation complete. Output saved to customer_segments.csv.")

# ========================
# 8. Visualizations
# ========================

# Tier distribution
plt.figure(figsize=(6, 4))
sns.countplot(x="Tier", data=df, palette="viridis", order=["High Value", "Medium Value", "Low Value"])
plt.title("Tier Distribution")
plt.savefig("tier_distribution.png")
plt.close()

# Spend distribution
plt.figure(figsize=(6, 4))
sns.boxplot(x="Tier", y="Monetary", data=df, palette="coolwarm", order=["High Value", "Medium Value", "Low Value"])
plt.title("Spend Distribution by Tier")
plt.savefig("spend_distribution.png")
plt.close()

# Recency vs Monetary
plt.figure(figsize=(6, 4))
sns.scatterplot(x="Recency", y="Monetary", hue="Tier", data=df, palette="Set2", s=60)
plt.title("Recency vs Monetary")
plt.savefig("recency_vs_monetary.png")
plt.close()

print("Visualizations saved: tier_distribution.png, spend_distribution.png, recency_vs_monetary.png")
