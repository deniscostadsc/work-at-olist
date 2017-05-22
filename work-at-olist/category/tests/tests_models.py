from django.test import TestCase

from ..models import Channel, Category


class TestChannel(TestCase):
    def test_channel_save(self):
        self.assertEquals(0, Channel.objects.count())
        Channel.objects.create(name='supermarket')
        self.assertEquals(1, Channel.objects.count())


class TestCategory(TestCase):
    def test_category_save(self):
        channel = Channel.objects.create(name='supermarket')
        Category.objects.create(name='Video Game', channel=channel)
        self.assertEquals(1, Category.objects.count())
