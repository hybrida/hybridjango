# Generated by Django 2.0.8 on 2019-01-30 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0015_auto_20180206_1946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField(default=0)),
                ('minutes', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['-marks'],
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('reason', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MarkPunishment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveIntegerField(default=0)),
                ('goes_on_secondary', models.PositiveIntegerField(default=0)),
                ('too_many_marks', models.PositiveIntegerField(default=0)),
                ('delay', models.ManyToManyField(blank=True, to='events.Delay')),
            ],
        ),
        migrations.CreateModel(
            name='ParticipationSecondary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(blank=True, default='', max_length=500)),
                ('punishment', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='events.MarkPunishment')),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='_attendance_participants_+', through='events.Participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='participationsecondary',
            name='attendance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Attendance'),
        ),
        migrations.AddField(
            model_name='participationsecondary',
            name='hybrid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='markpunishment',
            name='rules',
            field=models.ManyToManyField(blank=True, to='events.Rule'),
        ),
        migrations.AddField(
            model_name='delay',
            name='punishment',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='events.MarkPunishment'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='participantsSecondary',
            field=models.ManyToManyField(blank=True, related_name='_attendance_participantsSecondary_+', through='events.ParticipationSecondary', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='participationsecondary',
            unique_together={('hybrid', 'attendance')},
        ),
        migrations.AlterUniqueTogether(
            name='delay',
            unique_together={('marks', 'minutes')},
        ),
    ]