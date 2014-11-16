import random
import string
import factory

from models import Display, Displayable, Content
from templates.models import Template

class DisplayFactory(factory.Factory):
    class Meta:
        model = Display

    title = factory.Sequence(lambda n: 'display%d' % n)
    short_title = factory.Sequence(lambda n: 'short title%d' % n)
    enabled = random.random < 0.6
    blurb = factory.Sequence(lambda n: 'blurb%d' % n)
    slug = factory.Sequence(lambda n: 'slug%d' % n)

class ContentFactory(factory.Factory):
    class Meta:
        model = Content

    display = DisplayFactory()

    content_type = None
    object_id = 0
    enabled = True
    content_object = None


class TemplateFactory(factory.Factory):
    class Meta:
        model = Template

    name = 'base.html'
    content = factory.Sequence(lambda n: 'this is some content%d' % n)


class DisplayableFactory(factory.Factory):
    class Meta:
        model = Displayable

    title = factory.Sequence(lambda n: 'displayable%d' % n)
    short_title = factory.Sequence(lambda n: 'short title%d' % n)
    slug = factory.Sequence(lambda n: 'slug%d' % n)
    enabled = True
    template = TemplateFactory()