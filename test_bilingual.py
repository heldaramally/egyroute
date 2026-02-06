"""
Test script to verify bilingual system is working
"""

def test_content():
    """Test if content.py is properly structured"""
    try:
        from tourism.content import CONTENT
        
        print("✓ content.py imported successfully")
        
        # Check if both languages exist
        assert 'ar' in CONTENT, "Arabic content missing"
        assert 'en' in CONTENT, "English content missing"
        print("✓ Both languages found in CONTENT")
        
        # Check if key content exists
        required_keys = [
            'nav_home', 'nav_about', 'nav_contact',
            'home_hero_title', 'home_hero_subtitle'
        ]
        
        for key in required_keys:
            assert key in CONTENT['ar'], f"Key '{key}' missing in Arabic"
            assert key in CONTENT['en'], f"Key '{key}' missing in English"
        
        print(f"✓ All {len(required_keys)} required keys exist")
        
        # Sample output
        print("\n=== Sample Content ===")
        print(f"Arabic Home Title: {CONTENT['ar']['home_hero_title']}")
        print(f"English Home Title: {CONTENT['en']['home_hero_title']}")
        
        print("\n✅ All tests passed! Bilingual system is ready.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == '__main__':
    import sys
    import os
    import django
    
    # Add project to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egyroute.settings')
    django.setup()
    
    test_content()
