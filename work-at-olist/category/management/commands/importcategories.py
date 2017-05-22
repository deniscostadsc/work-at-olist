import csv
import os

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.db import transaction

from category.models import Channel, Category


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('channel_name', nargs=1)
        parser.add_argument('csv_file', nargs=1)

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                channel = Channel.objects.create(
                    name=options['channel_name'][0])
            self.stdout.write(self.style.SUCCESS('supermarket created.'))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING('supermarket already exists.'))
            channel = Channel.objects.get(name=options['channel_name'][0])

        if not os.path.exists(options['csv_file'][0]):
            self.stdout.write(
                self.style.WARNING('csv file doesn\'t exist.'))
            return

        with transaction.atomic():
            Category.objects.filter(channel=channel).delete()

            with open(options['csv_file'][0], newline='') as csvfile:
                rows = csv.DictReader(csvfile, delimiter=',', quotechar='"')
                categories_path = [row['category'] for row in rows]
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

        self.stdout.write(self.style.SUCCESS('Categories imported.'))
