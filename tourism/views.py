from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import (Category, TouristPlace, Governorate, ContactMessage,
                     UserProfile, SavedPlace, UserTripPlan, TripPlanDay)
from .forms import (ContactForm, TourPlannerForm, UserRegistrationForm,
                   UserLoginForm, UserProfileForm, TripPlanForm)
import random


def set_language(request, lang_code):
    """Switch between Arabic and English"""
    if lang_code in ['ar', 'en']:
        request.session['language'] = lang_code
    return redirect(request.META.get('HTTP_REFERER', '/'))


def home(request):
    """الصفحة الرئيسية"""
    categories = Category.objects.filter(is_active=True)
    featured_places = TouristPlace.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category', 'governorate')[:6]
    
    # إحصائيات
    stats = {
        'total_places': TouristPlace.objects.filter(is_active=True).count(),
        'total_governorates': Governorate.objects.filter(is_active=True).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
    }
    
    context = {
        'categories': categories,
        'featured_places': featured_places,
        'stats': stats,
    }
    return render(request, 'tourism/home.html', context)


def category_detail(request, slug):
    """صفحة قسم سياحي معين"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # الحصول على جميع المواقع في هذا القسم
    places_list = TouristPlace.objects.filter(
        category=category,
        is_active=True
    ).select_related('governorate').prefetch_related('images')
    
    # الترتيب
    sort_by = request.GET.get('sort', 'priority')
    if sort_by == 'name':
        places_list = places_list.order_by('name')
    elif sort_by == 'governorate':
        places_list = places_list.order_by('governorate__name')
    elif sort_by == 'popular':
        places_list = places_list.order_by('-view_count')
    else:
        places_list = places_list.order_by('priority')
    
    # Pagination
    paginator = Paginator(places_list, 12)
    page_number = request.GET.get('page')
    places = paginator.get_page(page_number)
    
    # المحافظات المتاحة في هذا القسم
    governorates = Governorate.objects.filter(
        places__category=category,
        places__is_active=True,
        is_active=True
    ).distinct()
    
    context = {
        'category': category,
        'places': places,
        'governorates': governorates,
        'sort_by': sort_by,
    }
    return render(request, 'tourism/category_detail.html', context)


def place_detail(request, slug):
    """صفحة موقع سياحي معين"""
    place = get_object_or_404(
        TouristPlace.objects.select_related('category', 'governorate')
                           .prefetch_related('images'),
        slug=slug,
        is_active=True
    )
    
    # زيادة عدد المشاهدات
    place.increment_views()
    
    # مواقع مشابهة
    related_places = TouristPlace.objects.filter(
        category=place.category,
        is_active=True
    ).exclude(id=place.id).select_related('governorate')[:4]
    
    # نموذج التواصل
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.place = place
            contact.save()
            messages.success(request, 'تم إرسال رسالتك بنجاح! سنتواصل معك قريباً.')
            return redirect('tourism:place_detail', slug=slug)
    else:
        form = ContactForm()
    
    context = {
        'place': place,
        'related_places': related_places,
        'form': form,
    }
    return render(request, 'tourism/place_detail.html', context)


def all_places(request):
    """صفحة جميع المواقع السياحية"""
    places_list = TouristPlace.objects.filter(
        is_active=True
    ).select_related('category', 'governorate').prefetch_related('images')
    
    # الفلترة
    category_slug = request.GET.get('category')
    governorate_slug = request.GET.get('governorate')
    search_query = request.GET.get('q')
    
    if category_slug:
        places_list = places_list.filter(category__slug=category_slug)
    
    if governorate_slug:
        places_list = places_list.filter(governorate__slug=governorate_slug)
    
    if search_query:
        places_list = places_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    # الترتيب
    sort_by = request.GET.get('sort', 'priority')
    if sort_by == 'name':
        places_list = places_list.order_by('name')
    elif sort_by == 'popular':
        places_list = places_list.order_by('-view_count')
    else:
        places_list = places_list.order_by('priority')
    
    # Pagination
    paginator = Paginator(places_list, 12)
    page_number = request.GET.get('page')
    places = paginator.get_page(page_number)
    
    # للفلاتر
    categories = Category.objects.filter(is_active=True)
    governorates = Governorate.objects.filter(is_active=True)
    
    context = {
        'places': places,
        'categories': categories,
        'governorates': governorates,
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_governorate': governorate_slug,
        'sort_by': sort_by,
    }
    return render(request, 'tourism/all_places.html', context)


def tour_planner(request):
    """مخطط البرنامج السياحي"""
    generated_program = None
    
    if request.method == 'POST':
        form = TourPlannerForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data['days']
            categories = form.cleaned_data['categories']
            
            # توليد برنامج سياحي
            generated_program = generate_tour_program(days, categories)
            
    else:
        form = TourPlannerForm()
    
    context = {
        'form': form,
        'generated_program': generated_program,
    }
    return render(request, 'tourism/tour_planner.html', context)


def generate_tour_program(days, categories):
    """توليد برنامج سياحي تلقائي"""
    program = {
        'days': days,
        'categories': categories,
        'schedule': []
    }
    
    # الحصول على المواقع حسب الأقسام المختارة
    places = TouristPlace.objects.filter(
        category__in=categories,
        is_active=True
    ).select_related('category', 'governorate').order_by('priority')
    
    # تحويل إلى قائمة وخلطها قليلاً لتنويع
    places_list = list(places)
    
    # توزيع المواقع على الأيام
    places_per_day = max(2, len(places_list) // days)
    
    for day_num in range(1, days + 1):
        start_idx = (day_num - 1) * places_per_day
        end_idx = start_idx + places_per_day
        
        day_places = places_list[start_idx:end_idx]
        
        if day_places:
            day_data = {
                'day_number': day_num,
                'title': f'اليوم {day_num}',
                'places': day_places,
                'total_duration': sum(p.suggested_duration for p in day_places),
            }
            program['schedule'].append(day_data)
    
    return program


def governorates_list(request):
    """قائمة المحافظات"""
    governorates = Governorate.objects.filter(
        is_active=True
    ).annotate(
        places_count=Count('places', filter=Q(places__is_active=True))
    ).filter(places_count__gt=0)
    
    context = {
        'governorates': governorates,
    }
    return render(request, 'tourism/governorates_list.html', context)


def governorate_detail(request, slug):
    """صفحة محافظة معينة"""
    governorate = get_object_or_404(Governorate, slug=slug, is_active=True)
    
    places_list = TouristPlace.objects.filter(
        governorate=governorate,
        is_active=True
    ).select_related('category').prefetch_related('images')
    
    # Pagination
    paginator = Paginator(places_list, 12)
    page_number = request.GET.get('page')
    places = paginator.get_page(page_number)
    
    # تجميع حسب القسم
    categories_with_places = {}
    for place in places_list:
        if place.category not in categories_with_places:
            categories_with_places[place.category] = []
        categories_with_places[place.category].append(place)
    
    context = {
        'governorate': governorate,
        'places': places,
        'categories_with_places': categories_with_places,
    }
    return render(request, 'tourism/governorate_detail.html', context)


def about(request):
    """صفحة عن الموقع"""
    return render(request, 'tourism/about.html')


def contact(request):
    """صفحة التواصل"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إرسال رسالتك بنجاح! سنتواصل معك قريباً.')
            return redirect('tourism:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'tourism/contact.html', context)


# ======= User Authentication Views =======

def register(request):
    """تسجيل مستخدم جديد"""
    if request.user.is_authenticated:
        return redirect('tourism:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # إنشاء ملف تعريف للمستخدم
            phone = form.cleaned_data.get('phone', '')
            UserProfile.objects.create(user=user, phone=phone)
            
            # تسجيل الدخول تلقائياً
            login(request, user)
            messages.success(request, f'مرحباً {user.first_name}! تم إنشاء حسابك بنجاح.')
            return redirect('tourism:profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'tourism/register.html', {'form': form})


def user_login(request):
    """تسجيل الدخول"""
    if request.user.is_authenticated:
        return redirect('tourism:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'مرحباً بعودتك {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'tourism:home')
                return redirect(next_url)
    else:
        form = UserLoginForm()
    
    return render(request, 'tourism/login.html', {'form': form})


@login_required
def user_logout(request):
    """تسجيل الخروج"""
    logout(request)
    messages.info(request, 'تم تسجيل خروجك بنجاح.')
    return redirect('tourism:home')


@login_required
def profile(request):
    """صفحة الملف الشخصي"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # تحديث بيانات المستخدم
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            
            form.save()
            messages.success(request, 'تم تحديث ملفك الشخصي بنجاح!')
            return redirect('tourism:profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = UserProfileForm(instance=profile, initial=initial_data)
    
    # الأماكن المحفوظة
    saved_places = SavedPlace.objects.filter(user=request.user).select_related('place')[:6]
    
    # خطط الرحلات
    trip_plans = UserTripPlan.objects.filter(user=request.user)[:5]
    
    context = {
        'form': form,
        'profile': profile,
        'saved_places': saved_places,
        'trip_plans': trip_plans,
    }
    return render(request, 'tourism/profile.html', context)


# ======= Saved Places Views =======

@login_required
@require_POST
def toggle_save_place(request, place_id):
    """حفظ أو إلغاء حفظ مكان"""
    place = get_object_or_404(TouristPlace, id=place_id, is_active=True)
    saved_place, created = SavedPlace.objects.get_or_create(
        user=request.user,
        place=place
    )
    
    if not created:
        saved_place.delete()
        return JsonResponse({
            'status': 'removed',
            'message': 'تم إزالة المكان من المحفوظات'
        })
    
    return JsonResponse({
        'status': 'saved',
        'message': 'تم حفظ المكان بنجاح'
    })


@login_required
def saved_places_list(request):
    """قائمة الأماكن المحفوظة"""
    saved_places = SavedPlace.objects.filter(
        user=request.user
    ).select_related('place', 'place__governorate', 'place__category')
    
    return render(request, 'tourism/saved_places.html', {
        'saved_places': saved_places
    })


# ======= Trip Planning Views =======

@login_required
def trip_plans_list(request):
    """قائمة خطط الرحلات"""
    trip_plans = UserTripPlan.objects.filter(user=request.user).prefetch_related('days__place')
    
    return render(request, 'tourism/trip_plans_list.html', {
        'trip_plans': trip_plans
    })


@login_required
def create_trip_plan(request):
    """إنشاء خطة رحلة جديدة"""
    if request.method == 'POST':
        form = TripPlanForm(request.POST)
        if form.is_valid():
            trip_plan = form.save(commit=False)
            trip_plan.user = request.user
            trip_plan.save()
            messages.success(request, 'تم إنشاء خطة الرحلة بنجاح!')
            return redirect('tourism:trip_plan_detail', plan_id=trip_plan.id)
    else:
        form = TripPlanForm()
    
    return render(request, 'tourism/create_trip_plan.html', {'form': form})


@login_required
def trip_plan_detail(request, plan_id):
    """تفاصيل خطة رحلة"""
    trip_plan = get_object_or_404(
        UserTripPlan.objects.prefetch_related('days__place'),
        id=plan_id,
        user=request.user
    )
    
    # تنظيم الأيام
    days_data = {}
    for day in trip_plan.days.all():
        if day.day_number not in days_data:
            days_data[day.day_number] = []
        days_data[day.day_number].append(day)
    
    # جميع الأماكن المتاحة للإضافة
    available_places = TouristPlace.objects.filter(is_active=True).select_related('governorate', 'category')
    
    context = {
        'trip_plan': trip_plan,
        'days_data': dict(sorted(days_data.items())),
        'available_places': available_places,
    }
    return render(request, 'tourism/trip_plan_detail.html', context)


@login_required
@require_POST
def add_place_to_plan(request, plan_id):
    """إضافة مكان إلى خطة الرحلة"""
    trip_plan = get_object_or_404(UserTripPlan, id=plan_id, user=request.user)
    place_id = request.POST.get('place_id')
    day_number = request.POST.get('day_number', 1)
    
    place = get_object_or_404(TouristPlace, id=place_id, is_active=True)
    
    try:
        trip_day, created = TripPlanDay.objects.get_or_create(
            trip_plan=trip_plan,
            place=place,
            day_number=int(day_number)
        )
        
        if created:
            return JsonResponse({
                'status': 'success',
                'message': f'تم إضافة {place.name} إلى اليوم {day_number}'
            })
        else:
            return JsonResponse({
                'status': 'exists',
                'message': 'هذا المكان موجود بالفعل في خطة الرحلة'
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
@require_POST
def remove_place_from_plan(request, plan_id, day_id):
    """إزالة مكان من خطة الرحلة"""
    trip_plan = get_object_or_404(UserTripPlan, id=plan_id, user=request.user)
    trip_day = get_object_or_404(TripPlanDay, id=day_id, trip_plan=trip_plan)
    
    trip_day.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'تم إزالة المكان من خطة الرحلة'
    })


@login_required
@require_POST
def delete_trip_plan(request, plan_id):
    """حذف خطة رحلة"""
    trip_plan = get_object_or_404(UserTripPlan, id=plan_id, user=request.user)
    trip_plan.delete()
    messages.success(request, 'تم حذف خطة الرحلة بنجاح')
    return redirect('tourism:trip_plans_list')
