from django.db import models

class Agency(models.Model):
    class Meta:
        verbose_name_plural = "Agencies"

    agency_id = models.CharField(max_length=10, primary_key=True)
    agency_name = models.CharField(max_length=100)
    agency_url = models.CharField(max_length=250)
    agency_timezone = models.CharField(max_length=50)
    agency_lang = models.CharField(max_length=50, blank=True)
    agency_phone = models.CharField(max_length=50, blank=True)
    agency_fare_url  = models.CharField(max_length=250, blank=True)
    agency_email = models.CharField(max_length=50, blank=True)