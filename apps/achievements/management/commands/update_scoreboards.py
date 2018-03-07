import json
from datetime import datetime
from os import path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.registration.models import Hybrid
from ...models import Badge


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        # lager en liste med dicts som inneholder brukernavnet og navnet til en hybrid i tillegg til scorepoints og hvilke badger de har
        scoreboardCurrent = []
        scoreboardAllTime = []

        #Lager Current Scoreboardet
        for hybrid in Hybrid.objects.all():
            grad_year = hybrid.graduation_year
            current_year = int(datetime.now().year)  # Getting the current datetime
            badgeliste = []
            if grad_year - current_year >= 0:
                score = 0
                username = hybrid.username
                full_name = hybrid.full_name

                for badge in Badge.objects.all():
                    for user in badge.user.all():
                        if username in user.username:
                            badgeliste.append(badge.name)
                            score += badge.scorepoints

                hybrid_dict = {
                    'Username': username,
                    'Score': score,
                    'Full_Name': full_name,
                    'Badger': badgeliste,
                    'Number': 0,
                }

                scoreboardCurrent.append(hybrid_dict)

        #Lager All Time Scoreboardet
        for hybrid in Hybrid.objects.all():
            badgeliste = []
            score = 0
            username = hybrid.username
            full_name = hybrid.full_name
            for badge in Badge.objects.all():
                for user in badge.user.all():
                    if username in user.username:
                        badgeliste.append(badge.name)
                        score += badge.scorepoints

            hybrid_dict = {
                'Username': username,
                'Score': score,
                'Full_Name': full_name,
                'Badger': badgeliste,
                'Number': 0,
            }

            scoreboardAllTime.append(hybrid_dict)

        #Sorterer Current Scoreboardet og legger til hvilken plass en bruker ligger på
        switch = True
        while (switch):

            switch = False
            for i in range(len(scoreboardCurrent) - 1):
                hybrid1 = scoreboardCurrent[i]
                hybrid2 = scoreboardCurrent[i + 1]

                if hybrid1['Score'] < hybrid2['Score']:
                    scoreboardCurrent[i] = hybrid2
                    scoreboardCurrent[i + 1] = hybrid1
                    switch = True

        x = 0
        for item in scoreboardCurrent:
            x += 1
            item['Number'] = x

        #Sorterer All Time Scoreboardet og legger til hvilken plass en bruker ligger på
        switch = True
        while (switch):

            switch = False
            for i in range(len(scoreboardAllTime) - 1):
                hybrid1 = scoreboardAllTime[i]
                hybrid2 = scoreboardAllTime[i + 1]

                if hybrid1['Score'] < hybrid2['Score']:
                    scoreboardAllTime[i] = hybrid2
                    scoreboardAllTime[i + 1] = hybrid1
                    switch = True

        x = 0
        for item in scoreboardAllTime:
            x += 1
            item['Number'] = x

        with open(path.join(settings.MEDIA_ROOT, "ScoreboardAllTime.json"), "w") as file:
            json.dump(scoreboardAllTime, file)
        with open(path.join(settings.MEDIA_ROOT, "ScoreboardCurrent.json"), "w") as file:
            json.dump(scoreboardCurrent, file)