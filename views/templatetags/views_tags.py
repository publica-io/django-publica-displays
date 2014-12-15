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
    try:
        if template and linkage.content_object.template:
            linkage.content_object.template.path = template
    except AttributeError:
        pass
    return linkage


@register.simple_tag(takes_context=True)
def view_proxy(context, proxy_view_slug, *args, **kwargs):
    '''
    The method takes as input a proxy view slug which is the view whose widgets have been featured
    are to be displayed.
    Currently it displays the top 4 widgets with a specified template which is done through
    View template, Also , added view_links inside 
    '''
    view_proxy_html = ''
    try:
        view = View.objects.get(slug=proxy_view_slug)
    except View.DoesNotExist:
        pass
    else:
        html = []
        counter = 1
        templates = {}
        view_links = kwargs.get('view_links', 0)
    
        for template_key, template_name in kwargs.iteritems():
            if template_key.startswith('template_'):
                templates[template_key] = template_name
        
        if templates:
            for linkage in view.linkages.all():
                if counter > view_links:
                    break
                elif linkage.content_object and linkage.content_object.featured:
                    if 'template_%s' % counter in templates.keys():
                        linkage = set_template(linkage, templates['template_%s' % counter])
                        html.append(linkage.render(context))
                    counter += 1
    
        view_proxy_html = ''.join(html)
    # Get rest of the content
    view_content = render_linkages(context)

    return view_proxy_html + view_content


