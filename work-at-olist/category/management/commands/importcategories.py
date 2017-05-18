from django.core.management.base import BaseCommand

from category.models import Channel


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('channel_name', nargs=1)

    def handle(self, *args, **options):
        Channel.objects.create(name=options['channel_name'][0])
        self.stdout.write(self.style.SUCCESS('supermarket created.'))
