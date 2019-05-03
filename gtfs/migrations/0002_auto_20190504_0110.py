# Generated by Django 2.2.1 on 2019-05-03 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gtfs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='agency_email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='agency',
            name='agency_fare_url',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='agency',
            name='agency_lang',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='agency',
            name='agency_phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('stop_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('stop_code', models.CharField(blank=True, max_length=50, null=True)),
                ('stop_name', models.CharField(blank=True, max_length=50, null=True)),
                ('stop_desc', models.CharField(blank=True, max_length=250, null=True)),
                ('stop_lat', models.FloatField(null=True)),
                ('stop_long', models.FloatField(null=True)),
                ('stop_url', models.CharField(blank=True, max_length=250, null=True)),
                ('location_type', models.IntegerField(choices=[(0, 'Stop or Platform'), (1, 'Station'), (2, 'Station Entrance/Exit'), (3, 'Generic'), (4, 'Boarding Area')], default=0)),
                ('stop_timezone', models.CharField(max_length=50)),
                ('wheelchair_boarding', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2')], default=0)),
                ('platform_code', models.CharField(blank=True, max_length=10, null=True)),
                ('parent_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='gtfs.Stop')),
            ],
        ),
    ]
