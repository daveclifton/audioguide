from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_http_methods

from .models import *
from .forms import *


def index(request, **kwargs):
    route, routes, waypoint, waypoints = get_context( **kwargs)
    return render(request, 'index.html', {'routes':routes} )


def route(request, **kwargs):
    route, routes, waypoint, waypoints = get_context( **kwargs)

    return render(request,
                  'route.html',
                  {'routes':       routes,
                   'route':        route,
                   'waypoints':    waypoints,
                   'waypoint':     None,
                  }
                )


@require_http_methods(["POST"])
def route_delete(request):
    route = get_object_or_404(Route.objects.all(),id=request.POST['id'])
    route.delete()
    route.save
    return HttpResponseRedirect( reverse('index' ) )


def route_edit(request, **kwargs):
    route, routes, waypoint, waypoints = get_context( **kwargs)

    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            route = form.save()
            return HttpResponseRedirect( reverse('route', args=(route.id,) )  )
    else:
        form = RouteForm(instance=route)

    return render(request,
                  'route_edit.html',
                  {'form':      form,
                   'routes':    routes,
                   'route':     route,
                   'waypoints': waypoints,
                   'waypoint':  waypoint,
                  }
                 )


def waypoint_edit(request, **kwargs):
    route, routes, waypoint, waypoints = get_context( **kwargs)

    if not route:
        raise Http404

    if request.method == 'POST':
        form = WaypointForm(request.POST, instance=waypoint)

        if form.is_valid():

            if route.waypoint_set.all():
                next_seq = max( w.seq for w in route.waypoint_set.all() ) + 1
            else:
                next_seq = 1

            waypoint.seq = next_seq
            route.waypoint_set.add(waypoint)
            route.save
            waypoint = form.save(commit=False)
            waypoint.route = route
            waypoint.save
            return HttpResponseRedirect( reverse('waypoint', args=(route.id,waypoint.seq) ) )
    else:
        form = WaypointForm(instance=waypoint)

    return render(request,
              'waypoint_edit.html',
              {'form': form,
               'routes':       routes,
               'route':        route,
               'waypoints':    waypoints,
               'waypoint':     waypoint,
              }
            )


@require_http_methods(["POST"])
def waypoint_delete(request, **kwargs):
    waypoint = get_object_or_404(Waypoint.objects.all(),id=request.POST['id'])
    waypoint.delete()
    waypoint.save
    return HttpResponseRedirect( reverse('route', args=(waypoint.route_id,) ) )


def waypoint(request, **kwargs):
    route, routes, waypoint, waypoints = get_context( **kwargs)

    if not route:
        raise Http404

    return render(request,
                  'waypoint.html',
                  {'routes':       routes,
                   'route':        route,
                   'waypoints':    waypoints,
                   'waypoint':     waypoint,
                  }
                )


def get_context( route_id=None, route_title=None, waypoint_id=None, waypoint_seq=None):

    routes = Route.objects.all().extra(select={'lower_title': 'lower(title)'}).order_by('lower_title')

    if route_id:
        route = routes.get(id=route_id)
    elif route_title:
        route = routes.get(title=route_title)
    else:
        route = None

    if not route:
        return (None,routes,None,None)

    waypoints = route.waypoint_set.all()

    if waypoint_seq:
        waypoint = waypoints.get(seq=waypoint_seq)
    elif waypoint_id:
        waypoint = waypoints.get(id=waypoint_id)
    else:
        waypoint = None

    return (route, routes, waypoint, waypoints)
