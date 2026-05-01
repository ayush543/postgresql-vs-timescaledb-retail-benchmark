import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

RAW_DIR = Path("data/raw/instacart")
OUT_DIR = Path("data/synthetic")
OUT_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

NUM_PRODUCTS = 5000
NUM_WAREHOUSES = 5
NUM_SUPPLIERS = 50
DAYS = 180

products = pd.read_csv(RAW_DIR / "products.csv").head(NUM_PRODUCTS)
product_ids = products["product_id"].unique()

# -----------------------------
# Suppliers
# -----------------------------
suppliers = pd.DataFrame({
    "supplier_id": range(1, NUM_SUPPLIERS + 1),
    "supplier_name": [f"Supplier_{i}" for i in range(1, NUM_SUPPLIERS + 1)],
    "region": np.random.choice(
        ["Midwest", "West", "South", "Northeast"],
        NUM_SUPPLIERS
    ),
    "lead_time_days": np.random.randint(2, 15, NUM_SUPPLIERS)
})

# -----------------------------
# Product to supplier mapping
# -----------------------------
product_supplier = pd.DataFrame({
    "product_id": product_ids,
    "supplier_id": np.random.choice(suppliers["supplier_id"], len(product_ids))
})

# -----------------------------
# Product demand skew
# 20% of products receive much higher demand
# -----------------------------
hot_product_count = int(0.20 * len(product_ids))
hot_products = set(np.random.choice(product_ids, hot_product_count, replace=False))

# -----------------------------
# Reorder rules
# -----------------------------
rules = []

for product_id in product_ids:
    for warehouse_id in range(1, NUM_WAREHOUSES + 1):
        if product_id in hot_products:
            reorder_threshold = np.random.randint(80, 180)
            target_stock_level = reorder_threshold + np.random.randint(300, 700)
        else:
            reorder_threshold = np.random.randint(20, 100)
            target_stock_level = reorder_threshold + np.random.randint(100, 400)

        rules.append([
            product_id,
            warehouse_id,
            reorder_threshold,
            target_stock_level
        ])

reorder_rules = pd.DataFrame(
    rules,
    columns=[
        "product_id",
        "warehouse_id",
        "reorder_threshold",
        "target_stock_level"
    ]
)

# -----------------------------
# Inventory snapshots
# -----------------------------
snapshots = []
start_date = datetime(2025, 1, 1)

for day in range(DAYS):
    current_date = start_date + timedelta(days=day)

    # Weekly seasonality
    day_of_week = current_date.weekday()

    if day_of_week in [5, 6]:
        seasonality_factor = 1.35   # weekend demand
    else:
        seasonality_factor = 1.00

    # Monthly demand spike around day 25-30
    if current_date.day >= 25:
        seasonality_factor *= 1.25

    # Random promotion spike days
    promotion_day = np.random.random() < 0.05

    for product_id in product_ids:
        supplier_id = product_supplier.loc[
            product_supplier["product_id"] == product_id,
            "supplier_id"
        ].iloc[0]

        product_skew_factor = 2.5 if product_id in hot_products else 1.0

        for warehouse_id in range(1, NUM_WAREHOUSES + 1):
            rule = reorder_rules[
                (reorder_rules["product_id"] == product_id) &
                (reorder_rules["warehouse_id"] == warehouse_id)
            ].iloc[0]

            base_stock = rule["target_stock_level"]

            demand_factor = seasonality_factor * product_skew_factor

            if promotion_day and product_id in hot_products:
                demand_factor *= np.random.uniform(1.5, 3.0)

            estimated_demand = int(np.random.poisson(25 * demand_factor))

            stock_quantity = base_stock - estimated_demand + np.random.randint(-30, 50)

            # Add random stockouts
            stockout_chance = 0.03

            if product_id in hot_products:
                stockout_chance = 0.08

            if np.random.random() < stockout_chance:
                stock_quantity = np.random.randint(0, 5)

            stock_quantity = max(stock_quantity, 0)

            snapshots.append([
                product_id,
                warehouse_id,
                stock_quantity,
                rule["reorder_threshold"],
                current_date,
                supplier_id
            ])

inventory_snapshots = pd.DataFrame(
    snapshots,
    columns=[
        "product_id",
        "warehouse_id",
        "stock_quantity",
        "reorder_threshold",
        "inventory_timestamp",
        "supplier_id"
    ]
)

# -----------------------------
# Save files
# -----------------------------
suppliers.to_csv(OUT_DIR / "suppliers.csv", index=False)
product_supplier.to_csv(OUT_DIR / "product_supplier.csv", index=False)
reorder_rules.to_csv(OUT_DIR / "reorder_rules.csv", index=False)
inventory_snapshots.to_csv(OUT_DIR / "inventory_snapshots.csv", index=False)

print("Synthetic supply chain data generated.")
print(f"Products used: {len(product_ids):,}")
print(f"Suppliers: {len(suppliers):,}")
print(f"Product-supplier rows: {len(product_supplier):,}")
print(f"Reorder rules: {len(reorder_rules):,}")
print(f"Inventory snapshot rows: {len(inventory_snapshots):,}")
