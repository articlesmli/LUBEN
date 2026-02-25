import os
import sys

# Path to your project folder
path = '/home/LUBEN/LUBEN'
if path not in sys.path:
    sys.path.append(path)

# nmr_site is the folder containing your settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'nmr_site.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()