import os

from django.core.management.base import BaseCommand

from category.models import Channel


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('channel_name', nargs=1)
        parser.add_argument('csv_file', nargs=1)

    def handle(self, *args, **options):
        channel_exists = Channel.objects.filter(
            name=options['channel_name'][0]).exists()

        if channel_exists:
            self.stdout.write(
                self.style.WARNING('supermarket already exists.'))
            return

        Channel.objects.create(name=options['channel_name'][0])
        self.stdout.write(self.style.SUCCESS('supermarket created.'))

        if not os.path.exists(options['csv_file'][0]):
            self.stdout.write(
                self.style.WARNING('csv file doesn\'t exist.'))
            return

        self.stdout.write(self.style.SUCCESS('Categories imported.'))
