from django.contrib import admin
from django.utils.datastructures import OrderedSet

from gtfs.models import Agency, Stop, Route, Transfer


class ReadOnlyModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return list(OrderedSet(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))


class StopAdmin(ReadOnlyModelAdmin):
    search_fields = ('stop_name',)


class RouteAdmin(ReadOnlyModelAdmin):
    list_filter = ('route_type',)
    search_fields = ('route_short_name', 'route_long_name', 'route_desc')


class TransferAdmin(ReadOnlyModelAdmin):
    search_fields = ('from_stop__stop_name', 'to_stop__stop_name')


admin.site.register(Agency, ReadOnlyModelAdmin)
admin.site.register(Stop, StopAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Transfer, TransferAdmin)
