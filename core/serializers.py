from rest_framework import serializers

from .models import New

class NewSerializer(serializers.ModelSerializer):
    """Serialize a new"""

    class Meta:
        model = New
        fields = ("__all__")
        read_only_fields = ('user',)

