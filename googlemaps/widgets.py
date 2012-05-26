# -*- mode: python; coding: utf-8; -*-

from django import forms
from django.utils.safestring import mark_safe
from settings import DEFAULT_WIDTH,DEFAULT_HEIGHT,DEFAULT_LAT,DEFAULT_LNG
from django.conf import settings

class LocationWidget(forms.TextInput):
    def __init__(self, *args, **kw):

        self.map_width = kw.pop("map_width", DEFAULT_WIDTH)
        self.map_height = kw.pop("map_height", DEFAULT_HEIGHT)

        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()
        #self.checkbox_widget = forms.widgets.CheckboxInput()

    def render(self, name, value, *args, **kwargs):
        if value is None:
            lat, lng = DEFAULT_LAT, DEFAULT_LNG
        else:
            if isinstance(value, unicode):
                a, b = value.split(',')
            else:
                a, b = value
            lat, lng = float(a), float(b)

        js = '''
        <!--http://www.webmonkey.com/2010/02/get_local_search_results_with_google_maps_and_ajax_apis/-->
        <script type="text/javascript" src="%(media_path)sjs/jquery.min.js" ></script>
        <script type="text/javascript">
//<![CDATA[
    var map_%(name)s;
    
    function savePosition_%(name)s(point)
    {
        var input = document.getElementById("id_%(name)s");
        input.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
        map_%(name)s.panTo(point);
    }
    
    function load_%(name)s() {
        var point = new google.maps.LatLng(%(lat)f, %(lng)f);

        var options = {
            zoom: 13,
            center: point,
            mapTypeId: google.maps.MapTypeId.ROADMAP
            // mapTypeControl: true,
            // navigationControl: true
        };
        
        map_%(name)s = new google.maps.Map(document.getElementById("map_%(name)s"), options);

        var marker = new google.maps.Marker({
                map: map_%(name)s,
                position: new google.maps.LatLng(%(lat)f, %(lng)f),
                draggable: true
        
        });
        google.maps.event.addListener(marker, 'dragend', function(mouseEvent) {
            savePosition_%(name)s(mouseEvent.latLng);
        });

        google.maps.event.addListener(map_%(name)s, 'click', function(mouseEvent){
            marker.setPosition(mouseEvent.latLng);
            savePosition_%(name)s(mouseEvent.latLng);
        });

    }
    
    $(document).ready(function(){
        load_%(name)s();
    });

//]]>
</script>
        ''' % dict(name=name, lat=lat, lng=lng, media_path=settings.ADMIN_MEDIA_PREFIX )
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat, lng), dict(id='id_%s' % name))
        #html += self.checkbox_widget.render("", "",{"onclick":"load_%s();"%name})
        html += '<div id="map_%s" style="width: %dpx; height: %dpx"></div>' % (name, self.map_width, self.map_height)

        return mark_safe(js + html)

    class Media:
        js = (
            'http://maps.google.com/maps/api/js?sensor=false',
        )
