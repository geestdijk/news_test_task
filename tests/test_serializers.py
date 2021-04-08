import pytest

from core.serializers import NewSerializer

pytestmark = pytest.mark.django_db


def test_new_serializer(new_fixture, sample_user_fixture, story_data):
    """Test updating the data New model object data using the serializer""" 
    serializer = NewSerializer(new_fixture, story_data)
    assert serializer.is_valid()
    assert serializer.errors == {}
    serializer.save()
    new_fixture.refresh_from_db()
    assert new_fixture.title == story_data['title']
    assert new_fixture.content == story_data['content']
