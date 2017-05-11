from __future__ import absolute_import, unicode_literals
from django.core.exceptions import ValidationError
from thecut.menus import settings

try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch


def validate_view(value):
    """Ensure that the value is a valid view identifier that can be resolved to
    a URL."""

    if settings.VALIDATE_VIEWLINKS:
        try:
            args = value.split()
            reverse(args[0], args=args[1:])
        except NoReverseMatch:
            raise ValidationError(
                "'{value}' cannot be resolved. Does the view exist?".format(
                    value=value))
