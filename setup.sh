#!/bin/bash

echo "Setting up Recipe Sharing project..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/Scripts/activate
fi

# Run makemigrations
echo "Making migrations..."
python manage.py makemigrations

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

echo "Setup complete!"