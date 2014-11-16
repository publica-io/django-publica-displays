from django import template
from displays.models import Display


register = template.Library()

@register.tag
def display(slug):

    try:
        display = Display.objects.get(slug=slug)
        return display.render()
    except Display.DoesNotExist:
        return ''
    except Display.MultipleObjectsReturned:
        display = Display.objects.filter(slug=slug)[0]
        return display.render()

