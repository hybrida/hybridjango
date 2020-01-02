from django.core.management.base import BaseCommand
from apps.events.models import Mark


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for mark in Mark.objects.all():
            mark.check_mark()
