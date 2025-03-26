"""
WSGI config for wad_recipe_sharing project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

# Add project directory to Python path
path = '/home/acul4321/wad-recipe-sharing'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'wad_recipe_sharing.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
