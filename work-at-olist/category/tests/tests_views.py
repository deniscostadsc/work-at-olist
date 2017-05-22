from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from ..models import Channel


class TestChannelAPIView(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_list_channels(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/simple.csv',
            stdout=self.out)
        call_command(
            'importcategories', 'new_supermarket', '../tests/files/simple.csv',
            stdout=self.out)

        supermarket = Channel.objects.get(name='supermarket')
        new_supermarket = Channel.objects.get(name='new_supermarket')

        response = self.client.get('/channels', follow=True)

        self.assertEquals(200, response.status_code)
        self.assertIn(supermarket.name, response.content.decode())
        self.assertIn(str(supermarket.uid), response.content.decode())
        self.assertIn(new_supermarket.name, response.content.decode())
        self.assertIn(str(new_supermarket.uid), response.content.decode())
