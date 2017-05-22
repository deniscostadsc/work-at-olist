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

        with open(options['csv_file'][0], newline='') as csvfile:
            rows = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            categories = [row['category'] for row in rows]

            for category in categories:
                category_name = category.split(' / ')[-1]
                Category.objects.create(name=category_name, channel=channel)
                self.stdout.write(self.style.SUCCESS(category_name))

        self.stdout.write(self.style.SUCCESS('Categories imported.'))
