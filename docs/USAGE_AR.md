# دليل الاستخدام — Real Estate Financial Analyst Skill

---

## 1. نظرة عامة

الـ Skill يحول أي AI Agent إلى محلل مالي Senior. هذا الدليل يشرح كل طرق الاستخدام.

---

## 2. طرق الاستخدام

### أ. التحليل المالي الشامل (Monthly Financial Analysis)

**متى:** شهريًا — لإعداد حزمة التقارير للإدارة.

**المدخلات:**
- Trial Balance أو P&L + BS + Cash Flow (Excel/CSV)
- تقرير المبيعات والتحصيلات
- الموازنة (Budget)

**Prompt مثال:**

> "هذه القوائم المالية لشهر يونيو 2025 + الموازنة. حلّل الأداء المالي، احسب Gross Margin و EBITDA و Net Margin، قارن Budget vs Actual، وحدد الانحرافات الجوهرية مع تفسير الأسباب والتوصيات. أخرج Executive Summary صفحة واحدة + تقرير تفصيلي."

**المخرجات:**
- Executive Summary (Health Rating + Top Findings + Risks + Recommendations)
- Detailed Analysis (P&L table + Margins + Vertical/Horizontal)
- Variance Report
- KPI Dashboard

**الـ Workflow:** `skill/workflows/monthly_financial_analysis.md`
**الـ Prompt:** `skill/prompts/financial_analysis_prompt.md`
**القالب:** `skill/templates/financial_analysis_report.md`

---

### ب. تحليل المشروع العقاري (Project Feasibility)

**متى:** عند تقييم مشروع جديد أو إعادة توقع ربع سنوي.

**المدخلات (14 مجموعة):**
- Land Cost, Construction, Infra, Design, Consultancy, Marketing, Commission, Financing, Admin, Contingency, Taxes
- Unit Mix (النوع، العدد، المساحة، السعر)
- Selling Price / Price per SQM
- Sales Schedule, Collection Schedule, Construction Schedule

**Prompt مثال:**

> "حلّل مشروع Green Valley: أرض 260M، إنشاء 620M، بنية تحتية 65M، سوفت 75M، تسويق 61M، تمويل 85M، إدارة 30M، طوارئ 31M، رسوم 22M. المساحة البيعية 62,000م، BUA 82,000م، 500 وحدة، GDV 1,750M. احسب التكلفة الإجمالية، هامش التطوير، IRR و NPV، Break-even، Peak Funding، ثم اعمل سيناريوهات Base/Best/Worst وحساسية."

**المخرجات:**
- GDV, GDC, Profit, Margin, Profit/SQM, Cost Ratios
- Project IRR, NPV, Equity IRR, Equity Multiple, Payback
- Break-even Sales & Price
- Scenario Comparison Table
- Sensitivity Tornado
- Risk Matrix
- Go/No-Go Recommendation

**الـ Workflow:** `skill/workflows/project_financial_analysis.md`
**القالب:** `skill/templates/project_analysis_report.md`

---

### ج. Budget vs Actual

**Prompt مثال:**

> "الموازنة للإنشاءات 100M والفعلي 112M. احسب Absolute Variance و Percentage Variance وصنّفها Favorable/Unfavorable/Neutral وفسّر الأسباب المحتملة وأعط توصية."

**المنطق:**

```
Variance = Actual − Budget = +12M
Variance % = 12M / 100M = +12%
Classification: Unfavorable (cost overrun)
Drivers: BOQ quantity +6%, steel price +4%, scope +2%
Recommendation: راجع BOQ، ثبّت سعر الحديد، ارفع Contingency لـ 7%
```

**الـ Workflow:** `skill/workflows/budget_vs_actual.md`
**القالب:** `skill/templates/variance_report.md`

---

### د. التدفقات النقدية (Cash Flow Forecast)

**Prompt مثال:**

> "هذه التدفقات النقدية المتوقعة لـ 15 شهرًا + الرصيد الافتتاحي. احسب Cumulative و Peak Funding Requirement و Runway و DSCR، وحلل Collection Efficiency، واعمل Stress Test لو تأخرت التحصيلات شهرين."

**المخرجات:**
- Monthly Net vs Cumulative
- Peak Funding (المبلغ والتوقيت)
- Collection vs Revenue Bridge
- Stress Scenarios

**الـ Workflow:** `skill/workflows/cashflow_forecast.md`

---

### هـ. تحليل الاستثمار (Investment Memo)

**Prompt مثال:**

> "عندي تدفقات نقدية للمشروع: [-420M, -380M, 150M, 680M, 471M] و Hurdle 18%. احسب Project IRR و NPV عند 15% و Equity IRR و Multiple، وقارن بالـ Hurdle، واعمل سيناريوهات وحساسية، وأعطني Investment Memo من صفحتين مع توصية Go/No-Go."

**القالب:** `skill/templates/investment_memo.md`

---

### و. الإدارة (Management Reporting)

**Prompt مثال:**

> "أعطني Executive Summary للإدارة عن أداء الشركة هذا الربع — Health Rating، أهم 3 نتائج، أهم 3 مخاطر، وأهم 3 توصيات عملية بمسؤول وجدول زمني."

**القالب:** `skill/templates/executive_summary.md`
**الـ Workflow:** `skill/workflows/management_reporting.md`

---

## 3. أنواع البيانات المقبولة

