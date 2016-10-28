import os
import csv

from django.contrib.auth.models import User

from apps.accounts.models import Hybrid
from hybridjango.settings import BASE_DIR
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    hybrids_csv = csv.DictReader(open(os.path.join(BASE_DIR, 'hybrider.csv'), 'rU'))

    def handle(self, *args, **options):
        for u in self.hybrids_csv:
            if not u['graduation_year']:
                print('{} har ikke avgangsår, blir ikke lagt til'.format(u['username']))
                continue
            new_user, user_created = User.objects.update_or_create(
                username=u['username'],
                first_name=u['first_name'],
                last_name=u['last_name'],
                email=u['email'],
            )
            new_hybrid, hybrid_created = Hybrid.objects.update_or_create(
                user=new_user,
                middle_name=u['middle_name'],
                graduation_year=u['graduation_year'],
                specialization=u['specialization'],
                member=u['member'] == 'true',
                gender=u['gender'],
                date_of_birth=(u['date_of_birth'] if u['date_of_birth'] and u['date_of_birth'] != '0000-00-00' else None),
            )
