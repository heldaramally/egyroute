# دليل نظام اللغتين (العربية والإنجليزية) - Bilingual System Guide

## نظرة عامة - Overview

تم تحويل الموقع من نظام الترجمة Django i18n إلى نظام محتوى ثنائي اللغة مستقل. الآن الموقع يدعم العربية والإنجليزية باستخدام نفس قاعدة البيانات ولوحة التحكم.

The website has been converted from Django i18n translation system to an independent bilingual content system. The site now supports Arabic and English using the same database and admin panel.

---

## كيف يعمل النظام - How It Works

### 1. تخزين اللغة - Language Storage
- اللغة الحالية تُخزن في الـ session
- Current language is stored in the session
- المفتاح: `request.session['language']`
- القيمة الافتراضية: `'ar'` (عربي)
- Default value: `'ar'` (Arabic)

### 2. ملف المحتوى - Content File
الملف: `tourism/content.py`

يحتوي على قاموس `CONTENT` مع كل المحتوى الثابت بالعربية والإنجليزية:

```python
CONTENT = {
    'ar': {
        'home_hero_title': 'اكتشف جمال مصر',
        'nav_home': 'الرئيسية',
        # ... المزيد
    },
    'en': {
        'home_hero_title': 'Discover the Beauty of Egypt',
        'nav_home': 'Home',
        # ... more
    }
}
```

### 3. Context Processor
الملف: `tourism/context_processors.py`

يضيف المحتوى تلقائياً لجميع القوالب:
- `LANGUAGE_CODE`: اللغة الحالية (ar/en)
- `content`: قاموس المحتوى للغة الحالية
- `LANGUAGES`: قائمة اللغات المتاحة

---

## استخدام المحتوى في القوالب - Using Content in Templates

### قبل (مع i18n):
```django
{% load i18n %}
{% trans "الرئيسية" %}
```

### بعد (النظام الجديد):
```django
{{ content.nav_home }}
```

### مثال كامل - Full Example:
```django
{% extends 'tourism/base.html' %}

{% block content %}
<h1>{{ content.home_hero_title }}</h1>
<p>{{ content.home_hero_subtitle }}</p>
<a href="{% url 'tourism:tour_planner' %}">
    {{ content.home_hero_button }}
</a>
{% endblock %}
```

---

## تبديل اللغة - Language Switching

### في القوالب - In Templates:
```django
<!-- Language Switcher في القائمة -->
<a href="{% url 'tourism:set_language' 'ar' %}">العربية</a>
<a href="{% url 'tourism:set_language' 'en' %}">English</a>

<!-- التحقق من اللغة الحالية -->
{% if LANGUAGE_CODE == 'ar' %}
    <link href="bootstrap.rtl.min.css" rel="stylesheet">
{% else %}
    <link href="bootstrap.min.css" rel="stylesheet">
{% endif %}
```

### في Views:
```python
def set_language(request, lang_code):
    """Switch between Arabic and English"""
    if lang_code in ['ar', 'en']:
        request.session['language'] = lang_code
    return redirect(request.META.get('HTTP_REFERER', '/'))
```

---

## إضافة محتوى جديد - Adding New Content

### 1. أضف إلى content.py:
```python
CONTENT = {
    'ar': {
        # ... محتوى موجود
        'new_key': 'نص جديد بالعربية',
    },
    'en': {
        # ... existing content
        'new_key': 'New text in English',
    }
}
```

### 2. استخدمه في القالب:
```django
{{ content.new_key }}
```

---

## محتوى قاعدة البيانات - Database Content

### المشكلة:
المحتوى في قاعدة البيانات (أسماء الأماكن، الأوصاف) مازال بلغة واحدة.

### الحلول الموصى بها:

#### الحل 1: إضافة حقول للغة الثانية (موصى به)
```python
# في models.py
class TouristPlace(models.Model):
    name = models.CharField(max_length=200)  # عربي
    name_en = models.CharField(max_length=200, blank=True)  # إنجليزي
    
    description = models.TextField()  # عربي
    description_en = models.TextField(blank=True)  # إنجليزي
    
    def get_name(self, lang='ar'):
        if lang == 'en' and self.name_en:
            return self.name_en
        return self.name
```

#### الحل 2: استخدام django-modeltranslation
```bash
pip install django-modeltranslation
```

```python
# في translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import TouristPlace

class TouristPlaceTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description')

translator.register(TouristPlace, TouristPlaceTranslationOptions)
```

