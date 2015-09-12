from django.db import models


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
