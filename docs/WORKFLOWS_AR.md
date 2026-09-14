# دليل الـ Workflows — Real Estate Financial Analyst Skill

> 6 Workflows احترافية تغطي كل احتياجات التحليل المالي العقاري. كل Workflow له Inputs → Steps → Outputs → Templates.

---

## 1. التحليل المالي الشهري (Monthly Financial Analysis)

**الملف:** `skill/workflows/monthly_financial_analysis.md`

**الهدف:** حزمة تقارير شهرية للإدارة (FP&A Pack).

**التكرار:** شهري

**المدخلات:**
- Trial Balance / P&L / BS / Cash Flow
- تقرير المبيعات والتحصيلات
- الموازنة

**الخطوات (9 خطوات):**

1. استيراد البيانات والتحقق من الفترة والعملة
2. فحص جودة البيانات (data_validation)
3. حساب الربحية: Revenue → Gross → EBITDA → Net + Margins
4. تحليل رأسي (Vertical) وأفقي (Horizontal) + مقارنة Benchmark
5. تحليل المبيعات والتحصيلات (Contracted vs Recognized vs Collected)
6. Budget vs Actual (Absolute + % + Classification)
7. تحليل التدفقات والسيولة (Peak Funding, Runway, DSCR)
8. مسح المخاطر (10 مخاطر)
9. إعداد Executive Summary

**المخرجات:**
- Executive Summary (1 صفحة)
- Detailed Financial Analysis Report
- Variance Report
- KPI Dashboard

**القوالب:**
- `templates/executive_summary.md`
- `templates/financial_analysis_report.md`
- `templates/variance_report.md`

**الأدوات:**
```python
from skill.tools.financial_calculations import calculate_gross_margin, calculate_variance
from skill.tools.data_validation import validate_financials
```

---

## 2. تحليل المشروع العقاري (Project Financial Analysis)

**الملف:** `skill/workflows/project_financial_analysis.md`

**الهدف:** دراسة جدوى كاملة لمشروع واحد.

**متى:** تقييم مشروع جديد / إعادة توقع ربع سنوي / لجنة استثمار.

**المدخلات (14 مجموعة):**

| المجموعة | الحقول |
|----------|--------|
| Land | التكلفة، المساحة، تاريخ الشراء |
| Construction | التكلفة الإجمالية أو per SQM، الجدولة |
| Infra / Soft | Design, Consultancy, PM |
| S&M | Marketing, Commission % |
| Financing | نسبة الدين، الفائدة، الرسوم |
| Contingency | نسبة أو مبلغ |
| Unit Mix | النوع، العدد، المساحة، السعر |
| Schedules | Sales Schedule, Collection Plan, Construction S-curve |

**الخطوات (11 خطوة):**

1. تعريف المشروع (الاسم، الموقع، النوع، الحجم، الجدول، العملة)
2. استيراد البيانات والتحقق
3. بناء GDV (Σ Units × Price) ومقارنة بالسوق
4. بناء GDC (مجموع التكاليف) ونسب التكلفة ومقارنة Benchmark
5. حساب الربحية: Profit, Margin, Profit/SQM, Margin on Cost
6. بناء التدفقات الشهرية وحساب IRR, NPV, Equity IRR, Multiple, Payback
7. Break-even (Sales Value, %, Price)
8. السيناريوهات (Base / Best / Worst)
9. الحساسية (Price, Cost, Delay, Rate) + Tornado
10. مصفوفة المخاطر
11. Executive Summary + توصية Go/No-Go

**المخرجات:**
- Feasibility Report (10-15 صفحة)
- Investment Memo (2 صفحات)
- Scenario & Sensitivity Tables
- Cash Flow Forecast & Peak Funding

**القوالب:**
- `templates/project_analysis_report.md`
- `templates/investment_memo.md`

---

## 3. Budget vs Actual

**الملف:** `skill/workflows/budget_vs_actual.md`

**الهدف:** تحليل منهجي للانحرافات.

**الخطوات (8 خطوات):**

1. إعداد البيانات (Budget نفس تفصيل Actual)
2. التحقق (مجاميع، تواريخ)
3. حساب لكل بند:
   ```
   Variance = Actual − Budget
   Variance % = (Actual−Budget)/|Budget|×100
   Classification: Favorable/Unfavorable/Neutral (|%|<2% neutral)
   Material: |%|≥5% أو |Abs|≥ threshold
   ```
4. الترتيب حسب |Variance| — Top 5-10 للتحليل العميق
5. تحليل الأسباب (Drivers): Volume / Price / Mix / Timing / Scope / Inflation / One-off
6. المطابقة المتقاطعة (هل تفسر انحرافات التكلفة تغير الهامش؟)
7. أثر التوقع السنوي (هل نعيد التوقع؟)
8. التقرير (Dashboard + Deep Dive + Forecast Impact + Action Plan)

**مثال:**

> Construction: Budget 100M, Actual 112M → Var +12M (+12%) Unfavorable
> الأسباب: كمية BOQ +6% (حوائط إضافية)، سعر الحديد +4%، عمالة +2%
> الأثر: Margin 35%→31% (−4pts), IRR −1.8pts
> التوصية: راجع BOQ، ثبّت أسعار، ارفع Contingency 5%→7%

**القالب:** `templates/variance_report.md`

---

## 4. توقع التدفقات النقدية (Cash Flow Forecast)

**الملف:** `skill/workflows/cashflow_forecast.md`

**الهدف:** توقع السيولة وتحديد Peak Funding.

**التكرار:** شهري متجدد (13 أسبوع + 12 شهر)

**الخطوات (8 خطوات):**

