# نظام اللغة الثنائي - Bilingual Language System

## التغييرات الرئيسية - Main Changes

تم تحويل الموقع من نظام ترجمة Django (i18n) إلى نظام محتوى ثنائي اللغة مستقل:

The website has been converted from Django translation system (i18n) to an independent bilingual content system:

### ✅ ما تم تنفيذه - What Has Been Implemented

1. **إزالة نظام الترجمة Django i18n**
   - حذف LocaleMiddleware
   - تعطيل USE_I18N
   - حذف ملفات الترجمة (.po/.mo)

2. **نظام محتوى ثنائي اللغة جديد**
   - ملف `tourism/content.py` يحتوي على كل المحتوى بالعربية والإنجليزية
   - تخزين اللغة في الـ session
   - منتقي لغة في شريط التنقل

3. **تحديث القوالب**
   - استبدال `{% trans %}` بـ `{{ content.key }}`
   - دعم RTL/LTR تلقائياً
   - Bootstrap متعدد اللغات

---

## كيفية التشغيل - How to Run

### 1. تفعيل البيئة الافتراضية - Activate Virtual Environment
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# أو Windows CMD
.\venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 2. تشغيل الخادم - Run Server
```bash
python manage.py runserver
```

### 3. فتح الموقع - Open Website
```
http://127.0.0.1:8000/
```

---

## التبديل بين اللغات - Switching Languages

### في الموقع - On the Website:
1. اذهب إلى الصفحة الرئيسية
2. انقر على أيقونة الكرة الأرضية (🌐) في شريط التنقل
3. اختر:
   - **العربية** للغة العربية
   - **English** للغة الإنجليزية

### برمجياً - Programmatically:
```python
# في أي view
request.session['language'] = 'en'  # or 'ar'
```

---

## استخدام المحتوى - Using Content

### في القوالب - In Templates:
```django
<!-- قبل (قديم) -->
{% load i18n %}
{% trans "الرئيسية" %}

<!-- بعد (جديد) -->
{{ content.nav_home }}
```

### إضافة محتوى جديد - Adding New Content:
1. افتح `tourism/content.py`
2. أضف النص في كلا اللغتين:
   ```python
   CONTENT = {
       'ar': {
           'new_text': 'نص جديد',
       },
       'en': {
           'new_text': 'New text',
       }
   }
   ```
3. استخدمه في القالب: `{{ content.new_text }}`

---

## الملفات المحدّثة - Updated Files

### ملفات جديدة - New Files:
- ✨ `tourism/content.py` - قاموس المحتوى الثنائي
- ✨ `BILINGUAL_GUIDE.md` - دليل شامل

### ملفات معدّلة - Modified Files:
- 📝 `egyroute/settings.py` - تعطيل i18n
- 📝 `tourism/context_processors.py` - إضافة محتوى
- 📝 `tourism/views.py` - وظيفة set_language
- 📝 `tourism/urls.py` - مسار set-language
- 📝 `templates/tourism/base.html` - منتقي اللغة
- 📝 `templates/tourism/home.html` - استخدام content

### ملفات محذوفة - Deleted Files:
- ❌ `locale/` - مجلد الترجمة
- ❌ `compile_translations.py`
- ❌ `compile_translations_polib.py`
- ❌ `TRANSLATION_FIX.md`
- ❌ `FULL_TRANSLATION_GUIDE.md`
- ❌ `LANGUAGE_SWITCHING_GUIDE.md`

---

## الخطوات التالية - Next Steps

### ✅ تم إنجازه - Completed:
- [x] إزالة نظام i18n
- [x] إنشاء نظام محتوى ثنائي
- [x] تحديث القوالب الرئيسية
- [x] إضافة منتقي اللغة

### 📋 يحتاج عمل - Needs Work:
- [ ] **تحديث باقي القوالب** (about.html, contact.html, إلخ)
- [ ] **إضافة ترجمة لمحتوى قاعدة البيانات** (أسماء الأماكن، الأوصاف)
- [ ] **اختبار جميع الصفحات**

---

## ترجمة محتوى قاعدة البيانات - Database Content Translation

حالياً، البيانات في قاعدة البيانات (أسماء الأماكن، الأوصاف) بلغة واحدة فقط.

