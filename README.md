# Sales Performance Dashboard

An end-to-end data analytics project analysing 12,000+ retail sales transactions across 2025 — from raw data generation through Python cleaning and EDA to an interactive Tableau Public dashboard.

**[View Live Dashboard →](https://public.tableau.com/views/SALESPERFORMANCEDASHBOARD-2025/Dashboard1ExecutiveSummary?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link
)**

---

## Project Overview

This project simulates a real-world analyst workflow: starting from a messy raw dataset, applying systematic data cleaning, conducting exploratory analysis to surface business insights, and delivering an interactive dashboard built for executive and operational audiences.

| | |
|---|---|
| **Tools** | Python, Pandas, NumPy, Matplotlib, Seaborn, Tableau Public |
| **Dataset** | 12,000+ synthetic retail sales rows, 2025 full year |
| **Dimensions** | 5 regions · 12 sales reps · 5 product categories · 3 customer segments |
| **Skills demonstrated** | Data cleaning, EDA, feature engineering, data visualisation, dashboard design |

---

## Dashboard Preview

### Executive Summary
![Executive Summary](dashboard/screenshots/screenshot_01_executive_summary.png)

### Product Performance
![Product Performance](dashboard/screenshots/screenshot_02_product_performance.png)

### Sales Rep Scorecard
![Rep Scorecard](dashboard/screenshots/screenshot_03_rep_scorecard.png)

### Filtered View — Northeast, Q4
![Filtered View](dashboard/screenshots/screenshot_04_filtered_view.png)

---

## Key Findings

1. **Q4 seasonality is the dominant revenue driver** — November and December alone account for ~28% of annual revenue, creating a predictable but concentrated risk if Q4 performance misses.

2. **Electronics leads in revenue, Apparel leads in margin** — Electronics drives the highest order volume but operates at thin margins (~15–20%). Apparel generates fewer orders at significantly higher margins (~45–55%), making it the most profitable category per dollar of revenue.

3. **Corporate segment punches above its weight** — Corporate accounts for ~30% of orders but generates disproportionately high revenue per order due to larger basket sizes and multi-unit purchases, despite receiving the deepest discounts.

4. **Significant rep performance disparity** — The gap between the top and bottom performing sales rep exceeds 60% in annual revenue, suggesting a coaching and territory optimisation opportunity rather than a market-level issue.

5. **Discounting erodes margin predictably** — Correlation analysis confirms a negative relationship between discount rate and gross margin. Orders with 15–20% discounts average 8–12 percentage points lower margin than undiscounted orders in the same category.

---

## Data Pipeline

```
generate_data.py          notebooks/01_data_cleaning.ipynb
Raw CSV (12,080 rows)  →  Cleaned CSV (12,000 rows)  →  EDA + KPI Summary  →  Tableau Dashboard
     ↓                           ↓                            ↓
  9 quality              Nulls, duplicates,           5 core KPIs,
  issues injected        outliers resolved            7 visual insights
```

---

## Repository Structure

```
sales-performance-dashboard/
│
├── README.md
│
├── data/
│   ├── raw/
│   │   └── sales_data_raw.csv
│   └── cleaned/
│       ├── sales_data_cleaned.csv
│       └── metrics_summary.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   └── 02_exploratory_analysis.ipynb
│
├── scripts/
│   └── generate_data.py
│
└── dashboard/
    └── screenshots/
        ├── screenshot_01_executive_summary.png
        ├── screenshot_02_product_performance.png
        ├── screenshot_03_rep_scorecard.png
        └── screenshot_04_filtered_view.png
```

---

## How to Reproduce

### 1. Clone the repository
```bash
git clone https://github.com/Ebi-dot- bit/sales-performance-dashboard.git
cd sales-performance-dashboard
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn
```

### 3. Generate the raw data
```bash
python scripts/generate_data.py
```

### 4. Run the notebooks in order
```bash
jupyter notebook
```
Open and run:
- `notebooks/01_data_cleaning.ipynb`
- `notebooks/02_exploratory_analysis.ipynb`

### 5. View the dashboard
Open the [live Tableau Public dashboard](https://public.tableau.com/app/profile/YOUR_PROFILE/viz/SalesPerformanceDashboard2025) in any browser — no software required.

---

## Notebook Highlights

### 01 — Data Cleaning

| Issue | Count | Treatment |
|-------|-------|-----------|
| Missing revenue values | ~240 | Recalculated from `unit_price × units_sold × (1 − discount)` |
| Missing region | ~180 | Inferred from sales rep's assigned region |
| Duplicate rows | ~80 | Removed via `order_id` deduplication |
| Negative revenue | ~60 | Recalculated from components (sign error) |
| Mixed date formats | ~60 | Unified with `pd.to_datetime(format='mixed')` |
| Inconsistent casing | ~120 | Standardised to title case |
| Outlier unit prices | 8 | Capped at 2× the 99th percentile per category |
| Whitespace in strings | ~96 | Stripped across all string columns |
| Missing sales rep | ~120 | Flagged as "Unknown" |

12 new features engineered including `gross_profit`, `gross_margin_pct`, `order_tier`, `margin_health`, and time-based dimensions.

### 02 — Exploratory Analysis
7 analysis sections covering revenue distribution, time series, regional performance, category analysis, rep performance, customer segments, and correlation analysis.

---

## Dashboard Features

- **3 interactive pages** — Executive Summary, Product Performance, Sales Rep Scorecard
- **4 global filters** — Date range, Region, Product Category, Customer Segment
- **Click-to-filter actions** — clicking a category or rep filters all related charts
- **Calculated fields** — MoM growth %, YTD running total, target achievement %, margin health labels
- **Colour-coded performance** — green/red encoding for above/below target throughout

---

## Skills Demonstrated

| Skill | Where |
|-------|-------|
| Python / Pandas | Data cleaning notebook — null handling, deduplication, type conversion, feature engineering |
| Data profiling | Systematic quality audit before any transformation |
| Exploratory analysis | Statistical summary, distributions, correlations |
| Data visualisation | Matplotlib + Seaborn, 7 publication-quality charts |
| Dashboard design | Tableau Public — 3-page dashboard, 8 chart types, interactive filters |
| Calculated fields | LOD expressions, table calculations, time intelligence |
| Version control | GitHub — structured repo, documented commits |
| Analytical communication | Findings written as business insights, not data descriptions |

---

## About

Built as Project 1 of a 90-day data analytics portfolio roadmap.
Connect on [LinkedIn](https://linkedin.com/in/onah-ebinum-9091a71a5) · [Tableau Public](https://public.tableau.com/app/profile/ebinum.onah/vizzes)
