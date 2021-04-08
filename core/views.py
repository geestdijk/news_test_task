from django.contrib.auth import get_user_model
from django.db.models import Count
from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import New
from .serializers import NewSerializer


class NewViewSet(viewsets.ModelViewSet):
    """Manage news in the database"""
    queryset = New.objects.all()
    serializer_class = NewSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_permissions(self):
        """Manage permissions so only admin can delete or update a story(new)"""
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Create a new story(new)"""
        serializer.save(user=self.request.user)


class IndexView(TemplateView):
    """Home page template view"""
    template_name = "main.html"


class NewsListView(ListView):
    """List of the news template view"""
    template_name = 'core/news_list.html'
    queryset = New.objects.select_related('user')
    context_object_name = 'news'

class Statistics(TemplateView):
    """Statistics of the number of news per the user"""
    template_name = 'core/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = get_user_model().objects.all().annotate(nums=Count('news', 
                                         distinct=True))
        context['users'] = users
        return context
