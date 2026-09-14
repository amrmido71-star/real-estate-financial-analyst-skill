# دليل المؤشرات المالية — Real Estate Financial Analyst Skill

> شرح كل مؤشر يحسبه الـ Skill: المعنى، المعادلة، التفسير، والـ Benchmark.

---

## 1. الربحية (Profitability)

### الإيراد (Revenue)

- **التعريف:** الإيراد المعترف به محاسبيًا (حسب POC أو التسليم). ليس هو المبيعات المتعاقد عليها ولا التحصيل النقدي.
- **المعادلة:** مجموع الإيراد المعترف به للفترة.
- **مثال:** مبيعات متعاقد عليها 100M لكن إنجاز الإنشاء 30% → إيراد معترف به 30M.
- **التمييز:** Contracted (تعاقد) vs Recognized (إيراد) vs Collected (تحصيل).

### تكلفة الإيراد (Cost of Revenue - COR)

- **تشمل:** تكلفة الأرض (مُطفأة) + تكلفة الإنشاء (حسب POC) + البنية التحتية المباشرة.
- **لا تشمل:** التسويق، المصاريف العمومية، التمويل (هذه Opex).

### إجمالي الربح (Gross Profit)

```
Gross Profit = Revenue − COR
```
- **مثال:** إيراد 64M − تكلفة 43.5M = 20.5M

### هامش الربح الإجمالي (Gross Margin)

```
Gross Margin = Gross Profit / Revenue × 100
```
- **مثال:** 20.5M / 64M = 32.0%
- **Benchmark سكني MENA:** متوسط 35%، ممتاز 45%، أقل من 20% = Watchlist
- **تحليل:** انخفاض الهامش قد يكون بسبب ارتفاع تكلفة الإنشاء أو انخفاض سعر البيع أو تغير المزيج.

### الربح التشغيلي (Operating Profit)

```
Operating Profit = Gross Profit − (S&M + G&A)
```
- **يُظهر:** ربح النشاط قبل الاستهلاك والفوائد والضرائب.

### EBITDA

```
EBITDA = Operating Profit + Depreciation + Amortization
       = EBIT + D&A
```
- **المعنى:** الربح التشغيلي النقدي قبل الاستثمار والتمويل — مقياس للقدرة التشغيلية.
- **هامش EBITDA:** EBITDA / Revenue — متوسط سكني ~25%.

### EBIT

```
EBIT = EBITDA − D&A
```

### صافي الربح (Net Profit) و الهامش الصافي (Net Margin)

```
Net Profit = EBIT − Interest − Tax
Net Margin = Net Profit / Revenue × 100
```
- **Benchmark:** متوسط 18% سكني، ممتاز 25%.
- **تحليل:** تأثره بالتمويل والضرائب — قارن EBITDA أولًا لفهم الأداء التشغيلي قبل أثر التمويل.

---

## 2. مؤشرات الاستثمار (Investment Metrics)

### ROI (Return on Investment)

```
ROI = (Gain − Cost) / Cost × 100
```
- **بسيط، لا يراعي الزمن.** للمقارنة السريعة فقط.

### IRR (Internal Rate of Return)

```
IRR = معدل الخصم الذي يجعل NPV = 0
```
- **الحساب:** تكراري (Newton-Raphson).
- **التفسير:** لو IRR = 22% و Hurdle = 18% → المشروع يتفوق بـ 4 نقاط.
- **تحذير:** IRR وحده مضلل إذا التدفقات غير نمطية — اعرض NPV معه دائمًا.
- **سنوي:** إذا التدفقات شهرية، يُحوّل: (1+monthlyIRR)^12 −1.

### NPV (Net Present Value)

```
NPV = Σ CFt / (1+r)^t − Initial
```
- **r:** معدل الخصم (WACC أو Hurdle، افتراضي 15%).
- **القرار:** NPV > 0 → يخلق قيمة. NPV < 0 → يدمر قيمة.

### ROIC

```
ROIC = NOPAT / Invested Capital × 100
NOPAT = EBIT × (1 − Tax Rate)
Invested Capital = Equity + Interest-bearing Debt
```

### Equity Multiple

```
Equity Multiple = Total Distributions / Equity Invested
```
- 1.0 = استرداد رأس المال، 2.0 = ضاعف رأس المال. لا يراعي الزمن — يُقرأ مع IRR.

### Cash-on-Cash

```
Cash-on-Cash = Annual Pre-Tax Cash Flow / Equity Invested × 100
```

### Payback Period

- **المدة لاسترداد الاستثمار.** باستخدام استيفاء خطي داخل الفترة.

---

## 3. مؤشرات التطوير العقاري (Real Estate Development)

### إجمالي قيمة التطوير (GDV)

