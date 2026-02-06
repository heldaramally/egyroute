from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    Category, Governorate, TouristPlace, 
    PlaceImage, TourProgram, TourProgramDay, ContactMessage,
    UserProfile, SavedPlace, UserTripPlan, TripPlanDay
)


class PlaceImageInline(admin.TabularInline):
    """Inline لإضافة صور متعددة للموقع السياحي"""
    model = PlaceImage
    extra = 1
    fields = ['image', 'caption', 'caption_en', 'is_main', 'order']
    classes = ['collapse']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """لوحة تحكم الأقسام السياحية"""
    list_display = ['name', 'name_en', 'icon_display', 'places_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_en', 'description']
    prepopulated_fields = {'slug': ('name_en',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('المعلومات الأساسية'), {
            'fields': ('name', 'name_en', 'slug', 'icon')
        }),
        (_('الوصف'), {
            'fields': ('description', 'description_en')
        }),
        (_('الإعدادات'), {
            'fields': ('order', 'is_active')
        }),
        (_('معلومات إضافية'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def icon_display(self, obj):
        """عرض الأيقونة"""
        return format_html(f'<i class="fas {obj.icon} fa-2x"></i>')
    icon_display.short_description = _('الأيقونة')

    def places_count(self, obj):
        """عدد المواقع"""
        count = obj.get_places_count()
        return format_html(f'<strong>{count}</strong>')
    places_count.short_description = _('عدد المواقع')


@admin.register(Governorate)
class GovernorateAdmin(admin.ModelAdmin):
    """لوحة تحكم المحافظات"""
    list_display = ['name', 'name_en', 'places_count', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name_en',)}

    def places_count(self, obj):
        """عدد المواقع في المحافظة"""
        count = obj.places.filter(is_active=True).count()
        return format_html(f'<strong>{count}</strong>')
    places_count.short_description = _('عدد المواقع')


@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    """لوحة تحكم المواقع السياحية"""
    list_display = [
        'name', 
        'category', 
        'governorate', 
        'city',
        'priority',
        'is_featured',
        'is_active',
        'view_count',
        'image_preview'
    ]
    list_editable = ['priority', 'is_featured', 'is_active']
    list_filter = [
        'category', 
        'governorate', 
        'is_featured', 
        'is_active',
        'suggested_duration',
        'created_at'
    ]
    search_fields = ['name', 'name_en', 'description', 'city']
    prepopulated_fields = {'slug': ('name_en',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'map_preview']
    inlines = [PlaceImageInline]
    autocomplete_fields = ['category', 'governorate']
    
    fieldsets = (
        ('المعلومات الأساسية - Basic Information', {
            'fields': (
                ('name', 'name_en'),
                'slug',
                'category',
                'governorate',
                ('city', 'city_en')
            )
        }),
        ('الوصف - Description', {
            'fields': (
                'short_description',
                'short_description_en',
                'description',
                'description_en'
            )
        }),
        ('الموقع الجغرافي - Location', {
            'fields': ('latitude', 'longitude', 'map_preview'),
            'classes': ('wide',)
        }),
        ('معلومات الزيارة - Visit Information', {
            'fields': (
                'suggested_duration',
                ('best_time_to_visit', 'best_time_to_visit_en'),
                ('entry_fee', 'entry_fee_en'),
                'visitor_tips',
                'visitor_tips_en'
            )
        }),
        ('الإعدادات - Settings', {
            'fields': ('priority', 'is_featured', 'is_active')
        }),
        ('الإحصائيات - Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """معاينة الصورة الرئيسية"""
        main_image = obj.get_main_image()
        if main_image and main_image.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                main_image.image.url
            )
        return '—'
    image_preview.short_description = 'الصورة'

    def map_preview(self, obj):
        """معاينة الخريطة"""
        if obj.latitude and obj.longitude:
            return format_html(
                '<div style="width: 100%; height: 300px;">'
                '<iframe width="100%" height="300" frameborder="0" style="border:0" '
                'src="https://www.openstreetmap.org/export/embed.html?bbox={},{},{},{}&layer=mapnik&marker={},{}" '
                'allowfullscreen></iframe>'
                '<br/><small><a href="https://www.google.com/maps?q={},{}" target="_blank">فتح في Google Maps</a></small>'
                '</div>',
                float(obj.longitude) - 0.01, float(obj.latitude) - 0.01,
                float(obj.longitude) + 0.01, float(obj.latitude) + 0.01,
                obj.latitude, obj.longitude,
                obj.latitude, obj.longitude
            )
        return 'لم يتم تحديد الموقع الجغرافي'
    map_preview.short_description = 'معاينة الخريطة'

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',)
        }


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    """لوحة تحكم صور المواقع"""
    list_display = ['place', 'caption', 'is_main', 'order', 'image_preview', 'uploaded_at']
    list_editable = ['is_main', 'order']
    list_filter = ['is_main', 'place__category', 'uploaded_at']
    search_fields = ['place__name', 'caption', 'caption_en']
    
    fieldsets = (
        ('معلومات الصورة', {
            'fields': ('place', 'image', ('caption', 'caption_en'), 'is_main', 'order')
        }),
    )
    
    def image_preview(self, obj):
        """معاينة الصورة"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'معاينة'


class TourProgramDayInline(admin.TabularInline):
    """Inline لأيام البرنامج السياحي"""
    model = TourProgramDay
    extra = 1
    fields = ['day_number', 'title', 'notes']
    classes = ['collapse']


@admin.register(TourProgram)
class TourProgramAdmin(admin.ModelAdmin):
    """لوحة تحكم البرامج السياحية"""
    list_display = ['title', 'duration_days', 'category', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_filter = ['category', 'is_active', 'duration_days']
    search_fields = ['title', 'description']
    inlines = [TourProgramDayInline]
    
    fieldsets = (
        ('معلومات البرنامج', {
            'fields': ('title', 'duration_days', 'category', 'description')
        }),
        ('الإعدادات', {
            'fields': ('is_active',)
        }),
    )


@admin.register(TourProgramDay)
class TourProgramDayAdmin(admin.ModelAdmin):
    """لوحة تحكم أيام البرامج السياحية"""
    list_display = ['program', 'day_number', 'title', 'places_count']
    list_filter = ['program']
    search_fields = ['title', 'notes']
    filter_horizontal = ['places']
    
    def places_count(self, obj):
        """عدد المواقع في اليوم"""
        return obj.places.count()
    places_count.short_description = 'عدد المواقع'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """لوحة تحكم رسائل التواصل"""
    list_display = ['name', 'email', 'subject', 'place', 'is_read', 'created_at']
    list_editable = ['is_read']
    list_filter = ['is_read', 'created_at', 'place']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('معلومات المرسل', {
            'fields': ('name', 'email', 'phone')
        }),
        ('الرسالة', {
            'fields': ('subject', 'message', 'place')
        }),
        ('الحالة', {
            'fields': ('is_read', 'created_at')
        }),
    )

    def has_add_permission(self, request):
        """منع إضافة رسائل من لوحة التحكم"""
        return False


# ======= User Management =======

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """لوحة تحكم ملفات المستخدمين"""
    list_display = ['user', 'get_full_name', 'phone', 'city', 'country', 'created_at']
    list_filter = ['country', 'city', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone', 'city']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('معلومات المستخدم', {
            'fields': ('user',)
        }),
        ('معلومات الاتصال', {
            'fields': ('phone', 'city', 'country')
        }),
        ('معلومات شخصية', {
            'fields': ('date_of_birth', 'bio', 'avatar')
        }),
        ('معلومات إضافية', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        """الاسم الكامل"""
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'الاسم الكامل'


@admin.register(SavedPlace)
class SavedPlaceAdmin(admin.ModelAdmin):
    """لوحة تحكم الأماكن المحفوظة"""
    list_display = ['user', 'place', 'created_at']
    list_filter = ['created_at', 'place__category', 'place__governorate']
    search_fields = ['user__username', 'place__name', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('user', 'place')
        }),
        ('ملاحظات', {
            'fields': ('notes',)
        }),
        ('معلومات إضافية', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


class TripPlanDayInline(admin.TabularInline):
    """Inline لإضافة أيام الرحلة"""
    model = TripPlanDay
    extra = 1
    fields = ['day_number', 'place', 'visit_time', 'notes', 'is_completed']
    autocomplete_fields = ['place']


@admin.register(UserTripPlan)
class UserTripPlanAdmin(admin.ModelAdmin):
    """لوحة تحكم خطط الرحلات"""
    list_display = ['title', 'user', 'status', 'start_date', 'end_date', 'get_duration', 'budget', 'created_at']
    list_filter = ['status', 'created_at', 'start_date']
    search_fields = ['title', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at', 'get_duration']
    date_hierarchy = 'created_at'
    inlines = [TripPlanDayInline]
    
    fieldsets = (
        ('معلومات الرحلة', {
            'fields': ('user', 'title', 'description', 'status')
        }),
        ('التواريخ والمدة', {
            'fields': ('start_date', 'end_date', 'get_duration')
        }),
        ('الميزانية', {
            'fields': ('budget',)
        }),
        ('معلومات إضافية', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_duration(self, obj):
        """المدة بالأيام"""
        duration = obj.get_duration_days()
        if duration > 0:
            return format_html(f'<strong>{duration} يوم</strong>')
        return 'غير محدد'
    get_duration.short_description = 'المدة'


@admin.register(TripPlanDay)
class TripPlanDayAdmin(admin.ModelAdmin):
    """لوحة تحكم أيام الرحلة"""
    list_display = ['trip_plan', 'day_number', 'place', 'visit_time', 'is_completed']
    list_filter = ['is_completed', 'day_number', 'trip_plan__status']
    search_fields = ['trip_plan__title', 'place__name', 'notes']
    list_editable = ['is_completed']
    autocomplete_fields = ['trip_plan', 'place']
    
    fieldsets = (
        ('معلومات اليوم', {
            'fields': ('trip_plan', 'day_number', 'place')
        }),
        ('تفاصيل الزيارة', {
            'fields': ('visit_time', 'notes', 'is_completed')
        }),
    )
