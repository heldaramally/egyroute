# ❓ الأسئلة الشائعة (FAQ) - EgyRoute

## 🚀 التثبيت والإعداد

### كيف أبدأ المشروع لأول مرة؟

اتبع الخطوات في [QUICKSTART.md](QUICKSTART.md) أو شغّل:

**Windows:**
```powershell
.\setup.ps1
```

**Linux/Mac:**
```bash
bash setup.sh
```

### ما هي متطلبات النظام؟

- Python 3.10 أو أحدث
- مساحة 500 MB على الأقل
- 2 GB RAM (موصى به)
- نظام Windows/Linux/Mac

### خطأ "python not found"

تأكد من تثبيت Python وإضافته إلى PATH:
```powershell
# Windows
python --version

# Linux/Mac
python3 --version
```

---

## 🗄️ قاعدة البيانات

### هل يمكنني استخدام MySQL بدلاً من SQLite؟

نعم! عدّل في `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'egyroute_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

ثم ثبّت:
```bash
pip install mysqlclient
```

### كيف أعمل نسخة احتياطية من البيانات؟

**SQLite:**
```bash
# نسخ ملف db.sqlite3
Copy-Item db.sqlite3 backups/db_backup_$(Get-Date -Format 'yyyyMMdd').sqlite3
```

**PostgreSQL:**
```bash
pg_dump -U user egyroute_db > backup.sql
```

### كيف أحذف جميع البيانات وأبدأ من جديد؟

```powershell
# احذف قاعدة البيانات
Remove-Item db.sqlite3

# أعد إنشاءها
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_data
```

---

## 🎨 التخصيص

### كيف أغير الألوان؟

عدّل في `templates/tourism/base.html` في قسم `<style>`:

```css
:root {
    --primary-color: #c4953b;      /* لونك الجديد */
    --secondary-color: #8b6914;
    /* ... */
}
```

### كيف أغير الشعار؟

عدّل في `templates/tourism/base.html`:

```html
<a class="navbar-brand" href="{% url 'tourism:home' %}">
    <i class="fas fa-route"></i> اسمك هنا
</a>
```

### كيف أضيف لغة إنجليزية؟

هذا يتطلب:
1. تفعيل i18n في Django
2. ترجمة جميع النصوص
3. إنشاء templates منفصلة

سيتم إضافته في نسخة مستقبلية.

---

## 🖼️ الصور والملفات

### ما هو الحجم الأمثل للصور؟

- **الأبعاد:** 1200x800 بكسل (نسبة 3:2)
- **التنسيق:** JPG للصور، PNG للشعارات
- **حجم الملف:** أقل من 2 MB

### كيف أضغط الصور؟

استخدم أدوات مثل:
- [TinyPNG](https://tinypng.com/)
- [Squoosh](https://squoosh.app/)
- [ImageOptim](https://imageoptim.com/) (Mac)

### الصور لا تظهر في الموقع

تحقق من:
1. وجود مجلد `media/`
2. إعدادات MEDIA_URL في settings.py
3. الصلاحيات على مجلد media

```python
# في settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 🗺️ الخرائط

### كيف أحصل على إحداثيات GPS؟

