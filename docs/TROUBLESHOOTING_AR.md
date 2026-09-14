# استكشاف الأخطاء وإصلاحها — Troubleshooting

---

## 1. مشاكل التثبيت

### `pip install -r requirements.txt` يفشل

**السبب:** إصدار Python قديم أو pip قديم.

**الحل:**
```bash
python --version  # يجب ≥3.9
pip install --upgrade pip
pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'skill'`

**الحل:**
```bash
# شغّل من جذر المشروع
pip install -e .
# أو أضف الجذر لـ PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest -v
```

### `openpyxl` غير مثبت — لا أستطيع قراءة Excel

```bash
pip install openpyxl
```

---

## 2. مشاكل الحسابات

### `Gross Margin` يرجع `None`

**السبب:** الإيراد صفر أو None.

**الحل:** تأكد أن `revenue` قيمة موجبة. لو صفر، الهامش غير معرف — هذا سلوك صحيح. الـ Skill يرجع `None` مع رسالة: "Cannot calculate — denominator is zero".

**الكود:**
```python
from skill.tools.financial_calculations import calculate_gross_margin
result = calculate_gross_margin(revenue=0, cost_of_revenue=50)
print(result)  # None — صحيح
```

### `Variance %` يرجع `None`

**السبب:** الموازنة صفر — النسبة غير معرفة (قسمة على صفر).

**الحل:** استخدم Absolute Variance فقط في هذه الحالة. الـ Skill يحمي من قسمة صفر.

### `IRR` يرجع `None`

**الأسباب:**
1. لا يوجد تغير إشارة في التدفقات (كلها موجبة أو كلها سالبة)
2. التدفقات قصيرة جدًا (<2 فترات)
3. التدفقات غير نمطية (تغيرات إشارة متعددة) — IRR متعدد

**الحل:**
```python
from skill.tools.investment_metrics import calculate_irr, calculate_npv
cfs = [-100, 60, 60]
irr = calculate_irr(cfs)
if irr is None:
    print("لا يمكن حساب IRR — تحقق من وجود outflow سالب و inflow موجب")
else:
    print(f"IRR: {irr*100:.1f}%")
# اعرض NPV مع IRR دائمًا حتى لو IRR None
print(f"NPV @15%: {calculate_npv(cfs, 0.15):,.0f}")
```

### `NPV` سالب جدًا — هل خطأ؟

**تحقق:**
- هل معدل الخصم عشري (0.15 = 15%) وليس 15؟
- هل التدفقات بالترتيب الزمني الصحيح (t0 سالب، t1... موجبة)؟
- هل العملة واحدة؟

```python
# صحيح
calculate_npv([-100, 60, 60], 0.15)
# خطأ: 15 بدل 0.15 سيعطي NPV خاطئ
calculate_npv([-100, 60, 60], 15)
```

### `Development Margin` سالب

**ليس خطأ بالضرورة —** يعني GDC > GDV (المشروع خاسر بالافتراضات الحالية). الـ Skill سيحذر: "GDC exceeds GDV — negative margin".

**الحل:** راجع افتراضات السعر والتكلفة. اختبر سيناريو Best.

---

## 3. مشاكل التحقق من البيانات (Data Validation)

### `Sold Units exceeds Total Units`

**الرسالة:** `Sold Units (520) exceeds Total Units (500) — data error.`

**الحل:** صحح ملف المبيعات — تأكد أن Available = Total − Sold − Reserved.

### `Sellable Area exceeds BUA`

**الرسالة:** تحذير — Sellable يجب ≤ BUA.

**الحل:** راجع جدول المساحات — BUA تشمل الحوائط والخدمات، Sellable هي الصافي.

### `Revenue is negative`

**الحل:** تحقق من Credit Notes أو إدخال خاطئ. الإيراد يجب أن يكون موجب.

### `Cumulative mismatch`

**الرسالة:** `Cumulative mismatch at period 3: reported X vs calculated Y`

**الحل:** أعد حساب Cumulative = Opening + Σ Net CF. تأكد أن Net = Inflows − Outflows + Financing.

---

## 4. مشاكل الـ AI Agent

### الـ Agent يخترع أرقامًا

**السبب:** لم تُحمّل `skill/prompts/system_prompt.md` أو `skill/SKILL.md`.

**الحل:**
- انسخ System Prompt كاملًا في إعدادات الـ Agent.
- أضف في بداية كل محادثة: "اتبع القاعدة: NEVER FABRICATE FINANCIAL DATA — إذا البيانات ناقصة قل بوضوح ما الناقص."

### الـ Agent يفترض عملة/دولة خاطئة

