from django.urls import path
from . import views

app_name = 'tourism'

urlpatterns = [
    # الصفحة الرئيسية
    path('', views.home, name='home'),
    
    # Language switching
    path('set-language/<str:lang_code>/', views.set_language, name='set_language'),
    
    # الأقسام السياحية
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # المواقع السياحية
    path('places/', views.all_places, name='all_places'),
    path('place/<slug:slug>/', views.place_detail, name='place_detail'),
    
    # المحافظات
    path('governorates/', views.governorates_list, name='governorates_list'),
    path('governorate/<slug:slug>/', views.governorate_detail, name='governorate_detail'),
    
    # مخطط الرحلة
    path('tour-planner/', views.tour_planner, name='tour_planner'),
    
    # صفحات عامة
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Saved Places
    path('saved-places/', views.saved_places_list, name='saved_places_list'),
    path('toggle-save-place/<int:place_id>/', views.toggle_save_place, name='toggle_save_place'),
    
    # Trip Planning
    path('trip-plans/', views.trip_plans_list, name='trip_plans_list'),
    path('trip-plans/create/', views.create_trip_plan, name='create_trip_plan'),
    path('trip-plans/<int:plan_id>/', views.trip_plan_detail, name='trip_plan_detail'),
    path('trip-plans/<int:plan_id>/add-place/', views.add_place_to_plan, name='add_place_to_plan'),
    path('trip-plans/<int:plan_id>/remove-place/<int:day_id>/', views.remove_place_from_plan, name='remove_place_from_plan'),
    path('trip-plans/<int:plan_id>/delete/', views.delete_trip_plan, name='delete_trip_plan'),
]