| النوع | الصيغ | أمثلة |
|-------|-------|--------|
| قوائم مالية | Excel, CSV, Trial Balance (+ PDF قراءة يدوية) | P&L, BS, Cash Flow |
| موازنات | Excel, CSV | Annual Budget, Cost Budget |
| تدفقات | Excel, CSV | Cash Flow Forecast |
| مبيعات | Excel, CSV | Sales Register, Reservation Report |
| تحصيلات | Excel, CSV | Collection Report, Aging |
| مخزون | Excel, CSV | Unit Inventory (Available/Sold) |
| تكاليف | Excel, CSV (+ PDF قراءة يدوية) | BOQ, Cost Report, IPC |
| إدارة | PDF, Excel, MD | Board Pack |

> **ملاحظة PDF:** استيراد Excel/CSV تلقائي عبر `data_loader.py` (production-ready). أما PDF فيُقرأ عبر قدرات الـ Agent (manual extraction) — التحليل التلقائي الكامل لـ PDF في الـ Roadmap (v1.2).

---

## 4. كيف يفكر الـ Agent (مهم)

الـ Agent يتبع هذا التسلسل دائمًا:

```
1. Understand Data — ما الفترة؟ ما العملة؟ accrual أم cash؟
2. Validate Data — فحص جودة البيانات
3. Identify Missing — ما الناقص؟ لا يخترع
4. Calculate Metrics — بالمعادلات الصحيحة
5. Compare — YoY / Budget / Benchmark
6. Identify Variances — Absolute & %
7. Identify Drivers — Volume/Price/Mix/Timing
8. Assess Risks — مصفوفة المخاطر
9. Generate Scenarios — Base/Best/Worst + Sensitivity
10. Provide Recommendations — عملية ومحددة
```

---

## 5. أمثلة Prompts إضافية (جاهزة للنسخ)

```
هل المشروع مربح؟ وما هامش التطوير؟

هل الـ IRR مقبول مقارنة بـ Hurdle 18%؟

ما حجم التمويل المطلوب (Peak Funding) ومتى؟

متى يصل المشروع إلى نقطة التعادل (Break-even)؟

ما أهم المخاطر؟

ماذا يحدث لو انخفضت أسعار البيع 10%؟

ماذا يحدث لو زادت تكلفة الإنشاء 15%؟

ما المشروع الأفضل من بين المشروعين A و B؟

لماذا انخفض الـ Margin من 35% إلى 31%؟

هل التدفقات النقدية كافية؟

هل التحصيلات تسير وفق الخطة؟

ما حجم الـ Receivables المتأخرة؟

هل هناك مشكلة سيولة؟

قارن أداء 3 مشاريع من حيث Margin و IRR و Peak Funding.

أعطني Variance Analysis مفصلة لكل بند.

أعطني Risk Assessment كامل مع Early Warning Indicators.
```

---

## 6. استخدام Python مباشر (بدون Agent)

```python
# تحليل مشروع كامل
from skill.tools.project_metrics import *
from skill.tools.investment_metrics import *
from skill.tools.cashflow_analysis import *
from skill.tools.scenario_analysis import *

# 1. المشروع
gdv = 1_750_500_000
gdc = 1_249_267_500
print(f"Margin: {calculate_development_margin(gdv, gdc):.1f}%")
print(f"Break-even: {calculate_break_even_pct(gdc, gdv):.1f}%")

# 2. الاستثمار
cfs = [-420_000_000, -380_000_000, 150_000_000, 680_000_000, 471_232_500]
print(f"IRR: {calculate_irr(cfs)*100:.1f}%")
print(f"NPV: {calculate_npv(cfs, 0.15):,.0f}")

# 3. السيناريوهات
base = {"gdv": gdv, "gdc": gdc, "cash_flows": cfs, "discount_rate": 0.15}
scenarios = run_scenarios(base, {"gdv": 1.08, "gdc": 0.93}, {"gdv": 0.90, "gdc": 1.15})
print(scenarios)

# 4. الحساسية
sens = run_sensitivity_analysis(base, "gdv", [-10, -5, 0, 5, 10])
for r in sens:
    print(f"{r['change_pct']:+.0f}% => Margin {r['margin_pct']:.1f}% IRR {r['irr_pct']:.1f}%")

# 5. التدفق النقدي
inflows = [58_000_000, 12_000_000, 45_000_000]
outflows = [34_500_000, 36_500_000, 44_300_000]
analysis = analyze_cashflow(inflows, outflows, opening_cash=0)
print(f"Peak: {analysis['peak_funding']}")
```

---

## 7. إعدادات الشركة

عدّل `skill/config/settings.yaml`:

```yaml
company:
  default_currency: "EGP"  # غيّر لـ SAR / AED / USD
  vat_rate: 0.14
  tax_rate: 0.225

thresholds:
  irr_hurdle_rate: 18.0
  variance_neutral_pct: 2.0
```

و `skill/config/industry_benchmarks.yaml` لمعايير السوق المحلي.

---

## 8. اللغة

- الـ Skill يرد بنفس لغة المستخدم تلقائيًا.
- إذا كتبت عربي → يرد عربي (مع المصطلحات الإنجليزية بين قوسين).
- إذا كتبت إنجليزي → يرد إنجليزي.

---

## 9. نصائح

- لا ترفع بيانات شركة حقيقية حساسة بدون إخفاء الأسماء.
- إذا كانت البيانات ناقصة، الـ Agent سيقول بوضوح ما الناقص — لا تجبره على الاختراع.
- اطلب دائمًا `Assumptions & Limitations` في نهاية التقرير.
- استخدم القوالب الجاهزة (`skill/templates/`) لضمان تناسق التقارير.

---

*المزيد: `docs/FINANCIAL_METRICS_AR.md` لشرح كل مؤشر، `docs/WORKFLOWS_AR.md` لتفاصيل الـ Workflows.*
