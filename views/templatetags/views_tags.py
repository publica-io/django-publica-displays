from django import template
from django.utils.html import mark_safe

from views.models import View


register = template.Library()


@register.simple_tag(takes_context=True)
def view(context, slug):

    try:
        view_obj = View.objects.get(slug=slug)
        return view_obj.render(context)
    except View.DoesNotExist:
        return ''
    except View.MultipleObjectsReturned:
        view_obj = View.objects.filter(slug=slug)[0]
        return view_obj.render(context)


@register.simple_tag(takes_context=True)
def render_linkages(context):
    view = context['view']
    html = []
    for linkage in view.linkages.all():
        html.append(linkage.render(context))

    return ''.join(html)


@register.simple_tag(takes_context=True)
def linkage(context, linkage):
    return linkage.render(context)
