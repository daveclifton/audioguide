import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import *


class ReverseUrlTests(TestCase):

    def test_reverse_url(self):
        self.assertEqual( reverse('index'),                      "/routebuilder/" )

    def test_reverse_url_route_1(self):
        self.assertEqual( reverse('route',args=(1,)),            "/routebuilder/route/1" )

    def test_reverse_url_route_add(self):
        self.assertEqual( reverse('route_add'),                  "/routebuilder/route/add" )

    def test_reverse_url_route_edit_1(self):
        self.assertEqual( reverse('route_edit',args=(1,) ),      "/routebuilder/route/edit/1" )

    def test_reverse_url_route_delete(self):
        self.assertEqual( reverse('route_delete' ),              "/routebuilder/route/delete" )

    def test_reverse_url_waypoint_1_1(self):
        self.assertEqual( reverse('waypoint',args=(1,1) ),       "/routebuilder/waypoint/1/1" )

    def test_reverse_url_waypoint_add_1(self):
        self.assertEqual( reverse('waypoint_add', args=(1,) ),   "/routebuilder/waypoint/add/1" )

    def test_reverse_url_waypoint_edit_1_1(self):
        self.assertEqual( reverse('waypoint_edit', args=(1,1) ), "/routebuilder/waypoint/edit/1/1" )

    def test_reverse_url_waypoint_delete(self):
        self.assertEqual( reverse('waypoint_delete' ),           "/routebuilder/waypoint/delete" )


class RenderTemplateTests(TestCase):

    def test_templates(self):
        response = self.client.get('/routebuilder/')
        self.assertTemplateUsed(response, 'index.html')

    def test_templates_index(self):
        response = self.client.get( reverse('index') )
        self.assertTemplateUsed(response, 'base.html')

    def test_templates_route_1(self):
        response = self.client.get( reverse('route',args=(1,)) )
        self.assertTemplateUsed(response, 'base.html')

    def test_templates_route_add(self):
        response = self.client.get( reverse('route_add') )
        self.assertTemplateUsed(response, 'base.html')

    def test_templates_route_edit(self):
        response = self.client.get( reverse('route_edit',args=(1,) ) )
        self.assertTemplateUsed(response, 'base.html')

    def test_templates_waypoint_1_1(self):
        response = self.client.get( reverse('waypoint',args=(1,1) ) )
        self.assertTemplateUsed(response, 'base.html')

    def test_templates_waypoint_add(self):
        response = self.client.get( reverse('waypoint_add', args=(1,) ) )
        self.assertTemplateUsed(response, 'base.html')

    def test_templates_waypoint_edit(self):
        response = self.client.get( reverse('waypoint_edit', args=(1,1) ) )
        self.assertTemplateUsed(response, 'base.html')


class RedirectTests(TestCase):

    def test_redirect_route_delete(self):
        response = self.client.post( reverse('route_delete' ), {'id':1} )
        self.assertRedirects(response, '/routebuilder/')

    def test_redirect_waypoint_delete(self):
        response = self.client.post( reverse('waypoint_delete' ), {'id':1} )
        self.assertRedirects(response, '/routebuilder/route/1')
