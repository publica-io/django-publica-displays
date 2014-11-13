import random
import string
import factory

from models import Display

class DisplayFactory(factory.Factory):
    class Meta:
        model = Display

    title = factory.Sequence(lambda n: 'display%d' % n)
    short_title = factory.Sequence(lambda n: 'short title%d' % n)
    enabled = random.random < 0.3
    blurb = factory.Sequence(lambda n: 'blurb%d' % n)