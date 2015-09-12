from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic

from .models import *
from .forms import *


def index(request):
    routes = Route.objects.all().extra(select={'lower_title': 'lower(title)'}).order_by('lower_title')

    return render(request, 'index.html', {'routes':routes} )


def route(request, **kwargs):

    routes = Route.objects.all().extra(select={'lower_title': 'lower(title)'}).order_by('lower_title')

    if 'route_id' in kwargs:
        route = get_object_or_404(routes,id=kwargs['route_id'])
    elif 'route_title' in kwargs:
        route = get_object_or_404(routes,title=kwargs['route_title'])
    else:
        pass
        # GET 404 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    return render(request,
                  'route.html',
                  {'routes':       routes,
                   'route':        route,
                   'waypoints':    route.waypoint_set.all(),
                   'waypoint':     None,
                  }
                )


def route_delete(request, **kwargs):

    route = get_object_or_404(Route.objects.all(),id=request.POST['id'])

    route.delete()
    route.save
    return HttpResponseRedirect( reverse('index' ) )


def route_edit(request, **kwargs):

    routes = Route.objects.all().extra(select={'lower_title': 'lower(title)'}).order_by('lower_title')

    if 'route_id' in kwargs:
        route = get_object_or_404(routes,id=kwargs['route_id'])
    elif 'route_title' in kwargs:
        route = get_object_or_404(routes,title=kwargs['route_title'])
    else:
        route = Route()

    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            route = form.save()
            return HttpResponseRedirect( reverse('route', args=(route.id,) )  )
    else:
        form = RouteForm(instance=route)

    return render(request,
                  'route_edit.html',
                  {'form': form,
                   'routes':    routes,
                   'route':     route,
                   'waypoints': route.waypoint_set.all(),
                   'waypoint':  None,
                  }
                 )


def waypoint_edit(request, **kwargs):
    print "waypint edit", kwargs
    routes = Route.objects.all().extra(select={'lower_title': 'lower(title)'}).order_by('lower_title')

    if 'route_id' in kwargs:
        print "search for route ", kwargs['route_id']
        route = get_object_or_404(routes,id=kwargs['route_id'])

    waypoint = Waypoint()
    waypoints = route.waypoint_set.all()

    if 'waypoint_id' in kwargs:
        waypoint = get_object_or_404(waypoints,id=kwargs['waypoint_id'])
    elif 'waypoint_seq' in kwargs:
        waypoint = get_object_or_404(waypoints,seq=kwargs['waypoint_seq'])

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


def waypoint_delete(request, **kwargs):
    waypoint = get_object_or_404(Waypoint.objects.all(),id=request.POST['id'])

    ###################################if request.method == 'POST':
    waypoint.delete()
    waypoint.save
    return HttpResponseRedirect( reverse('route', args=(waypoint.route_id,) ) )


def waypoint(request, **kwargs):

    routes = Route.objects.all().extra(select={'lower_title': 'lower(title)'}).order_by('lower_title')

    if 'route_id' in kwargs:
        route = get_object_or_404(routes,id=kwargs['route_id'])
    elif 'route_title' in kwargs:
        route = get_object_or_404(routes,title=kwargs['route_title'])
    else:
        pass
        # GET 404 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    waypoints = route.waypoint_set.all()

    waypoint = None
    if 'waypoint_seq' in kwargs:
        waypoint = get_object_or_404(waypoints,seq=kwargs['waypoint_seq'])
    elif 'waypoint_id' in kwargs:
        waypoint = get_object_or_404(waypoints,id=kwargs['waypoint_id'])
    else:
        pass
        # GET 404 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    return render(request,
                  'waypoint.html',
                  {'routes':       routes,
                   'route':        route,
                   'waypoints':    route.waypoint_set.all(),
                   'waypoint':     waypoint,
                  }
                )



