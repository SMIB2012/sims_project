#!/bin/bash
# SIMS Deployment Script WITHOUT Virtual Environment (Fixes venv hanging issue)
# Run this script on your server to deploy the SIMS project

echo "🚀 SIMS Deployment Script (System-wide Python) for 172.236.152.35"
echo "=================================================================="

# Set working directory
echo "📁 Navigating to project directory..."
cd /var/www/sims_project || { echo "❌ Project directory not found"; exit 1; }

echo "📦 Installing Python packages system-wide..."
# Install packages directly with system pip (bypass venv issue)
sudo apt update
sudo apt install -y nginx python3-pip python3-dev build-essential python3-django
sudo pip3 install --break-system-packages django gunicorn requests pytest pytest-django

echo "📁 Setting up directories..."
mkdir -p static staticfiles media logs backups

echo "🔐 Setting environment variables..."
export SECRET_KEY="django-insecure-temp-key-for-deployment"
export DEBUG="False"
export ALLOWED_HOSTS="172.236.152.35,localhost,127.0.0.1"

echo "🗄️ Setting up database..."
python3 manage.py migrate

echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput

echo "🔧 Setting file permissions..."
sudo chown -R www-data:www-data /var/www/sims_project
sudo chmod -R 755 /var/www/sims_project
sudo chmod -R 775 /var/www/sims_project/media
sudo chmod -R 775 /var/www/sims_project/logs
sudo chmod 664 /var/www/sims_project/db.sqlite3

echo "⚙️ Setting up services..."
# Stop conflicting services
sudo systemctl stop apache2 2>/dev/null || true
sudo systemctl stop nginx 2>/dev/null || true
sudo systemctl stop sims 2>/dev/null || true
sudo rm -f /var/www/sims_project/sims.sock

# Copy configuration files
sudo cp nginx_sims.conf /etc/nginx/sites-available/sims
sudo ln -sf /etc/nginx/sites-available/sims /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo cp sims.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sims

echo "🧪 Testing configuration..."
sudo nginx -t
python3 manage.py check --deploy

echo "🚀 Starting services..."
sudo systemctl start sims
sleep 3

if sudo systemctl is-active --quiet sims; then
    echo "✅ SIMS service started"
    sudo systemctl restart nginx
    if sudo systemctl is-active --quiet nginx; then
        echo "✅ Nginx started"
        echo ""
        echo "✅ Deployment complete!"
        echo "🌐 Access SIMS at: http://172.236.152.35/"
        echo ""
        echo "👤 Create admin user with:"
        echo "   cd /var/www/sims_project"
        echo "   python3 manage.py createsuperuser"
    else
        echo "❌ Nginx failed"
        sudo journalctl -u nginx -n 5 --no-pager
    fi
else
    echo "❌ SIMS service failed"
    sudo journalctl -u sims -n 5 --no-pager
fi
