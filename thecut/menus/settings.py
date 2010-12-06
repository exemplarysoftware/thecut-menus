from django.conf import settings


SELECTABLE_MODELS = getattr(settings, 'MENUS_SELECTABLE_MODELS',
    ['menus.Menu', 'menus.ViewLink', 'menus.WebLink'])

