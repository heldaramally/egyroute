"""
Script to create or reset admin user password
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egyroute.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check existing superusers
superusers = User.objects.filter(is_superuser=True)
print(f"\n{'='*50}")
print(f"عدد مديري النظام الموجودين: {superusers.count()}")
print(f"{'='*50}\n")

if superusers.exists():
    print("مديرو النظام الموجودون:")
    for i, user in enumerate(superusers, 1):
        print(f"{i}. اسم المستخدم: {user.username}")
        print(f"   البريد: {user.email}")
        print(f"   نشط: {'نعم' if user.is_active else 'لا'}")
        print()
    
    print("\nخيارات:")
    print("1. إعادة تعيين كلمة مرور مستخدم موجود")
    print("2. إنشاء مدير نظام جديد")
    choice = input("\nاختر (1 أو 2): ").strip()
    
    if choice == '1':
        username = input("أدخل اسم المستخدم: ").strip()
        try:
            user = User.objects.get(username=username, is_superuser=True)
            new_password = input("أدخل كلمة المرور الجديدة: ")
            user.set_password(new_password)
            user.save()
            print(f"\n✅ تم تغيير كلمة المرور بنجاح لـ: {username}")
            print(f"   اسم المستخدم: {username}")
            print(f"   كلمة المرور: {new_password}")
        except User.DoesNotExist:
            print(f"\n❌ المستخدم '{username}' غير موجود")
    elif choice == '2':
        print("\n--- إنشاء مدير نظام جديد ---")
        username = input("اسم المستخدم: ").strip()
        email = input("البريد الإلكتروني: ").strip()
        password = input("كلمة المرور: ")
        
        if User.objects.filter(username=username).exists():
            print(f"\n❌ المستخدم '{username}' موجود بالفعل")
        else:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"\n✅ تم إنشاء مدير النظام بنجاح!")
            print(f"   اسم المستخدم: {username}")
            print(f"   البريد: {email}")
            print(f"   كلمة المرور: {password}")
else:
    print("لا يوجد مديرو نظام!")
    print("\n--- إنشاء مدير نظام جديد ---")
    username = input("اسم المستخدم (اتركه فارغاً لاستخدام 'admin'): ").strip() or 'admin'
    email = input("البريد الإلكتروني (اتركه فارغاً لاستخدام 'admin@egyroute.com'): ").strip() or 'admin@egyroute.com'
    password = input("كلمة المرور (اتركها فارغة لاستخدام 'admin123'): ").strip() or 'admin123'
    
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"\n✅ تم إنشاء مدير النظام بنجاح!")
    print(f"   اسم المستخدم: {username}")
    print(f"   البريد: {email}")
    print(f"   كلمة المرور: {password}")

print(f"\n{'='*50}")
print("يمكنك الآن تسجيل الدخول في:")
print("http://127.0.0.1:8000/admin/")
print(f"{'='*50}\n")
