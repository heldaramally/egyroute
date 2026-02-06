#!/bin/bash
# EgyRoute - Quick Setup Script for Linux/Mac
# Run this script to set up the project automatically

echo "🏛️ EgyRoute - Egypt Tourism Website Setup"
echo "========================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1)
if [[ $PYTHON_VERSION =~ Python\ 3\.([0-9]+) ]]; then
    MINOR_VERSION="${BASH_REMATCH[1]}"
    if [ "$MINOR_VERSION" -ge 10 ]; then
        echo "  ✓ $PYTHON_VERSION found"
    else
        echo "  ✗ Python 3.10+ required. Current: $PYTHON_VERSION"
        exit 1
    fi
else
    echo "  ✗ Python not found or version check failed"
    exit 1
fi

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ -d "venv" ]; then
    echo "  ✓ Virtual environment already exists"
else
    python3 -m venv venv
    echo "  ✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo "  ✓ Virtual environment activated"

# Install requirements
echo ""
echo "✓ Installing requirements..."
pip install -r requirements.txt --quiet
echo "  ✓ Requirements installed"

# Create .env file
echo ""
echo "✓ Creating .env file..."
if [ -f ".env" ]; then
    echo "  ✓ .env file already exists"
else
    cp .env.example .env
    echo "  ✓ .env file created from .env.example"
    echo "  ⚠ Remember to update .env with your settings!"
fi

# Run migrations
echo ""
echo "✓ Creating database..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo "  ✓ Database created and migrations applied"

# Create superuser prompt
echo ""
echo "✓ Create admin user..."
read -p "Do you want to create a superuser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
else
    echo "  ⚠ You can create a superuser later with: python manage.py createsuperuser"
fi

# Load sample data
echo ""
echo "✓ Loading sample data..."
read -p "Do you want to load sample tourism data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py load_sample_data
    echo "  ✓ Sample data loaded"
else
    echo "  ⚠ You can load sample data later with: python manage.py load_sample_data"
fi

# Create media directories
echo ""
echo "✓ Creating media directories..."
mkdir -p media/places
echo "  ✓ Media directories created"

# Summary
echo ""
echo "========================================="
echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "  1. Update the .env file with your settings"
echo "  2. Run: python manage.py runserver"
echo "  3. Visit: http://127.0.0.1:8000/"
echo "  4. Admin: http://127.0.0.1:8000/admin/"
echo ""
echo "For more information, see README.md"
echo "========================================="

# Ask to run server
echo ""
read -p "Do you want to start the development server now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting development server..."
    echo "Press Ctrl+C to stop the server"
    echo ""
    python manage.py runserver
fi
