from django.test import TestCase

from ..models import Channel


class TestChannel(TestCase):
    def test_channel_save(self):
        self.assertEquals(0, Channel.objects.count())
        Channel.objects.create(name='supermarket')
        self.assertEquals(1, Channel.objects.count())
