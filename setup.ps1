# EgyRoute - Quick Setup Script for Windows PowerShell
# Run this script to set up the project automatically

Write-Host "🏛️ EgyRoute - Egypt Tourism Website Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "✓ Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.([0-9]+)") {
    $minorVersion = [int]$Matches[1]
    if ($minorVersion -ge 10) {
        Write-Host "  ✓ $pythonVersion found" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Python 3.10+ required. Current: $pythonVersion" -ForegroundColor Red
        exit
    }
} else {
    Write-Host "  ✗ Python not found or version check failed" -ForegroundColor Red
    exit
}

# Create virtual environment
Write-Host ""
Write-Host "✓ Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "✓ Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

# Install requirements
Write-Host ""
Write-Host "✓ Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "  ✓ Requirements installed" -ForegroundColor Green

# Create .env file
Write-Host ""
Write-Host "✓ Creating .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✓ .env file already exists" -ForegroundColor Green
} else {
    Copy-Item .env.example .env
    Write-Host "  ✓ .env file created from .env.example" -ForegroundColor Green
    Write-Host "  ⚠ Remember to update .env with your settings!" -ForegroundColor Magenta
}

# Run migrations
Write-Host ""
Write-Host "✓ Creating database..." -ForegroundColor Yellow
python manage.py makemigrations --noinput
python manage.py migrate --noinput
Write-Host "  ✓ Database created and migrations applied" -ForegroundColor Green

# Create superuser prompt
Write-Host ""
Write-Host "✓ Create admin user..." -ForegroundColor Yellow
$createSuperuser = Read-Host "Do you want to create a superuser now? (y/n)"
if ($createSuperuser -eq "y" -or $createSuperuser -eq "Y") {
    python manage.py createsuperuser
} else {
    Write-Host "  ⚠ You can create a superuser later with: python manage.py createsuperuser" -ForegroundColor Magenta
}

# Load sample data
Write-Host ""
Write-Host "✓ Loading sample data..." -ForegroundColor Yellow
$loadData = Read-Host "Do you want to load sample tourism data? (y/n)"
if ($loadData -eq "y" -or $loadData -eq "Y") {
    python manage.py load_sample_data
    Write-Host "  ✓ Sample data loaded" -ForegroundColor Green
} else {
    Write-Host "  ⚠ You can load sample data later with: python manage.py load_sample_data" -ForegroundColor Magenta
}

# Create media directories
Write-Host ""
Write-Host "✓ Creating media directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "media\places" | Out-Null
Write-Host "  ✓ Media directories created" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Update the .env file with your settings" -ForegroundColor White
Write-Host "  2. Run: python manage.py runserver" -ForegroundColor White
Write-Host "  3. Visit: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "  4. Admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see README.md" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Ask to run server
Write-Host ""
$runServer = Read-Host "Do you want to start the development server now? (y/n)"
if ($runServer -eq "y" -or $runServer -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Starting development server..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    python manage.py runserver
}
