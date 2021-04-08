from django.contrib.auth.models import User
from django.http import HttpRequest
from model_bakery import baker
from rest_framework.test import APIClient
import pytest

from core import models


@pytest.fixture
def sample_user_fixture(db):
    """Create a sample user fixture"""

    user = User.objects.create_user(
        username='sample_user', password='password'
    )
    return user


@pytest.fixture
def client(db):
    """Create a fixture for rest_framework APIClient"""
    client = APIClient()
    return client


@pytest.fixture
def story_data(sample_user_fixture):
    """Sample data for a story(new) creation"""
    data = {
        'title': 'test_title',
        'content': 'test_content',
        'user': sample_user_fixture,
    }
    return data


@pytest.fixture
def new_fixture(sample_user_fixture, db):
    return baker.make(models.New, user=sample_user_fixture)


@pytest.fixture
def news_fixture(sample_user_fixture, db):
    news = baker.make(models.New, _quantity=5, user=sample_user_fixture)
