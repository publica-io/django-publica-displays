from django import template
from displays.models import Display


register = template.Library()

@register.inclusion_tag('displays/display_content.html')
def display(slug):

    try:
        content = Display.objects.get(slug=slug).contents
    except Display.DoesNotExist:
        content = None

    return {'content': content}