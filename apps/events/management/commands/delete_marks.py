
import requests
from django.core.management.base import BaseCommand
from apps.events.models import Mark

#Kommando som kjøres automatisk og sjekker om en prikk skal slettes
class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for mark in Mark.objects.all():
            mark.checkMark()