from django.db import models
from django.contrib.contenttypes import generic

from templates.mixins import TemplateMixin

from attrs.mixins import GenericAttrMixin
from entropy.mixins import (
    EnabledMixin, OrderingMixin, TitleMixin, SlugMixin, TextMixin
)
from images.mixins import ImageMixin

try:
    from publica_admin.mixins import PublicaAdminMixin
except ImportError:
    PublicaAdminMixin = object


from settings import CONTENT_MODELS


class PageView(OrderingMixin):

    position = models.ForeignKey(
        'positions.Position',
        help_text='The Named Position upon the Page whereas the Page Content View will appear')

    page = models.ForeignKey(
        'pages.Page',
        help_text='The Page to link the Page Content View')

    view = models.ForeignKey(
        'View',
        help_text='The Page Content View to link to the Page')

    class Meta:
        ordering = ('order', )
        verbose_name = 'Attached Page Content View'
        verbose_name_plural = 'Attachable Page Content Views'

    def __unicode__(self):
        return '"{}" (Content View/Widgets) at the "{}" page position on the "{}" page'.format(self.view.title, self.position.title, self.page.title)


class View(GenericAttrMixin, EnabledMixin, TitleMixin, SlugMixin, TextMixin, TemplateMixin, ImageMixin, PublicaAdminMixin):
    '''
    A View of ViewLinkage or Widgets with a given template.

    Some templates accept parameters, such as slideshow duration
    '''
    class Meta:
        verbose_name = 'Page Content View'
        verbose_name_plural = 'Page Content Views that use Content Widgets'


class ViewLinkage(EnabledMixin, OrderingMixin):
    '''
    ViewLinkage for View
    '''

    view = models.ForeignKey('View', related_name='linkages')

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        limit_choices_to={'model__in': CONTENT_MODELS},
        blank=True,
        help_text='Choose the Content Type of the content to link to in the Page Content View',
        null=True
    )
    object_id = models.PositiveIntegerField(
        help_text='Choose the Content Object to link to')
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Link to Content Widget'
        verbose_name_plural = 'Links to Content Widgets'


    def render(self, context=None):
        '''
        The method would render the html of the content
        '''
        try:
            return self.content_object.render(context)
        except AttributeError:
            # We're choosing to fail silently here
            return ''
