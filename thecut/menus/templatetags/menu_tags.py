from menus import *  # NOQA
import warnings


warnings.warn('{% load menu_tags %} is deprecated, use {% load menus %}.',
              DeprecationWarning)
