from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

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

    def test_import_with_semocolon_sepated_value_file(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/semicolon.csv',
            '--csvdelimiter', ';', stdout=self.out)
        self.assertIn('Categories imported', self.out.getvalue())

    def test_import_with_another_quotechar(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/pipe.csv',
            '--quotechar', '|', stdout=self.out)
        self.assertIn(',Bo,oks', self.out.getvalue())
        self.assertIn('Categories imported', self.out.getvalue())

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

    def test_import_correct_parents(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/simple.csv',
            stdout=self.out)
        books = Category.objects.get(name='Books')
        national_literature = Category.objects.get(name='National Literature')
        science_fiction = Category.objects.get(name='Science Fiction')
        self.assertIsNone(books.parent)
        self.assertEquals(books, national_literature.parent)
        self.assertEquals(national_literature, science_fiction.parent)

    def test_import_correct_parents_with_unordered_csv(self):
        call_command(
            'importcategories', 'supermarket',
            '../tests/files/unordered_simple.csv', stdout=self.out)
        books = Category.objects.get(name='Books')
        national_literature = Category.objects.get(name='National Literature')
        science_fiction = Category.objects.get(name='Science Fiction')
        self.assertIsNone(books.parent)
        self.assertEquals(books, national_literature.parent)
        self.assertEquals(national_literature, science_fiction.parent)

    def test_import_correct_parents_with_more_than_one_root_category(self):
        call_command(
            'importcategories', 'supermarket', '../tests/files/correct.csv',
            stdout=self.out)
        books = Category.objects.get(name='Books')
        games = Category.objects.filter(name='Games').first()
        computers = Category.objects.filter(name='Computers').last()
        self.assertIsNone(books.parent)
        self.assertIsNone(games.parent)
        self.assertIsNone(computers.parent)

    def test_csv_without_category_column(self):
        call_command(
            'importcategories', 'supermarket',
            '../tests/files/no_category.csv', stdout=self.out)
        self.assertIn('csv file has no category column', self.out.getvalue())
