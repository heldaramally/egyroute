# تحديث النظام الثنائي اللغة - Bilingual System Update

## التحديثات الجديدة - New Updates

تم إضافة دعم كامل للمحتوى الإنجليزي في قاعدة البيانات!

### ✅ ما تم إضافته:

#### 1. حقول إنجليزية جديدة في Models:

**Category (القسم السياحي):**
- `description_en`: الوصف بالإنجليزية
- وظيفة `get_name(lang)` و `get_description(lang)`

**Governorate (المحافظة):**
- حقل `name_en` موجود مسبقاً
- وظيفة `get_name(lang)`

**TouristPlace (الموقع السياحي):**
- `city_en`: المدينة بالإنجليزية
- `short_description_en`: الوصف المختصر بالإنجليزية
- `description_en`: الوصف التفصيلي بالإنجليزية
- `visitor_tips_en`: نصائح الزائر بالإنجليزية
- `best_time_to_visit_en`: أفضل وقت للزيارة بالإنجليزية
- `entry_fee_en`: رسوم الدخول بالإنجليزية

**PlaceImage (صورة الموقع):**
- `caption_en`: عنوان الصورة بالإنجليزية
- وظيفة `get_caption(lang)`

#### 2. Template Tags جديدة:

ملف: `tourism/templatetags/localization_tags.py`

```django
{% load localization_tags %}

<!-- استخدام في القوالب -->
{% get_localized_field place 'name' %}
{% get_localized_field category 'description' %}
```

#### 3. تحديث القوالب:

- ✅ **base.html**: Footer يتغير حسب اللغة
- ✅ **home.html**: جميع البيانات تعرض باللغة المناسبة

---

## كيفية استخدام النظام الجديد:

### في لوحة التحكم (Django Admin):

1. اذهب إلى لوحة التحكم: `http://127.0.0.1:8000/admin/`
2. افتح أي موقع سياحي أو قسم
3. املأ الحقول الإنجليزية:
   - **Name (English)**: الاسم بالإنجليزية
   - **Description (English)**: الوصف بالإنجليزية
   - **Short Description (English)**: وصف مختصر بالإنجليزية
   - **City (English)**: المدينة بالإنجليزية
   - وغيرها...

### في القوالب (Templates):

#### الطريقة 1: استخدام Template Tag (موصى به)

```django
{% load localization_tags %}

<!-- للأسماء -->
<h1>{% get_localized_field place 'name' %}</h1>

<!-- للوصف -->
<p>{% get_localized_field place 'description' %}</p>

<!-- للمدينة -->
<span>{% get_localized_field place 'city' %}</span>

<!-- للقسم -->
<span>{% get_localized_field place.category 'name' %}</span>

<!-- للمحافظة -->
<span>{% get_localized_field place.governorate 'name' %}</span>
```

#### الطريقة 2: استخدام الوظائف مباشرة

```django
<!-- في Python View -->
def my_view(request):
    lang = request.session.get('language', 'ar')
    place = TouristPlace.objects.first()
    
    name = place.get_name(lang)
    description = place.get_description(lang)
    
    return render(request, 'template.html', {
        'name': name,
        'description': description
    })

<!-- في القالب -->
<h1>{{ name }}</h1>
<p>{{ description }}</p>
```

---

## الحقول المتاحة للترجمة:

### Category:
- `name` / `name_en`
- `description` / `description_en`

### Governorate:
- `name` / `name_en`

### TouristPlace:
- `name` / `name_en`
- `city` / `city_en`
- `short_description` / `short_description_en`
- `description` / `description_en`
- `visitor_tips` / `visitor_tips_en`
- `best_time_to_visit` / `best_time_to_visit_en`
- `entry_fee` / `entry_fee_en`

### PlaceImage:
- `caption` / `caption_en`

---

## مثال عملي كامل:

### 1. في لوحة التحكم:

```
الموقع السياحي: أهرامات الجيزة
----------------------------
Name: أهرامات الجيزة
Name (English): Giza Pyramids

Short Description: من عجائب الدنيا السبع القديمة
Short Description (English): One of the Seven Wonders of the Ancient World

Description: الأهرامات هي مقابر ملكية...
Description (English): The Pyramids are royal tombs...

City: الجيزة
City (English): Giza
```

### 2. في القالب:

