from django.test import TestCase

from ..models import Channel, Category


class TestChannel(TestCase):
    def test_channel_save(self):
        self.assertEquals(0, Channel.objects.count())
        channel = Channel.objects.create(name='supermarket')
        self.assertEquals(1, Channel.objects.count())
        self.assertEquals('supermarket', str(channel))


class TestCategory(TestCase):
    def test_category_save(self):
        channel = Channel.objects.create(name='supermarket')
        category = Category.objects.create(name='Video Game', channel=channel)
        self.assertEquals(1, Category.objects.count())
        self.assertEquals('Video Game', str(category))
