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


def set_template(linkage, template):
    '''
    ..TODO.. confirm and change checking of template through template model
    '''
    if template:
        linkage.content_object.template.name = template
    return linkage


@register.simple_tag(takes_context=True)
def view_proxy(context, proxy_view_slug, *args, **kwargs):
    '''
    The method takes as input a proxy view slug which is the view whose widgets have been featured_on_homepage
    are to be displayed.
    Currently it displays the top 4 widgets with a specified template which is done through
    View template
    '''
    view = View.objects.get(slug=proxy_view_slug)
    html = []
    counter = 0
    template_1 = kwargs.get('template_1', None)
    template_2 = kwargs.get('template_2', None)
    template_3 = kwargs.get('template_3', None)
    template_4 = kwargs.get('template_4', None)

    for linkage in view.linkages.all():
        if linkage.content_object.featured_on_homepage:
            if counter == 0:
                linkage = set_template(linkage, template_1)
                
            elif counter == 1:
                linkage = set_template(linkage, template_2)

            elif counter == 2:
                linkage = set_template(linkage, template_3)

            elif counter == 3:
                linkage = set_template(linkage, template_4)

            elif counter == 4:
                break

            counter += 1
            html.append(linkage.render(context))

    widget_proxy = ''.join(html)
    # Get rest of the content
    view_content = render_linkages(context)

    return widget_proxy + view_content

