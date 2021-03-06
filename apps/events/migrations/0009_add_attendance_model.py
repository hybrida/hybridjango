# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 00:49
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def copy_attendance(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    Attendance = apps.get_model('events', 'Attendance')
    Participation = apps.get_model('events', 'Participation')
    for event in Event.objects.all().order_by('id'):
        if event.max_participants and event.signup_start:
            attendance = Attendance.objects.create(
                event=event,
                max_participants=event.max_participants,
                price=event.price,
                signup_start=event.signup_start,
                signup_end=event.signup_end,
                genders=event.genders,
                grades=event.grades,
            )
            attendance.save()
            for participant in event.participants.all().order_by('id'):
                Participation.objects.create(
                    hybrid=participant,
                    attendance=attendance
                )


def reverse_copy_attendance(apps, schema_editor):
    pass  # the whole table is deleted when reversing this migration anyway


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0004_switch_specialization_model'),
        ('events', '0008_auto_20170209_0114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Påmelding', max_length=50)),
                ('max_participants', models.PositiveIntegerField(default=0)),
                ('price', models.PositiveIntegerField(default=0)),
                ('signup_start', models.DateTimeField()),
                ('signup_end', models.DateTimeField()),
                ('genders', models.CharField(default='MFU', max_length=3)),
                ('grades', models.CharField(default='12345', max_length=50)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Attendance')),
                ('hybrid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([('hybrid', 'attendance')]),
        ),
        migrations.AddField(
            model_name='attendance',
            name='participants',
            field=models.ManyToManyField(blank=True, through='events.Participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance',
            name='specializations',
            field=models.ManyToManyField(blank=True, to='registration.Specialization'),
        ),
        migrations.RunPython(copy_attendance, reverse_copy_attendance),
    ]
