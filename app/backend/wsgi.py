import os

from django.core.wsgi import get_wsgi_application

project_name = os.environ.get('PROJECT_NAME')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')

application = get_wsgi_application()