```django
{% load localization_tags %}

<div class="place-card">
    <h2>{% get_localized_field place 'name' %}</h2>
    <!-- سيعرض: "أهرامات الجيزة" بالعربي أو "Giza Pyramids" بالإنجليزي -->
    
    <p class="short-desc">{% get_localized_field place 'short_description' %}</p>
    <!-- سيعرض الوصف المختصر المناسب -->
    
    <div class="location">
        <i class="fas fa-map-marker"></i>
        {% get_localized_field place 'city' %}, 
        {% get_localized_field place.governorate 'name' %}
    </div>
    <!-- سيعرض: "الجيزة, الجيزة" بالعربي أو "Giza, Giza" بالإنجليزي -->
    
    <div class="description">
        {% get_localized_field place 'description' as desc %}
        {{ desc|safe }}
    </div>
</div>
```

---

## القوالب التي تحتاج تحديث:

الصفحات التالية تحتاج إضافة `{% load localization_tags %}` واستخدام `{% get_localized_field %}`:

- [ ] `category_detail.html`
- [ ] `place_detail.html`
- [ ] `governorate_detail.html`
- [ ] `governorates_list.html`
- [ ] `all_places.html`
- [ ] `tour_planner.html`
- [ ] `saved_places.html`
- [ ] `trip_plan_detail.html`

---

## خطوات تحديث أي قالب:

### 1. أضف في أول السطر:
```django
{% load localization_tags %}
```

### 2. استبدل:
```django
<!-- قبل -->
{{ place.name }}
{{ place.description }}
{{ category.name }}

<!-- بعد -->
{% get_localized_field place 'name' %}
{% get_localized_field place 'description' %}
{% get_localized_field category 'name' %}
```

---

## الوظائف المتاحة في Models:

### Category:
```python
category.get_name('ar')  # or 'en'
category.get_description('ar')  # or 'en'
```

### Governorate:
```python
governorate.get_name('ar')  # or 'en'
```

### TouristPlace:
```python
place.get_name('ar')
place.get_city('ar')
place.get_short_description('ar')
place.get_description('ar')
place.get_visitor_tips('ar')
place.get_best_time('ar')
place.get_entry_fee('ar')
```

### PlaceImage:
```python
image.get_caption('ar')
```

---

## Context Processors المحدثة:

الآن يتوفر في جميع القوالب:

- `LANGUAGE_CODE`: 'ar' أو 'en'
- `is_arabic`: True إذا كانت اللغة عربية
- `is_english`: True إذا كانت اللغة إنجليزية
- `content`: قاموس المحتوى الثابت

```django
{% if is_english %}
    <!-- English content -->
{% else %}
    <!-- محتوى عربي -->
{% endif %}
```

---

## ملاحظات مهمة:

### ⚠️ الحقول الإنجليزية اختيارية:
- إذا لم تملأ الحقل الإنجليزي، سيعرض المحتوى العربي
- يُفضل ملء جميع الحقول للحصول على تجربة أفضل

### 📝 في لوحة التحكم:
1. جميع الحقول الإنجليزية ظاهرة الآن
2. يمكنك تعديل المحتوى القديم وإضافة الترجمة الإنجليزية
3. عند إضافة موقع جديد، املأ الحقول العربية والإنجليزية معاً

### 🔄 الترحيل (Migration):
- تم إنشاء migration جديدة: `0003_category_description_en_placeimage_caption_en_and_more.py`
- جميع الحقول الجديدة `blank=True` فلن تحتاج لملء بيانات قديمة

---

## اختبار النظام:

### 1. تشغيل الخادم:
```bash
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### 2. التبديل للإنجليزية:
- افتح الموقع
- اضغط على 🌐 في القائمة
- اختر "English"

### 3. التحقق:
- Footer يجب أن يكون بالإنجليزية
- الصفحة الرئيسية تعرض المحتوى الإنجليزي
- إذا ملأت حقول إنجليزية في لوحة التحكم، ستظهر هنا

---

## الخطوات التالية:

1. ✅ **املأ المحتوى الإنجليزي في لوحة التحكم**
   - ابدأ بالأقسام (Categories)
   - ثم المحافظات (Governorates)
   - ثم الأماكن السياحية (Tourist Places)

2. ⏳ **حدّث باقي القوالب**
   - استخدم نفس الطريقة المستخدمة في home.html
   - أضف `{% load localization_tags %}`
   - استبدل الحقول المباشرة بـ `{% get_localized_field %}`

3. ⏳ **اختبر جميع الصفحات**
   - تأكد من ظهور المحتوى الصحيح
   - تأكد من عدم وجود أخطاء

---

**تم التحديث:** يناير 2026  
**الحالة:** النظام جاهز! يحتاج فقط ملء المحتوى الإنجليزي في لوحة التحكم 🎉
