"""
Management command to ensure admin user exists
This is useful for automated deployments
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'إنشاء مستخدم admin إذا لم يكن موجوداً'

    def handle(self, *args, **options):
        # Get credentials from environment or use defaults
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@egyroute.com')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin@123456')

        # Check if admin already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'⚠️  المستخدم {username} موجود بالفعل')
            )
            return

        # Create superuser
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ تم إنشاء admin بنجاح!')
            )
            self.stdout.write(f'   Username: {username}')
            self.stdout.write(f'   Email: {email}')
            if os.environ.get('DEBUG', 'True') == 'True':
                self.stdout.write(f'   Password: {password}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ خطأ في إنشاء admin: {str(e)}')
            )
