from django.contrib import admin

from .models import Route, Waypoint


class WaypointInlines(admin.TabularInline):
    model = Waypoint
    extra = 1


class RouteAdmin(admin.ModelAdmin):
    field = ['description','title']
    search_fields = ['title','description']
    inlines = [WaypointInlines]


class WaypointAdmin(admin.ModelAdmin):
    search_fields = ['title','description']


admin.site.register(Route, RouteAdmin)
admin.site.register(Waypoint, WaypointAdmin)
