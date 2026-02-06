from django.test import TestCase
from django.urls import reverse
from .models import Category, Governorate, TouristPlace


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='السياحة الفرعونية',
            name_en='Pharaonic Tourism',
            slug='pharaonic-tourism',
            description='Test description',
            icon='fa-landmark'
        )
    
    def test_category_creation(self):
        """Test category is created properly"""
        self.assertEqual(self.category.name, 'السياحة الفرعونية')
        self.assertEqual(str(self.category), 'السياحة الفرعونية')
    
    def test_slug_generation(self):
        """Test slug is generated from name_en"""
        category = Category.objects.create(
            name='Test Category',
            name_en='Test Category New',
            description='Test'
        )
        self.assertEqual(category.slug, 'test-category-new')


class TouristPlaceModelTest(TestCase):
    """Test TouristPlace model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='السياحة الفرعونية',
            name_en='Pharaonic',
            description='Test'
        )
        self.governorate = Governorate.objects.create(
            name='القاهرة',
            name_en='Cairo'
        )
        self.place = TouristPlace.objects.create(
            name='الأهرامات',
            name_en='Pyramids',
            category=self.category,
            governorate=self.governorate,
            city='الجيزة',
            short_description='Test description',
            description='<p>Detailed description</p>',
            latitude=29.9792,
            longitude=31.1342,
            suggested_duration=4
        )
    
    def test_place_creation(self):
        """Test place is created properly"""
        self.assertEqual(self.place.name, 'الأهرامات')
        self.assertEqual(str(self.place), 'الأهرامات')
    
    def test_view_count_increment(self):
        """Test view count increments"""
        initial_count = self.place.view_count
        self.place.increment_views()
        self.assertEqual(self.place.view_count, initial_count + 1)


class ViewsTest(TestCase):
    """Test views"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='السياحة الفرعونية',
            name_en='Pharaonic',
            slug='pharaonic',
            description='Test',
            is_active=True
        )
        self.governorate = Governorate.objects.create(
            name='القاهرة',
            name_en='Cairo',
            slug='cairo',
            is_active=True
        )
        self.place = TouristPlace.objects.create(
            name='الأهرامات',
            name_en='Pyramids',
            slug='pyramids',
            category=self.category,
            governorate=self.governorate,
            city='الجيزة',
            short_description='Test',
            description='<p>Test</p>',
            is_active=True
        )
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get(reverse('tourism:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EgyRoute')
    
    def test_category_detail(self):
        """Test category detail page"""
        response = self.client.get(
            reverse('tourism:category_detail', kwargs={'slug': 'pharaonic'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'السياحة الفرعونية')
    
    def test_place_detail(self):
        """Test place detail page"""
        response = self.client.get(
            reverse('tourism:place_detail', kwargs={'slug': 'pyramids'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'الأهرامات')
    
    def test_all_places(self):
        """Test all places page"""
        response = self.client.get(reverse('tourism:all_places'))
        self.assertEqual(response.status_code, 200)
    
    def test_tour_planner(self):
        """Test tour planner page"""
        response = self.client.get(reverse('tourism:tour_planner'))
        self.assertEqual(response.status_code, 200)
