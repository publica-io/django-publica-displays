from django import template
from displays.models import Display


register = template.Library()

@register.simple_tag()
def display(slug):

    try:
        display = Display.objects.get(slug=slug).contents
        return display.render()
    except Display.DoesNotExist:
        return ''

