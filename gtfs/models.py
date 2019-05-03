from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

LOCATION_TYPE = (
    (0, 'Stop or Platform'),
    (1, 'Station'),
    (2, 'Station Entrance/Exit'),
    (3, 'Generic'),
    (4, 'Boarding Area'),
)

WHEELCHAIR_BOARDING = (
    (0, "0"),
    (1, "1"),
    (2, "2"),
)


class Agency(models.Model):
    class Meta:
        verbose_name_plural = "Agencies"

    agency_id = models.CharField(max_length=10, primary_key=True)
    agency_name = models.CharField(max_length=100)
    agency_url = models.CharField(max_length=250)
    agency_timezone = models.CharField(max_length=50)
    agency_lang = models.CharField(max_length=50, blank=True, null=True)
    agency_phone = models.CharField(max_length=50, blank=True, null=True)
    agency_fare_url = models.CharField(max_length=250, blank=True, null=True)
    agency_email = models.CharField(max_length=50, blank=True, null=True)


class Stop(models.Model):
    pass
    stop_id = models.CharField(max_length=100, primary_key=True)
    stop_code = models.CharField(max_length=50, blank=True, null=True)
    stop_name = models.CharField(max_length=50, blank=True, null=True)
    stop_desc = models.CharField(max_length=250, blank=True, null=True)
    stop_lat = models.FloatField(null=True)
    stop_long = models.FloatField(null=True)
    stop_url = models.CharField(max_length=250, blank=True, null=True)
    location_type = models.IntegerField(choices=LOCATION_TYPE, default=0)
    parent_station = models.ForeignKey("self", null=True, related_name="children", on_delete=models.PROTECT)
    stop_timezone = models.CharField(max_length=50)
    wheelchair_boarding = models.IntegerField(choices=WHEELCHAIR_BOARDING, default=0)
    platform_code = models.CharField(max_length=10, blank=True, null=True)