**الحل:** اذكر بوضوح في Prompt: "العملة EGP، المشروع في مصر، معدل الخصم 15%". أو عدّل `skill/config/settings.yaml`.

### الـ Agent يخلط بين Revenue و Collections

**الحل:** وضّح: "Revenue = POC accrual، Collections = cash، Contracted = bookings — لا تجمعهم". الـ Knowledge في `real_estate_finance.md` يشرح الفرق.

### الـ Agent يرد بالإنجليزية وأريد عربي

**الحل:** اكتب Prompt بالعربي — الـ Skill يرد بنفس لغة المستخدم تلقائيًا. أو أضف: "رد باللغة العربية".

---

## 5. مشاكل الـ Excel / CSV

### الأرقام تُقرأ كنص

**الحل:** تأكد أن الخلايا Number وليست Text. احذف الفواصل والرموز قبل الاستيراد، أو استخدم:

```python
import pandas as pd
df = pd.read_csv("example_financials.csv")
df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
```

### التاريخ بصيغة خاطئة

**المتوقع:** `YYYY-MM-DD` (مثلاً 2025-06-30)

**الحل:** وحّد صيغة التاريخ. الـ Skill يتوقع `YYYY-MM-DD` حسب `settings.yaml`.

### ملف كبير جدًا / بطيء

**الحل:** قسّم الملف حسب المشروع أو الفترة. الـ Skill يعمل أفضل مع <10,000 صف.

---

## 6. مشاكل الاختبارات

### `pytest` غير موجود

```bash
pip install pytest
pytest -v
```

### اختبار يفشل

```bash
pytest -v --tb=short
# اقرأ رسالة الخطأ — غالبًا مشكلة استيراد أو Python قديم
pytest tests/test_investment_metrics.py::test_irr_basic -v
```

### كل الاختبارات تمر لكن النتائج تبدو خاطئة

**تحقق:**
- هل تستخدم العملة والمعدل الصحيح؟
- هل التدفقات مرتبة زمنيًا؟
- هل GDV و GDC بنفس العملة والفترة؟

---

## 7. مشاكل GitHub

### `git push` يرفض

```bash
git remote -v  # تأكد من URL
git branch -M main
git pull --rebase origin main  # إذا كان هناك commits بعيدة
git push -u origin main
```

### نسيت إضافة `.gitignore`

```bash
# تأكد أن .gitignore موجود ويحتوي على __pycache__, .venv, .env
cat .gitignore
git rm -r --cached .  # إزالة الملفات المتجاهلة من التتبع
git add .
git commit -m "fix: respect .gitignore"
```

### رفعت Secrets بالخطأ

```bash
# خطر! احذف فورًا:
git filter-repo --path secrets.yaml --invert-paths
# أو أعد إنشاء المفاتيح وأبطل القديمة
# وأضف الملف لـ .gitignore
```

---

## 8. أسئلة شائعة

**س: هل الـ Skill يعمل مع شركات المقاولات أم التطوير فقط؟**

ج: مصمم للتطوير، لكن 80% من التحليل (P&L, Cash Flow, Variance) ينطبق على المقاولات. فقط GDV/GDC خاص بالتطوير.

**س: هل يدعم العملات المتعددة؟**

ج: نعم — حدد العملة في `settings.yaml` وفي كل تحليل. لكن لا يحوّل العملات تلقائيًا — يجب توحيد العملة قبل التحليل.

**س: هل يحسب الضرائب تلقائيًا؟**

ج: لا — يأخذ `tax` كمدخل أو يحسب `NOPAT = EBIT × (1−tax_rate)` إذا زودت المعدل. عدّل `tax_rate` في `settings.yaml`.

**س: كيف أضيف مؤشر جديد؟**

ج: أضف function في `skill/tools/` + اختبار في `tests/` + وثّقه في `docs/FINANCIAL_METRICS_AR.md`.

**س: الـ Skill يعطي Health = Watchlist — ماذا أفعل؟**

ج: اقرأ Key Risks و Recommendations — الـ Skill يعطي إجراءات محددة. راجع `templates/executive_summary.md`.

---

## 9. طلب المساعدة

1. اقرأ هذا الدليل + `GETTING_STARTED_AR.md` + `USAGE_AR.md`
2. شغّل `pytest -v` وتأكد أن الاختبارات تمر
3. راجع `examples/example_analysis.md` كمثال مرجعي
4. افتح Issue على GitHub مع:
   - وصف المشكلة
   - خطوات الإعادة
   - رسالة الخطأ كاملة
   - ملف بيانات مجهول (بدون أسماء حقيقية)

---

*آخر تحديث: 2026-09-14 — Skill v1.0.0*
