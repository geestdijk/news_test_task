from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views


router = DefaultRouter()
router.register('news', views.NewViewSet)


app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]