```
GDV = Σ (Units × Selling Price)
    = Sellable Area × Weighted Avg Price/SQM
```
- **هي:** إجمالي قيمة المبيعات لو بيع 100% بالأسعار الحالية.
- **تنبيه:** تفترض بيع كامل — اختبر سيناريو 90% و 85%.

### إجمالي تكلفة التطوير (GDC)

```
GDC = Land + Construction + Infra + Soft + S&M + Financing + Admin + Contingency + Fees
```
- **تشمل:** الفوائد المرسملة. وضّح إذا مستبعدة.

### ربح التطوير و هامشه

```
Profit = GDV − GDC
Development Margin = (GDV − GDC) / GDV × 100
Margin on Cost = (GDV − GDC) / GDC × 100
Profit per SQM = (GDV−GDC) / Sellable Area
```
- **Target:** 20-30% على GDV. أقل من 15% هامشي، أقل من 10% لا يُنصح إلا بمعالجة.

### التكلفة لكل متر (Cost per SQM)

```
Cost per BUA SQM = GDC / BUA
Cost per Sellable SQM = GDC / Sellable Area
Price per SQM = GDV / Sellable Area
```

### نسب التكلفة

```
Land % = Land / GDC × 100  (Typical 15-30%)
Construction % = Construction / GDC × 100 (Typical 40-65%)
```

### Residual Land Value

```
Residual Land Value = GDV − (Construction + Soft + S&M + Financing + Profit Target + Fees)
```
- **الاستخدام:** أقصى سعر للأرض مع تحقيق هامش مستهدف.

### Break-even

```
Break-even Sales % = GDC / GDV × 100
Break-even Price = GDC / Sellable Area (مبسط)
Break-even with Margin = GDC / ((1−Margin) × Area)
Safety Margin = (GDV − Break-even) / GDV × 100
```
- **تفسير:** لو Break-even = 71% → يمكن تحمل عدم بيع 29% قبل الخسارة. أقل من 70% صحي.

---

## 4. المبيعات (Sales Metrics)

| المؤشر | المعادلة | الصحي |
|--------|----------|-------|
| Sales Value | مجموع قيمة العقود | — |
| Units Sold / Available | Sold / Total | — |
| Sales Rate | Sold / Total ×100 | — |
| Velocity | Units Sold / Months | — |
| ASP | Sales Value / Units Sold | — |
| Price/SQM | Sales Value / Area Sold | — |
| Cancellation Rate | Cancelled / Sold ×100 | <5% صحي |
| Inventory Months | Unsold / Avg Monthly Sales | <18 شهر صحي |

---

## 5. التحصيل (Collection Metrics)

| المؤشر | المعادلة | الصحي |
|--------|----------|-------|
| Contracted Sales | مجموع العقود الموقعة | — |
| Collected Cash | النقد المحصل | — |
| Outstanding | Contracted − Collected | — |
| Collection Efficiency | Collected / Due ×100 | >90% ممتاز، <85% تحذير |
| Aging Buckets | 0-30, 31-60, 61-90, 91-180, 180+ | >90 يوم >20% = خطر |
| Overdue Ratio | Overdue >90d / Total Receivables | <20% |

---

## 6. التدفقات النقدية (Cash Flow)

| المؤشر | المعادلة |
|--------|----------|
| Operating CF | Collections − Operating Outflows |
| Development CF | Land + Construction + Soft (outflows) |
| Financing CF | Drawdowns − Repayments − Interest |
| Free CF | Operating + Development |
| Net CF | Free + Financing |
| Cumulative | Opening + Σ Net CF |
| Peak Funding | MIN(Cumulative) — أقصى احتياج تمويلي |
| Runway | Cash / Avg Monthly Burn |
| DSCR | Operating CF / Debt Service |

---

## 7. رأس المال العامل (Working Capital)

```
WCR = Receivables + Inventory (Unsold at Cost) − Payables
```

---

## 8. كيف تقرأ المؤشرات معًا (مثال)

> **Gross Margin 32%** (أقل من Budget 35%) + **COR +11.5% Unfavorable** → السبب تكلفة الإنشاء.
> **Net Margin 10.9%** (أقل من Benchmark 18%) → الربحية ضعيفة حتى بعد التمويل.
> **Collection Efficiency 86%** + **Peak Funding -77M أعمق من الخطة** → ضغط سيولة رغم ربحية دفترية.
> **Development Margin 28.6%** + **IRR 18.2%** (فقط يلامس Hurdle) + **Break-even 71%** → المشروع مجدٍ لكن هامش الأمان ضيق — أي انخفاض سعر 5% يهبط IRR دون Hurdle.

---

## 9. المراجع

- `skill/config/industry_benchmarks.yaml` — أرقام Benchmark حسب القطاع
- `skill/knowledge/financial_metrics.md` — تعاريف تفصيلية إنجليزية
- `skill/knowledge/real_estate_metrics.md` — مؤشرات عقارية تفصيلية
- `skill/knowledge/valuation_methods.md` — طرق التقييم
