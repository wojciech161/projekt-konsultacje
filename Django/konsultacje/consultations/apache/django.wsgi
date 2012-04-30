import os
import sys

sys.path.append('/home/kons/repo/projekt-konsultacje/Django/konsultacje')
sys.path.append('/home/kons/repo/projekt-konsultacje/Django/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'konsultacje.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
