from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

PREFIX_URL = settings.PREFIX_URL

schema_view = get_schema_view(
    openapi.Info(
        title="Book management system",
        default_version='v1',
        description="Author - Chingal",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^{}(?P<format>\.json|\.yaml)$'.format(PREFIX_URL), schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^{}$'.format(PREFIX_URL), schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^{}redoc/$'.format(PREFIX_URL), schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('api/<version>/', include('backend.accounts.api.urls')),
    path('api/<version>/', include('backend.books.api.urls')),
]
