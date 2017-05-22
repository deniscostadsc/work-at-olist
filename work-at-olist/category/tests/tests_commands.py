from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command

from category.models import Channel, Category


class ImportCategories(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_output_on_creation_when_importing_categories(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/correct.csv',
            stdout=self.out)
        self.assertIn('supermarket created.', self.out.getvalue())

    def test_save_channel_when_importing_categories(self):
        self.assertEquals(
            0, Channel.objects.filter(name='supermarket').count())
        call_command(
            'importcategories', 'supermarket', '../tests/files/correct.csv',
            stdout=self.out)
        self.assertEquals(
            1, Channel.objects.filter(name='supermarket').count())

    def test_save_channel_with_correct_name(self):
        self.assertEquals(
            0, Channel.objects.filter(name='another-vendor').count())
        call_command(
            'importcategories', 'another-vendor', '../tests/files/correct.csv',
            stdout=self.out)
        self.assertEquals(
            1, Channel.objects.filter(name='another-vendor').count())

    def test_dont_create_channel_with_the_same_name(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/correct.csv',
            stdout=self.out)
        self.assertEquals(
            1, Channel.objects.filter(name='supermarket').count())
        call_command(
            'importcategories', 'supermarket', '../tests/files/correct.csv',
            stdout=self.out)
        self.assertEquals(
            1, Channel.objects.filter(name='supermarket').count())
        self.assertIn('supermarket already exist', self.out.getvalue())

    def test_save_category(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/correct.csv',
            stdout=self.out)
        self.assertIn('Categories imported', self.out.getvalue())

    def test_non_existing_csv_file(self):
        call_command(
            'importcategories', 'supermarket', 'doesnt_exist.csv',
            stdout=self.out)
        self.assertIn('csv file doesn\'t exist', self.out.getvalue())

    def test_create_categories_from_csv(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/simple.csv',
            stdout=self.out)
        self.assertEquals(
            3, Category.objects.count())

    def test_full_update_on_import(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/correct.csv',
            stdout=self.out)
        channel = Channel.objects.get(name='supermarket')
        self.assertEquals(
            23, Category.objects.filter(channel=channel).count())
        call_command(
            'importcategories', 'supermarket', '../tests/files/simple.csv',
            stdout=self.out)
        channel = Channel.objects.get(name='supermarket')
        self.assertEquals(
            3, Category.objects.filter(channel=channel).count())
