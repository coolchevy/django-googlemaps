from django.template import Library, TemplateSyntaxError, Node, Variable
from googlemaps.widgets import LocationWidget
from django.template.loader import get_template
from django.template import Context
from googlemaps.settings import DEFAULT_WIDTH,DEFAULT_HEIGHT,API_KEY

register = Library()

class GoogleMapNode(Node):
    def __init__(self, geopos_var, wh):
        self.geopos_var = Variable(geopos_var)
        self.wh = wh

    def render(self, context):
        geopos = self.geopos_var.resolve(context)
        if len(geopos.split(','))<2:
            raise TemplateSyntaxError('googlemap tag got undefined params')
        geopos_lat, geopos_lng = geopos.split(',')
        if not geopos:
            return ""
        media = LocationWidget().media
        ctx = {
                'geopos_lat':geopos_lat,
                'geopos_lng':geopos_lng,
                'map_width':DEFAULT_WIDTH,
                'map_height':DEFAULT_HEIGHT,
                }
        if self.wh:
            ctx.update({
                'map_width':self.wh[0],
                'map_height':self.wh[1],
                })
        t = get_template("googlemaps/map.html")
        body = t.render(Context(ctx))
        return "%s %s" % (media,body)

class GoogleMapByAddressNode(Node):
    def __init__(self, address, title, wh):
        self.address = Variable(address)
        self.title = Variable(title)
        self.wh = wh

    def render(self, context):
        address = self.address.resolve(context)
        title = self.title.resolve(context)
        ctx = {
                'map_width':DEFAULT_WIDTH,
                'map_height':DEFAULT_HEIGHT,
                "title":title,
                "address":address,
                "API_KEY":API_KEY,
                }
        if self.wh:
            ctx.update({
                'map_width':self.wh[0],
                'map_height':self.wh[1],
                })
        t = get_template("googlemaps/map_by_address.html")
        return t.render(Context(ctx))

@register.tag
def google_map(parser, token):
    """
    {% google_map value width,height %}
    """
    bits = token.split_contents()
    if len(bits)<2:
        raise TemplateSyntaxError('%s tag requires more arguments' % bits[0])
    if len(bits) == 3:
        wh = bits[2].split(",")
        if len(wh)<2:
            raise TemplateSyntaxError('%s tag has invalid wight,height argument' % bits[0])
    else:
        wh = None
    return GoogleMapNode(bits[1],wh)

@register.tag
def google_map_by_address(parser, token):
    """
    {% google_map_by_address address infobox width,height %}
    """
    bits = token.split_contents()
    if len(bits)<3:
        raise TemplateSyntaxError('%s tag requires more arguments' % bits[0])
    if len(bits) == 4:
        wh = bits[3].split(",")
        if len(wh)<2:
            raise TemplateSyntaxError('%s tag has invalid wight,height argument' % bits[0])
    else:
        wh = None
    return GoogleMapByAddressNode(bits[1],bits[2],wh)
