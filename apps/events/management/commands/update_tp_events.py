import json

import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.events.models import TPEvent


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        event_list = requests.get(
            'https://teknologiporten.no/intern/event_list'
        ).content.decode('utf-8')
        relevant_events = [
            {
                'tp_id': key,
                'title': '{} - {}'.format(value['company'], value['title'])[:150],
                'event_start': value['time']
            }
            for key, value in json.loads(event_list).items()
            if '17' in value['invited_programs'].keys()
               or not value['invited_programs']
        ]
        with transaction.atomic():
            for event in relevant_events:
                TPEvent.objects.update_or_create(
                    tp_id=event['tp_id'], defaults=event
                )
