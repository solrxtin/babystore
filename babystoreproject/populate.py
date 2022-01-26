import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'babystoreproject.settings')

import django
django.setup()
from  app.models import Department, Item


