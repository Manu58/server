from django.db import models
from django.db.models import UniqueConstraint


# Create your models here.


class ShipMessage(models.Model):
    class Status(models.TextChoices):
        A = 'A', 'ok'
        V = 'V', 'navigation receiver warning'

    class LatDir(models.TextChoices):
        N = 'N', 'North'
        S = 'S', 'South'

    class LonDir(models.TextChoices):
        N = 'E', 'East'
        S = 'W', 'West'

    device_id = models.TextField(blank=False, max_length=20)
    datetime = models.DateTimeField(blank=False)
    address_ip = models.GenericIPAddressField(blank=False, protocol='ipv4')
    address_port = models.PositiveIntegerField(blank=False)
    original_message_id = models.TextField(blank=False, max_length=20)
    status = models.CharField(max_length=1, choices=Status.choices)
    lat = models.FloatField()
    lat_dir = models.CharField(max_length=1, choices=LatDir.choices)
    lon = models.FloatField()
    lon_dir = models.CharField(max_length=1, choices=LonDir.choices)
    spd_over_grnd = models.FloatField()
    true_course = models.FloatField()
    datestamp = models.PositiveIntegerField()
    mag_variation = models.FloatField()
    mag_var_dir = models.CharField(max_length=1, choices=LonDir.choices)

    UniqueConstraint(
        name='unique_ship_message',
        fields=['device_id', 'datetime']
    )

    class Meta:
        ordering = ('device_id', 'datetime')

    def __str__(self):
        return f'{self.device_id} {self.original_message_id}'


class WeatherStation(models.Model):

    timezone = models.CharField(max_length=20, blank=False)
    state_code = models.CharField(max_length=2, blank=False)
    country_code = models.CharField(max_length=3, blank=False)
    lat = models.FloatField()
    lon = models.FloatField()
    city_name = models.CharField(max_length=20)
    station_id = models.CharField(max_length=12)
    city_id = models.CharField(max_length=7)

    UniqueConstraint(
        name='unique_location',
        fields=['lat', 'lon']
    )

    class Meta:
        ordering = ('lat', 'lon')

    def __str__(self):
        return f'{self.lat}_{self.lon}'


class Measurement(models.Model):

    wind_spd = models.FloatField()
    timestamp_utc = models.DateTimeField()
    pres = models.FloatField()
    weather = models.CharField(max_length=30)
    temp = models.FloatField()
    weather_station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE, related_name='measurements')
    timestamp_local = models.DateTimeField()


class Ship1a2090(models.Model):

    datetime = models.DateTimeField()
    wind_spd = models.FloatField()
    weather = models.CharField(max_length=30)
    temp = models.FloatField()
    pres = models.FloatField()
