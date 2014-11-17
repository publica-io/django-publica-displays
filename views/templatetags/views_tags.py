from django import template
from views.models import View


register = template.Library()


@register.tag
def view(slug):
    try:
        view_obj = View.objects.get(slug=slug)
        return view_obj.render()
    except View.DoesNotExist:
        return ''
    except View.MultipleObjectsReturned:
        view_obj = View.objects.filter(slug=slug)[0]
        return view_obj.render()
