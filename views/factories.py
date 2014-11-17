import random
import factory

from models import View, Viewable, ViewLinkage
from templates.models import Template


class ViewFactory(factory.Factory):
    class Meta:
        model = View

    title = factory.Sequence(lambda n: 'display%d' % n)
    short_title = factory.Sequence(lambda n: 'short title%d' % n)
    enabled = random.random < 0.6
    blurb = factory.Sequence(lambda n: 'blurb%d' % n)
    slug = factory.Sequence(lambda n: 'slug%d' % n)


class ViewLinkageFactory(factory.Factory):
    class Meta:
        model = ViewLinkage

    view = ViewFactory()

    content_type = None
    object_id = 0
    enabled = True
    content_object = None


class TemplateFactory(factory.Factory):
    class Meta:
        model = Template

    name = 'base.html'
    content = factory.Sequence(lambda n: 'this is some content%d' % n)


class ViewableFactory(factory.Factory):
    class Meta:
        model = Viewable

    title = factory.Sequence(lambda n: 'displayable%d' % n)
    short_title = factory.Sequence(lambda n: 'short title%d' % n)
    slug = factory.Sequence(lambda n: 'slug%d' % n)
    enabled = True
    template = TemplateFactory()
