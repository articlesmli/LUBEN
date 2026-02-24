import os
import sys

# 1. Add your project directory to the sys.path
path = '/home/LUBEN/LUBEN'
if path not in sys.path:
    sys.path.append(path)

# 2. Tell Django where the settings are
# (Ensure 'nmr_site' is the folder name containing settings.py)
os.environ['DJANGO_SETTINGS_MODULE'] = 'nmr_site.settings'

# 3. Start the application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()