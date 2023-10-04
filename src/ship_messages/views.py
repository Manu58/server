from django.http import QueryDict
from rest_framework.generics import CreateAPIView

from .models import WeatherStation
from .serializers import WeatherStationSerializer


# Create your views here.


class WeatherStationView(CreateAPIView):

    serializer_class = WeatherStationSerializer

    def get_queryset(self):
        return WeatherStation.objects.all().prefetch_related('measurements')

    @staticmethod
    def get_measurement(value):
        return {
            'wind_spd': value['wind_spd'],
            'timestamp_utc': value['timestamp_utc'],
            'pres': value['pres'],
            'weather': value['weather']['description'],
            'temp': value['temp'],
            'timestamp_local': value['timestamp_local']
        }

    def get_station(self, station):
        data = station.pop('data')
        station.pop('sources')
        station['measurements'] = [self.get_measurement(value) for value in data]
        return station

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request._full_data = self.get_station(request.data)
        return super().post(request, *args, **kwargs)