### الحل الموصى به - Recommended Solution:

#### الخيار 1: إضافة حقول منفصلة (بسيط)
```python
# في tourism/models.py
class TouristPlace(models.Model):
    # الحقول الحالية
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # حقول جديدة للإنجليزية
    name_en = models.CharField(max_length=200, blank=True)
    description_en = models.TextField(blank=True)
    
    def get_name(self, request=None):
        """Get name based on current language"""
        if request and request.session.get('language') == 'en' and self.name_en:
            return self.name_en
        return self.name
```

#### تشغيل Migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### استخدام في القوالب:
```django
<!-- قبل -->
<h1>{{ place.name }}</h1>

<!-- بعد -->
<h1>{% if LANGUAGE_CODE == 'en' and place.name_en %}{{ place.name_en }}{% else %}{{ place.name }}{% endif %}</h1>
```

---

## دليل سريع للمطورين - Quick Developer Guide

### إضافة نص جديد - Add New Text:
1. أضف في `tourism/content.py`:
   ```python
   'my_key': 'النص بالعربية'  # في قسم 'ar'
   'my_key': 'Text in English'  # في قسم 'en'
   ```
2. استخدم في القالب: `{{ content.my_key }}`

### التحقق من اللغة الحالية - Check Current Language:
```django
{% if LANGUAGE_CODE == 'ar' %}
    <!-- محتوى عربي -->
{% else %}
    <!-- English content -->
{% endif %}
```

### تغيير اتجاه النص - Change Text Direction:
```django
<div dir="{% if LANGUAGE_CODE == 'ar' %}rtl{% else %}ltr{% endif %}">
```

---

## المميزات - Features

✅ **المزايا:**
- نفس قاعدة البيانات للغتين
- نفس لوحة التحكم Django Admin
- تبديل سريع وسهل بين اللغات
- لا حاجة لتجميع ملفات ترجمة
- أداء أفضل (لا معالجة ترجمة إضافية)
- سهولة الصيانة والتحديث

✅ **Advantages:**
- Same database for both languages
- Same Django Admin panel
- Quick and easy language switching
- No need to compile translation files
- Better performance (no additional translation processing)
- Easy maintenance and updates

---

## استكشاف الأخطاء - Troubleshooting

### المشكلة: اللغة لا تتغير
**الحل:**
- تأكد من تفعيل sessions في settings.py
- امسح الكوكيز والـ cache
- تحقق من `request.session['language']`

### المشكلة: المحتوى لا يظهر
**الحل:**
- تحقق من وجود المفتاح في `content.py`
- تأكد من استيراد المحتوى في `context_processors.py`
- راجع أخطاء القالب في console

---

## المراجع - References

- 📚 الدليل الشامل: [BILINGUAL_GUIDE.md](BILINGUAL_GUIDE.md)
- 📁 ملف المحتوى: [tourism/content.py](tourism/content.py)
- ⚙️ الإعدادات: [egyroute/settings.py](egyroute/settings.py)

---

## الدعم - Support

للأسئلة أو المساعدة:
1. راجع [BILINGUAL_GUIDE.md](BILINGUAL_GUIDE.md)
2. تحقق من الأمثلة في القوالب
3. انظر إلى `tourism/content.py`

---

**تم التحديث:** يناير 2026  
**Updated:** January 2026

---

## ملاحظة مهمة - Important Note

⚠️ **القوالب الأخرى:**
حالياً تم تحديث القوالب الرئيسية فقط (base.html و home.html). ستحتاج إلى تحديث باقي القوالب بنفس الطريقة:
- about.html
- contact.html
- category_detail.html
- place_detail.html
- وغيرها...

Currently, only the main templates have been updated (base.html and home.html). You'll need to update the other templates in the same way:
- about.html
- contact.html
- category_detail.html
- place_detail.html
- and others...

**الطريقة:**
استبدل جميع `{% trans "..." %}` بـ `{{ content.key }}` بعد إضافة المفاتيح المناسبة في `content.py`.

**Method:**
Replace all `{% trans "..." %}` with `{{ content.key }}` after adding the appropriate keys in `content.py`.
