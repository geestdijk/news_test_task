from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin

from .models import New


class NewAdminForm(forms.ModelForm):
    """Custom form for the New model in an admin panel with the CKEditor widget"""
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = New
        fields = "__all__"


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    form = NewAdminForm
    list_display = ['__str__', 'date_added', 'user', ]
    ordering = ['-date_added', ]
