from django.contrib.auth import get_user_model
from faker import Faker
from random import choice

from .models import New

fake = Faker()


def create_new_story():
    pks = get_user_model().objects.values_list(
        'pk', flat=True)  #fetched a list of users' pks
    user = get_user_model().objects.get(pk=choice(pks))  #chose a random user
    New.objects.create(title=fake.sentence(nb_words=6),
                       content=fake.paragraph(nb_sentences=5),
                       user=user)
