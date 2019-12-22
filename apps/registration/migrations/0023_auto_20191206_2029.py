# Generated by Django 2.0.8 on 2019-12-06 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0022_auto_20191206_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='average_score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='grades_link',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='subject',
            name='ntnu_link',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='subject',
            name='number_of_evaluations',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='semester',
            field=models.CharField(choices=[('Autumn', 'Høst'), ('Spring', 'Vår'), ('Both', 'Begge')], default='', max_length=250, verbose_name='Semester'),
        ),
        migrations.AddField(
            model_name='subject',
            name='specialization',
            field=models.CharField(blank=True, choices=[('Geomatikk', 'Geomatikk'), ('Konstruksjonsteknikk', 'Konstruksjonsteknikk'), ('Marin teknikk', 'Marin teknikk'), ('Petroleumsfag', 'Petroleumsfag'), ('Produksjonsledelse', 'Produksjonsledelse'), ('Maskinteknikk', 'Maskinteknikk')], max_length=250, verbose_name='Spesialisering'),
        ),
        migrations.AddField(
            model_name='subject',
            name='year',
            field=models.CharField(choices=[('First', 'Første'), ('Second', 'Andre'), ('Third', 'Tredje'), ('Fourth', 'Fjerde'), ('Fifth', 'Femte'), ('Third-Fifth', 'Tredje til Femte')], default='', max_length=250, verbose_name='Trinn'),
        ),
    ]