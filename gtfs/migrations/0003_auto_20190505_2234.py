# Generated by Django 2.2.1 on 2019-05-05 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gtfs', '0002_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='route_type',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_type', models.IntegerField()),
                ('min_transfer_time', models.IntegerField()),
                ('from_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='gtfs.Stop')),
                ('to_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtfs.Stop')),
            ],
        ),
    ]
