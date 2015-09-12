from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',                       views.index,                  name='index'),
  #  url(r'^waypoint/(?P<pk>\d+)$',   views.WaypointView.as_view(), name='waypoint'),
  #  url(r'^route/new$',              views.route_edit,             name='route_new'),


    url(r'^route/(?P<route_id>\d+)$',                           views.route,         name='route'),
    url(r'^route/(?P<route_title>[^\/]+)$',                     views.route,         name='route'),
    url(r'^route/edit/(?P<route_id>\d+)$',                      views.route_edit,    name='route_edit'),
    url(r'^route/(?P<route_id>\d+)/(?P<waypoint_id>\d+)$',      views.waypoint,      name='route'),
    url(r'^route/edit/(?P<route_id>\d+)/(?P<waypoint_id>\d+)$', views.waypoint_edit, name='route_edit'),

]
