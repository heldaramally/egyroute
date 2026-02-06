# EgyRoute - Egypt Tourism Website

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive tourism website for Egypt showcasing Pharaonic, Islamic, and Coptic heritage sites with interactive maps and personalized tour planning.

## 🌟 Features

- **Multi-category Tourism**: Pharaonic, Islamic, and Coptic sites
- **Interactive Maps**: Leaflet/OpenStreetMap integration
- **Automated Tour Planner**: Generate custom itineraries based on trip duration
- **WhatsApp Integration**: Instant communication
- **Rich Media Gallery**: Multiple images per location
- **Advanced Search**: Filter by category, governorate, and keywords
- **Responsive Design**: Bootstrap 5 with RTL support
- **SEO Optimized**: Clean URLs and meta tags
- **Admin Dashboard**: Customized Django admin panel

## 🚀 Quick Start

### Windows
```powershell
.\setup.ps1
```

### Linux/Mac
```bash
bash setup.sh
```

Or manually:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_data
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## 📚 Documentation

- [README (Arabic)](README.md) - Comprehensive guide
- [Quick Start](QUICKSTART.md) - Get started quickly
- [Deployment Guide](DEPLOYMENT.md) - Production deployment
- [FAQ](FAQ.md) - Frequently asked questions
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Content Management](CONTENT_MANAGEMENT_GUIDE.md) - Admin guide

## 🛠️ Tech Stack

**Backend:**
- Python 3.12
- Django 4.2+
- PostgreSQL (Production) / SQLite (Development)

**Frontend:**
- Bootstrap 5 RTL
- Font Awesome 6
- Leaflet.js
- Google Fonts (Cairo)

**Tools:**
- CKEditor - Rich text editing
- Pillow - Image processing
- python-decouple - Configuration management

## 📁 Project Structure

```
egyroute/
├── egyroute/           # Project settings
├── tourism/            # Main app
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── media/             # User uploads
└── manage.py          # Django CLI
```

## 🎯 Key Models

- **Category**: Tourism types (Pharaonic, Islamic, Coptic)
- **Governorate**: Egyptian governorates
- **TouristPlace**: Tourist sites with details
- **PlaceImage**: Image gallery
- **TourProgram**: Tour itineraries
- **ContactMessage**: Contact form submissions

## 🌐 Main Pages

- `/` - Home with featured places
- `/category/<slug>/` - Category pages
- `/place/<slug>/` - Place details with map
- `/places/` - All places with filters
- `/tour-planner/` - Automated tour generator
- `/governorates/` - Browse by governorate
- `/admin/` - Admin dashboard

## 📱 Screenshots

### Home Page
Modern, responsive design with featured attractions.

### Place Details
Comprehensive information with interactive maps, images, and visitor tips.

### Tour Planner
AI-powered tour generation based on preferences.

### Admin Panel
Intuitive content management system.

## 🔒 Security

- CSRF protection
- SQL injection prevention
- XSS protection
- Secure password hashing
- Environment-based configuration

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- VPS setup (Ubuntu)
- Nginx configuration
- SSL/HTTPS setup
- Database migration
- Static files handling

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code standards
- Pull request process
- Development guidelines

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- **Django** - Web framework
- **Bootstrap** - UI framework
- **Leaflet** - Maps library
- **Font Awesome** - Icons
- **OpenStreetMap** - Map data

## 📧 Contact

- Website: http://127.0.0.1:8000
- Issues: [GitHub Issues](https://github.com/your-username/egyroute/issues)

## 🗺️ Roadmap

### Version 1.1
- [ ] Multi-language support (Arabic/English)
- [ ] User reviews and ratings
- [ ] Booking system integration

### Version 1.2
- [ ] Mobile application
- [ ] Social media integration
- [ ] Blog section

### Version 2.0
- [ ] AI recommendations
- [ ] Virtual tours (360°)
- [ ] AR features

---

**Made with ❤️ in Egypt** 🇪🇬

© 2026 EgyRoute. All rights reserved.
