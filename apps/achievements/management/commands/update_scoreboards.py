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
        #Creating the lists that will contain the scoreboards
        scoreboardCurrent = []
        scoreboardAllTime = []

        #Function to create the Current Scoreboard
        for hybrid in Hybrid.objects.all():

            badgeliste = [] #List that will contain the names of the badges the user has

            #Checking if a user hasn't graduated yet
            grad_year = hybrid.graduation_year
            current_year = int(datetime.now().year)  # Getting the current datetime

            if grad_year - current_year >= 0:

                score = 0
                username = hybrid.username
                full_name = hybrid.full_name

                #Funcion that checks which badges the user has, then adding the badges the user has to the badgeliste and the score of the badges to the users score
                for badge in Badge.objects.all():
                    for user in badge.user.all():
                        if username in user.username:
                            badgeliste.append(badge.name)
                            score += badge.scorepoints
                #Dictionary containing all the information needed for the scoreboard
                hybrid_dict = {
                    'Username': username,
                    'Score': score,
                    'Full_Name': full_name,
                    'Badger': badgeliste,
                    'Number': 0,
                }
                #Adding the dictionary to the scoreboard list
                scoreboardCurrent.append(hybrid_dict)



        #Function to create the All Time scoreboard
        for hybrid in Hybrid.objects.all():

            badgeliste = []#List that will contain the names of the badges the user has
            score = 0
            username = hybrid.username
            full_name = hybrid.full_name

            # Funcion that checks which badges the user has, then adding the badges the user has to the badgeliste and the score of the badges to the users score
            for badge in Badge.objects.all():
                for user in badge.user.all():
                    if username in user.username:
                        badgeliste.append(badge.name)
                        score += badge.scorepoints
            #Dictionary containing all the information needed for the scoreboard
            hybrid_dict = {
                'Username': username,
                'Score': score,
                'Full_Name': full_name,
                'Badger': badgeliste,
                'Number': 0,
            }
            # Adding the dictionary to the scoreboard list
            scoreboardAllTime.append(hybrid_dict)

        #Sorting the Current scoreboard
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

        #Adding what place a user has on the scoreboard
        x = 0
        for item in scoreboardCurrent:
            x += 1
            item['Number'] = x

        #Sorting the All Time scoreboard
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

        # Adding what place a user has on the scoreboard
        x = 0
        for item in scoreboardAllTime:
            x += 1
            item['Number'] = x

        #Wrighting the two scoreboards to seperate .json files in /uploads
        with open(path.join(settings.MEDIA_ROOT, "ScoreboardAllTime.json"), "w") as file:
            json.dump(scoreboardAllTime, file)
        with open(path.join(settings.MEDIA_ROOT, "ScoreboardCurrent.json"), "w") as file:
            json.dump(scoreboardCurrent, file)