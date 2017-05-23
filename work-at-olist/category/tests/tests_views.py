from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.urls import reverse

from ..models import Category, Channel


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

        response = self.client.get('/channel', follow=True)

        self.assertEquals(200, response.status_code)
        self.assertIn(supermarket.name, response.content.decode())
        self.assertIn(str(supermarket.uid), response.content.decode())
        self.assertIn(new_supermarket.name, response.content.decode())
        self.assertIn(str(new_supermarket.uid), response.content.decode())

    def test_detail_channel(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/simple.csv',
            stdout=self.out)
        supermarket = Channel.objects.get(name='supermarket')
        response = self.client.get(
            reverse('channel_detail', kwargs={'uid': supermarket.uid}))
        self.assertIn(supermarket.name, response.content.decode())
        self.assertIn('Books', response.content.decode())

    def test_list_view(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/simple.csv',
            stdout=self.out)
        category = Category.objects.get(name='National Literature')
        response = self.client.get(reverse('categories'))
        self.assertIn(category.name, response.content.decode())

    def test_detail_category(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/simple.csv',
            stdout=self.out)
        category = Category.objects.get(name='National Literature')
        response = self.client.get(
            reverse('category_detail', kwargs={'uid': category.uid}))
        self.assertIn('National Literature', response.content.decode())
        self.assertIn('"ancestors":["Books"]', response.content.decode())
        self.assertIn(
            '"children":["Science Fiction"]', response.content.decode())
