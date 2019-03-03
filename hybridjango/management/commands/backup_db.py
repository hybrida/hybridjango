from django.core.management.base import BaseCommand
from django.core.management import call_command
from datetime import datetime
from os import path, mkdir
from hybridjango import settings
from hybridjango.utils import ISO_8601, drive


class Command(BaseCommand):
    help = 'Creates a backup of the database'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--upload',
            action='store_true',
            dest='upload',
            help='Upload backup file to Google Drive',
        )

    def handle(self, *args, **options):
        # exclude troublesome or otherwise unnecessary tables
        exclude = ['sessions', 'auth.Permission', 'contenttypes', 'admin.LogEntry']
        # filename with date as ISO-8601 (YYYY-MM-DD HH:MM) format
        now = datetime.now()
        filename = now.strftime('BACKUP {}.json'.format(ISO_8601))
        # backups should be in uploads/backups
        folder = path.join(settings.MEDIA_ROOT, 'backups')
        # if folder does not exist, create it
        if not path.exists(folder):
            mkdir(folder)
        filename = path.join(folder, filename)
        with open(filename, 'w') as f:
            call_command('dumpdata', indent=2, use_natural_foreign_keys=True, exclude=exclude, stdout=f)

        if options['upload']:
            drive.upload_db_backup(filename)