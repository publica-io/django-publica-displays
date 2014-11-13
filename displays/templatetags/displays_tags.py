from django import template
from displays.models import Display


register = template.Library()

@register.inclusion_tag('displays/default.html')
def display(slug):

    try:
        display = Display.objects.get(slug=slug).contents
    except Display.DoesNotExist:
        display = None

    return {'display': display }