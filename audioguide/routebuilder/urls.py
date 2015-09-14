from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',                                                      views.index,           name='index'),
    url(r'^route/add$',                                             views.route_edit,      name='route_add'),
    url(r'^route/edit/(?P<route_id>\d+)$',                          views.route_edit,      name='route_edit'),
    url(r'^route/sort/(?P<route_id>\d+)$',                          views.route_sort,      name='route_sort'),
    url(r'^route/delete$',                                          views.route_delete,    name='route_delete'),
    url(r'^route/(?P<route_id>\d+)$',                               views.route,           name='route'),
    url(r'^waypoint/add/(?P<route_id>\d+)$',                        views.waypoint_edit,   name='waypoint_add'),
    url(r'^waypoint/edit/(?P<route_id>\d+)/(?P<waypoint_id>\d+)$',  views.waypoint_edit,   name='waypoint_edit'),
    url(r'^waypoint/delete$',                                       views.waypoint_delete, name='waypoint_delete'),
    url(r'^waypoint/(?P<route_id>\d+)/(?P<waypoint_id>\d+)$',       views.waypoint,        name='waypoint'),
]