---

## اتجاه النص - Text Direction

النظام يدعم RTL و LTR تلقائياً:

```django
<html lang="{{ LANGUAGE_CODE }}" 
      dir="{% if LANGUAGE_CODE == 'ar' %}rtl{% else %}ltr{% endif %}">
```

### Bootstrap:
```django
{% if LANGUAGE_CODE == 'ar' %}
    <link href="bootstrap.rtl.min.css" rel="stylesheet">
{% else %}
    <link href="bootstrap.min.css" rel="stylesheet">
{% endif %}
```

---

## الأيقونات والاتجاهات - Icons and Directions

### الأسهم - Arrows:
```django
<i class="fas fa-arrow-{% if LANGUAGE_CODE == 'ar' %}left{% else %}right{% endif %}"></i>
```

### المحاذاة - Alignment:
```django
<div class="text-{% if LANGUAGE_CODE == 'ar' %}end{% else %}start{% endif %}">
```

---

## لوحة التحكم - Admin Panel

لوحة التحكم Django تبقى بلغة واحدة (عربي أو إنجليزي حسب LANGUAGE_CODE في settings.py).

لتعديل لغة الإدارة:
```python
# في settings.py
LANGUAGE_CODE = 'ar'  # أو 'en'
```

---

## الميزات - Features

✅ **المميزات:**
- نفس قاعدة البيانات للغتين
- نفس لوحة التحكم
- تبديل سهل بين اللغات
- لا حاجة لملفات .po/.mo
- أداء أفضل (لا معالجة ترجمة)
- سهولة الصيانة

❌ **القيود:**
- محتوى قاعدة البيانات يحتاج معالجة منفصلة
- يجب تحديث المحتوى في ملف content.py يدوياً

---

## الملفات المهمة - Important Files

```
egyroute/
├── tourism/
│   ├── content.py              # قاموس المحتوى الثابت
│   ├── context_processors.py  # معالج السياق
│   ├── views.py               # وظيفة set_language
│   └── urls.py                # مسار set-language
├── templates/
│   └── tourism/
│       ├── base.html          # القالب الأساسي + منتقي اللغة
│       └── home.html          # مثال على الاستخدام
└── egyroute/
    └── settings.py            # USE_I18N = False
```

---

## أمثلة الاستخدام - Usage Examples

### 1. نص بسيط - Simple Text:
```django
<h1>{{ content.page_title }}</h1>
```

### 2. نص مع HTML:
```django
<button>
    <i class="fas fa-save"></i>
    {{ content.form_save }}
</button>
```

### 3. شرط بناءً على اللغة - Conditional Based on Language:
```django
{% if LANGUAGE_CODE == 'ar' %}
    <p>محتوى عربي خاص</p>
{% else %}
    <p>Special English content</p>
{% endif %}
```

### 4. في JavaScript:
```django
<script>
    const lang = '{{ LANGUAGE_CODE }}';
    const messages = {
        ar: {
            confirm: 'هل أنت متأكد؟',
            success: 'تم بنجاح'
        },
        en: {
            confirm: 'Are you sure?',
            success: 'Success'
        }
    };
    
    alert(messages[lang].confirm);
</script>
```

---

## التحديثات المستقبلية - Future Updates

### لإضافة لغة ثالثة:
1. أضف اللغة في settings.py:
   ```python
   LANGUAGES = [
       ('ar', 'العربية'),
       ('en', 'English'),
       ('fr', 'Français'),
   ]
   ```

2. أضف المحتوى في content.py:
   ```python
   CONTENT = {
       'ar': {...},
       'en': {...},
       'fr': {...},
   }
   ```

3. حدّث منتقي اللغة في base.html

---

## الدعم - Support

للمساعدة أو الأسئلة:
- راجع الكود في `tourism/content.py`
- تحقق من `tourism/context_processors.py`
- انظر أمثلة في القوالب

---

## ملاحظات مهمة - Important Notes

⚠️ **تذكر:**
1. كل محتوى ثابت جديد يجب إضافته في content.py
2. محتوى قاعدة البيانات يحتاج حقول منفصلة للترجمة
3. استخدم `LANGUAGE_CODE` للتحقق من اللغة الحالية
4. استخدم `content.key` للوصول للمحتوى المترجم
5. منتقي اللغة موجود في base.html في شريط التنقل

---

تم إنشاء هذا الدليل بتاريخ: يناير 2026
Created: January 2026
