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

    def __str__(self):
        return self.agency_name


class Stop(models.Model):
    stop_id = models.CharField(max_length=100, primary_key=True)
    stop_code = models.CharField(max_length=50, blank=True, null=True)
    stop_name = models.CharField(max_length=50, blank=True, null=True)
    stop_desc = models.CharField(max_length=250, blank=True, null=True)
    stop_lat = models.FloatField(null=True)
    stop_lon = models.FloatField(null=True)
    stop_url = models.CharField(max_length=250, blank=True, null=True)
    location_type = models.IntegerField(choices=LOCATION_TYPE, default=0)
    parent_station = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE)
    stop_timezone = models.CharField(max_length=50, null=True, blank=True)
    wheelchair_boarding = models.IntegerField(choices=WHEELCHAIR_BOARDING, default=0)
    platform_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        if self.platform_code and self.platform_code != '':
            return self.stop_name + ' / ' + self.platform_code
        else:
            return self.stop_name


class Route(models.Model):
    route_id = models.CharField(max_length=100, primary_key=True)
    agency = models.ForeignKey(Agency, related_name="routes", on_delete=models.CASCADE)
    route_short_name = models.CharField(max_length=10, blank=True, null=True)
    route_long_name = models.CharField(max_length=50, blank=True, null=True)
    route_desc = models.CharField(max_length=250, blank=True, null=True)
    route_type = models.IntegerField()
    route_url = models.CharField(max_length=250, blank=True, null=True)
    route_color = models.CharField(max_length=10, blank=True, null=True)
    route_text_color = models.CharField(max_length=10, blank=True, null=True)
    route_sort_order = models.IntegerField(null=True)

    def __str__(self):
        desc = ''
        if self.route_short_name:
            desc = self.route_short_name
        elif self.route_long_name:
            desc = self.route_long_name

        if self.route_desc:
            desc += ' / ' + self.route_desc

        desc += ' (' + self.agency.agency_name + ')'
        return desc


class Transfer(models.Model):
    from_stop = models.ForeignKey(Stop, related_name="transfers", on_delete=models.CASCADE)
    to_stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    transfer_type = models.IntegerField()
    min_transfer_time = models.IntegerField()

    def __str__(self):
        return self.from_stop.__str__() + ' -> ' + self.to_stop.__str__() + ': ' + str(self.min_transfer_time)


class Calendar(models.Model):
    service_id = models.CharField(max_length=100, primary_key=True)
    monday = models.IntegerField(choices=((0, "Available"), (1, "Not available")))
    tuesday = models.IntegerField(choices=((0, "Available"), (1, "Not available")))
    wednesday = models.IntegerField(choices=((0, "Available"), (1, "Not available")))
    thursday = models.IntegerField(choices=((0, "Available"), (1, "Not available")))
    friday = models.IntegerField(choices=((0, "Available"), (1, "Not available")))
    saturday = models.IntegerField(choices=((0, "Available"), (1, "Not available")))
    sunday = models.IntegerField(choices=((0, "Available"), (1, "Not available")))
    start_date = models.DateField()
    end_date = models.DateField()


class CalendarDate(models.Model):
    service_id = models.CharField(max_length=100)
    date = models.DateField()
    exception_type = models.IntegerField(choices=((1, 'Added'), (2, 'Removed')))


class Trip(models.Model):
    trip_id = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=100)
    trip_headsign = models.CharField(max_length=100, blank=True, null=True)
    trip_short_name = models.CharField(max_length=100, blank=True, null=True)
    direction_id = models.IntegerField(choices=((0, "0"), (1, "1")), null=True)
    block_id = models.CharField(max_length=100, blank=True, null=True)
    wheelchair_accessible = models.CharField(choices=((0, "No information"), (1, "Yes"), (2, "No")), null=True,
                                             blank=True, max_length=1)
    bikes_allowed = models.CharField(choices=((0, "No information"), (1, "Yes"), (2, "No")), null=True, blank=True,
                                     max_length=1)

    def __str__(self):
        return self.route.__str__()
