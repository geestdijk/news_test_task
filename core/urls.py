from django.urls import path


from core import views


app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('statistics/', views.Statistics.as_view(), name='statistics'),
]