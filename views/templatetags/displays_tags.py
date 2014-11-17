from django import template
from views.models import View


register = template.Library()

@register.tag
def display(slug):

    try:
        display = View.objects.get(slug=slug)
        return display.render()
    except View.DoesNotExist:
        return ''
    except View.MultipleObjectsReturned:
        display = View.objects.filter(slug=slug)[0]
        return display.render()

