# 🚀 دليل النشر للإنتاج - EgyRoute

هذا الدليل يشرح كيفية نشر موقع EgyRoute على خادم إنتاج.

## المتطلبات

- ✅ خادم Linux (Ubuntu 20.04+ موصى به)
- ✅ Python 3.10+
- ✅ PostgreSQL 12+
- ✅ Nginx
- ✅ Gunicorn
- ✅ Supervisor (لإدارة العمليات)
- ✅ Domain name

---

## الخطوة 1: إعداد الخادم

### تحديث النظام

```bash
sudo apt update
sudo apt upgrade -y
```

### تثبيت المتطلبات

```bash
# Python والمكتبات
sudo apt install python3-pip python3-venv python3-dev -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Nginx
sudo apt install nginx -y

# Supervisor
sudo apt install supervisor -y

# مكتبات إضافية
sudo apt install libpq-dev build-essential -y
```

---

## الخطوة 2: إعداد قاعدة البيانات

### إنشاء قاعدة بيانات PostgreSQL

```bash
# الدخول إلى PostgreSQL
sudo -u postgres psql

# إنشاء قاعدة البيانات والمستخدم
CREATE DATABASE egyroute_db;
CREATE USER egyroute_user WITH PASSWORD 'your_strong_password_here';
ALTER ROLE egyroute_user SET client_encoding TO 'utf8';
ALTER ROLE egyroute_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE egyroute_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE egyroute_db TO egyroute_user;
\q
```

---

## الخطوة 3: رفع المشروع

### استنساخ المشروع

```bash
# إنشاء مجلد للمشروع
sudo mkdir -p /var/www/egyroute
sudo chown $USER:$USER /var/www/egyroute

# الانتقال للمجلد
cd /var/www/egyroute

# استنساخ المشروع (أو رفع الملفات)
# إذا كنت تستخدم Git:
git clone https://github.com/your-username/egyroute.git .

# أو ارفع الملفات باستخدام SCP/FTP
```

### إنشاء البيئة الافتراضية

```bash
python3 -m venv venv
source venv/bin/activate
```

### تثبيت المتطلبات

```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

---

## الخطوة 4: إعداد الإعدادات

### إنشاء ملف .env

```bash
nano .env
```

أضف:

```env
SECRET_KEY=your-very-long-and-random-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# Database
DATABASE_NAME=egyroute_db
DATABASE_USER=egyroute_user
DATABASE_PASSWORD=your_strong_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432

# WhatsApp
WHATSAPP_NUMBER=201234567890

# Google Maps (Optional)
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

### تحديث settings.py للإنتاج

أضف في `egyroute/settings.py`:

```python
import os
from decouple import config

# Database for production
if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD'),
            'HOST': config('DATABASE_HOST', default='localhost'),
            'PORT': config('DATABASE_PORT', default='5432'),
        }
    }
```

---

## الخطوة 5: تجهيز Django

### تطبيق Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### إنشاء Superuser

```bash
python manage.py createsuperuser
```

### جمع الملفات الثابتة

```bash
python manage.py collectstatic --noinput
```

### تحميل البيانات التجريبية (اختياري)

```bash
python manage.py load_sample_data
```

---

## الخطوة 6: إعداد Gunicorn

### إنشاء ملف socket

```bash
sudo nano /etc/systemd/system/egyroute.socket
```

أضف:

```ini
[Unit]
Description=egyroute socket

[Socket]
ListenStream=/run/egyroute.sock

[Install]
WantedBy=sockets.target
```

### إنشاء ملف service

```bash
sudo nano /etc/systemd/system/egyroute.service
```

أضف:

```ini
[Unit]
Description=EgyRoute Django Application
Requires=egyroute.socket
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/var/www/egyroute
Environment="PATH=/var/www/egyroute/venv/bin"
ExecStart=/var/www/egyroute/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/egyroute.sock \
          egyroute.wsgi:application

[Install]
WantedBy=multi-user.target
```

### تفعيل الخدمة

```bash
sudo systemctl start egyroute.socket
sudo systemctl enable egyroute.socket
sudo systemctl start egyroute.service
sudo systemctl enable egyroute.service

# التحقق من الحالة
sudo systemctl status egyroute.service
```

