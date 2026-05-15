"""
generate_data.py — Synthetic Sales Data Generator
Sales Performance Dashboard | Project 01
Generates ~12,000 rows of realistic retail sales data with intentional quality issues.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# ── Configuration ──
NUM_ROWS = 12000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

REGIONS = ["Northeast", "Southeast", "Midwest", "West", "Southwest"]
REGION_WEIGHTS = [0.25, 0.20, 0.20, 0.22, 0.13]

CATEGORIES = {
    "Electronics":    {"price_range": (49.99, 999.99), "margin_range": (0.08, 0.25)},
    "Apparel":        {"price_range": (14.99, 199.99), "margin_range": (0.35, 0.60)},
    "Home & Garden":  {"price_range": (9.99, 499.99),  "margin_range": (0.25, 0.45)},
    "Sports":         {"price_range": (19.99, 349.99), "margin_range": (0.20, 0.40)},
    "Office Supplies": {"price_range": (4.99, 149.99), "margin_range": (0.30, 0.55)},
}

PRODUCTS = {
    "Electronics":     ["Wireless Headphones", "Bluetooth Speaker", "Tablet", "Smart Watch", "Webcam", "Portable Charger"],
    "Apparel":         ["Running Shoes", "Winter Jacket", "Polo Shirt", "Joggers", "Baseball Cap", "Sunglasses"],
    "Home & Garden":   ["Air Purifier", "Plant Pot Set", "LED Desk Lamp", "Throw Blanket", "Tool Kit", "Candle Set"],
    "Sports":          ["Yoga Mat", "Dumbbells", "Resistance Bands", "Jump Rope", "Foam Roller", "Water Bottle"],
    "Office Supplies": ["Notebook Set", "Ergonomic Mouse", "Desk Organizer", "Whiteboard", "Planner", "Pen Set"],
}

CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Small Business"]
SEGMENT_WEIGHTS = [0.50, 0.30, 0.20]

SALES_REPS = [
    "Marcus Thompson", "Priya Sharma", "James O'Brien", "Sofia Rodriguez",
    "David Kim", "Aisha Patel", "Ryan Mitchell", "Chen Wei",
    "Olivia Foster", "Kwame Asante", "Emily Nakamura", "Carlos Mendez",
]

# Assign reps to regions
REP_REGIONS = {}
reps_per_region = len(SALES_REPS) // len(REGIONS)
for i, rep in enumerate(SALES_REPS):
    region_idx = min(i // reps_per_region, len(REGIONS) - 1)
    REP_REGIONS[rep] = REGIONS[region_idx]

# ── Seasonality multipliers (by month) ──
SEASONALITY = {
    1: 0.85, 2: 0.80, 3: 0.90, 4: 0.95, 5: 1.00, 6: 1.05,
    7: 1.00, 8: 0.95, 9: 1.05, 10: 1.10, 11: 1.30, 12: 1.45
}


def generate_dates(n):
    total_days = (END_DATE - START_DATE).days
    dates = []
    for _ in range(n):
        month = np.random.choice(range(1, 13), p=[
            s / sum(SEASONALITY.values()) for s in SEASONALITY.values()
        ])
        day = random.randint(1, 28)
        dates.append(datetime(2025, month, day))
    return dates


def generate_sales_data(n):
    dates = generate_dates(n)
    rows = []

    for i in range(n):
        order_id = f"ORD-{100000 + i}"
        date = dates[i]
        region = np.random.choice(REGIONS, p=REGION_WEIGHTS)
        category = random.choice(list(CATEGORIES.keys()))
        product = random.choice(PRODUCTS[category])

        # Pick a rep from this region (or random if mismatch — adds realism)
        region_reps = [r for r, reg in REP_REGIONS.items() if reg == region]
        if region_reps:
            sales_rep = random.choice(region_reps)
        else:
            sales_rep = random.choice(SALES_REPS)

        customer_segment = np.random.choice(CUSTOMER_SEGMENTS, p=SEGMENT_WEIGHTS)

        price_lo, price_hi = CATEGORIES[category]["price_range"]
        unit_price = round(np.random.uniform(price_lo, price_hi), 2)

        # Units: Corporate buys more
        if customer_segment == "Corporate":
            units = np.random.choice(range(1, 25), p=np.array([max(0.01, 0.30 - 0.012 * x) for x in range(24)]) / sum([max(0.01, 0.30 - 0.012 * x) for x in range(24)]))
        elif customer_segment == "Small Business":
            units = random.randint(1, 10)
        else:
            units = random.randint(1, 5)

        # Discount logic
        if customer_segment == "Corporate":
            discount = round(np.random.choice([0, 0.05, 0.10, 0.15, 0.20], p=[0.20, 0.25, 0.30, 0.15, 0.10]), 2)
        elif customer_segment == "Small Business":
            discount = round(np.random.choice([0, 0.05, 0.10], p=[0.40, 0.35, 0.25]), 2)
        else:
            discount = round(np.random.choice([0, 0.05, 0.10, 0.15], p=[0.50, 0.25, 0.15, 0.10]), 2)

        revenue = round(unit_price * units * (1 - discount), 2)

        margin_lo, margin_hi = CATEGORIES[category]["margin_range"]
        cost_pct = 1 - np.random.uniform(margin_lo, margin_hi)
        cogs = round(unit_price * units * cost_pct, 2)

        # Monthly target per rep (~$40K/month baseline, adjusted by seasonality)
        target = round(40000 * SEASONALITY[date.month] / 30, 2)

        rows.append({
            "order_id": order_id,
            "order_date": date.strftime("%Y-%m-%d"),
            "region": region,
            "sales_rep": sales_rep,
            "customer_segment": customer_segment,
            "product_category": category,
            "product_name": product,
            "unit_price": unit_price,
            "units_sold": int(units),
            "discount_pct": discount,
            "revenue": revenue,
            "cogs": cogs,
            "daily_target": target,
        })

    return pd.DataFrame(rows)


def inject_data_quality_issues(df):
    """Inject realistic messiness for the cleaning notebook to address."""
    df = df.copy()
    n = len(df)
    rng = np.random.default_rng(42)

    # 1. ~2% missing revenue values
    missing_rev = rng.choice(n, size=int(n * 0.02), replace=False)
    df.loc[missing_rev, "revenue"] = np.nan

    # 2. ~1.5% missing region
    missing_region = rng.choice(n, size=int(n * 0.015), replace=False)
    df.loc[missing_region, "region"] = np.nan

    # 3. ~1% missing sales_rep
    missing_rep = rng.choice(n, size=int(n * 0.01), replace=False)
    df.loc[missing_rep, "sales_rep"] = np.nan

    # 4. ~80 duplicate rows
    dup_indices = rng.choice(n, size=80, replace=False)
    duplicates = df.iloc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    # 5. ~0.5% negative revenue (data entry errors)
    neg_rev = rng.choice(len(df), size=int(len(df) * 0.005), replace=False)
    df.loc[neg_rev, "revenue"] = df.loc[neg_rev, "revenue"].apply(
        lambda x: -abs(x) if pd.notna(x) else x
    )

    # 6. Inconsistent region casing (~1%)
    case_issues = rng.choice(len(df), size=int(len(df) * 0.01), replace=False)
    for idx in case_issues:
        if pd.notna(df.loc[idx, "region"]):
            df.loc[idx, "region"] = df.loc[idx, "region"].upper()

    # 7. A few outlier unit prices (10x normal — fat finger errors)
    outlier_idx = rng.choice(len(df), size=8, replace=False)
    df.loc[outlier_idx, "unit_price"] = df.loc[outlier_idx, "unit_price"] * 10

    # 8. Some dates as different format (~0.5%)
    fmt_issues = rng.choice(len(df), size=int(len(df) * 0.005), replace=False)
    for idx in fmt_issues:
        if pd.notna(df.loc[idx, "order_date"]):
            d = datetime.strptime(df.loc[idx, "order_date"], "%Y-%m-%d")
            df.loc[idx, "order_date"] = d.strftime("%m/%d/%Y")

    # 9. Whitespace in some product names
    ws_issues = rng.choice(len(df), size=int(len(df) * 0.008), replace=False)
    for idx in ws_issues:
        df.loc[idx, "product_name"] = "  " + df.loc[idx, "product_name"] + "  "

    # Shuffle the dataframe
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    return df


def main():
    print("Generating synthetic sales data...")
    df = generate_sales_data(NUM_ROWS)

    print(f"  Clean rows: {len(df)}")
    df = inject_data_quality_issues(df)
    print(f"  After injecting issues: {len(df)} rows")

    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/sales_data_raw.csv"
    df.to_csv(output_path, index=False)
    print(f"  Saved to {output_path}")

    # Quick summary
    print("\n── Data Summary ──")
    print(f"  Date range: 2025-01-01 to 2025-12-31")
    print(f"  Regions: {len(REGIONS)}")
    print(f"  Sales Reps: {len(SALES_REPS)}")
    print(f"  Product Categories: {len(CATEGORIES)}")
    print(f"  Products: {sum(len(v) for v in PRODUCTS.values())}")
    print(f"  Customer Segments: {len(CUSTOMER_SEGMENTS)}")
    print(f"\n  Quality issues injected:")
    print(f"    - ~240 missing revenue values")
    print(f"    - ~180 missing regions")
    print(f"    - ~120 missing sales reps")
    print(f"    - ~80 duplicate rows")
    print(f"    - ~60 negative revenue entries")
    print(f"    - ~120 inconsistent region casing")
    print(f"    - 8 outlier unit prices (10x)")
    print(f"    - ~60 inconsistent date formats")
    print(f"    - ~96 whitespace in product names")


if __name__ == "__main__":
    main()
