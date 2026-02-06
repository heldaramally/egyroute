from django.conf import settings
from .content import CONTENT


def site_context(request):
    """Context processor لإضافة معلومات عامة لجميع الصفحات"""
    # Get current language from session
    current_lang = request.session.get('language', 'ar')
    
    # Site content based on language
    site_content = {
        'ar': {
            'SITE_NAME': 'EgyRoute - اكتشف مصر',
            'SITE_DESCRIPTION': 'دليلك الشامل لاكتشاف المواقع السياحية في مصر',
        },
        'en': {
            'SITE_NAME': 'EgyRoute - Discover Egypt',
            'SITE_DESCRIPTION': 'Your comprehensive guide to discovering tourist sites in Egypt',
        }
    }
    
    return {
        'WHATSAPP_NUMBER': settings.WHATSAPP_NUMBER,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'SITE_NAME': site_content[current_lang]['SITE_NAME'],
        'SITE_DESCRIPTION': site_content[current_lang]['SITE_DESCRIPTION'],
        'LANGUAGE_CODE': current_lang,
        'LANGUAGES': settings.LANGUAGES,
        'content': CONTENT.get(current_lang, CONTENT['ar']),
        'is_english': current_lang == 'en',  # Helper for templates
        'is_arabic': current_lang == 'ar',   # Helper for templates
    }
