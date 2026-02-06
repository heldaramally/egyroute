"""
URL configuration for egyroute project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', include('tourism.urls')),
    prefix_default_language=True,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = _('إدارة موقع مصر السياحي')
admin.site.site_title = _('لوحة التحكم')
admin.site.index_title = _('مرحباً بك في لوحة التحكم')
