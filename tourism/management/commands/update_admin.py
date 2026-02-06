"""
Management command to update admin user
Usage:
    python manage.py update_admin --username admin --password new_password
    python manage.py update_admin --username admin --email new@email.com
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'تحديث بيانات مستخدم admin'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='اسم المستخدم')
        parser.add_argument('--password', type=str, help='كلمة المرور الجديدة')
        parser.add_argument('--email', type=str, help='البريد الإلكتروني الجديد')
        parser.add_argument('--new-username', type=str, help='اسم مستخدم جديد')

    def handle(self, *args, **options):
        username = options.get('username', 'admin')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"❌ المستخدم '{username}' غير موجود")

        updated = False

        # تحديث كلمة المرور
        if options.get('password'):
            user.set_password(options['password'])
            self.stdout.write(self.style.SUCCESS(f'✅ تم تحديث كلمة المرور'))
            updated = True

        # تحديث البريد الإلكتروني
        if options.get('email'):
            user.email = options['email']
            self.stdout.write(self.style.SUCCESS(f'✅ تم تحديث البريد الإلكتروني'))
            updated = True

        # تحديث اسم المستخدم
        if options.get('new_username'):
            if User.objects.filter(username=options['new_username']).exists():
                raise CommandError(f"❌ اسم المستخدم '{options['new_username']}' موجود بالفعل")
            user.username = options['new_username']
            self.stdout.write(self.style.SUCCESS(f'✅ تم تحديث اسم المستخدم'))
            updated = True

        if updated:
            user.save()
            self.stdout.write(self.style.SUCCESS('\n✅ تم الحفظ بنجاح!'))
            self.stdout.write(f'\n📋 البيانات الحالية:')
            self.stdout.write(f'   اسم المستخدم: {user.username}')
            self.stdout.write(f'   البريد: {user.email}')
        else:
            self.stdout.write(self.style.WARNING('⚠️ لم يتم تحديد أي بيانات للتحديث'))
