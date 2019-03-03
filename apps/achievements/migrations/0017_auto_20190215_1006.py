# Generated by Django 2.0.8 on 2019-02-15 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('achievements', '0016_remove_badgeforslag_profil'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('D', 'Denied')], max_length=1)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='achievements.Badge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='badgerequest',
            unique_together={('badge', 'user')},
        ),
    ]