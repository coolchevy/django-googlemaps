# -*- mode: python; coding: utf-8; -*-

from django.db import models
from googlemaps.forms import LocationFormField
from googlemaps.widgets import LocationWidget

class LocationField(models.CharField):

    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults.update(kwargs)
        defaults['widget'] = LocationWidget
        return super(LocationField, self).formfield(**defaults)
