from django.conf import settings


# @@@ TODO: recurse through available content apps and dynamically set this
CONTENT_MODELS = getattr(settings,
                         'VIEWS_CONTENT_MODELS',
                         ['post', 'page', 'widget', ])
