from django.test import TestCase

from django.contrib.auth.models import User

from userman.models import ApiKey


def create_active_user():
    user = User.objects.create(
        username='admin',
        password='admin',
        email='i@sayan.com',
    )
    return user


class ApiKeyTests(TestCase):
    def test_api_key_save(self):
        self.user = create_active_user()
        self.apikey = ApiKey.objects.create(
            api_key='random',
            user=self.user,
        )
        self.assertEquals(self.apikey.api_key, 'random')