---

## الخطوة 7: إعداد Nginx

### إنشاء ملف إعدادات Nginx

```bash
sudo nano /etc/nginx/sites-available/egyroute
```

أضف:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 10M;
    
    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias /var/www/egyroute/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /var/www/egyroute/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/egyroute.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

### تفعيل الموقع

```bash
# إنشاء رابط رمزي
sudo ln -s /etc/nginx/sites-available/egyroute /etc/nginx/sites-enabled/

# اختبار الإعدادات
sudo nginx -t

# إعادة تشغيل Nginx
sudo systemctl restart nginx
```

---

## الخطوة 8: إعداد SSL (HTTPS)

### استخدام Let's Encrypt

```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx -y

# الحصول على شهادة SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# التجديد التلقائي
sudo certbot renew --dry-run
```

---

## الخطوة 9: إعدادات الأمان

### إعدادات Firewall

```bash
# السماح بـ SSH, HTTP, HTTPS
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### تأمين PostgreSQL

```bash
sudo nano /etc/postgresql/12/main/pg_hba.conf

# غيّر من trust إلى md5
local   all             all                                     md5
```

### صلاحيات الملفات

```bash
sudo chown -R www-data:www-data /var/www/egyroute
sudo chmod -R 755 /var/www/egyroute
sudo chmod -R 775 /var/www/egyroute/media
```

---

## الخطوة 10: النسخ الاحتياطي

### نسخ احتياطي لقاعدة البيانات

```bash
# إنشاء نسخة احتياطية
pg_dump -U egyroute_user egyroute_db > backup_$(date +%Y%m%d).sql

# استعادة من نسخة احتياطية
psql -U egyroute_user egyroute_db < backup_20260120.sql
```

### نسخ احتياطي للملفات

```bash
# نسخ احتياطي للـ media
tar -czf media_backup_$(date +%Y%m%d).tar.gz /var/www/egyroute/media/

# نسخ احتياطي للمشروع
tar -czf egyroute_backup_$(date +%Y%m%d).tar.gz /var/www/egyroute/
```

### أتمتة النسخ الاحتياطي

```bash
# إضافة cron job
crontab -e

# نسخ احتياطي يومي في الساعة 2 صباحاً
0 2 * * * pg_dump -U egyroute_user egyroute_db > /backups/egyroute_$(date +\%Y\%m\%d).sql
```

---

## الخطوة 11: المراقبة والصيانة

### مراقبة السجلات

```bash
# سجلات Django/Gunicorn
sudo journalctl -u egyroute.service -f

# سجلات Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### إعادة التشغيل بعد التحديثات

```bash
# بعد تحديث الكود
cd /var/www/egyroute
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart egyroute.service
```

---

## استكشاف الأخطاء

### خطأ 502 Bad Gateway

```bash
# تحقق من حالة Gunicorn
sudo systemctl status egyroute.service

# تحقق من السجلات
sudo journalctl -u egyroute.service --since today

# تحقق من الصلاحيات
sudo chown -R www-data:www-data /var/www/egyroute
```

### خطأ Static Files

```bash
# تأكد من جمع الملفات
python manage.py collectstatic --noinput

# تحقق من المسار في Nginx
sudo nginx -t
```

### مشاكل Database

```bash
# تحقق من اتصال PostgreSQL
sudo systemctl status postgresql

# اختبار الاتصال
psql -U egyroute_user -d egyroute_db -h localhost
```

---

## قائمة التحقق النهائية

- [ ] DEBUG = False
- [ ] SECRET_KEY محدث وآمن
- [ ] ALLOWED_HOSTS محدث
- [ ] Database في PostgreSQL
- [ ] Static files تم جمعها
- [ ] Media files لها صلاحيات صحيحة
- [ ] SSL/HTTPS مفعّل
- [ ] Firewall مضبوط
- [ ] Backups مجدولة
- [ ] Monitoring مفعّل
- [ ] DNS يشير للسيرفر

---

## موارد إضافية

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**نجح النشر! 🎉**

موقعك الآن جاهز على: https://yourdomain.com
