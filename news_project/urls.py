from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.api_urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    from news_project import debug_urls
    urlpatterns = debug_urls.urlpatterns + urlpatterns
