from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command

from category.models import Channel


class ImportCategories(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_output_on_creation_when_importing_categories(self):
        call_command('importcategories', 'supermarket', stdout=self.out)
        self.assertIn('supermarket created.', self.out.getvalue())

    def test_save_channel_when_importing_categories(self):
        self.assertEquals(
            0, Channel.objects.filter(name='supermarket').count())
        call_command('importcategories', 'supermarket', stdout=self.out)
        self.assertEquals(
            1, Channel.objects.filter(name='supermarket').count())

    def test_save_channel_with_correct_name(self):
        call_command('importcategories', 'another-vendor', stdout=self.out)
        channel_count = Channel.objects.filter(name='another-vendor').count()
        self.assertEquals(1, channel_count)
