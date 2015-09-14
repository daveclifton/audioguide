from django.db import models
import json


class Route(models.Model):
    id           = models.AutoField(primary_key=True)
    title        = models.CharField('title',max_length=40)
    description  = models.CharField('description',max_length=2000)
    color        = models.CharField('color',max_length=7)
    cover_image  = models.CharField('cover image',max_length=160)
    timestamp    = models.DateTimeField('last updated')

    class Meta:
        ordering = ['title']

    def __repr__(self):
        return '<Route %r>' % (self.id)

    def __unicode__(self):
        return u'{}: {}'.format(self.id, self.title)

    def as_dict(self):
        return {
            "title":       self.title,
            "description": self.description,
            "color":       self.color,
            "waypoints":   [ w.as_dict() for w in self.waypoint_set.all() ]
        }

    def as_json(self):
            return json.dumps(self.as_dict(), indent=4)



class Waypoint(models.Model):
    id           = models.AutoField(primary_key=True)
    route        = models.ForeignKey(Route)
    seq          = models.IntegerField('sequence')
    title        = models.CharField('title',max_length=40)
    description  = models.CharField('description',max_length=2000)
    lat          = models.FloatField('latitude')
    lng          = models.FloatField('longitude')
    image        = models.CharField('image',max_length=160)
    audio_file   = models.CharField('audio file',max_length=120)

    class Meta:
        ordering = ['route_id', 'seq']

    def __repr__(self):
        return '<Waypoint %r>' % (self.id)

    def __unicode__(self):
        return u'{}.{} > {}'.format(self.id, self.route, self.title)

    def as_dict(self):
        return {
            "waypoint_id": self.id,
            "title":       self.title,
            "lat":         self.lat,
            "lng":         self.lng,
            "audio_file":  self.audio_file,
        }

    def as_json(self):
            return json.dumps(self.as_dict(), indent=4)
