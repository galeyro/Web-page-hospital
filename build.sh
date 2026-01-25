#!/bin/bash
set -o errexit

# 1. Build Frontend
echo "🏗️ Building Frontend..."
cd frontend
npm install
npm run build
cd ..

# 2. Build Backend
echo "🐍 Building Backend..."
pip install -r hospital/requirements.txt

cd hospital
python manage.py collectstatic --no-input
python manage.py migrate
