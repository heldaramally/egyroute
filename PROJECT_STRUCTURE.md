# EgyRoute Project Structure

## Project Overview
A comprehensive tourism website for Egypt featuring Pharaonic, Islamic, and Coptic sites.

## Directory Structure

```
egyroute/
│
├── egyroute/                    # Main project configuration
│   ├── __init__.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
│
├── tourism/                     # Main tourism app
│   ├── management/
│   │   └── commands/
│   │       └── load_sample_data.py  # Sample data loader
│   ├── migrations/              # Database migrations
│   ├── __init__.py
│   ├── admin.py                # Admin panel customization
│   ├── apps.py                 # App configuration
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── urls.py                 # App URL patterns
│   ├── forms.py                # Forms
│   └── context_processors.py  # Context processors
│
├── templates/                   # HTML templates
│   └── tourism/
│       ├── base.html           # Base template
│       ├── home.html           # Homepage
│       ├── place_detail.html   # Place details
│       ├── category_detail.html # Category page
│       ├── tour_planner.html   # Tour planner
│       ├── all_places.html     # All places listing
│       ├── governorates_list.html
│       ├── governorate_detail.html
│       ├── about.html
│       └── contact.html
│
├── static/                      # Static files (CSS, JS, images)
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── main.js
│
├── media/                       # User uploaded files
│   └── places/                 # Place images
│
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables example
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
└── QUICKSTART.md              # Quick start guide
```

## Key Features

1. **Models:**
   - Category (Tourism types)
   - Governorate (Egyptian governorates)
   - TouristPlace (Tourist sites)
   - PlaceImage (Site images)
   - TourProgram (Tour programs)
   - ContactMessage (Contact messages)

2. **Views:**
   - Home page with featured places
   - Category listing and details
   - Place details with maps
   - Tour planner with automatic generation
   - Search and filter functionality

3. **Admin Panel:**
   - Customized Django admin
   - Image upload and management
   - Map preview
   - Rich text editor

4. **Frontend:**
   - Bootstrap 5 RTL
   - Responsive design
   - Leaflet maps integration
   - WhatsApp integration

## Technologies Used

- **Backend:** Django 4.2+, Python 3.12
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Frontend:** Bootstrap 5, Font Awesome, Leaflet
- **Rich Text:** CKEditor
- **Maps:** Leaflet/OpenStreetMap

## Getting Started

See QUICKSTART.md for installation instructions.

## License

MIT License
