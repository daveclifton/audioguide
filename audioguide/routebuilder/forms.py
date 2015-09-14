from django import forms
from .models import *

class RouteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        # Force a bootstrap class onto all fields.
        [ f.widget.attrs.update({ 'class': 'form-control' }) for f in self.fields.values() ]

    #id           = forms.IntegerField(label='id')
    title        = forms.CharField(label='title',max_length=40)
    description  = forms.CharField(label='description',max_length=500,widget=forms.Textarea())
    color        = forms.CharField(label='color',max_length=7)
    cover_image  = forms.CharField(label='cover image',max_length=160)
    timestamp    = forms.DateTimeField(label='last updated',
                                       widget=forms.TextInput(attrs={'class':'datepicker'})
                                      )

    class Meta:
        model = Route
        fields = ['id', 'title','description','color','cover_image','timestamp']


class WaypointForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WaypointForm, self).__init__(*args, **kwargs)
        # Force a bootstrap class onto all fields.
        [ f.widget.attrs.update({ 'class': 'form-control' }) for f in self.fields.values() ]

    #route        = forms.ModelChoiceField(Route.objects)
    #seq          = forms.IntegerField(label='sequence')
    title        = forms.CharField(label='title',max_length=40)
    description  = forms.CharField(label='description', max_length=500, widget=forms.Textarea())
    lat          = forms.FloatField(label='latitude')
    lng          = forms.FloatField(label='longitude')
    image        = forms.CharField(label='image', max_length=160)
    audio_file   = forms.CharField(label='audio file',max_length=120)

    class Meta:
        model = Waypoint
        fields = ['id', 'title','description','lat','lng','image','audio_file']