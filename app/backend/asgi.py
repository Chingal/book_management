import os

from django.core.asgi import get_asgi_application

project_name = os.environ.get('PROJECT_NAME')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')

application = get_asgi_application()
