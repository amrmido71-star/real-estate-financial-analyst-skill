# Cash Flow Methods — Real Estate Development

## 1. Cash Flow Categories

### A. Operating Cash Flow (OCF)
```
OCF = Collections (cash) − Operating Cash Outflows (S&M, G&A, Taxes paid)
```
- **Driver:** Sales & collections timing, not accounting revenue.
- **In Development:** Often negative early (spending on marketing), positive later (installments).

### B. Development / Investing Cash Flow (DCF_investing)
```
Development Outflow = Land + Construction (IPC) + Infrastructure + Soft Costs
```
- **Phasing:** Follow construction S-curve (slow → peak → taper) and land upfront.
- **Sign:** Negative (outflow).

### C. Financing Cash Flow (FCF_fin)
```
Financing CF = Debt Drawdowns + Equity Injections − Debt Repayments − Interest Paid − Dividends
```
- **Sign:** Positive when raising, negative when servicing.

### D. Net & Cumulative
```
Free Cash Flow (FCF) = OCF + Development CF  (before financing)
Net Cash Flow = FCF + Financing CF
Cumulative Cash = Opening Cash + Σ Net CF (running total)
Peak Funding Requirement = MIN(Cumulative Cash) — most negative point (absolute value needed)
```

## 2. Forecasting Methodology

### Step 1: Timeline
- Define period granularity: Monthly for construction phase (0-36 months), Quarterly thereafter.
- Anchor: Land payment at T0, construction per S-curve, sales per velocity, collections per payment plan.

### Step 2: Inflow Forecast
- **Sources:** Down payment, installments, delivery payment, mortgage disbursement, financing drawdowns.
- **Model:** Sales Velocity × Payment Plan.
  - Example: Sell 10 units/month at 6M each = 60M contracted sales/month
  - Collection: 10% down (6M immediately), 5% quarterly × 8 quarters, 50% on delivery at month 24
- **Haircut:** Apply collection efficiency (e.g., 90%) — not 100% collected on time.

### Step 3: Outflow Forecast
- **Construction:** Use S-curve: 10% Y1, 40% Y2, 35% Y3, 15% Y4 (example for 4-yr) OR monthly BOQ schedule.
- **Soft/S&M:** Front-loaded (design early, marketing at launch).
- **Financing:** Interest capitalized vs paid.

### Step 4: Net & Cumulative
- Compute period Net, then Cumulative.
- Identify peak negative and recovery month.

### Step 5: Scenario & Stress
- Delay sales 6 months, cost +15%, collection efficiency 80% — re-run peak.

## 3. Cash vs Accrual Reconciliation

| Accrual (P&L) | Cash |
|---------------|------|
| Revenue (POC) | Collections (installments) |
| COR (POC) | IPC payments to contractor |
| Profit | Net Cash Flow (different timing) |

- **Why gap?** In off-plan, cash collected often **exceeds** revenue early (customer funding), then profit catches up at handover. In delayed collections, profit > cash — liquidity risk.
- **KPIs to bridge:** Contracted vs Recognized vs Collected — show all three.

## 4. Liquidity Metrics

```
Months of Runway = Cash Balance / Average Monthly Net Outflow (burn)
Collection Efficiency = Collected / Due × 100
Overdue Receivables = Σ (Due Date < Today & Not Collected)
Peak Funding / GDV = Peak Requirement / GDV × 100  (>30% warning)
```

## 5. Financing & DSCR

```
DSCR = Operating Cash Flow (or EBITDA) / Debt Service
Debt Service = Principal Repayment + Interest
```
- Forecast DSCR per period — flag if <1.2.
- If DSCR projected <1.0, need equity injection or rescheduling.

## 6. Presentation Format

| Month | Collections | Construction | Other Outflows | Financing (Net) | Net CF | Cumulative | Notes |
|-------|-------------|--------------|----------------|-----------------|--------|------------|-------|

- Visual: Cumulative curve (hockey-stick down then up) — mark peak funding point.

## 7. Common Errors

- Forgetting land as upfront outflow (huge peak driver)
- Assuming 100% collection on due date (use efficiency & delay)
- Not linking sales velocity to collections (sell slow = collect slow)
- Ignoring interest during construction in outflows
- Double counting financing as inflow and also as revenue
- Using P&L profit as cash proxy

## 8. MENA Nuances

- Escrow regimes (UAE RERA, KSA WAFI): collections locked until construction milestones — reduces free cash availability, changes phasing.
- Customer funding is primary source in Egypt — peak funding highly sensitive to sales rate.
- FX (EGP devaluation): imported materials cost spike — include FX sensitivity.
