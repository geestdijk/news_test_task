from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
import pytest
from rest_framework import status

from core.models import New
from core.serializers import NewSerializer


NEWS_URL = reverse('core:new-list')

pytestmark = pytest.mark.django_db


class TestAnonymousUserAPI:
    """Test unauthenticated News API access"""

    def test_access_to_news_api(self, client, new_fixture):
        pk = str(new_fixture.pk) + '/'
        res = client.get(NEWS_URL)
        assert res.status_code == status.HTTP_403_FORBIDDEN
        res = client.post(NEWS_URL, {})
        assert res.status_code == status.HTTP_403_FORBIDDEN
        res = client.put(NEWS_URL+pk, {})
        assert res.status_code == status.HTTP_403_FORBIDDEN
        res = client.patch(NEWS_URL+pk, {})
        assert res.status_code == status.HTTP_403_FORBIDDEN
        res = client.delete(NEWS_URL+pk)
        assert res.status_code == status.HTTP_403_FORBIDDEN


class TestPrivateUserAPI:
    """Test News API access with an authenticated user"""
    @pytest.fixture(autouse=True)
    def setup_method(self, client, sample_user_fixture):
        self.active_user = sample_user_fixture
        self.client = client
        self.client.force_authenticate(user=self.active_user)

    def test_access_to_news_api_list(self):
        news = baker.make(New, _quantity=5, user=self.active_user)
        res = self.client.get(NEWS_URL)
        assert len(res.data) == 5

    def test_get_single_new_object(self):
        news = baker.make(New, _quantity=5, user=self.active_user)
        last_new = New.objects.last()
        pk_str = f"{last_new.pk}/"
        res = self.client.get(NEWS_URL+pk_str)
        for key in res.data.keys():
            if key == 'date_added':
                object_time = str(getattr(last_new, key))
                assert res.data[key] in object_time
            elif key == 'user':
                assert res.data[key] == getattr(last_new, key).pk
            else:
                assert res.data[key] == getattr(last_new, key)

    def test_create_single_new_object(self, story_data):
        res = self.client.post(NEWS_URL, story_data)
        assert res.status_code == status.HTTP_201_CREATED
        created_new = New.objects.last()
        for key, value in story_data.items():
            assert getattr(created_new, key) == value

    def test_update_single_new_object_put_method(self, story_data):
        created_new = New.objects.create(**story_data)
        pk_str = f"{New.objects.last().pk}/"
        story_data['title'] = 'another_title'
        res = self.client.put(NEWS_URL+pk_str, story_data)
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_update_single_new_object_patch_method(self, story_data):
        created_new = New.objects.create(**story_data)
        pk_str = f"{New.objects.last().pk}/"
        res = self.client.patch(NEWS_URL+pk_str, {'title': 'another_title'})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_update_single_new_object_delete_method(self, story_data, new_fixture):
        pk_str = f"{new_fixture.pk}/"
        res = self.client.delete(NEWS_URL+pk_str)
        assert res.status_code == status.HTTP_403_FORBIDDEN


class TestAdminUserAPI:
    """Test News API access with an authenticated user"""
    @pytest.fixture(autouse=True)
    def setup_method(self, client, sample_user_fixture):
        self.active_user = sample_user_fixture
        self.active_user.is_staff = True
        self.active_user.save()
        self.client = client
        self.client.force_authenticate(user=self.active_user)

    def test_update_single_new_object_put_method(self, story_data):
        created_new = New.objects.create(**story_data)
        pk_str = f"{New.objects.last().pk}/"
        story_data['title'] = 'another_title'
        res = self.client.put(NEWS_URL+pk_str, story_data)
        print(res.data)
        assert res.status_code == status.HTTP_200_OK
        created_new.refresh_from_db()
        assert created_new.title == 'another_title'

    def test_update_single_new_object_patch_method(self, story_data):
        created_new = New.objects.create(**story_data)
        pk_str = f"{New.objects.last().pk}/"
        res = self.client.patch(NEWS_URL+pk_str, {'title': 'another_title'})
        assert res.status_code == status.HTTP_200_OK
        created_new.refresh_from_db()
        assert created_new.title == 'another_title'

    def test_update_single_new_object_delete_method(self, story_data):
        created_new = New.objects.create(**story_data)
        pk_str = f"{created_new.pk}/"
        res = self.client.delete(NEWS_URL+pk_str)
        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert New.objects.count() == 0
