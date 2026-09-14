# مهارة المحلل المالي العقاري — Real Estate Financial Analyst Skill

> **Skill احترافي Production-Ready يحوّل أي AI Agent إلى محلل مالي Senior متخصص في شركات التطوير العقاري (FP&A + تحليل استثماري + دراسة جدوى).**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-70%2B%20passing-brightgreen)](#الاختبارات)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](#)

**ثنائي اللغة:** عربي + إنجليزي — يرد بنفس لغة المستخدم.  
**التخصص:** سكني، تجاري، متعدد الاستخدامات، ضيافة، تطوير أراضي — قابل للتكيف مع أي سوق (MENA، الخليج، عالمي).  
**متوافق مع أي Agent:** Claude, GPT, Gemini, أو أي LLM عبر حقن System Prompt.

---

## ✨ ماذا يفعل؟

| القدرة | الوصف |
|--------|-------|
| **تحليل القوائم المالية** | P&L, BS, Cash Flow — تحليل رأسي/أفقي، هوامش، EBITDA، صافي |
| **تحليل المشروع** | GDV, GDC، هامش التطوير، ربح/م²، نسب التكلفة، القيمة المتبقية للأرض |
| **المبيعات والتحصيلات** | مباع vs متاح، معدل البيع، متوسط السعر، كفاءة التحصيل، الأعمار |
| **التدفقات والسيولة** | تشغيل/تطوير/تمويل، التراكمي، Peak Funding، Runway، DSCR |
| **الموازنة vs الفعلي** | انحراف مطلق ونسبي، Favorable/Unfavorable/Neutral، تحليل الأسباب |
| **مؤشرات الاستثمار** | IRR, NPV, ROI, ROIC, Equity Multiple, Cash-on-Cash, Payback |
| **السيناريوهات** | أساسي / متفائل / متشائم — جدول مقارنة |
| **الحساسية** | السعر، التكلفة، السرعة، الفائدة، التأخير — ترتيب Tornado |
| **المخاطر** | 10 فئات مخاطر مع Prob×Impact ومؤشرات إنذار مبكر |
| **التقارير الإدارية** | Executive Summary جاهز للإدارة + تقارير تفصيلية + مذكرات استثمارية |

**المبدأ:** المحلل يفكر كـ **مستشار CFO، ليس آلة حاسبة** — كل رقم له سبب ومخاطر وتوصية. **لا يخترع بيانات أبدًا.**

---

## 📁 هيكل المشروع

```
real-estate-financial-analyst-skill/
├── README.md / README_AR.md
├── LICENSE / CHANGELOG.md / CONTRIBUTING.md
├── requirements.txt / pyproject.toml / .gitignore
│
├── skill/
│   ├── SKILL.md                          # ★ التعريف الأساسي للـ Skill
│   ├── config/
│   │   ├── settings.yaml                 # إعدادات الشركة (عملة، hurdle، thresholds)
│   │   ├── financial_rules.yaml          # قواعد التحقق والحساب
│   │   └── industry_benchmarks.yaml      # Benchmarks حسب القطاع
│   ├── prompts/
│   │   ├── system_prompt.md              # الـ System Prompt الرئيسي
│   │   ├── financial_analysis_prompt.md
│   │   ├── project_analysis_prompt.md
│   │   ├── cashflow_analysis_prompt.md
│   │   ├── variance_analysis_prompt.md
│   │   └── investment_analysis_prompt.md
│   ├── knowledge/
│   │   ├── real_estate_finance.md
│   │   ├── financial_metrics.md
│   │   ├── real_estate_metrics.md
│   │   ├── valuation_methods.md
│   │   ├── cashflow_methods.md
│   │   └── financial_analysis_rules.md
│   ├── workflows/
│   │   ├── monthly_financial_analysis.md
│   │   ├── project_financial_analysis.md
│   │   ├── budget_vs_actual.md
│   │   ├── cashflow_forecast.md
│   │   ├── investment_analysis.md
│   │   └── management_reporting.md
│   ├── templates/
│   │   ├── executive_summary.md
│   │   ├── financial_analysis_report.md
│   │   ├── project_analysis_report.md
│   │   ├── variance_report.md
│   │   └── investment_memo.md
│   └── tools/ (محرك Python)
│       ├── financial_calculations.py
│       ├── project_metrics.py
│       ├── cashflow_analysis.py
│       ├── investment_metrics.py
│       ├── scenario_analysis.py
│       └── data_validation.py
│
├── examples/
│   ├── example_project.md
│   ├── example_financials.csv
│   ├── example_cashflow.csv
│   └── example_analysis.md
│
├── tests/ (70+ اختبار)
│
└── docs/
    ├── GETTING_STARTED_AR.md
    ├── USAGE_AR.md
    ├── FINANCIAL_METRICS_AR.md
    ├── WORKFLOWS_AR.md
    └── TROUBLESHOOTING_AR.md
```

---

## 🚀 البدء السريع

### 1. التثبيت

```bash
git clone https://github.com/your-org/real-estate-financial-analyst-skill.git
cd real-estate-financial-analyst-skill
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v  # يجب أن تنجح ~70 اختبارًا
```

### 2. الاستخدام المباشر بـ Python (بدون Agent)

```python
from skill.tools.financial_calculations import calculate_gross_margin, calculate_variance, classify_variance
from skill.tools.project_metrics import calculate_gdv, calculate_gdc, calculate_development_margin
from skill.tools.investment_metrics import calculate_irr, calculate_npv

# هامش الربح
print(calculate_gross_margin(1_000_000, 650_000))  # 35.0%

# مشروع
gdv = calculate_gdv([{"units": 100, "price_per_unit": 2_000_000}])
gdc = calculate_gdc({"land": 40_000_000, "construction": 90_000_000, "soft": 15_000_000})
print(f"هامش التطوير: {calculate_development_margin(gdv, gdc):.1f}%")

# استثمار
cfs = [-100_000_000, 30_000_000, 50_000_000, 70_000_000]
print(f"IRR: {calculate_irr(cfs)*100:.1f}%")
print(f"NPV @15%: {calculate_npv(cfs, 0.15):,.0f}")

# الانحراف
print(calculate_variance(112_000_000, 100_000_000))  # 12,000,000
print(classify_variance(112_000_000, 100_000_000, is_revenue=False))  # Unfavorable
```

### 3. الاستخدام مع AI Agent

**الطريقة A — حقن System Prompt (الأسهل):**

1. انسخ `skill/prompts/system_prompt.md` كـ System Prompt للـ Agent.
2. ارفع `skill/knowledge/*.md` كـ Knowledge Base.
3. سجّل `skill/tools/*.py` كـ Function Tools (إن كان مدعومًا).
4. اسأل: *"حلّل هذا المشروع: أرض 50M، إنشاء 120M، مساحة 10,000م، سعر 25k/م"*

**الطريقة B — مرجع SKILL.md:**

وجّه الـ Agent لقراءة `skill/SKILL.md` عند البدء.

**الطريقة C — استيراد Python:**

استورد الأدوات مباشرة كما فوق في أي Agent يدعم Python.

عدّل `skill/config/settings.yaml` لشركتك (العملة، الضريبة، Hurdle 18%، الحدود).

---

## 📊 مثال مخرج — Executive Summary

```
الصحة العامة: Watchlist
هامش 32% مستقر لكن سيولة ضاغطة — Runway 2.8 شهر، تحصيل 86%

أهم النتائج:
1. Gross Margin 32% vs 35% موازنة (−3pts) — تجاوز إنشاء +11.5%
2. Net Margin 10.9% vs 13.3% موازنة — أقل من Benchmark 18%
3. مبيعات 65 vs 70 وحدة (−7.1%) — سرعة أقل 5% من الخطة

المشروع: Green Valley — GDV 1.75B | GDC 1.25B | هامش 28.6% | IRR 18.2% | NPV +58M | تعادل 71.4%

التدفقات: Peak Funding −77.9M عند M9 | التعافي M14 | DSCR ~1.0 عند القاع (تحذير <1.2)
التحصيلات: كفاءة 86.1% vs 88% مستهدف — 9.4M متأخر

أهم المخاطر:
1. سيولة — حرج — تسريع تحصيلات 91-180d (22M)
2. تجاوز تكلفة — عالٍ — إعادة تفاوض الحديد
3. سرعة مبيعات — متوسط — ترويج 2BR

التوصيات:
1. حملة تحصيل أسبوعية (مسؤول: مدير التحصيل، 60 يوم، +8M سيولة)
2. مراجعة BOQ ورفع Contingency 5%→7% (مسؤول: PM، 14 يوم)
3. تأكيد تسهيل +20M (مسؤول: CFO، 14 يوم)
```

المثال الكامل: `examples/example_analysis.md`

---

## 🧮 محرك المؤشرات

| المجموعة | المؤشرات |
|----------|----------|
| **الربحية** | Revenue, COR, Gross Profit/Margin, Operating Profit, EBITDA/EBIT, Net Profit/Margin |
| **الاستثمار** | ROI, IRR, NPV, ROIC, Equity Multiple, Cash-on-Cash, Payback |
| **التطوير العقاري** | GDV, GDC، هامش التطوير، ربح/م²، تكلفة/م²، سعر/م²، نسبة الأرض/الإنشاء، القيمة المتبقية |
| **المبيعات** | قيمة المبيعات، مباع/متاح، معدل البيع، متوسط السعر، سعر/م²، معدل الإلغاء |
| **التحصيلات** | متعاقد vs محصل vs مستحق، الكفاءة، الأعمار، المتأخر |
| **التدفقات** | تشغيل/تطوير/تمويل، Free، Net، تراكمي، Peak Funding، Runway، DSCR |
| **الانحرافات** | مطلق، %، Favorable/Unfavorable/Neutral، السبب (Volume/Price/Mix/Timing) |

راجع `docs/FINANCIAL_METRICS_AR.md` للمعادلات والـ Benchmarks.

---

## 🔄 الـ Workflows

| الـ Workflow | متى | القالب |
|-------------|-----|--------|
| التحليل المالي الشهري | حزمة شهرية للإدارة | `financial_analysis_report.md` |
| تحليل المشروع | مشروع جديد / إعادة توقع ربع سنوي | `project_analysis_report.md` |
| الموازنة vs الفعلي | مراجعة الانحرافات الشهرية | `variance_report.md` |
| توقع التدفقات | السيولة و Peak Funding | (قسم Cash Flow) |
| تحليل الاستثمار | قرار لجنة الاستثمار / شراء أرض | `investment_memo.md` |
| التقارير الإدارية | حزمة الإدارة / Board | `executive_summary.md` |

التفاصيل: `docs/WORKFLOWS_AR.md`

---

## 🧪 الاختبارات

```bash
pytest -v
pytest --cov=skill/tools
pytest tests/test_investment_metrics.py -v
```

- 70+ اختبار يغطي كل المحركات والحالات الحدية (قسمة صفر، بيانات ناقصة، تقارب IRR، منطق السيناريوهات).
- محمي من: قسمة صفر، مدخلات ناقصة، إيراد سالب، مباع>إجمالي، منطق التواريخ، عدم تطابق المجاميع.

---

## 🌍 التكيف مع سوقك

عدّل `skill/config/settings.yaml`:

```yaml
company:
  default_currency: "EGP"   # SAR / AED / USD / EUR
  tax_rate: 0.225
thresholds:
  irr_hurdle_rate: 18.0
  variance_neutral_pct: 2.0
```

و `skill/config/industry_benchmarks.yaml` لمعايير القطاع محليًا.

---

## 🧠 كيف يفكر الـ Agent

```
1. فهم البيانات → 2. التحقق → 3. تحديد الناقص
→ 4. الحساب → 5. المقارنة (YoY/موازنة/Benchmark)
→ 6. تحديد الانحرافات → 7. تحديد الأسباب (Volume/Price/Mix/Timing)
→ 8. تقييم المخاطر → 9. بناء السيناريوهات → 10. التوصيات
```

إذا البيانات ناقصة: *"البيانات غير كافية لحساب [المؤشر] — المطلوب: [X, Y, Z]"* — لا يخترع أبدًا.

---

## 📚 التوثيق

| الملف | اللغة | المحتوى |
|-------|-------|---------|
| `docs/GETTING_STARTED_AR.md` | عربي | بدء سريع 10 دقائق |
| `docs/USAGE_AR.md` | عربي | دليل الاستخدام الكامل + Prompts |
| `docs/FINANCIAL_METRICS_AR.md` | عربي | كل مؤشر مع معادلته و Benchmark |
| `docs/WORKFLOWS_AR.md` | عربي | الـ 6 Workflows |
| `docs/TROUBLESHOOTING_AR.md` | عربي | حل المشاكل |
| `README.md` | إنجليزي | English README |
| `skill/SKILL.md` | إنجليزي | مواصفات الـ Skill |
| `skill/knowledge/*.md` | إنجليزي | المعرفة التخصصية |

---

## 🌐 رفعه إلى GitHub

```bash
git init
git add .
git commit -m "feat: initial release — Real Estate Financial Analyst Skill v1.0.0"
git branch -M main
git remote add origin https://github.com/your-org/real-estate-financial-analyst-skill.git
git push -u origin main
```

للتحديث لاحقًا:

```bash
git add .
git commit -m "feat: add excel ingestion helpers"
git push
```

راجع `CONTRIBUTING.md`.

---

## 🗺️ خارطة الطريق

- [ ] مساعد استيراد Excel (يقرأ P&L / Trial Balance تلقائيًا)
- [ ] محلل PDF للقوائم المالية
- [ ] أتمتة IFRS 15 (Revenue Recognition)
- [ ] مولد Dashboard تفاعلي (HTML)
- [ ] معالجة عملات متعددة مع FX

---

## 🤝 المساهمة

راجع `CONTRIBUTING.md`. الـ PRs مرحب بها — أضف اختبارات لأي تغيير في المعادلات.

---

## 📄 الترخيص

MIT — راجع `LICENSE`.

---

## 🙏 شكر

صُمم للمحللين الماليين الذين يرفضون أن يكونوا مجرد آلات حاسبة.

> **الإصدار 1.0.0 — 2026-09-14 — جاهز للإنتاج (Production Ready)**
