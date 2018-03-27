from django.core.management.base import BaseCommand

from ...models import Badge
from apps.registration.models import Hybrid
from datetime import datetime

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        current_year = int(datetime.now().year)  # Getting the current datetime
        #function to reset member badges
        if Badge.objects.filter(name="Medlemskaps Medalje").exists():
            badge = Badge.objects.get(name="Medlemskaps Medalje")
            badge.user.clear

        medals = [["1års Medalje", 4], ["3års Medalje", 2], ["5års Medalje", 0], ["6+års Medalje", -1]]  # list that contains all the year medals we have, consist of elements with the variables name, and what year requirement they need too be achieved
        #function to reset all year badges
        for medal in medals:  # iteration trough every single year Medal, which unfortunatley is hardcoded
            badge = Badge.objects.get(name=medal[0])  # getting each medal for each iteration of the loop
            badge.user.clear

        #Going through all users to award the member badge and year badges
        for hybrid in Hybrid.objects.all():
            grad_year = hybrid.graduation_year

            # function that awards membership badge
            if hybrid.member:
                if Badge.objects.filter(name="Medlemskaps Medalje").exists():
                    badge = Badge.objects.get(name="Medlemskaps Medalje")
                    badge.user.add(hybrid)
                    badge.save()

            # function that awards 1,3,5 and 6+ year medals based on the amount of time they have been in Hybrida, not necessarily which year they are in. Also, atm, this function will award these at new years eve, so that you will have the medals for the second semester each year.
            for medal in medals:  # iteration trough every single year Medal, which unfortunatley is hardcoded
                badge = Badge.objects.get(name=medal[0])  # getting each medal for each iteration of the loop
                if grad_year - current_year <= medal[1]:
                    badge.user.add(hybrid)
                    badge.save()
