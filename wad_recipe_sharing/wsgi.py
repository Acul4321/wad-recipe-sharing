"""
WSGI config for wad_recipe_sharing project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
import dotenv
from django.core.wsgi import get_wsgi_application

# Add project directory to Python path
PROJECT_DIR = '/home/acul4321/acul4321.pythonanywhere.com'
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

# Add the parent directory to Python path
PARENT_DIR = os.path.dirname(PROJECT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

# Load environment variables
env_path = os.path.join(PROJECT_DIR, '.env')
if os.path.exists(env_path):
    dotenv.read_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_recipe_sharing.settings')
application = get_wsgi_application()
