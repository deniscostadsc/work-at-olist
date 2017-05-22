import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError

from category.models import Channel, Category


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('channel_name', nargs=1, help='Channel name')
        parser.add_argument('csv_file', nargs=1, help='Csv file path')
        parser.add_argument(
            '--csvdelimiter', nargs=1, type=str, default=',',
            help='Change de csv delimiter. Default \',\'')
        parser.add_argument(
            '--quotechar', nargs=1, type=str, default='"',
            help='Change the character that quote strings. Default \'"\'')

    def handle(self, *args, **options):
        channel_name = options['channel_name'][0]
        csv_file = options['csv_file'][0]
        csv_delimiter = options['csvdelimiter'][0]
        quotechar = options['quotechar'][0]

        channel = self._get_or_create(channel_name)

        if not self._csv_file_exists(csv_file):
            self.stdout.write(self.style.ERROR('csv file doesn\'t exist.'))
            return

        with open(csv_file, newline='') as csvfile:
            rows = csv.DictReader(
                csvfile, delimiter=csv_delimiter, quotechar=quotechar)

            if 'category' not in rows.fieldnames:
                self.stdout.write(self.style.ERROR(
                    'csv file has no category column.'))
                return

            categories_path = [row['category'] for row in rows]

        self._flush_and_create_categories(channel, categories_path)

        self.stdout.write(self.style.SUCCESS('Categories imported.'))

    def _csv_file_exists(self, csvfile):
        return os.path.exists(csvfile)

    def _get_or_create(self, channel_name):
        try:
            with transaction.atomic():
                channel = Channel.objects.create(name=channel_name)
            self.stdout.write(self.style.SUCCESS('supermarket created.'))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING('supermarket already exists.'))
            channel = Channel.objects.get(name=channel_name)

        return channel

    def _flush_and_create_categories(self, channel, categories_path):
        with transaction.atomic():
            Category.objects.filter(channel=channel).delete()

            categories_path.sort()

            category = None
            for category_path in categories_path:
                category_path = category_path.split(' / ')

                if len(category_path) == 1:
                    category = None

                category_name = category_path[-1]
                category = Category.objects.create(
                    name=category_name, channel=channel, parent=category)
                self.stdout.write(self.style.SUCCESS(category_name))
