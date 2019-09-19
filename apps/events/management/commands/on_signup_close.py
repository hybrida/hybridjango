from django.core.management.base import BaseCommand

from apps.events.models import Attendance, Participation, ParticipationSecondary
from apps.events.views import SendAdmittedMail
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        yesterday = datetime.combine(datetime.today() - timedelta(days=1), datetime.min.time())
        for attendance in Attendance.objects.filter(signup_end__range = [yesterday, datetime.now()]).all():
            while attendance.participantsSecondary.count() > 0 and not attendance.full():
                secondary = attendance.get_sorted_secondary()
                user = secondary[0]
                Participation.objects.get_or_create(hybrid=user, attendance=attendance)
                ParticipationSecondary.objects.filter(hybrid=user, attendance=attendance).delete()
                SendAdmittedMail(user, attendance)