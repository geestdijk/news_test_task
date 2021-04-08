import pytest

from core import models
from django.utils.text import slugify


pytestmark = pytest.mark.django_db

class TestModels:
    def test_create_a_new(self, sample_user_fixture, story_data):
        """Test creating New model object and representation"""
        new = models.New.objects.create(**story_data)

        assert new.slug == slugify(story_data['title'])
        assert str(new) == story_data['title']
