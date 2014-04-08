import os
import sys

path = '/var/www/proyecto_1'
if path not in sys.path:
    sys.path.insert(0, '/var/www/proyecto_1')

os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto_1.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
