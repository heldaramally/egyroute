from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ContactMessage, Category, UserProfile, UserTripPlan, TripPlanDay


class ContactForm(forms.ModelForm):
    """نموذج التواصل"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسمك الكريم',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'البريد الإلكتروني',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الهاتف (اختياري)',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع الرسالة',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'رسالتك',
                'rows': 5,
                'required': True
            }),
        }


class TourPlannerForm(forms.Form):
    """نموذج تخطيط البرنامج السياحي"""
    
    days = forms.IntegerField(
        label='عدد الأيام',
        min_value=1,
        max_value=14,
        initial=3,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'كم يوم ستقضي في مصر؟'
        })
    )
    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(is_active=True),
        label='نوع السياحة المفضل',
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True
    )
    
    def clean_categories(self):
        """التحقق من اختيار قسم واحد على الأقل"""
        categories = self.cleaned_data.get('categories')
        if not categories:
            raise forms.ValidationError('يرجى اختيار نوع سياحة واحد على الأقل')
        return categories


class UserRegistrationForm(UserCreationForm):
    """نموذج تسجيل مستخدم جديد"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'البريد الإلكتروني'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'الاسم الأول'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم العائلة'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'رقم الهاتف (اختياري)'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم المستخدم'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'كلمة المرور'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'تأكيد كلمة المرور'
        })


class UserLoginForm(AuthenticationForm):
    """نموذج تسجيل الدخول"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم المستخدم'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور'
        })
    )


class UserProfileForm(forms.ModelForm):
    """نموذج تحديث الملف الشخصي"""
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'city', 'country', 'date_of_birth', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TripPlanForm(forms.ModelForm):
    """نموذج إنشاء خطة رحلة"""
    class Meta:
        model = UserTripPlan
        fields = ['title', 'description', 'start_date', 'end_date', 'budget', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثل: رحلتي إلى القاهرة'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'وصف مختصر للرحلة...'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'الميزانية المتوقعة (جنيه مصري)'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
