from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic

from .models import *
from .forms import *



def index(request):
    return render(request, 'index.html')


#class RoutesListView(generic.ListView):
#    model = Route
#    context_object_name = 'route_list'
#
#    def get_queryset(self):
#        return Route.objects.order_by('id')

#def route_waypoint_list_view(request):
#    query_set = Route.objects.prefetch_related('waypoint_set')
#    routes = query_set.order_by('id').all()
#    return render(request, 'route_waypoint_list.html', {'routes':routes})

class RouteView(generic.DetailView):
    model = Route

class WaypointView(generic.DetailView):
    model = Waypoint


##############################################################################################


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


def route_edit(request, **kwargs):

    routes = Route.objects.all().extra(select={'lower_title': 'lower(title)'}).order_by('lower_title')

    if 'route_id' in kwargs:
        route = get_object_or_404(routes,id=kwargs['route_id'])
    elif 'route_title' in kwargs:
        route = get_object_or_404(routes,title=kwargs['route_title'])
    else:
        route = Route()


    waypoints = route.waypoint_set.all()
    waypoint = None
    #try:
    #    waypoint = None
    #    if 'waypoint_seq' in kwargs:
    #        waypoint = waypoints.get(seq=kwargs['waypoint_seq'])
    #    elif 'waypoint_id' in kwargs:
    #        waypoint = waypoints.get(seq=kwargs['waypoint_id'])
    #except:
    #    pass


    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)

        ##### IS VALID FAILING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!<<<<<<<<<<<<<<
        if form.is_valid():
            route = form.save()
            return HttpResponseRedirect( reverse('route', route_id=route.id)  )
    else:
        form = RouteForm(instance=route)

    return render(request,
                  'route_edit.html',
                  {'form': form,
                   'routes':       routes,
                   'route':        route,
                   'waypoints':    waypoints,
                   'waypoint':     waypoint,
                  }
                )


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




def waypoint_edit(request, **kwargs):

    routes = Route.objects.all().extra(select={'lower_title': 'lower(title)'}).order_by('lower_title')

    if 'route_id' in kwargs:
        route = get_object_or_404(routes,id=kwargs['route_id'])
    else:
        waypoint = Waypoint()

    waypoints = route.waypoint_set.all()

    if 'waypoint_id' in kwargs:
        waypoint = get_object_or_404(waypoints,id=kwargs['waypoint_id'])
    else:
        waypoint = Waypoint()

    if request.method == 'POST':
        form = WaypointForm(request.POST, instance=waypoint)
        if form.is_valid():
            waypoint = form.save()
            return HttpResponseRedirect( reverse('route', route_id=route.id, waypoint_id=waypoint.id)  )
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

