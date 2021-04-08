from django.contrib import admin
from django.urls import path, include

from core import views as core_views


# api_urlpatterns = (
#     [
#         path("news/", core_views.NewViewSet.as_view(), name="news"),
#     ],
#     "api",
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]
