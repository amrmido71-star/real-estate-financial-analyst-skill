# Valuation Methods for Real Estate Development

## 1. Discounted Cash Flow (DCF) — Primary Method

**Use:** Development project valuation, feasibility, investment decision.

```
NPV = Σ [CF_t / (1+r)^t] − Initial Investment
IRR = r where NPV = 0
```
- **Cash flows:** Levered vs Unlevered — label clearly.
  - Project (Unlevered): before financing (shows project quality)
  - Equity (Levered): after debt service (shows equity return)
- **Discount rate (r):** WACC, hurdle rate, or cost of equity depending on cash flow type. For development, often 14-18% (MENA) reflecting risk.
- **Period:** Monthly for <2yr, Quarterly/Yearly for longer. Annualize IRR if monthly.
- **Decision:** NPV >0 => creates value at given r. IRR > hurdle => attractive. Both, not just IRR.

**Pros:** Captures time value, phasing.
**Cons:** Sensitive to assumptions; garbage in = garbage out.

## 2. Residual Method (Land Valuation)

**Use:** What to pay for land.

```
Land Value = GDV − (Construction + Professional Fees + S&M + Financing + Developer Profit + Contingency + Acquisition Costs)
Developer Profit often 15-20% of GDV or target IRR — explicit.
```

**Steps:**
1. Estimate GDV (via comps or price/SQM)
2. Estimate all costs (with contingency)
3. Deduct required developer profit (e.g., 20% of GDV)
4. Remainder = maximum land bid

**Sensitivity:** Test GDV ±10%, Cost ±15% — land value swings dramatically.

## 3. Comparable Method (Market Approach)

**Use:** GDV estimation, price benchmarking, exit value.

```
Value = Comparable Price/SQM × Subject Area × Adjustments
Adjustments: location, finish, view, floor, age, amenities ±%
```

**Source:** Recent transactions (3-6 months), same micro-market, similar product.
**Caution:** In fast-moving markets, comps lag. In illiquid markets, few comps — widen sensitivity.

## 4. Income Capitalization (For Rental / Stabilized Assets)

**Use:** Commercial, retail, hospitality after stabilization — less common for pure development sell-out but useful for retained assets.

```
Value = NOI / Cap Rate
NOI = Rental Income − Operating Expenses (excl. financing & tax)
Cap Rate = market yield (e.g., 8-9% retail, 9-11% office MENA)
```

**For Development:** Can value retained rental component at exit (e.g., mall within mixed-use).

## 5. Cost Approach

**Use:** Rare for development — replacement cost.

```
Value = Land Value + Depreciated Construction Cost
```
- Upper bound; useful to sanity-check DCF.

## 6. Choosing Method

| Situation | Primary | Cross-Check |
|-----------|---------|-------------|
| Development sell-out project | DCF (Project IRR/NPV) | Residual + Comps for GDV |
| Land bidding | Residual | Comps |
| Price setting | Comps | DCF (what price needed for hurdle IRR?) |
| Retained income asset | Income Cap | DCF |
| Portfolio valuation | Sum of DCFs | Market comps |

## 7. Common Valuation Errors

- Using project IRR without NPV
- Discounting levered cash flows at WACC (should be cost of equity)
- Forgetting to include financing costs in GDC but also counting debt separately (double count)
- Using nominal vs real cash flows inconsistently with discount rate
- Ignoring tax (or applying incorrectly)
- Not annualizing monthly IRR

## 8. Board Presentation Tips

- Always show **range**, not point estimate: Base NPV ± scenarios
- Show **hurdle vs IRR** visually
- Show **break-even price** — "Price can fall X% before NPV hits zero"
- State key assumptions table (Price/SQM, Cost/SQM, Sales velocity, Discount rate)