1. افتح [Google Maps](https://maps.google.com)
2. ابحث عن الموقع
3. اضغط بالزر الأيمن على المكان
4. اختر "ما هنا؟"
5. انسخ الأرقام (مثال: 29.9792, 31.1342)

### هل أحتاج Google Maps API؟

لا! نستخدم OpenStreetMap (Leaflet) المجاني افتراضياً.

لكن يمكنك استخدام Google Maps بإضافة API Key في `.env`:
```env
GOOGLE_MAPS_API_KEY=your-api-key-here
```

### الخريطة لا تظهر

تحقق من:
1. وجود latitude و longitude للموقع
2. اتصال بالإنترنت
3. عدم حظر Leaflet CDN

---

## 📱 WhatsApp

### كيف أغير رقم WhatsApp؟

في ملف `.env`:
```env
WHATSAPP_NUMBER=201234567890
# الصيغة: رمز الدولة + الرقم بدون أصفار أو علامات
```

### الرسالة الافتراضية في WhatsApp

عدّل في `templates/tourism/base.html`:

```html
<a href="https://wa.me/{{ WHATSAPP_NUMBER }}?text=رسالتك هنا">
```

---

## 👨‍💼 لوحة التحكم (Admin)

### نسيت كلمة مرور المدير

```bash
python manage.py changepassword admin_username
```

### كيف أضيف مستخدم إداري آخر؟

```bash
python manage.py createsuperuser
```

### كيف أخصص لوحة التحكم؟

عدّل في `tourism/admin.py` - تحديداً في classes المنتهية بـ `Admin`.

### كيف أغير شعار لوحة التحكم؟

في `egyroute/urls.py`:
```python
admin.site.site_header = 'شعارك هنا'
admin.site.site_title = 'عنوانك'
admin.site.index_title = 'العنوان الرئيسي'
```

---

## 🔍 البحث والفلترة

### كيف أحسّن البحث؟

حالياً يبحث في:
- اسم الموقع
- الوصف
- المدينة

لإضافة حقول أخرى، عدّل في `tourism/views.py`:

```python
places_list = places_list.filter(
    Q(name__icontains=search_query) |
    Q(description__icontains=search_query) |
    Q(city__icontains=search_query) |
    Q(governorate__name__icontains=search_query)  # إضافة
)
```

---

## 🚀 الأداء

### الموقع بطيء، كيف أحسّن الأداء؟

1. **تفعيل Caching:**
   ```python
   # في settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

2. **تحسين الاستعلامات:**
   ```python
   # استخدم select_related و prefetch_related
   places = TouristPlace.objects.select_related('category', 'governorate')
   ```

3. **ضغط الصور**

4. **استخدام CDN للملفات الثابتة**

### كيف أقلل استهلاك الذاكرة؟

- قلل عدد workers في Gunicorn
- استخدم pagination
- احذف الصور غير المستخدمة

---

## 🔒 الأمان

### كيف أؤمّن الموقع؟

1. **غيّر SECRET_KEY في الإنتاج**
2. **عطّل DEBUG**
   ```python
   DEBUG = False
   ```
3. **استخدم HTTPS**
4. **حدّث Django بانتظام**
5. **استخدم كلمات مرور قوية**

### كيف أمنع الـ SQL Injection؟

Django يحمي تلقائياً باستخدام ORM. تجنب استخدام:
```python
# خطأ ❌
cursor.execute("SELECT * FROM table WHERE id = " + user_input)

# صحيح ✅
Model.objects.filter(id=user_input)
```

---

## 📊 البيانات

### كيف أستورد بيانات من Excel؟

استخدم مكتبة pandas:

```python
import pandas as pd
from tourism.models import TouristPlace

df = pd.read_excel('places.xlsx')
for _, row in df.iterrows():
    TouristPlace.objects.create(
        name=row['name'],
        # ... باقي الحقول
    )
```

### كيف أصدّر البيانات؟

من لوحة التحكم أو باستخدام:

```bash
python manage.py dumpdata tourism > data.json
```

---

## 🌐 النشر

### أين يمكنني نشر الموقع؟

خيارات مجانية:
- **PythonAnywhere** (سهل للمبتدئين)
- **Heroku** (مجاني محدود)
- **Railway**
- **Render**

خيارات مدفوعة:
- **DigitalOcean**
- **AWS**
- **Google Cloud**
- **Azure**

### كيف أنشر على PythonAnywhere؟

1. أنشئ حساب على [PythonAnywhere](https://www.pythonanywhere.com/)
2. Upload الملفات
3. اتبع [دليلهم](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)

### كيف أنشر على خادم خاص؟

اتبع [DEPLOYMENT.md](DEPLOYMENT.md) للتعليمات الكاملة.

---

## 📧 التواصل والدعم

### كيف أضيف نموذج اتصال email؟

ستحتاج لإعداد SMTP في `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

ثم في `views.py`:
```python
from django.core.mail import send_mail

send_mail(
    'موضوع',
    'الرسالة',
    'from@example.com',
    ['to@example.com'],
)
```

---

## 🐛 استكشاف الأخطاء

### خطأ "CSRF verification failed"

تأكد من وجود `{% csrf_token %}` في جميع forms:
```html
<form method="post">
    {% csrf_token %}
    <!-- حقول النموذج -->
</form>
```

### خطأ "TemplateDoesNotExist"

تحقق من:
1. مسار التيمبلت صحيح
2. TEMPLATES في settings.py مضبوط
3. اسم الملف صحيح (case-sensitive في Linux)

### خطأ "No module named ..."

```bash
# تأكد من تفعيل البيئة الافتراضية
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# ثم ثبت المكتبة
pip install module-name
```

---

## 💡 نصائح عامة

### أفضل ممارسات

✅ عمل commit منتظم للكود
✅ نسخ احتياطية دورية
✅ اختبار قبل النشر
✅ توثيق التغييرات
✅ استخدام .gitignore
✅ عدم رفع .env إلى Git

### موارد مفيدة

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap RTL](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Leaflet](https://leafletjs.com/)

---

## 🆘 لم تجد إجابة؟

1. راجع [README.md](README.md)
2. افتح [Issue](https://github.com/your-repo/egyroute/issues) على GitHub
3. تواصل عبر WhatsApp (إن وُجد)

---

**آخر تحديث:** يناير 2026

هل لديك سؤال غير موجود؟ افتح Issue وسنضيفه! 🎯
