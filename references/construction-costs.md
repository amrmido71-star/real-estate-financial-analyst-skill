# Construction Costs

EAC = Actual + ETC, ETC via ETC calc, not double contingency via contingency_pct in assumptions.
Reconciliation: expected = budget*(1+esc)^(months/12), variance, variance_pct, status PASS if abs(actual-expected) <= max(expected*0.5%,1000).
