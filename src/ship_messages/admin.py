from django.contrib import admin
from django.db.models import Avg, QuerySet
from django.db.models.functions import TruncHour

from .models import ShipMessage, Ship1a2090


# Register your models here.


@admin.register(ShipMessage)
class ShipMessageAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'datetime', 'original_message_id')

    def changelist_view(self, request, extra_context=None):

        ships = ShipMessage.objects.values('device_id').distinct('device_id')
        nr_ships = ships.count()
        ships_speed = (ShipMessage
                       .objects
                       .filter(datetime__year='2019')
                       .filter(datetime__month='02')
                       .filter(datetime__day='13')
                       .values('device_id', hour=TruncHour('datetime'))
                       .annotate(avg_speed=Avg('spd_over_grnd'))
                       .order_by('device_id', 'hour'))
        weather = Ship1a2090.objects.all()

        extra_context = {'nr_of_ships': nr_ships, 'ships': ships, 'ships_speed': ships_speed, 'weather': weather}
        return super().changelist_view(request, extra_context=extra_context)