1. فحص الرصيد الافتتاحي والحدود التمويلية
2. توقع التدفقات الداخلة (Collections = Sales Velocity × Payment Plan × Efficiency) + تمويل
3. توقع التدفقات الخارجة (Land, Construction S-curve, Soft, S&M, Financing, Admin)
4. حساب Net & Cumulative + تحديد Peak Funding & Runway & DSCR
5. استخراج النتائج الرئيسية
6. Stress Test (تأخير تحصيل شهرين، تكلفة +15%، مبيعات −30%)
7. تقييم المخاطر (سيولة، تحصيل، تمويل)
8. التقرير (جدول شهري + منحنى تراكمي + توصيات)

**المنحنى:** يهبط ثم يصعد — نقطة القاع هي Peak Funding.

**القالب:** جزء من `financial_analysis_report.md` (قسم Cash Flow)

**الأدوات:**
```python
from skill.tools.cashflow_analysis import analyze_cashflow
analysis = analyze_cashflow(inflows, outflows, financing, opening_cash)
print(analysis['peak_funding'])
```

---

## 5. تحليل الاستثمار (Investment Analysis)

**الملف:** `skill/workflows/investment_analysis.md`

**الهدف:** قرار استثماري (Go/No-Go) لمشروع أو محفظة أو شراء أرض.

**المدخلات:**
- التدفقات (Project & Equity)، معدل الخصم، هيكل التمويل، مقارنات سوقية

**الخطوات (10 خطوات):**

1. تحديد النطاق (Project vs Equity، العملة، اسمي vs حقيقي، مصدر Hurdle)
2. التحقق من التدفقات (الإشارات، الفترات، تعدد IRR)
3. حساب: Project IRR, NPV, Equity IRR, Multiple, ROI, ROIC, Payback, DSCR, Cash-on-Cash
4. المقارنة بالـ Hurdle & Benchmarks
5. السيناريوهات (Base/Best/Worst بجدول افتراضات)
6. الحساسية (متغير واحد كل مرة + Tornado)
7. Break-even & Downside Protection
8. تقدير مرجح بالمخاطر
9. تدقيق تقييمي (Residual + Comps)
10. التوصية (Go / Conditional / No-Go مع شروط)

**القالب:** `templates/investment_memo.md`

**الأدوات:**
```python
from skill.tools.investment_metrics import calculate_irr, calculate_npv
from skill.tools.scenario_analysis import run_scenarios, run_sensitivity_analysis
```

---

## 6. التقارير الإدارية (Management Reporting)

**الملف:** `skill/workflows/management_reporting.md`

**الهدف:** تقرير إداري Board-Ready يحرك القرارات.

**الجمهور:** CEO, Board, Investment Committee

**المبدأ:** صفحة Executive Summary أولًا، التفاصيل بعد. Numbers → So What → Now What.

**الهيكل (9 أقسام):**

1. **Executive Summary (1 صفحة — دائمًا أولًا):**
   - Health Rating + تبرير
   - Key Findings (3-5)
   - Financial Performance (جدول مضغوط)
   - Project Performance (إن وجد)
   - Cash Flow (Peak, Runway, Efficiency)
   - Key Risks (Top 3)
   - Recommendations (3-5 عملية مع Owner & Timeline)
   - Confidence

2. Detailed Financial Analysis (2-3 صفحات)
3. Project Dashboard (1-2 صفحة لكل مشروع)
4. Budget vs Actual (1 صفحة)
5. Cash Flow & Liquidity (1 صفحة)
6. Sales & Collections (1 صفحة)
7. Investment & Scenarios (إن لزم) (1-2 صفحة)
8. Risk Matrix (1 صفحة)
9. Appendix (Assumptions, Gaps, Glossary)

**قواعد الكتابة:**

- ابدأ كل قسم ببصيرة، ليس رقم: "هامش الربح انضغط 4 نقاط بسبب تجاوز الإنشاء — يتطلب مراجعة Contingency"
- استخدم الصوت النشط، جمل قصيرة
- رتّب حسب الأهمية
- أرقام مع عملة ونسبة ومقارنة
- ترميز لوني: 🟢 On track, 🟡 Watch, 🔴 Action needed

**Checklist قبل التوزيع:**

- [ ] Executive Summary صفحة واحدة
- [ ] Health Rating مبرر
- [ ] كل انحراف له سبب وتوصية
- [ ] الأرقام متطابقة (مجاميع = مجموع البنود)
- [ ] الافتراضات والفجوات مذكورة
- [ ] اللغة تناسب الجمهور
- [ ] لا بيانات مخترعة — مستوى الثقة مذكور
- [ ] مراجعة CFO تمت

**القوالب:**
- `templates/executive_summary.md` (الأساس)
- `templates/financial_analysis_report.md`
- `templates/project_analysis_report.md`
- `templates/variance_report.md`
- `templates/investment_memo.md`

---

## كيف تختار الـ Workflow؟

| سؤالك | الـ Workflow |
|-------|-------------|
| "كيف أداء الشهر؟" | Monthly Financial Analysis |
| "هل المشروع مجدٍ؟" | Project Financial Analysis |
| "لماذا زادت التكلفة؟" | Budget vs Actual |
| "هل السيولة كافية؟" | Cash Flow Forecast |
| "هل أستثمر؟" | Investment Analysis |
| "ماذا أقول للإدارة؟" | Management Reporting |

---

## التكامل مع الـ Agent

كل Workflow مرتبط بـ:
- **Prompt** في `skill/prompts/` — انسخه كتعليمات للـ Agent
- **Knowledge** في `skill/knowledge/` — مرجع معرفي
- **Template** في `skill/templates/` — مخرج جاهز
- **Tools** في `skill/tools/` — حسابات Python

> **نصيحة:** ابدأ بـ Management Reporting إذا أردت تقريرًا سريعًا، ثم تعمق في الـ Workflow المخصص حسب الحاجة.
