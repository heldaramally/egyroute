# 🚀 دليل التشغيل السريع - EgyRoute

## تشغيل المشروع لأول مرة

### 1. إنشاء البيئة الافتراضية
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. تثبيت المتطلبات
```powershell
pip install -r requirements.txt
```

### 3. إعداد ملف البيئة
```powershell
Copy-Item .env.example .env
```

### 4. تطبيق قاعدة البيانات
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. إنشاء حساب المدير
```powershell
python manage.py createsuperuser
```

### 6. تحميل البيانات التجريبية
```powershell
python manage.py load_sample_data
```

### 7. تشغيل السيرفر
```powershell
python manage.py runserver
```

## 🌐 الروابط المهمة

- **الموقع:** http://127.0.0.1:8000/
- **لوحة التحكم:** http://127.0.0.1:8000/admin/

## ⚡ أوامر مفيدة

### إنشاء تطبيق جديد
```powershell
python manage.py startapp app_name
```

### إنشاء migrations جديدة
```powershell
python manage.py makemigrations
```

### تطبيق migrations
```powershell
python manage.py migrate
```

### جمع الملفات الثابتة
```powershell
python manage.py collectstatic
```

### إنشاء superuser جديد
```powershell
python manage.py createsuperuser
```

### تشغيل shell
```powershell
python manage.py shell
```

### فحص المشروع
```powershell
python manage.py check
```

## 🔧 حل المشاكل الشائعة

### خطأ: "No module named 'django'"
```powershell
pip install -r requirements.txt
```

### خطأ: "ERRORS: ... table already exists"
```powershell
python manage.py migrate --fake-initial
```

### مشكلة في الصور
تأكد من وجود مجلد `media/` في المشروع

### خطأ في Static Files
```powershell
python manage.py collectstatic --clear
```

## 📝 ملاحظات

1. تأكد من تفعيل البيئة الافتراضية دائماً قبل العمل
2. لا تنسَ تحديث `.env` بمعلوماتك الخاصة
3. قم بعمل backup منتظم لقاعدة البيانات
4. راجع ملف README.md للتفاصيل الكاملة

---

**تم إنشاؤه بواسطة EgyRoute Team 🇪🇬**
