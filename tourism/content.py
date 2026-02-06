"""
Content dictionary for Arabic and English versions
This file contains all static content for the website in both languages
"""

CONTENT = {
    'ar': {
        # Home page
        'home_hero_title': 'اكتشف جمال مصر',
        'home_hero_subtitle': 'رحلة عبر التاريخ والحضارة من الفراعنة إلى الحاضر',
        'home_hero_button': 'خطط رحلتك الآن',
        
        # Stats
        'stat_places': 'موقع سياحي',
        'stat_governorates': 'محافظة',
        'stat_categories': 'نوع سياحة',
        
        # Sections
        'section_categories': 'أنواع السياحة في مصر',
        'section_featured': 'أماكن مميزة',
        'view_more': 'عرض المزيد',
        'view_details': 'عرض التفاصيل',
        
        # Navigation
        'nav_home': 'الرئيسية',
        'nav_about': 'من نحن',
        'nav_governorates': 'المحافظات',
        'nav_places': 'الأماكن السياحية',
        'nav_planner': 'مخطط الرحلة',
        'nav_contact': 'اتصل بنا',
        'nav_login': 'تسجيل الدخول',
        'nav_register': 'إنشاء حساب',
        'nav_profile': 'الملف الشخصي',
        'nav_logout': 'تسجيل الخروج',
        'nav_saved': 'الأماكن المحفوظة',
        'nav_trips': 'رحلاتي',
        
        # Categories
        'cat_pharaonic': 'سياحة فرعونية',
        'cat_islamic': 'سياحة إسلامية',
        'cat_coptic': 'سياحة قبطية',
        'cat_beach': 'سياحة شاطئية',
        'cat_desert': 'سياحة صحراوية',
        'cat_medical': 'سياحة علاجية',
        
        # Place details
        'place_location': 'الموقع',
        'place_governorate': 'المحافظة',
        'place_category': 'النوع',
        'place_description': 'الوصف',
        'place_gallery': 'معرض الصور',
        'place_map': 'الخريطة',
        'place_related': 'أماكن مشابهة',
        'place_save': 'حفظ المكان',
        'place_saved': 'تم الحفظ',
        'place_visit': 'زيارة الموقع',
        
        # Forms
        'form_name': 'الاسم',
        'form_email': 'البريد الإلكتروني',
        'form_phone': 'رقم الهاتف',
        'form_message': 'الرسالة',
        'form_send': 'إرسال',
        'form_submit': 'إرسال',
        'form_cancel': 'إلغاء',
        'form_save': 'حفظ',
        'form_delete': 'حذف',
        'form_edit': 'تعديل',
        
        # Contact
        'contact_title': 'اتصل بنا',
        'contact_subtitle': 'نحن هنا للإجابة على استفساراتك',
        'contact_info': 'معلومات التواصل',
        'contact_address': 'العنوان',
        'contact_phone': 'الهاتف',
        'contact_email': 'البريد الإلكتروني',
        'contact_whatsapp': 'واتساب',
        
        # About
        'about_title': 'من نحن',
        'about_subtitle': 'دليلك الشامل لاكتشاف مصر',
        
        # Trip Planner
        'planner_title': 'مخطط الرحلة',
        'planner_create': 'إنشاء رحلة جديدة',
        'planner_my_trips': 'رحلاتي',
        'planner_trip_name': 'اسم الرحلة',
        'planner_start_date': 'تاريخ البدء',
        'planner_end_date': 'تاريخ الانتهاء',
        'planner_days': 'أيام',
        'planner_places': 'أماكن',
        
        # Messages
        'msg_success': 'تمت العملية بنجاح',
        'msg_error': 'حدث خطأ، يرجى المحاولة مرة أخرى',
        'msg_login_required': 'يجب تسجيل الدخول للقيام بهذه العملية',
        'msg_saved': 'تم الحفظ بنجاح',
        'msg_deleted': 'تم الحذف بنجاح',
        
        # Footer
        'footer_about': 'عن الموقع',
        'footer_description': 'دليلك الشامل لاكتشاف جمال مصر وتاريخها العريق. استكشف المواقع الفرعونية والإسلامية والقبطية.',
        'footer_links': 'روابط سريعة',
        'footer_contact': 'تواصل معنا',
        'footer_social': 'تابعنا',
        'footer_rights': 'جميع الحقوق محفوظة',
        
        # Search & Filter
        'search_placeholder': 'ابحث عن أماكن سياحية...',
        'filter_by': 'تصفية حسب',
        'sort_by': 'ترتيب حسب',
        'sort_priority': 'الأولوية',
        'sort_name': 'الاسم',
        'sort_popular': 'الأكثر شعبية',
        'sort_governorate': 'المحافظة',
        
        # Pagination
        'pagination_previous': 'السابق',
        'pagination_next': 'التالي',
        'pagination_page': 'صفحة',
        
        # Empty states
        'no_places': 'لا توجد أماكن حالياً',
        'no_trips': 'لا توجد رحلات حالياً',
        'no_saved': 'لا توجد أماكن محفوظة',
        
        # Auth
        'auth_login_title': 'تسجيل الدخول',
        'auth_register_title': 'إنشاء حساب جديد',
        'auth_username': 'اسم المستخدم',
        'auth_password': 'كلمة المرور',
        'auth_confirm_password': 'تأكيد كلمة المرور',
        'auth_remember': 'تذكرني',
        'auth_forgot': 'نسيت كلمة المرور؟',
        'auth_no_account': 'لا تملك حساب؟',
        'auth_have_account': 'لديك حساب؟',
        
        # Profile
        'profile_title': 'الملف الشخصي',
        'profile_edit': 'تعديل الملف الشخصي',
        'profile_info': 'معلومات الحساب',
        'profile_bio': 'نبذة عني',
        'profile_avatar': 'الصورة الشخصية',
    },
    'en': {
        # Home page
        'home_hero_title': 'Discover the Beauty of Egypt',
        'home_hero_subtitle': 'A Journey Through History and Civilization from the Pharaohs to the Present',
        'home_hero_button': 'Plan Your Trip Now',
        
        # Stats
        'stat_places': 'Tourist Places',
        'stat_governorates': 'Governorates',
        'stat_categories': 'Tourism Types',
        
        # Sections
        'section_categories': 'Types of Tourism in Egypt',
        'section_featured': 'Featured Places',
        'view_more': 'View More',
        'view_details': 'View Details',
        
        # Navigation
        'nav_home': 'Home',
        'nav_about': 'About',
        'nav_governorates': 'Governorates',
        'nav_places': 'Tourist Places',
        'nav_planner': 'Trip Planner',
        'nav_contact': 'Contact',
        'nav_login': 'Login',
        'nav_register': 'Register',
        'nav_profile': 'Profile',
        'nav_logout': 'Logout',
        'nav_saved': 'Saved Places',
        'nav_trips': 'My Trips',
        
        # Categories
        'cat_pharaonic': 'Pharaonic Tourism',
        'cat_islamic': 'Islamic Tourism',
        'cat_coptic': 'Coptic Tourism',
        'cat_beach': 'Beach Tourism',
        'cat_desert': 'Desert Tourism',
        'cat_medical': 'Medical Tourism',
        
        # Place details
        'place_location': 'Location',
        'place_governorate': 'Governorate',
        'place_category': 'Category',
        'place_description': 'Description',
        'place_gallery': 'Photo Gallery',
        'place_map': 'Map',
        'place_related': 'Related Places',
        'place_save': 'Save Place',
        'place_saved': 'Saved',
        'place_visit': 'Visit Website',
        
        # Forms
        'form_name': 'Name',
        'form_email': 'Email',
        'form_phone': 'Phone Number',
        'form_message': 'Message',
        'form_send': 'Send',
        'form_submit': 'Submit',
        'form_cancel': 'Cancel',
        'form_save': 'Save',
        'form_delete': 'Delete',
        'form_edit': 'Edit',
        
        # Contact
        'contact_title': 'Contact Us',
        'contact_subtitle': 'We are here to answer your questions',
        'contact_info': 'Contact Information',
        'contact_address': 'Address',
        'contact_phone': 'Phone',
        'contact_email': 'Email',
        'contact_whatsapp': 'WhatsApp',
        
        # About
        'about_title': 'About Us',
        'about_subtitle': 'Your Comprehensive Guide to Discovering Egypt',
        
        # Trip Planner
        'planner_title': 'Trip Planner',
        'planner_create': 'Create New Trip',
        'planner_my_trips': 'My Trips',
        'planner_trip_name': 'Trip Name',
        'planner_start_date': 'Start Date',
        'planner_end_date': 'End Date',
        'planner_days': 'Days',
        'planner_places': 'Places',
        
        # Messages
        'msg_success': 'Operation completed successfully',
        'msg_error': 'An error occurred, please try again',
        'msg_login_required': 'You must login to perform this action',
        'msg_saved': 'Saved successfully',
        'msg_deleted': 'Deleted successfully',
        
        # Footer
        'footer_about': 'About',
        'footer_description': 'Your comprehensive guide to discovering the beauty and rich history of Egypt. Explore Pharaonic, Islamic, and Coptic sites.',
        'footer_links': 'Quick Links',
        'footer_contact': 'Contact Us',
        'footer_social': 'Follow Us',
        'footer_rights': 'All Rights Reserved',
        
        # Search & Filter
        'search_placeholder': 'Search for tourist places...',
        'filter_by': 'Filter by',
        'sort_by': 'Sort by',
        'sort_priority': 'Priority',
        'sort_name': 'Name',
        'sort_popular': 'Most Popular',
        'sort_governorate': 'Governorate',
        
        # Pagination
        'pagination_previous': 'Previous',
        'pagination_next': 'Next',
        'pagination_page': 'Page',
        
        # Empty states
        'no_places': 'No places available',
        'no_trips': 'No trips available',
        'no_saved': 'No saved places',
        
        # Auth
        'auth_login_title': 'Login',
        'auth_register_title': 'Create New Account',
        'auth_username': 'Username',
        'auth_password': 'Password',
        'auth_confirm_password': 'Confirm Password',
        'auth_remember': 'Remember Me',
        'auth_forgot': 'Forgot Password?',
        'auth_no_account': "Don't have an account?",
        'auth_have_account': 'Have an account?',
        
        # Profile
        'profile_title': 'Profile',
        'profile_edit': 'Edit Profile',
        'profile_info': 'Account Information',
        'profile_bio': 'Bio',
        'profile_avatar': 'Avatar',
    }
}


def get_content(request, key):
    """Get content based on current language"""
    lang = request.session.get('language', 'ar')
    return CONTENT.get(lang, {}).get(key, key)
