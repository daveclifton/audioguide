from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',                       views.index,                  name='index'),
  #  url(r'^waypoint/(?P<pk>\d+)$',   views.WaypointView.as_view(), name='waypoint'),
  #  url(r'^route/new$',              views.route_edit,             name='route_new'),

#    url(r'^route/(?P<action>add)$',                             views.route_edit,    name='route_edit'),
#    url(r'^route/(?P<route_id>\d+)$',                           views.route,         name='route'),
#    url(r'^route/(?P<route_title>[^\/]+)$',                     views.route,         name='route'),
#
#    url(r'^route/(?P<route_id>\d+)/(?P<action>new)$',           views.waypoint_edit, name='waypoint_edit'),
#    url(r'^route/(?P<route_id>\d+)/(?P<waypoint_seq>\d+)$',      views.waypoint,      name='route'),
#
#    url(r'^route/(?P<route_id>\d+)/(?P<action>edit)$',                      views.route_edit,    name='route_edit'),
#    url(r'^route/(?P<route_id>\d+)/(?P<waypoint_seq>\d+)/(?P<action>edit)$', views.waypoint_edit, name='waypoint_edit'),


    url(r'^route/(?P<action>add)$',                                 views.route_edit,    name='route_edit'),
    url(r'^route/(?P<action>edit)/(?P<route_id>\d+)$',              views.route_edit,    name='route_edit'),
    url(r'^route/delete$',                                          views.route_delete,  name='route_delete'),
    url(r'^route/(?P<route_id>\d+)$',                               views.route,         name='route'),
    url(r'^route/(?P<route_title>[^\/]+)$',                         views.route,         name='route'),

    url(r'^waypoint/(?P<route_id>\d+)/(?P<waypoint_seq>\d+)$',      views.waypoint,      name='waypoint'),
    url(r'^waypoint/(?P<action>add)/(?P<route_id>\d+)$',            views.waypoint_edit, name='waypoint_edit'),
    url(r'^waypoint/(?P<action>edit)/(?P<route_id>\d+)/(?P<waypoint_seq>\d+)$', views.waypoint_edit, name='waypoint_edit'),
    url(r'^waypoint/delete$',                                       views.waypoint_delete, name='waypoint_delete'),


]
