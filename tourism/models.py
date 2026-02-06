from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Category(models.Model):
    """نموذج لأنواع السياحة (فرعونية - إسلامية - قبطية)"""
    name = models.CharField(_('الاسم'), max_length=100)
    name_en = models.CharField(_('الاسم بالإنجليزية'), max_length=100)
    slug = models.SlugField(_('الرابط'), unique=True, max_length=100, blank=True)
    description = HTMLField(_('الوصف'))
    description_en = HTMLField(_('الوصف بالإنجليزية'), blank=True)
    icon = models.CharField(_('أيقونة'), max_length=50, default='fa-landmark', 
                           help_text=_('FontAwesome icon class (مثل: fa-mosque, fa-cross)'))
    order = models.IntegerField(_('الترتيب'), default=0)
    is_active = models.BooleanField(_('نشط'), default=True)
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاريخ التحديث'), auto_now=True)

    class Meta:
        verbose_name = _('قسم سياحي')
        verbose_name_plural = _('الأقسام السياحية')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def get_places_count(self):
        """عدد المواقع في هذا القسم"""
        return self.places.filter(is_active=True).count()
    
    def get_name(self, lang='ar'):
        """Get name based on language"""
        if lang == 'en' and self.name_en:
            return self.name_en
        return self.name
    
    def get_description(self, lang='ar'):
        """Get description based on language"""
        if lang == 'en' and self.description_en:
            return self.description_en
        return self.description


class Governorate(models.Model):
    """نموذج للمحافظات المصرية"""
    name = models.CharField(_('الاسم'), max_length=100)
    name_en = models.CharField(_('الاسم بالإنجليزية'), max_length=100)
    slug = models.SlugField(_('الرابط'), unique=True, max_length=100, blank=True)
    is_active = models.BooleanField(_('نشط'), default=True)

    class Meta:
        verbose_name = _('محافظة')
        verbose_name_plural = _('المحافظات')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)
    
    def get_name(self, lang='ar'):
        """Get name based on language"""
        if lang == 'en' and self.name_en:
            return self.name_en
        return self.name


