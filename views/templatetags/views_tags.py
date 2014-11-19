from django import template
from views.models import View


register = template.Library()


class ViewNode(template.Node):
    def __init__(self, slug):
        self.slug = slug

    def render(self, context):
        try:
            view_obj = View.objects.get(slug=self.slug)
        except View.MultipleObjectsReturned:
            view_obj = View.objects.filter(slug=self.slug).first()
        except View.DoesNotExist:
            raise template.TemplateSyntaxError(
                'View with slug {} does not exists'.format(self.slug)
            )

        return view_obj.render()


@register.tag
def view(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '{} tag requires a single argument'.format(
                token.contents.split()[0]
            )
        )

    return ViewNode(slug)
