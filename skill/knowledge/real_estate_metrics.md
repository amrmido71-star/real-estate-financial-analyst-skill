# Real Estate Development Metrics — Deep Dive

## 1. Gross Development Value (GDV)
```
GDV = Σ (Units_i × Price_i)
     = Total Sellable Area × Weighted Avg Price/SQM
```
- **Is:** Total sales value if 100% sold at current price assumptions.
- **Note:** GDV assumes full sell-out — sensitivity must test 90%, 85% sales scenarios.
- **Benchmark:** GDV/SQM varies hugely by location/segment — always compare like-for-like.

## 2. Gross Development Cost (GDC) / Total Development Cost (TDC)
```
GDC = Land + Construction + Infrastructure + Soft + S&M + Financing + Admin + Contingency + Fees/Taxes
```
- **Includes financing** (capitalized interest) — some feasibility excludes it, label clearly.
- **Cost per SQM:**
  - Cost per BUA SQM = GDC / Built-Up Area
  - Hard Cost per SQM = Construction / BUA

## 3. Development Profit & Margin
```
Development Profit = GDV − GDC
Development Margin = (GDV − GDC) / GDV × 100
Profit per SQM = (GDV−GDC) / Sellable Area
Margin on Cost = (GDV−GDC) / GDC × 100  (alternative view)
```
- **Target:** 20-30% margin on GDV (residential MENA). <15% = marginal, <10% = no-go without mitigation.
- **Margin compression drivers:** Land inflation, construction cost overrun, price discounting, slow velocity (carrying cost).

## 4. Cost Ratios
```
Land % = Land / GDC
Construction % = Construction / GDC
S&M % = (Marketing + Commission) / GDV  (or / GDC — label!)
Financing % = Financing / GDC
```
- **Use:** Diagnose cost structure — if Land >35% of GDC, land was expensive or density low.

## 5. Sales Metrics
```
Sales Rate = Units Sold / Total Units × 100
Sales Velocity = Units Sold / Months elapsed
ASP (Avg Selling Price) = Sales Value / Units Sold
Price per SQM = Sales Value / Area Sold
Booking Rate = Reservations / Inquiries (if data)
Cancellation Rate = Cancelled / Sold × 100
Collection Rate = Collected / Due × 100
```
- **Inventory Months** = Unsold Units / Avg Monthly Sales — >18 months = over-supply/slow market.

## 6. Residual Land Value (Valuation)
```
Residual Land Value = GDV − (Construction + Soft + S&M + Financing + Developer Profit + Fees)
```
- **Uses:** Bid for land — max you can pay and still hit target margin/IRR.
- **Sensitivity:** Highly sensitive to GDV assumption — test ±10%.

## 7. Break-Even Analysis
```
Break-even Sales % = GDC / GDV × 100
Break-even Sales Value = GDC  (if no target profit)
Break-even with Target Profit = (GDC + Target Profit)/GDV — or fixed costs / CM ratio for trading analysis
Break-even Price = (GDC × (1 − target margin)) / Sellable Area — simplified
Safety Margin = (GDV − GDC)/GDV  or (Actual Sales − Break-even)/Actual
```
- **Interpretation:** If Break-even >75% of GDV, low safety margin — risky.

## 8. Working Capital in Development
- **Inventory:** Unsold units at cost (not GDV) sits on balance sheet.
- **Receivables:** Installments due but not yet collected.
- **WCR peaks** around 60-80% construction before major collections/handover.

## 9. Per-Project vs Portfolio
- Portfolio GDV/GDC aggregates mask weak projects — always show project-level margin & IRR ranking.
- Concentration: if one project = >60% of portfolio GDV, flag concentration risk.

## 10. Common Errors to Avoid
- Using GDV instead of Revenue (GDV is sell-out value, Revenue is recognized portion)
- Forgetting contingency in GDC
- Mixing cash and accrual in same metric without label
- Calculating margin on cost vs on GDV interchangeably without stating
