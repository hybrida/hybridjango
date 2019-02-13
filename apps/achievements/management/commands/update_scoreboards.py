import json
from datetime import datetime
from os import path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.registration.models import Hybrid


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        scoreboard_current = []
        scoreboard_all_time = []

        current_year = int(datetime.now().year)

        for hybrid in Hybrid.objects.all():
            badges = hybrid.hybridbadges.all()
            hybrid_dict = {
                'Username': hybrid.username,
                'Score': sum(badge.scorepoints for badge in badges),
                'Full_Name': hybrid.full_name,
                'Badger': [badge.name for badge in badges],
                'Number': 0,
            }

            scoreboard_all_time.append(hybrid_dict)

            if hybrid.graduation_year >= current_year:
                scoreboard_current.append(hybrid_dict.copy())

        scoreboard_current.sort(key=lambda dct: dct['Score'], reverse=True)
        scoreboard_all_time.sort(key=lambda dct: dct['Score'], reverse=True)

        for lst in [scoreboard_all_time, scoreboard_current]:
            current_score = None
            current_pos = 0
            step = 1
            for dct in lst:
                if dct['Score'] == current_score:
                    step += 1
                else:
                    current_score = dct['Score']
                    current_pos += step
                    step = 1
                dct['Number'] = current_pos

        with open(path.join(settings.MEDIA_ROOT, "ScoreboardAllTime.json"), "w") as file:
            json.dump(scoreboard_all_time, file)
        with open(path.join(settings.MEDIA_ROOT, "ScoreboardCurrent.json"), "w") as file:
            json.dump(scoreboard_current, file)