class TouristPlace(models.Model):
    """نموذج للمواقع السياحية"""
    
    DURATION_CHOICES = [
        (1, _('ساعة واحدة')),
        (2, _('ساعتان')),
        (3, _('3 ساعات')),
        (4, _('4 ساعات')),
        (5, _('5 ساعات')),
        (6, _('نصف يوم')),
        (8, _('يوم كامل')),
        (12, _('يوم ونصف')),
        (16, _('يومان')),
    ]

    name = models.CharField(_('اسم الموقع'), max_length=200)
    name_en = models.CharField(_('الاسم بالإنجليزية'), max_length=200)
    slug = models.SlugField(_('الرابط'), unique=True, max_length=200, blank=True)
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='places',
        verbose_name='القسم السياحي'
    )
    
    governorate = models.ForeignKey(
        Governorate, 
        on_delete=models.CASCADE, 
        related_name='places',
        verbose_name='المحافظة'
    )
    
    city = models.CharField('المدينة / المنطقة', max_length=100)
    city_en = models.CharField('المدينة / المنطقة (إنجليزي)', max_length=100, blank=True)
    
    short_description = models.TextField('وصف مختصر', max_length=300)
    short_description_en = models.TextField('وصف مختصر (إنجليزي)', max_length=300, blank=True)
    description = HTMLField('الوصف التفصيلي')
    description_en = HTMLField('الوصف التفصيلي (إنجليزي)', blank=True)
    
    # Location
    latitude = models.DecimalField(
        'خط العرض', 
        max_digits=9, 
        decimal_places=6,
        null=True,
        blank=True,
        help_text='مثال: 30.047778'
    )
    longitude = models.DecimalField(
        'خط الطول', 
        max_digits=9, 
        decimal_places=6,
        null=True,
        blank=True,
        help_text='مثال: 31.233889'
    )
    
    # Visit information
    suggested_duration = models.IntegerField(
        'مدة الزيارة المقترحة (بالساعات)',
        choices=DURATION_CHOICES,
        default=3
    )
    
    visitor_tips = HTMLField('نصائح للزائر', blank=True)
    visitor_tips_en = HTMLField('نصائح للزائر (إنجليزي)', blank=True)
    
    best_time_to_visit = models.CharField(
        'أفضل وقت للزيارة',
        max_length=200,
        blank=True,
        help_text='مثال: الشتاء، الصباح الباكر'
    )
    best_time_to_visit_en = models.CharField(
        'أفضل وقت للزيارة (إنجليزي)',
        max_length=200,
        blank=True,
        help_text='Example: Winter, Early morning'
    )
    
    entry_fee = models.CharField(
        'رسوم الدخول',
        max_length=100,
        blank=True,
        help_text='مثال: 200 جنيه للأجانب، 50 جنيه للمصريين'
    )
    entry_fee_en = models.CharField(
        'رسوم الدخول (إنجليزي)',
        max_length=100,
        blank=True,
        help_text='Example: 200 EGP for foreigners, 50 EGP for Egyptians'
    )
    
    # Priority and status
    priority = models.IntegerField(
        'الأولوية',
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='1 = أعلى أولوية، 10 = أقل أولوية'
    )
    
    is_featured = models.BooleanField('مميز', default=False)
    is_active = models.BooleanField('نشط', default=True)
    
    view_count = models.IntegerField('عدد المشاهدات', default=0, editable=False)
    
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = 'موقع سياحي'
        verbose_name_plural = 'المواقع السياحية'
        ordering = ['priority', '-is_featured', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def increment_views(self):
        """زيادة عدد المشاهدات"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def get_main_image(self):
        """الحصول على الصورة الرئيسية"""
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image
        return self.images.first()
    
    def get_name(self, lang='ar'):
        """Get name based on language"""
        if lang == 'en' and self.name_en:
            return self.name_en
        return self.name
    
    def get_city(self, lang='ar'):
        """Get city based on language"""
        if lang == 'en' and self.city_en:
            return self.city_en
        return self.city
    
    def get_short_description(self, lang='ar'):
        """Get short description based on language"""
        if lang == 'en' and self.short_description_en:
            return self.short_description_en
        return self.short_description
    
    def get_description(self, lang='ar'):
        """Get description based on language"""
        if lang == 'en' and self.description_en:
            return self.description_en
        return self.description
    
    def get_visitor_tips(self, lang='ar'):
        """Get visitor tips based on language"""
        if lang == 'en' and self.visitor_tips_en:
            return self.visitor_tips_en
        return self.visitor_tips
    
    def get_best_time(self, lang='ar'):
        """Get best time to visit based on language"""
        if lang == 'en' and self.best_time_to_visit_en:
            return self.best_time_to_visit_en
        return self.best_time_to_visit
    
    def get_entry_fee(self, lang='ar'):
        """Get entry fee based on language"""
        if lang == 'en' and self.entry_fee_en:
            return self.entry_fee_en
        return self.entry_fee


class PlaceImage(models.Model):
    """نموذج لصور المواقع السياحية"""
    place = models.ForeignKey(
        TouristPlace,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='الموقع السياحي'
    )
    image = models.ImageField('الصورة', upload_to='places/%Y/%m/')
    caption = models.CharField('عنوان الصورة', max_length=200, blank=True)
    caption_en = models.CharField('عنوان الصورة (إنجليزي)', max_length=200, blank=True)
    is_main = models.BooleanField('صورة رئيسية', default=False)
    order = models.IntegerField('الترتيب', default=0)
    uploaded_at = models.DateTimeField('تاريخ الرفع', auto_now_add=True)

    class Meta:
        verbose_name = 'صورة'
        verbose_name_plural = 'الصور'
        ordering = ['-is_main', 'order']
    
    def get_caption(self, lang='ar'):
        """Get caption based on language"""
        if lang == 'en' and self.caption_en:
            return self.caption_en
        return self.caption

    def __str__(self):
        return f'{self.place.name} - {self.caption or "صورة"}'

    def save(self, *args, **kwargs):
        # إذا كانت صورة رئيسية، قم بإزالة الخاصية من الصور الأخرى
        if self.is_main:
            PlaceImage.objects.filter(
                place=self.place, 
                is_main=True
            ).update(is_main=False)
        super().save(*args, **kwargs)


class TourProgram(models.Model):
    """نموذج للبرامج السياحية المقترحة"""
    title = models.CharField('عنوان البرنامج', max_length=200)
    duration_days = models.IntegerField('عدد الأيام')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='programs',
        verbose_name='القسم السياحي'
    )
    description = models.TextField('وصف البرنامج', blank=True)
    is_active = models.BooleanField('نشط', default=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)

    class Meta:
        verbose_name = 'برنامج سياحي'
        verbose_name_plural = 'البرامج السياحية'
        ordering = ['duration_days']

    def __str__(self):
        return f'{self.title} - {self.duration_days} أيام'


class TourProgramDay(models.Model):
    """نموذج ليوم في البرنامج السياحي"""
    program = models.ForeignKey(
        TourProgram,
        on_delete=models.CASCADE,
        related_name='days',
        verbose_name='البرنامج'
    )
    day_number = models.IntegerField('رقم اليوم')
    title = models.CharField('عنوان اليوم', max_length=200)
    places = models.ManyToManyField(
        TouristPlace,
        related_name='program_days',
        verbose_name='المواقع السياحية'
    )
    notes = models.TextField('ملاحظات', blank=True)

    class Meta:
        verbose_name = 'يوم في البرنامج'
        verbose_name_plural = 'أيام البرنامج'
        ordering = ['program', 'day_number']
        unique_together = ['program', 'day_number']

    def __str__(self):
        return f'{self.program.title} - اليوم {self.day_number}'


class ContactMessage(models.Model):
    """نموذج لرسائل التواصل"""
    name = models.CharField('الاسم', max_length=100)
    email = models.EmailField('البريد الإلكتروني')
    phone = models.CharField('رقم الهاتف', max_length=20, blank=True)
    subject = models.CharField('الموضوع', max_length=200)
    message = models.TextField('الرسالة')
    place = models.ForeignKey(
        TouristPlace,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
        verbose_name='الموقع المعني'
    )
    is_read = models.BooleanField('مقروءة', default=False)
    created_at = models.DateTimeField('تاريخ الإرسال', auto_now_add=True)

    class Meta:
        verbose_name = 'رسالة تواصل'
        verbose_name_plural = 'رسائل التواصل'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'


class UserProfile(models.Model):
    """ملف تعريف المستخدم"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('رقم الهاتف', max_length=20, blank=True)
    city = models.CharField('المدينة', max_length=100, blank=True)
    country = models.CharField('البلد', max_length=100, default='مصر')
    date_of_birth = models.DateField('تاريخ الميلاد', null=True, blank=True)
    bio = models.TextField('نبذة عني', blank=True, max_length=500)
    avatar = models.ImageField('الصورة الشخصية', upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField('تاريخ التسجيل', auto_now_add=True)
    
    class Meta:
        verbose_name = 'ملف المستخدم'
        verbose_name_plural = 'ملفات المستخدمين'
    
    def __str__(self):
        return f'{self.user.username} - {self.user.get_full_name() or self.user.username}'


class SavedPlace(models.Model):
    """الأماكن المحفوظة للمستخدم"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_places')
    place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='saved_by')
    notes = models.TextField('ملاحظات', blank=True)
    created_at = models.DateTimeField('تاريخ الحفظ', auto_now_add=True)
    
    class Meta:
        verbose_name = 'مكان محفوظ'
        verbose_name_plural = 'الأماكن المحفوظة'
        unique_together = ['user', 'place']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.place.name}'


class UserTripPlan(models.Model):
    """خطة رحلة المستخدم"""
    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('planned', 'مخطط'),
        ('in_progress', 'جاري التنفيذ'),
        ('completed', 'مكتملة'),
        ('cancelled', 'ملغية'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_plans')
    title = models.CharField('عنوان الرحلة', max_length=200)
    description = models.TextField('وصف الرحلة', blank=True)
    start_date = models.DateField('تاريخ البداية', null=True, blank=True)
    end_date = models.DateField('تاريخ النهاية', null=True, blank=True)
    budget = models.DecimalField('الميزانية', max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField('الحالة', max_length=20, choices=STATUS_CHOICES, default='draft')
    places = models.ManyToManyField(TouristPlace, through='TripPlanDay', related_name='in_plans')
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    
    class Meta:
        verbose_name = 'خطة رحلة'
        verbose_name_plural = 'خطط الرحلات'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.title}'
    
    def get_duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0


class TripPlanDay(models.Model):
    """يوم في خطة الرحلة"""
    trip_plan = models.ForeignKey(UserTripPlan, on_delete=models.CASCADE, related_name='days')
    place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE)
    day_number = models.IntegerField('رقم اليوم')
    visit_time = models.TimeField('وقت الزيارة', null=True, blank=True)
    notes = models.TextField('ملاحظات', blank=True)
    is_completed = models.BooleanField('مكتملة', default=False)
    
    class Meta:
        verbose_name = 'يوم في خطة الرحلة'
        verbose_name_plural = 'أيام خطة الرحلة'
        ordering = ['trip_plan', 'day_number']
        unique_together = ['trip_plan', 'day_number', 'place']
    
    def __str__(self):
        return f'{self.trip_plan.title} - اليوم {self.day_number} - {self.place.name}'
