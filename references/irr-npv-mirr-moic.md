# IRR / NPV / MIRR / MOIC

NPV: cash_flows[0]=Period 0 not discounted (regression: [-100,60,60]@10%≈4.13). Discount_rate validated.
IRR: via calculate_irr, handles no IRR (None), multiple detection via count_sign_changes (Potential Multiple IRR Detection, not Full Solver), extreme values overflow-safe via _npv_at.
MIRR: finance_rate + reinvest_rate → verified.
MOIC = total_dist / total_equity, Payback via calculate_payback_period.
