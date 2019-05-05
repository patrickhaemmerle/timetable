from django.contrib import admin

from gtfs.models import Agency, Stop, Route


class StopAdmin(admin.ModelAdmin):
    raw_id_fields = ('parent_station',)
    search_fields = ('stop_name',)

class RouteAdmin(admin.ModelAdmin):
    list_filter = ('route_type',)
    search_fields = ('route_short_name', 'route_long_name', 'route_desc')

admin.site.register(Agency)
admin.site.register(Stop, StopAdmin)
admin.site.register(Route, RouteAdmin)
