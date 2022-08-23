import json
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Restaurant, Vote


class Settings(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create authorized user
        user = get_user_model()
        cls.user = user.objects.create_user(username='Test_user', password='123')
        cls.client = Client()
        tokens = cls.client.post(
            reverse('token_obtain_pair'),
            data={'username': 'Test_user', 'password': '123'},
        ).content.decode("utf-8")
        cls.access_token = json.loads(tokens)['access']


class CreateRestTest(Settings):
    def setUp(self):
        rest = self.client.post(
            reverse('restaraunt-list'),
            format='json',
            data={'name': 'TestRest'},
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            follow=True,
        )

    def test_rests_list(self):
        rests = self.client.get(
            reverse('restaraunt-list'),
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            follow=True,
        )
        print(rests.content)

    def test_vote(self):
        vote = self.client.post(
            reverse('vote-detail', kwargs={'pk': 1}),
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            follow=True,
        )
        print(vote.content)
        votes = self.client.get(
            reverse('vote-list'),
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            follow=True,
        )
        print(votes.content)
