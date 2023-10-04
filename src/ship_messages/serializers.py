from rest_framework import serializers

from .models import Measurement, WeatherStation


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = ('wind_spd', 'timestamp_utc', 'pres', 'weather', 'temp', 'timestamp_local')


class WeatherStationSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = WeatherStation
        fields = '__all__'

    def create(self, validated_data):
        measurements = validated_data.pop('measurements')
        station = WeatherStation.objects.create(**validated_data)
        for measurement in measurements:
            Measurement.objects.create(weather_station=station, **measurement)
        return station
