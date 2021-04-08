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
