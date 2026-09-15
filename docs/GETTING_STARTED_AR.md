# دليل البدء السريع — Real Estate Financial Analyst Skill

> هذا الدليل يشرح كيف تبدأ استخدام الـ Skill خلال 10 دقائق.

---

## 1. ما هو هذا الـ Skill؟

هذا Skill احترافي يجعل أي AI Agent يعمل كـ **محلل مالي Senior متخصص في التطوير العقاري**، قادر على:

- تحليل القوائم المالية والربحية
- تحليل المشروع (GDV / GDC / Margin / IRR / NPV)
- تحليل المبيعات والتحصيلات
- تحليل التدفقات النقدية وتحديد Peak Funding
- تحليل Budget vs Actual والانحرافات
- تحليل السيناريوهات والحساسية
- تقييم المخاطر وإعداد تقارير للإدارة

---

## 2. المتطلبات

- Python 3.9 أو أحدث
- pip
- (اختياري) AI Agent مثل Claude / GPT مع إمكانية حقن System Prompt

---

## 3. التثبيت

### خطوة 1: تحميل المشروع

```bash
git clone https://github.com/amrmido71-star/real-estate-financial-analyst-skill.git
cd real-estate-financial-analyst-skill
```

### خطوة 2: إنشاء بيئة افتراضية

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac / Linux
source .venv/bin/activate
```

### خطوة 3: تثبيت المتطلبات

```bash
pip install -r requirements.txt
# أو
pip install -e .
```

### خطوة 4: تشغيل الاختبارات (التحقق أن كل شيء يعمل)

```bash
pytest -v
```

يجب أن ترى `passed` لجميع الاختبارات (~70 اختبار).

---

## 4. الاستخدام السريع — بدون AI Agent (Python مباشر)

```python
from skill.tools.financial_calculations import calculate_gross_margin, calculate_variance, classify_variance
from skill.tools.project_metrics import calculate_gdv, calculate_gdc, calculate_development_margin
from skill.tools.investment_metrics import calculate_irr, calculate_npv

# 1. حساب هامش الربح
margin = calculate_gross_margin(revenue=1_000_000, cost_of_revenue=650_000)
print(f"Gross Margin: {margin:.1f}%")  # 35.0%

# 2. تحليل مشروع
gdv = calculate_gdv([{"units": 100, "price_per_unit": 2_000_000}])  # 200M
gdc = calculate_gdc({"land": 40_000_000, "construction": 90_000_000, "soft": 15_000_000})
print(f"Development Margin: {calculate_development_margin(gdv, gdc):.1f}%")

# 3. IRR / NPV
cash_flows = [-100_000_000, 30_000_000, 50_000_000, 70_000_000]
print(f"IRR: {calculate_irr(cash_flows)*100:.1f}%")
print(f"NPV @15%: {calculate_npv(cash_flows, 0.15):,.0f}")

# 4. Variance
print(calculate_variance(112_000_000, 100_000_000))        # 12,000,000
print(classify_variance(112_000_000, 100_000_000, is_revenue=False))  # Unfavorable
```

---

## 5. الاستخدام مع AI Agent

### الطريقة A: حقن System Prompt (الأسهل)

1. افتح `skill/prompts/system_prompt.md` وانسخ محتواه.
2. الصقه كـ System Prompt في الـ AI Agent الخاص بك (Claude / GPT Custom Instructions / OpenAI Assistant).
3. ارفع ملفات `skill/knowledge/*.md` كـ Knowledge Base للـ Agent.
4. سجل أدوات `skill/tools/*.py` كـ Function Tools (إذا كان الـ Agent يدعم Python tools).

الآن اسأل الـ Agent:

> "حلّل لي هذا المشروع: أرض 50M، إنشاء 120M، تسويق 10M، إجمالي مساحة 10,000م، سعر البيع 25k/م"

سيرد الـ Agent بتحليل كامل مع Executive Summary.

### الطريقة B: مرجع SKILL.md

- وجّه الـ Agent لقراءة `skill/SKILL.md` عند البدء. هذا الملف يحتوي تعريف كامل للدور والقدرات.

### الطريقة C: الإعدادات

- عدّل `skill/config/settings.yaml` لتناسب شركتك:
  - العملة الافتراضية
  - معدل الضريبة
  - Hurdle Rate (مثلاً 18%)
  - Thresholds للـ Variance

---

## 6. رفع الملفات

الـ Skill يدعم:

- Excel, CSV, Trial Balance (PDF مع قراءة يدوية - التحليل التلقائي قادم), Budgets, Forecasts, Sales Reports

**ماذا ترفع؟**

- القوائم المالية (P&L, BS, Cash Flow)
- جدول الوحدات (Unit Mix + Prices)
- تقرير المبيعات والحجوزات
- تقرير التحصيلات والأعمار (Aging)
- تقرير التكاليف (BOQ, Cost Report)
- الموازنة (Budget)

**ماذا سيحدث؟**

1. الـ Agent يفحص جودة البيانات (Data Validation)
2. يحسب المؤشرات
3. يقارن Budget vs Actual
4. يحدد المخاطر والتوصيات
5. يخرج Executive Summary + تقرير تفصيلي

---

## 7. أمثلة Prompts جاهزة

```
حلّل القوائم المالية المرفقة للربع الثاني 2025 وقارنها بالموازنة ونفس الربع العام الماضي.

حلّل مشروع Green Valley المرفق: احسب GDV و GDC وهامش التطوير و IRR.

قارن Budget vs Actual للإنشاءات: الموازنة 100M والفعلي 112M — ما السبب والتوصية؟

ما هو Peak Funding Requirement للمشروع؟ ومتى يحدث؟

ماذا يحدث لو انخفضت أسعار البيع 10%؟ أثرها على IRR و NPV والمارجن.

هل المشروع مربح؟ وهل IRR مقبول مقارنة بـ Hurdle 18%؟

أعطني Executive Summary للإدارة (صفحة واحدة) عن الأداء المالي هذا الشهر.

حلل التدفقات النقدية: هل التحصيلات كافية لتغطية التدفقات الخارجة؟
```

المزيد في `docs/USAGE_AR.md` و `docs/WORKFLOWS_AR.md`.

---

## 8. التحقق السريع

```bash
# شغل مثال المشروع
python -c "
from skill.tools.project_metrics import calculate_gdv, calculate_gdc, calculate_development_margin
from examples.example_project import *
# أو اقرأ examples/example_project.md
"
# أو ببساطة افتح examples/example_analysis.md لترى ناتج تحليل كامل جاهز
```

---

## 9. الخطوة التالية

- اقرأ `docs/USAGE_AR.md` للتعمق في الاستخدام
- اقرأ `docs/FINANCIAL_METRICS_AR.md` لفهم كل المؤشرات
- اقرأ `docs/WORKFLOWS_AR.md` لمعرفة الـ 6 Workflows الاحترافية
- جرب `examples/example_financials.csv` و `examples/example_cashflow.csv` مع الـ Agent

---

## 10. الدعم

- اقرأ `docs/TROUBLESHOOTING_AR.md` للمشاكل الشائعة
- افتح Issue على GitHub
- راجع `CONTRIBUTING.md` للمساهمة

> جاهز؟ افتح `examples/example_analysis.md` لترى كيف يبدو التحليل النهائي الاحترافي.
