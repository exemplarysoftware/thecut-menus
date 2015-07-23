from __future__ import absolute_import, unicode_literals
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, NoReverseMatch


def validate_view(value):
    """Ensure that the value is a valid view identifier that can be resolved to
    a URL."""

    try:
        reverse(value)
    except NoReverseMatch:
        raise ValidationError(
            "'{value}' cannot be resolved. Does the view exist?".format(
                value=value))
