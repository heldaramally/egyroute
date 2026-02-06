# Management command to load sample data
from django.core.management.base import BaseCommand
from tourism.models import Category, Governorate, TouristPlace


class Command(BaseCommand):
    help = 'Load sample tourism data into database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')

        # Create Categories
        categories_data = [
            {
                'name': 'السياحة الفرعونية',
                'name_en': 'Pharaonic Tourism',
                'slug': 'pharaonic-tourism',
                'description': 'استكشف عظمة الحضارة المصرية القديمة من خلال الأهرامات والمعابد والمتاحف',
                'icon': 'fa-landmark',
                'order': 1
            },
            {
                'name': 'السياحة الإسلامية',
                'name_en': 'Islamic Tourism',
                'slug': 'islamic-tourism',
                'description': 'تعرّف على روائع العمارة الإسلامية والمساجد التاريخية',
                'icon': 'fa-mosque',
                'order': 2
            },
            {
                'name': 'السياحة القبطية',
                'name_en': 'Coptic Tourism',
                'slug': 'coptic-tourism',
                'description': 'اكتشف المعالم المسيحية التاريخية والكنائس الأثرية',
                'icon': 'fa-cross',
                'order': 3
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))

        # Create Governorates
        governorates_data = [
            {'name': 'القاهرة', 'name_en': 'Cairo', 'slug': 'cairo'},
            {'name': 'الجيزة', 'name_en': 'Giza', 'slug': 'giza'},
            {'name': 'الأقصر', 'name_en': 'Luxor', 'slug': 'luxor'},
            {'name': 'أسوان', 'name_en': 'Aswan', 'slug': 'aswan'},
            {'name': 'الإسكندرية', 'name_en': 'Alexandria', 'slug': 'alexandria'},
        ]

        for gov_data in governorates_data:
            governorate, created = Governorate.objects.get_or_create(
                slug=gov_data['slug'],
                defaults=gov_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created governorate: {governorate.name}'))

        # Create Sample Places
        pharaonic = Category.objects.get(slug='pharaonic-tourism')
        islamic = Category.objects.get(slug='islamic-tourism')
        coptic = Category.objects.get(slug='coptic-tourism')
        
        cairo = Governorate.objects.get(slug='cairo')
        giza = Governorate.objects.get(slug='giza')
        luxor = Governorate.objects.get(slug='luxor')

        places_data = [
            {
                'name': 'أهرامات الجيزة',
                'name_en': 'Giza Pyramids',
                'slug': 'giza-pyramids',
                'category': pharaonic,
                'governorate': giza,
                'city': 'الهرم',
                'short_description': 'واحدة من عجائب الدنيا السبع القديمة، الأهرامات الثلاثة الشهيرة وأبو الهول',
                'description': '<p>تُعد أهرامات الجيزة من أشهر المعالم السياحية في العالم وأحد عجائب الدنيا السبع القديمة. بُنيت هذه الأهرامات منذ أكثر من 4500 عام كمقابر للملوك الفراعنة.</p><p>يضم الموقع ثلاثة أهرامات رئيسية: هرم خوفو (الهرم الأكبر)، هرم خفرع، وهرم منقرع، بالإضافة إلى تمثال أبو الهول الشهير.</p>',
                'latitude': 29.9792,
                'longitude': 31.1342,
                'suggested_duration': 4,
                'best_time_to_visit': 'الشتاء والربيع، من نوفمبر إلى مارس',
                'entry_fee': '200 جنيه للأجانب، 60 جنيه للمصريين',
                'visitor_tips': '<ul><li>احرص على زيارة الموقع في الصباح الباكر لتجنب الحرارة والزحام</li><li>ارتدِ ملابس مريحة وأحذية مناسبة للمشي</li><li>أحضر كمية كافية من الماء</li><li>يمكنك ركوب الجمال للتجول حول المنطقة</li></ul>',
                'is_featured': True,
                'priority': 1
            },
            {
                'name': 'المتحف المصري',
                'name_en': 'Egyptian Museum',
                'slug': 'egyptian-museum',
                'category': pharaonic,
                'governorate': cairo,
                'city': 'التحرير',
                'short_description': 'أكبر متحف للآثار المصرية القديمة في العالم، يضم كنوز توت عنخ آمون',
                'description': '<p>يُعد المتحف المصري بالتحرير من أهم وأشهر المتاحف في العالم. يحتوي على أكثر من 120 ألف قطعة أثرية من مختلف العصور الفرعونية.</p><p>من أبرز معروضات المتحف: كنوز الملك توت عنخ آمون الذهبية، المومياوات الملكية، والتماثيل الضخمة.</p>',
                'latitude': 30.0478,
                'longitude': 31.2336,
                'suggested_duration': 3,
                'best_time_to_visit': 'أي وقت من السنة',
                'entry_fee': '200 جنيه للأجانب، 30 جنيه للمصريين',
                'visitor_tips': '<ul><li>خصص وقتاً كافياً للزيارة (3-4 ساعات على الأقل)</li><li>يُنصح بالاستعانة بمرشد سياحي</li><li>التصوير ممنوع داخل المتحف</li></ul>',
                'is_featured': True,
                'priority': 2
            },
            {
                'name': 'مسجد محمد علي',
                'name_en': 'Mohamed Ali Mosque',
                'slug': 'mohamed-ali-mosque',
                'category': islamic,
                'governorate': cairo,
                'city': 'القلعة',
                'short_description': 'مسجد تاريخي يقع داخل قلعة صلاح الدين، يُعرف بمسجد المرمر',
                'description': '<p>يُعد مسجد محمد علي من أجمل المساجد في مصر. بُني في القرن التاسع عشر على الطراز العثماني داخل قلعة صلاح الدين الأيوبي.</p><p>يتميز المسجد بقبته الضخمة ومآذنه الرشيقة، ويُطلق عليه اسم "مسجد المرمر" نسبة إلى الرخام الذي يكسو جدرانه.</p>',
                'latitude': 30.0291,
                'longitude': 31.2597,
                'suggested_duration': 2,
                'best_time_to_visit': 'الصباح أو قبل المغرب',
                'entry_fee': '80 جنيه للأجانب، 20 جنيه للمصريين',
                'visitor_tips': '<ul><li>ارتدِ ملابس محتشمة</li><li>يُنصح بزيارة القلعة بأكملها</li><li>يوفر المسجد إطلالة رائعة على القاهرة</li></ul>',
                'is_featured': True,
                'priority': 3
            },
            {
                'name': 'الكنيسة المعلقة',
                'name_en': 'Hanging Church',
                'slug': 'hanging-church',
                'category': coptic,
                'governorate': cairo,
                'city': 'مصر القديمة',
                'short_description': 'واحدة من أقدم الكنائس في مصر، تُعرف بالكنيسة المعلقة لبنائها على برجين',
                'description': '<p>الكنيسة المعلقة هي إحدى أقدم الكنائس في مصر والشرق الأوسط، تعود للقرن الثالث الميلادي. سُميت بهذا الاسم لأنها بُنيت على برجين من الأبراج القديمة للحصن الروماني.</p><p>تتميز الكنيسة بأيقوناتها القديمة وتصميمها المعماري الفريد.</p>',
                'latitude': 30.0056,
                'longitude': 31.2306,
                'suggested_duration': 1,
                'best_time_to_visit': 'أي وقت',
                'entry_fee': 'مجاناً',
                'visitor_tips': '<ul><li>يُنصح بزيارة المتحف القبطي المجاور</li><li>ارتدِ ملابس محتشمة</li><li>الزيارة قصيرة نسبياً</li></ul>',
                'is_featured': False,
                'priority': 5
            },
            {
                'name': 'معبد الكرنك',
                'name_en': 'Karnak Temple',
                'slug': 'karnak-temple',
                'category': pharaonic,
                'governorate': luxor,
                'city': 'الأقصر',
                'short_description': 'أكبر معبد فرعوني في العالم، مجمع ديني ضخم يضم عدة معابد',
                'description': '<p>معبد الكرنك هو أكبر مجمع معابد في العالم. بُني على مدار أكثر من 2000 عام من قبل فراعنة متعاقبين. يضم المعبد قاعة الأعمدة الشهيرة التي تحتوي على 134 عموداً ضخماً.</p>',
                'latitude': 25.7188,
                'longitude': 32.6573,
                'suggested_duration': 3,
                'best_time_to_visit': 'الشتاء، من نوفمبر إلى فبراير',
                'entry_fee': '200 جنيه للأجانب، 40 جنيه للمصريين',
                'visitor_tips': '<ul><li>احجز جولة ليلية لعرض الصوت والضوء</li><li>أحضر قبعة وواقي شمس</li><li>المشي داخل المعبد يتطلب لياقة بدنية</li></ul>',
                'is_featured': True,
                'priority': 1
            }
        ]

        for place_data in places_data:
            place, created = TouristPlace.objects.get_or_create(
                slug=place_data['slug'],
                defaults=place_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created place: {place.name}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data loaded successfully!'))
        self.stdout.write(self.style.WARNING('\nNote: Remember to add images through the admin panel'))
